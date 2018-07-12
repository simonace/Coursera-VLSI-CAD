class PcnFile(object):

    def __init__(self, fileName):
        self.fileName = fileName
        try:
            self.rawFile = open(fileName)
        except:
            raise Exception("File Name Error!")

    def _isRawCubeFormatCorrect(self, rawCube):
        return True if int(rawCube[0]) == len(rawCube) - 1 else False

    def parseFileCrudely(self):
        if self.rawFile:
            f = self.rawFile
        else:
            raise Exception("File doesn't Exist!")
        f.seek(0,0)
        try:
            self.varNum = int(f.readline().strip())
            self.cubeNum = int(f.readline().strip())
        except:
            raise Exception("Input File Format Error! (Head)")
        self.rawCubeList = []
        for i in range(self.cubeNum):
            self.rawCubeList.append(f.readline().strip().split())
        for l in self.rawCubeList:
            if not self._isRawCubeFormatCorrect(l):
                raise Exception("Cube line format wrong!")
