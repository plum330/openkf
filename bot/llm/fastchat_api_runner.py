# Copyright © 2023 OpenIM open source community. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# multiprocessing 基于进程的并行
# python多进程 多线程 多协程：https://juejin.cn/post/7088521649070276644
import multiprocessing as mp
from multiprocessing import Event
import sys
import os
# 用于函数在结束前执行的代码
import atexit
from typing import List

# Add parent dir to sys.path so we can import from parent dir
sys.path.append("..")

from fastapi import FastAPI
# uvicorn用于构建异步web服务
import uvicorn
# httpx发送网络请求
import httpx

import utils.config as config
import utils.log as log
from utils import banner
import constants.constants as constants

# 设置httpx请求客户端参数
httpx._config.DEFAULT_TIMEOUT_CONFIG.connect = 120
httpx._config.DEFAULT_TIMEOUT_CONFIG.read = 120
httpx._config.DEFAULT_TIMEOUT_CONFIG.write = 120

logger = None


# 定义多进程相关的类
# 类继承Process，用类作为进程
# http://kaito-kidd.com/2018/05/11/python-advance-process-thread/
class FastChatControllerRunner(mp.Process):
    '''
    Fastchat controller process
    '''

    def __init__(self, prev_event: Event, curr_event: Event, host: str,
                 port: int, log_path: str, dispatch_method: str):
        super().__init__()

        self.prev_event = prev_event
        self.curr_event = curr_event
        self.host = host
        self.port = port
        self.log_path = log_path
        self.dispatch_method = dispatch_method
        self.app = self._create_controller()

    # 构建api
    def _create_controller(self) -> FastAPI:
        from fastchat.serve.controller import app, Controller
        from fastapi.middleware.cors import CORSMiddleware
        import fastchat.constants

        # 设置fastchat日志路径
        fastchat.constants.LOGDIR = self.log_path

        app.add_middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        controller = Controller(self.dispatch_method)
        # sys.modules对加载模块进行缓冲，提高程序运行速度
        sys.modules["fastchat.serve.controller"].controller = controller

        @app.on_event("startup")
        async def startup_event():
            if self.prev_event:
                # 进程阻塞等待
                self.prev_event.wait()
            if self.curr_event:
                # 设置event flag = true
                self.curr_event.set()

        return app

    # 通过重写Process类的run()方法，以便进程执行start()时调用
    def run(self):
        uvicorn.run(self.app,
                    host=self.host,
                    port=self.port,
                    log_level="debug")


class FastChatModelRunner(mp.Process):
    '''
    Fastchat model process
    '''

    def __init__(self, prev_event: Event, curr_event: Event, host: str,
                 port: int, log_path: str, model_path: str,
                 model_names: List[str], limit_worker_concurrency: int,
                 controller_addr: str, worker_addr: str, device: str,
                 num_gpus: int, max_gpu_memory: str):
        super().__init__()

        self.prev_event = prev_event
        self.curr_event = curr_event
        self.host = host
        self.port = port
        self.log_path = log_path
        self.model_path = model_path
        self.model_names = model_names
        self.limit_worker_concurrency = limit_worker_concurrency
        self.controller_addr = controller_addr
        self.worker_addr = worker_addr
        self.device = device
        self.num_gpus = num_gpus
        self.max_gpu_memory = max_gpu_memory
        self.app = self._create_controller()

    def _create_controller(self) -> FastAPI:
        from fastapi.middleware.cors import CORSMiddleware
        import fastchat.constants
        fastchat.constants.LOGDIR = self.log_path
        from fastchat.serve.model_worker import app, ModelWorker, worker_id

        app.add_middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        worker = ModelWorker(
            controller_addr=self.controller_addr,
            worker_addr=self.worker_addr,
            worker_id=worker_id,
            model_path=self.model_path,
            model_names=self.model_names,
            limit_worker_concurrency=self.limit_worker_concurrency,
            no_register=False,
            device=self.device,
            num_gpus=self.num_gpus,
            max_gpu_memory=self.max_gpu_memory,
        )

        sys.modules["fastchat.serve.model_worker"].worker = worker

        @app.on_event("startup")
        async def startup_event():
            if self.prev_event:
                self.prev_event.wait()
            if self.curr_event:
                self.curr_event.set()

        return app

    def run(self):
        uvicorn.run(self.app,
                    host=self.host,
                    port=self.port,
                    log_level="debug")


class FastChatApiRunner(mp.Process):
    '''
    Fastchat api process
    '''

    def __init__(self, prev_event: Event, curr_event: Event, host: str,
                 port: int, log_path: str, controller_addr: str,
                 api_keys: List[str]):
        super().__init__()

        self.prev_event = prev_event
        self.curr_event = curr_event
        self.host = host
        self.port = port
        self.log_path = log_path
        self.controller_addr = controller_addr
        self.api_keys = api_keys
        self.app = self._create_controller()

    def _create_controller(self) -> FastAPI:
        from fastchat.serve.openai_api_server import app, app_settings
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        app_settings.controller_address = self.controller_addr
        app_settings.api_keys = self.api_keys

        @app.on_event("startup")
        async def startup_event():
            if self.prev_event:
                self.prev_event.wait()
            if self.curr_event:
                self.curr_event.set()

        return app

    def run(self):
        uvicorn.run(self.app,
                    host=self.host,
                    port=self.port,
                    log_level="debug")


def stop_fastchat(processes: List[mp.Process]):
    for process in processes:
        process.terminate() # 杀死子进程
        process.join(timeout=60)


def main():
    # Init system
    # 获取系统配置参数
    kf_config = config.KBConfig("../config.yaml")
    global logger
    # 日志初始化
    log.KFLog.init_logger(
        kf_config.get_app_log_path(), constants.LOG_LEVEL_DEBUG
        if kf_config.get_app_debug() else constants.LOG_LEVEL_INFO)
        # banner设置
    banner.kf_banner(kf_config.get_app_version(), kf_config.get_app_debug(),
                     kf_config.get_app_log_path())

    # python多进程编程:http://kaito-kidd.com/2018/05/11/python-advance-process-thread/
    # 定义多进程时间Event()
    '''
    https://blog.csdn.net/weixin_43794311/article/details/116116516
    1. event.set:解除阻塞
    2.event.clear:清除状态
    3.event.wait:等待后续继续处理
    https://cloud.tencent.com/developer/article/1485103
    '''
    cr_event = Event()
    mr_event = Event()
    ar_event = Event()

    # Start process
    # 初始化类作为进程
    cr = FastChatControllerRunner(
        None, cr_event, kf_config.get_fastchat_controller_host(),
        int(kf_config.get_fastchat_controller_port()),
        kf_config.get_app_log_path(), "shortest_queue")
    # 启动进程
    cr.start()

    mr = FastChatModelRunner(
        cr_event,
        mr_event,
        kf_config.get_fastchat_model_worker_host(),
        int(kf_config.get_fastchat_model_worker_port()),
        kf_config.get_app_log_path(),
        kf_config.get_fastchat_models_model_path(),
        [
            kf_config.get_fastchat_models_llm_model_name(),
            kf_config.get_fastchat_models_embedding_model_name(),
        ],
        kf_config.get_fastchat_model_worker_limit_worker_concurrency(),
        "http://" + kf_config.get_fastchat_controller_host() + ":" +
        kf_config.get_fastchat_controller_port(),
        "http://" + kf_config.get_fastchat_model_worker_host() + ":" +
        kf_config.get_fastchat_model_worker_port(),
        kf_config.get_fastchat_model_worker_device(),
        int(kf_config.get_fastchat_model_worker_num_gpus()),
        kf_config.get_fastchat_model_worker_max_gpu_memory(),
    )
    mr.start()

    ar = FastChatApiRunner(
        mr_event, ar_event, kf_config.get_fastchat_openai_api_server_host(),
        int(kf_config.get_fastchat_openai_api_server_port()),
        kf_config.get_app_log_path(),
        "http://" + kf_config.get_fastchat_controller_host() + ":" +
        kf_config.get_fastchat_controller_port(), [])
    ar.start()

    # Stop process
    # 主进程等待子进程执行结束
    try:
        cr.join()
        mr.join()
        ar.join()
    except KeyboardInterrupt:
        # 注册函数退出时的回调函数
        atexit.register(stop_fastchat, [cr, mr, ar])


if __name__ == "__main__":
    main()