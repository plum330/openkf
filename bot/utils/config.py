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

import sys
import os 

import yaml
from colorama import Fore
# 等价于sys.path.append('..') 获取上一层目录
# https://blog.csdn.net/JOJOY_tester/article/details/54598713
"""
sys.path是Python解释器搜索模块的目录列表
所以sys.path.append的作用就是将项目中的模块路径追加到python解释器的搜索列表中
"""
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# 定义配置读取类
class KBConfig:
    '''
    KBConfig is a class that loads the configuration file.
    Use load_config to load the configuration file, and use get_* to get the configuration.
    '''
    # 定义类构造函数(实例初始化函数),指定file变量类型是str， 返回值是空None
    def __init__(self, file: str) -> None:
        # 初始化_config变量为None
        self._config = None
        # 文件打开操作
        with open(file, encoding="utf-8") as fp:
            # fp.read()文件读操作
            self._config = yaml.safe_load(fp.read()) # yaml文件读操作

    ###############################
    # OpenKF bot config
    ###############################
    # 定义从配置文件self._config变量中获取各个配置字段，并指定函数的返回类型
    def get_app_version(self) -> str:
        return self._config['app']['version']

    def get_app_host(self) -> str:
        """
        这是python条件表达式的写法
        也可以改写成[self._config['app']['host'], "0.0.0.0"][self._config['app']['host']==""],
        False返回第一个， True返回第二个。
        if 字符串非空时 认为是True，否则False
        下面的语句相当于是：
        if self._config['app']['host']:
            return self._config['app']['host']
        else:
            return '0.0.0.0'
        """
        return self._config['app']['host'] if self._config['app']['host'] else "0.0.0.0"

    def get_app_port(self) -> str:
        return self._config['app']['port']

    def get_app_debug(self) -> str:
        return self._config['app']['debug']
    
    def get_app_file_dir(self) -> str:
        return self._config['app']['file_dir']

    def get_app_log_path(self) -> str:
        return self._config['app']['log_path']

    def get_app_doc(self) -> str:
        return self._config['app']['doc']
    
    def get_app_token(self) -> str:
        return self._config['app']['token']
    
    def get_openai_api_key(self) -> str:
        return self._config['app']['openai_api_key']

    ###############################
    # LLM langchain config
    ###############################
    def get_inference_device(self) -> str:
        return self._config['inference']['device']

    def get_model_history(self) -> str:
        return self._config['model']['history']

    def get_model_temperature(self) -> str:
        return self._config['model']['temperature']

    def get_model_top_k(self) -> str:
        return self._config['model']['top_k']

    def get_model_top_p(self) -> str:
        return self._config['model']['top_p']
    
    ###############################
    # LLM fastchat config
    ###############################
    def get_fastchat_models_model_path(self) -> str:
        # 强制转换成字符串类型
        return str(self._config['fastchat']['models']['model_path'])
    
    def get_fastchat_models_llm_model_name(self) -> str:
        return str(self._config['fastchat']['models']['llm_model_name'])
    
    def get_fastchat_models_embedding_model_name(self) -> str:
        return str(self._config['fastchat']['models']['embedding_model_name'])
    
    def get_fastchat_controller_host(self) -> str:
        return str(self._config['fastchat']['controller']['host'])
    
    def get_fastchat_controller_port(self) -> str:
        return str(self._config['fastchat']['controller']['port'])
    
    def get_fastchat_model_worker_host(self) -> str:
        return str(self._config['fastchat']['model_worker']['host'])
    
    def get_fastchat_model_worker_port(self) -> str:
        return str(self._config['fastchat']['model_worker']['port'])
    
    def get_fastchat_model_worker_device(self) -> str:
        return str(self._config['fastchat']['model_worker']['device'])
    
    def get_fastchat_model_worker_limit_worker_concurrency(self) -> str:
        return str(self._config['fastchat']['model_worker']['limit_worker_concurrency'])
    
    def get_fastchat_model_worker_num_gpus(self) -> str:
        return str(self._config['fastchat']['model_worker']['num_gpus'])
   
    def get_fastchat_model_worker_max_gpu_memory(self) -> str:
        return str(self._config['fastchat']['model_worker']['max_gpu_memory'])
    
    def get_fastchat_openai_api_server_host(self) -> str:
        return str(self._config['fastchat']['openai_api_server']['host'])
    
    def get_fastchat_openai_api_server_port(self) -> str:
        return str(self._config['fastchat']['openai_api_server']['port'])
    
    ###############################
    # Milvus config
    ###############################
    def get_milvus_host(self) -> str:
        return self._config['milvus']['host']
    
    def get_milvus_port(self) -> str:
        return self._config['milvus']['port']
    
    def get_milvus_top_k(self) -> str:
        return self._config['milvus']['top_k']
    
    def get_milvus_score_threshold(self) -> str:
        return self._config['milvus']['score_threshold']