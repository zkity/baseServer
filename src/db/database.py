from src.lib.singleton import Singleton
from flask_sqlalchemy import SQLAlchemy

''' 数据库连接的单例
'''
class DataBase(object, metaclass=Singleton):
    DB = SQLAlchemy()