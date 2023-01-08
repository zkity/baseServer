from src.db.database import DataBase

db = DataBase.DB

''' 用户表
'''
class User(db.Model):
    __tablename__ = 'user'

    key = db.Column(db.Integer(), autoincrement=True, unique=True, primary_key=True, nullable=False)
    user = db.Column(db.String(100), nullable=False, unique=True, index=True)
    passwd = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Integer(), autoincrement=True, nullable=False, index=True)
    active = db.Column(db.Boolean, nullable=False, unique=False, index=True)
    date = db.Column(db.DateTime, server_default=db.func.now(), nullable=False, unique=False)