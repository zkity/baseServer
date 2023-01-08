import os
import jwt
import sys
import yaml

from src.lib.role import Role
from flask import request, abort, current_app, g
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError, InvalidTokenError

''' 鉴别权限
'''
class Promision(object):

    def __init__(self, rolePath):

        rolePath = os.path.join(rolePath)

        self.logger = current_app.logger
        self.salt = current_app.config['SALT']

        self.roleConfig = None
        with open(rolePath, 'r') as rf:
            self.roleConfig = yaml.safe_load(rf)

        if self.roleConfig:
            for k, v in self.roleConfig.items():
                self.roleConfig[k] = set(v)
        else:
            self.logger.error('初始化权限失败')
            sys.exit()
        
        # 获取权限 值-名称 字典
        self.roleMap = dict()
        for item in Role:
            self.roleMap[item.value] = item.name

    ''' 自定义权限的鉴别
    '''
    def check(self):
        reqMethod = request.method
        url = request.path

        self.logger.info(f'[promision check] request: {url}, method: {reqMethod}')

        # 放行 OPTIONS 请求
        if reqMethod == 'OPTIONS':
            self.logger.info('[promision check] res: pass, as: OPTIONS allow')
        else:
            resCode = 500

            # 放行登陆请求
            if url == '/login':
                self.logger.info('[promision check] res: pass, as: login allow')
            else:
                ''' 检查Token '''
                token = None
                # 下载GET链接鉴别参数
                if url.split('/')[-1] == 'download':
                    token = request.args.get('token')
                # 普通请求鉴别请求头Authorization
                else:
                    token = request.headers.get('Authorization', default=None)

                if token is None:
                    self.logger.error('[promision check] res: forbidden, as: token missing')
                    resCode = 401
                else:
                    # 解析token成功
                    try:
                        tokenDec = jwt.decode(token, self.salt, algorithms=["HS256"], verify=True)
                        self.logger.info('[promision check] res: pass, as: token check success')
                        resCode = 1
                    # token 过期
                    except ExpiredSignatureError:
                        self.logger.error('[promision check] res: forbidden, as: token expried')
                        resCode = 405
                    # token 被篡改
                    except InvalidSignatureError:
                        self.logger.error('[promision check] res: forbidden, as: token invalid')
                        resCode = 404
                    # 其他错误
                    except InvalidTokenError:
                        self.logger.error('[promision check] res: forbidden, as: token check failed')
                        resCode = 406
                if resCode != 1:
                    # token 检查完成，失败则返回
                    abort(resCode)
                else:
                    ''' 检查权限 '''
                    role = tokenDec.get('role')
                    roleCode = 500
                    if role in self.roleMap:
                        allowSetName = self.roleMap.get(role)
                        if allowSetName in self.roleConfig:
                            allowSet = self.roleConfig.get(allowSetName)
                            # 没有权限
                            if url in allowSet:
                                self.logger.error('[promision check] res: forbidden, as: promision denied')
                                roleCode = 403
                            else:
                                self.logger.info('[promision check] res: pass, as: promision check success')
                                roleCode = 1
                                g.user = tokenDec.get('user')
                                g.role = role
                        # 权限配置文件解析错误
                        else:
                            self.logger.error('[promision check] res: forbidden, as: promision config file error')
                            roleCode = 406
                    # role参数配置错误
                    else:
                        self.logger.error('[promision check] res: forbidden, as: role config file error')
                        roleCode = 406
                    
                    if roleCode != 1:
                        abort(roleCode)