#!/usr/bin/python3
# coding=utf-8

import os
from src.lib.singleton import Singleton

''' 获取工程的根目录
'''
class BasePath(object, metaclass=Singleton):
    BASE_PATH = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
