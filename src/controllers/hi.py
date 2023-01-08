''' 测试接口
'''

from flask import request
from src.lib.resp import Resp
from src.lib.respCode import RespCode

def sayHi():
    resp = Resp(code=RespCode.HI_OK.value, data={'res': 'hi'})
    return resp.res()

def sayHello():
    data = request.get_json()
    who = data.get('greet')

    resp = Resp(code=RespCode.HELLO_OK.value, data={'res': f'hello {who} !'})
    return resp.res()

