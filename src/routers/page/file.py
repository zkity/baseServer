from src.controllers.file import upload
from src.controllers.file import download

def router(b1):
    b1.route('/upload', methods=['POST'])(upload)
    b1.route('/download', methods=['GET'])(download)