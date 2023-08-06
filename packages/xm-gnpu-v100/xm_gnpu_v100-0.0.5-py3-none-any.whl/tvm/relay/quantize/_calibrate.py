# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Find scales for quantization on the dataset."""
from __future__ import absolute_import
import math
import logging
import multiprocessing as mp
import numpy as np
import tvm
import tvm.driver
from tvm.ir import IRModule

from . import _quantize
from . import quantize
from .. import op as _op
from .. import expr as _expr
from .. import analysis as _analysis
from .. import build_module as _build_module
from ...contrib import graph_executor
from .kl_divergence import _find_scale_by_kl


def _get_profile_runtime(mod):
    func = mod["main"]
    func = _quantize.CreateStatsCollector(func)

    if tvm.target.Target.current():
        target = tvm.target.Target.current()
        dev = tvm.device(target.kind.name)
    else:
        target = "llvm"
        dev = tvm.device(target)
    with tvm.transform.PassContext(opt_level=3):
        lib = _build_module.build(func, target=target)
    #geyijun@20220422
    #和下面打印scale的索引号对齐(通过head数组的索引就是对应的输出层节点)
    #操作方法:把json文件用解释器打开(https://c.runoob.com/front-end/53/)
    #根据索引到head下找到对应的节点号，再根据节点号找到对应的节点。
    #print("[geyijun]:_get_profile_runtime--------->lib.json:",lib.get_json());
    #
    runtime = graph_executor.GraphModule(lib["default"](dev))
    return runtime

#
#说明:chunk_by=-1,表示把所有层的数据采样放在一个chunk中(既:全部放一起)
#说明:chunk_by=1,表示把1层的数据采样放在一个chunk中(既:每层分开放)
#说明:chunk_by=2,表示把2层的数据采样放在一个chunk中(既:每2层分开放)
#主要是为了节省内存吧???
def collect_stats(mod, dataset, chunk_by=-1):
    """Given an annotated graph, create a profile graph to collect profile data from the
    calibration dataset. This pass collects simulated_quantize op input into a tuple.
    Simulated_quantize ops are rewritten to identity mode. The tuple is the output of the profile
    graph.

    Parameters
    ----------
    mod: Module
        The simulation graph after annotation.

    dataset: Iterable[NDArray]
        The calibration dataset.

    chunk_by: optional, int
        The size of chunk to be returned in one iteration. It is meant to be
        used for reducing memory usage. If not specified, return samples for
        all layers in one chunk.

    Returns
    -------
    ret: Iterable[list of ndarray]
        List of output data of each layer, chunked by the chunk_by parameter
    """
    logging.info("collecting statistics for calibration...")
    runtime = _get_profile_runtime(mod)
    #注意:每层是一个输出(layer_out),不是整个网络的输出。
    num_outputs = runtime.get_num_outputs()     
    chunk_by = num_outputs if chunk_by == -1 else chunk_by
    #print("[geyijun]:collect_stats--------->chunk_by:",chunk_by);
    #print("[geyijun]:collect_stats--------->num_outputs:",num_outputs);
    
    #代码逻辑说明一下:
    #如果chunk_by=-1  ,chunk_by=num_outputs,
    #   则:for执行一次,则:outputs=[[]*num_outputs],一次输出所有层的结果
    #如果chunk_by=1,
    #   则:for执行num_outputs次,则:outputs=[[]*1],一次输出一层的结果
    #注意:outputs=[[]],是一个双层list
    #   第一级的元素是layer，第二级的元素是该层不同batch的采样值。
    #有上面的说明之后，代码就非常容易理解了。
    for i in range(0, num_outputs, chunk_by):
        outputs = [[] for i in range(min(chunk_by, num_outputs - i))]
        for batch in dataset:
            runtime.set_input(**batch)
            runtime.run()
            #说明:j-i,是为了定位到对应层的输出
            for j in range(i, min(i + chunk_by, num_outputs)):
                outputs[j - i].append(runtime.get_output(j).asnumpy())
        yield [np.concatenate(output).reshape(-1) for output in outputs]


def _activation_kl_scale(mod, dataset):
    cfg = quantize.current_qconfig()
    chunk_by = cfg.calibrate_chunk_by
    scales = []
    for samples in collect_stats(mod, dataset, chunk_by):
        logging.info("finding threshold with kl for calibration...")
        with mp.Pool() as pool:
            scales += list(pool.map(_find_scale_by_kl, samples))

    #这里的scales,对应到每一层输出的最大值, 配置到ndom_scale = scale/128
    debuginfo = [(i,scales[i]) for i in range(len(scales))]
    # print("[geyijun]:_activation_kl_scale--------->scales:",debuginfo);

    def func(_):
        scale = scales[func.scale_idx]
        func.scale_idx += 1
        return scale

    func.scale_idx = 0
    return func


def _find_scale_by_percentile(arr, percentile=0.99999):
    assert isinstance(arr, np.ndarray)
    x = np.abs(arr)
    max_k = int(x.size * percentile)        #索引
    return np.partition(x, max_k)[max_k]    #内部会先对数组排序(升序)


def _activation_percentile_scale(mod, dataset):
    cfg = quantize.current_qconfig()
    chunk_by = cfg.calibrate_chunk_by
    scales = []
    for samples in collect_stats(mod, dataset, chunk_by):
        logging.info("finding threshold with percentile for calibration...")
        with mp.Pool() as pool:
            scales += list(pool.map(_find_scale_by_percentile, samples))
   
    #这里的scales,对应到每一层输出的最大值, 配置到ndom_scale = scale/128
    #注意:打印的序号要和上面的_get_profile_runtime中创建的模型对齐...
    debuginfo = [(i,scales[i]) for i in range(len(scales))]
    # print("[geyijun]:_activation_percentile_scale--------->scales:",debuginfo);

    def func(_):
        scale = scales[func.scale_idx]
        func.scale_idx += 1
        return scale

    func.scale_idx = 0
    return func

def _find_scale_by_max(arr):
    assert isinstance(arr, np.ndarray)
    val = np.amax(np.abs((arr)))
    return val

def _activation_max_scale(mod, dataset):
    cfg = quantize.current_qconfig()
    chunk_by = cfg.calibrate_chunk_by
    scales = []
    for samples in collect_stats(mod, dataset, chunk_by):
        logging.info("finding threshold with percentile for calibration...")
        with mp.Pool() as pool:
            scales += list(pool.map(_find_scale_by_max, samples))

    #这里的scales,对应到每一层输出的最大值, 配置到ndom_scale = scale/128
    #注意:打印的序号要和上面的_get_profile_runtime中创建的模型对齐...
    debuginfo = [(i,scales[i]) for i in range(len(scales))]
    # print("[geyijun]:_activation_max_scale--------->scales:",debuginfo);

    def func(_):
        scale = scales[func.scale_idx]
        func.scale_idx += 1
        return scale

    func.scale_idx = 0
    return func

def _activation_power2_scale(mod, dataset):
    cfg = quantize.current_qconfig()
    chunk_by = cfg.calibrate_chunk_by
    scales = []
    for samples in collect_stats(mod, dataset, chunk_by):
        logging.info("finding threshold with percentile for calibration...")
        with mp.Pool() as pool:
            scales += list(pool.map(_find_scale_by_max, samples))

    #按照power2对齐
    for i in range(len(scales)):
        assert (scales[i] > 0)
        scales[i] = 2 ** np.math.ceil(np.math.log(scales[i],2))

    #这里的scales,对应到每一层输出的最大值, 配置到ndom_scale = scale/128
    #注意:打印的序号要和上面的_get_profile_runtime中创建的模型对齐...
    debuginfo = [(i,scales[i]) for i in range(len(scales))]
    # print("[geyijun]:_activation_max_scale--------->scales:",debuginfo);

    def func(_):
        scale = scales[func.scale_idx]
        func.scale_idx += 1
        return scale

    func.scale_idx = 0
    return func

# input scale functions
def _activation_global_scale(sq_call):  # pylint: disable=unused-argument
    cfg = quantize.current_qconfig()
    return cfg.global_scale

# weight scale functions
def _weight_power2_scale(sq_call):  # pylint: disable=unused-argument
    """calculate weight scale with nearest mode-2 scale"""
    var = sq_call.args[0]
    assert isinstance(var, _expr.Constant)
    val = np.amax(np.abs(var.data.asnumpy()))
    # print("_weight_power2_scale->",val)
    return 2 ** np.math.ceil(np.math.log(val, 2)) if val > (0.000001*128) else 1.0  #如果scale==0,则修正一下

def _weight_max_scale(sq_call):
    """calculate weight scale with maximum absolute value"""
    var = sq_call.args[0]
    assert isinstance(var, _expr.Constant)
    val = np.amax(np.abs(var.data.asnumpy()))
    return val if val > (0.000001*128) else 1.0  #如果scale==0,则修正一下

def _set_params(mod, input_scale_func, weight_scale_func):
    quantize_op = _op.get("relay.op.annotation.simulated_quantize")
    cfg = quantize.current_qconfig()
    const_params = {}

    def visit_func(expr):
        """visitor function for traverse"""
        if isinstance(expr, _expr.Call) and expr.op == quantize_op:
            _, ndom_scale, nclip_min, nclip_max = expr.args
            attrs = expr.attrs
            kind = attrs.kind
            nbit = cfg.get_nbit_by_kind(kind)
            valid_bit = nbit - attrs.sign

            # set scale
            if kind == quantize.QAnnotateKind.WEIGHT:
                assert isinstance(expr.args[0], _expr.Constant)
                scale = weight_scale_func(expr)
                # print("weight_scale--->",scale)
            else:
                scale = input_scale_func(expr)

            def _make_const(val):
                return _expr.const(val, "float32")

            valid_range = 2 ** valid_bit
            const_params[ndom_scale] = _make_const(scale / valid_range)
            const_params[nclip_min] = _make_const(-(valid_range - 1))
            const_params[nclip_max] = _make_const((valid_range - 1))

    main_func = mod["main"]
    _analysis.post_order_visit(main_func, visit_func)
    main_func = _expr.bind(main_func, const_params)
    func_dict = {}
    for global_var, func in mod.functions.items():
        if global_var.name_hint != "main":
            func_dict[global_var] = func
    return IRModule.from_expr(main_func, func_dict)



def calibrate(dataset=None):
    """The calibrate procedure will try to calculate the content of
    dom_scale, nbit, clip_min, clip_max for every `simulated_quantize`
    operator.

    Parameters
    ---------
    dataset: Optional[Iterable[NDArray]]
        The calibration dataset.

    Returns
    -------
    ret: Function
        The module pass function.
    """

    def wrapped_func(mod, _):
        """make transform.module pass happy"""
        cfg = quantize.current_qconfig()

        if cfg.vta_adjust_scale == True:
            if (cfg.calibrate_mode != "kl_divergence" and cfg.calibrate_mode != "max" and cfg.calibrate_mode != "power2") \
            or (cfg.weight_scale != "max"  and cfg.weight_scale != "power2") : 
                raise ValueError("vta_adjust_scale:invalid calibrate mode {} {} "\
                        .format(cfg.calibrate_mode,cfg.weight_scale))

        if cfg.calibrate_mode == "global_scale":
            input_scale_func = _activation_global_scale
        elif cfg.calibrate_mode == "kl_divergence":
            input_scale_func = _activation_kl_scale(mod, dataset)
        elif cfg.calibrate_mode == "percentile":
            input_scale_func = _activation_percentile_scale(mod, dataset)
        elif cfg.calibrate_mode == "max":
            input_scale_func = _activation_max_scale(mod, dataset)
        elif cfg.calibrate_mode == "power2":
            input_scale_func = _activation_power2_scale(mod, dataset)            
        else:
            raise ValueError("Unknown calibrate mode {}".format(cfg.calibrate_mode))

        if cfg.weight_scale == "max":
            weight_scale_func = _weight_max_scale
        elif cfg.weight_scale == "power2":
            weight_scale_func = _weight_power2_scale
        else:
            raise ValueError("Unknown weight scale mode {}".format(cfg.weight_scale))

        return _set_params(mod, input_scale_func, weight_scale_func)

    return wrapped_func
