from src.controllers.user import login
from src.controllers.user import changePass

def router(b1):
    b1.route('/login', methods=['POST'])(login)
    b1.route('/changePass', methods=['POST'])(changePass)