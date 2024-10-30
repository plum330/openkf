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
import datetime
# 导入日志模块
from loguru import logger
import constants.constants as constants
"""
os.path.dirname(__file__)获取到当前模块路径
os.path.dirname("xxx")获取上一层路径
sys.path.append()将相关路径添加到python解释器搜索路径中
"""
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

#python类中存在的函数有：构造函数(__init__)、 普通函数def(self, ..)也是实例方法， @staticmethod() @classmethod(cls)
# 定义日志类
class KFLog:
    # 定义类成员变量，相当于是类共用变量， 不需要共用的变量可以定义成实例变量
    # __init__函数是用于类实例化的，如果类没有定义该函数，则说明该类不能/不需要实例化
    # 日志文件&路径
    # datetime.datetime.now()获取当前时间
    # strftime格式化时间
    log_path = datetime.datetime.now().strftime("logs/%Y-%m-%d.log")
    # 日志默认登录
    log_level = constants.LOG_LEVEL_INFO

    # @staticmethod，可不实例化直接访问，基本上只是一个函数，在语法上就像一个方法一样，但不能访问该对象。可用于如参数校验
    # https://blog.csdn.net/qq_23981335/article/details/103798741
    # @classmethod修饰的方法不需要实例化，可用于在类初始化前(执行__init__)，先进行一些处理
    @classmethod
    def init_logger(cls, log_path: str, log_level: str):
        KFLog.log_level = log_level
        KFLog.log_path = os.path.join(log_path, datetime.datetime.now().strftime("%Y-%m-%d.log"))
        logger.add(KFLog.log_path, rotation="10 MB", retention="1 day", level=cls.log_level)

    @classmethod
    def get_logger(cls):
        return logger


# python类继承：https://www.cnblogs.com/bigberg/p/7182741.html
# python类多态： https://www.cnblogs.com/yund/p/17371708.html