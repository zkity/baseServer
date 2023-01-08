from src.controllers.hi import sayHi
from src.controllers.hi import sayHello

def router(b1):
    b1.route('/hi', methods=['GET'])(sayHi)

    b1.route('/hello', methods=['POST'])(sayHello)