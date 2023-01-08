#!/usr/bin/python3
# coding=utf-8

''' 单例的一种实现，使用metaclass的方法，推荐使用的方法

@Usage:
    class MyClass(BaseClass, metaclass=Singleton):
        pass
'''

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
