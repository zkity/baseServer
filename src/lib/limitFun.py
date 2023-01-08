from flask import request

''' 设置限频的方法
'''
class LimitFun(object):

    ''' 通过请求的 X-Forwarder-For 识别
    '''
    def xForwordFun(self):
        return str(request.headers.get("X-Forwarded-For", "127.0.0.1"))