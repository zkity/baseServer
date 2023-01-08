''' 用户相关实现

login - 登陆
changePass - 改密码
register - 注册
'''
import jwt
import time

from src.beans.user import User
from flask import current_app, request, g

from src.db.database import DataBase

from src.lib.resp import Resp
from src.lib.respCode import RespCode

db = DataBase.DB

''' 登陆方法
@method: post
@param:
    @require:
    user: String 用户名
    pass: String 密码的sha256摘要
    @optional:
    week: Int 1-jwt有效时间1周, 0-jwt有效时间1小时, 默认为1小时
'''
def login():
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    salt = current_app.config['SALT']
    exp = int(time.time() + 3600)
    expWeek = int(time.time() + 604800)

    data = request.get_json()
    user = data.get('user')
    passwd = data.get('pass')
    week = data.get('week')

    if (user and passwd) is None:
        # 参数不全
        res = Resp(code=RespCode.LOGIN_PARAM_ERR.value)
    else:
        iden = db.session.query(User.passwd, User.role).filter(User.user == user).all()
        if len(iden) > 0:
            dbPass = iden[0][0]
            role = iden[0][1]
            if dbPass == passwd:
                if week == "1":
                    exp = expWeek
                payload = {
                    'user': user,
                    'exp': exp,
                    'role': role
                }
                token = jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers)
                # 验证成功，并返回token
                res = Resp(code=RespCode.LOGIN_OK.value, data={'token': token})
            else:
                # 密码错误
                res = Resp(code=RespCode.LOGIN_PASS_ERR.value)
        else:
            # 用户名错误
            res = Resp(code=RespCode.LOGIN_USER_ERR.value)
    return res.res()


''' 改密码
@method: post
@param: ora: String 原密码的sha256摘要
@param: new: String 新密码的sha256摘要
'''
def changePass():
    data = request.get_json()
    oraPass = data.get('ora')
    newPass = data.get('new')

    # 新密码为空
    if newPass == 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855':
        res = Resp(code=RespCode.CHANGE_PASS_NEW_ERR)

    user = g.user
    iden = db.session.query(User.passwd, User.role).filter(User.user == user).all()
    if len(iden) > 0:
        dbPass = iden[0][0]
        if dbPass == oraPass:
            db.session.query(User).filter(User.user == user).update({User.passwd: newPass})
            # 修改成功
            res = Resp(code=RespCode.CHANGE_PASS_OK)
        else:
            # 原密码错误
            res = Resp(code=RespCode.CHANGE_PASS_ORA_ERR)
    # 用户不存在
    else:
        res = Resp(code=RespCode.CHANGE_PASS_USER_ERR)

    return res.res()

# TODO: 增加注册功能
def register():
    pass
