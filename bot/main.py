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

import utils.config as config
import utils.log as log
from utils import banner
import constants.constants as constants
from router.router import get_api

import os
import uvicorn

# Version 1.1.0
logger = None


def run(config: config.KBConfig):
    # app是构建的业务服务端server
    app = get_api(config)
    # 运行web服务host/port
    uvicorn.run(app, host=config.get_app_host(), port=config.get_app_port())


def main():
    # Init system
    # 读取系统配置文件
    kf_config = config.KBConfig("config.yaml")
    global logger
    # 初始化日志log(日志路径/日志等级)
    log.KFLog.init_logger(
        kf_config.get_app_log_path(), constants.LOG_LEVEL_DEBUG
        if kf_config.get_app_debug() else constants.LOG_LEVEL_INFO)
    # 设置全局日志
    logger = log.KFLog.get_logger()
    banner.kf_banner(kf_config.get_app_version(), kf_config.get_app_debug(),
                     kf_config.get_app_log_path())

    # Init env
    # 设置langchain运行的环境变量
    os.environ["OPENAI_API_KEY"] = kf_config.get_openai_api_key()
    os.environ["OPENAI_API_BASE"] = "http://" + kf_config.get_fastchat_openai_api_server_host() + \
        ":" + kf_config.get_fastchat_openai_api_server_port() + "/v1"

    # Run
    run(kf_config)


if __name__ == "__main__":
    main()

"""
python虚拟环境作用：不同的项目需要使用不同版本对的包，可能会产生冲突，这是就需要一个虚拟环境将每个项目需要的包进行独立，有效避免冲突。
所以虚拟环境用于管理不同项目的依赖包。
"""