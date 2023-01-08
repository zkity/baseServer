
''' 统一返回结构
'''
class Resp(object):

    def __init__(self, code, data=None):
        self.resCode = code
        self.resData = data

    ''' 返回结构的一种
    '''
    def res(self):
        res = {
            'code': self.resCode
        }
        if self.resData is not None:
            res['data'] = self.resData
        return res