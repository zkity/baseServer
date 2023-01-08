import os

from src.lib.basePath import BasePath

from src.lib.singleton import Singleton
from flask import Blueprint

class RouterBase(object, metaclass=Singleton):

    def __init__(self):
        self.b1 = Blueprint('b1', __name__)

        basePath = BasePath.BASE_PATH

        routers = os.listdir(os.path.join(basePath, 'src/routers/page'))
        routers = [x.replace('.py', '') for x in routers if x.endswith('.py')]

        for router in routers:
            exec(f'from src.routers.page import {router}')
            exec(f'{router}.router(self.b1)')
    
    def inst(self):
        return self.b1
