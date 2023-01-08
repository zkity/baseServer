import os
from src.lib.basePath import BasePath

''' 检查volume目录是否存在，不存在则创建
'''
class VolumeTool():
    def __init__(self) -> None:
        self.baseDir = BasePath.BASE_PATH

    def checkPath(self, pathDict):
        iden = 'VOLUME'
        if iden in pathDict:
            resDict = dict()
            volumeDict = pathDict.get(iden)
            for k, v in volumeDict.items():
                tarPath = os.path.join(self.baseDir, v)
                if not os.path.exists(tarPath):
                    os.makedirs(tarPath)
                resDict[k] = tarPath

                pathDict[k] = tarPath

        return pathDict
