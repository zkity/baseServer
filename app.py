#!/usr/bin/env python3

# 基础库
import os
import yaml

# 日志
import logging

# Flask 处理请求
from flask import Flask, request

# 限制频率
from flask_limiter import Limiter

# CORS
from flask_cors import CORS

# 定时任务
from flask_apscheduler import APScheduler

# 功能API
from src.db.database import DataBase
from src.lib.basePath import BasePath
from src.lib.jsonEncoder import JSONEncoder
from src.lib.volumeTool import VolumeTool
from src.routers.routerBase import RouterBase
from src.lib.limitFun import LimitFun
from src.lib.schedulerJob import SchedulerJob
from src.lib.promision import Promision

''' 获取全局变量 '''
db = DataBase.DB
basePath = BasePath.BASE_PATH

''' logger配置 '''
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(os.path.join(basePath, 'log/run.log'), encoding='UTF-8')
formatter = logging.Formatter("%(asctime)s - %(funcName)s - %(lineno)d -%(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

''' 初始化Flask '''
app = Flask(__name__)
app.json_encoder = JSONEncoder

''' 加载flask配置 '''
flaskConfigPath = os.path.join(basePath, 'config/flask.yaml')
with open(flaskConfigPath, 'r') as rf:
    flaskConfig = yaml.safe_load(rf)
app.config.update(flaskConfig)

''' 初始化数据库配置 '''
db.init_app(app)

''' 加载用户自定义配置 '''
userConfigPath = os.path.join(basePath, 'config/user.yaml')
with open(userConfigPath, 'r') as rf:
    userConfig = yaml.safe_load(rf)
userConfig = VolumeTool().checkPath(userConfig)
app.config.update(userConfig)

''' 注册router '''
b1 = RouterBase().inst()
app.register_blueprint(b1)

''' 通用限频配置 '''
limiter = Limiter(app, key_func=LimitFun().xForwordFun, default_limits=["100 per day", "2 per second"])

# 限频白名单
@limiter.request_filter
def method_whitelist():
    return request.method == "OPTIONS"

''' 开启跨域 '''
CORS(app, resources={ r'/*': {'origins': app.config['ORIGINS']}}, supports_credentials=True)

''' 定时任务 '''
scheduler = APScheduler()
job = SchedulerJob(app)

# 每周天的零点执行 sayHiJob
@scheduler.task('cron', id='sayHiJob', week='*', day_of_week='sun', hour='00', minute='00', second='00')
def sayHiJob():
    job.sayHi()

scheduler.init_app(app)
scheduler.start()

''' 权限配置 '''
rolePath = os.path.join(basePath, 'config/role.yaml')

# 全局拦截器
@app.before_request
def beforReq():
    promission = Promision(rolePath=rolePath)
    promission.check()

if __name__ == '__main__':
    # 删除所有表并新建
    with app.app_context():
        db.drop_all()
        db.create_all()