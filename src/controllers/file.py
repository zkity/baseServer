''' 文件上传及下载功能

'''

import os
import time
from werkzeug.utils import secure_filename
from flask import current_app, request, Response

from src.lib.resp import Resp
from src.lib.respCode import RespCode

''' 文件上传

@method: post

@param: file 上传的文件
'''
def upload():
    allowSuffix = ['pdf', 'epub']

    current_app.logger.info("upload call")
    if 'file' not in request.files:
        res = Resp(RespCode.UPLOAD_FILE_ERR.value)

    fileReq = request.files['file']

    file_ora_name = fileReq.filename
    if file_ora_name:
        if file_ora_name == '':
            res = Resp(RespCode.UPLOAD_NAME_ERR.value)
        else:
            suffix = file_ora_name.split('.')[-1]
            if suffix in allowSuffix:
                file_name = secure_filename(file_ora_name)
                current_app.logger.warning(f"upload file name: {file_name}")
                file_save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)
                fileReq.save(file_save_path)
                file_size = os.path.getsize(file_save_path)

                res = Resp(code=RespCode.UPLOAD_FILE_OK.value, data={'name': file_name, 'size': file_size})
            else:
                res = Resp(code=RespCode.UPLOAD_TYPE_ERR.value)
    else:
        res = Resp(code=RespCode.UPLOAD_NAME_ERR.value)

    return res.res()

''' 文件下载
@method: get
@param:
    id: String 文件id
    suffix: String 文件后缀
    name: String 文件名
'''
def download():
    fileId = request.args.get('id')
    suffix = request.args.get('suffix')
    fileName = request.args.get('name')

    fileName = f'{fileName}.{suffix}'
    saveName = f'{fileId}.{suffix}'

    return streamDownload(current_app.config['DOWNLOAD_FOLDER'], saveName, fileName)

''' 流式下载文件
@param:
    baseDir: String 下载目录
    savaName: String fileId.suffix
    fileName: String fileName.suffix
'''
def streamDownload(baseDir, saveName, fileName):
    def send():
        with open(filePath, 'rb') as source:
            while 1:
                cache = source.read( 1 * 1024 * 1024)
                if not cache:
                    break
                yield cache
    filePath = os.path.join(baseDir, saveName)
    if os.path.exists(filePath):
        response = Response(send(), content_type="application/octet-stream")
        response.headers["Content-disposition"] = f"attachment; filename={fileName}"
        return response
    else:
        return Resp(code=RespCode.DOWNLOAD_FILE_ERR.value, data={"fileID not exit": saveName}).res()