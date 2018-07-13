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


class PcnCube(object):
    def __init__(self, rawCube=[], varNum=0, binaryNotation=[]):
        if varNum>0 and rawCube:
            self.varNum = varNum
            self.noneDcEntryNum = int(rawCube[0])
            self.noneDcEntries = [int(e) for e in rawCube[1:]]
            self.getBinaryNotationForm()
        elif binaryNotation:
            self.varNum = len(binaryNotation)
            if varNum>0:
                if varNum != self.varNum:
                    raise Exception("The given number of variable is inconsistent with the number of variable in the given cube.")
            self.binaryNotation = binaryNotation
            self.getNoneDontCareEntryListForm()
            self._refreshNoneDcEntryNum()
        else:
            raise Exception("PcnCube construction error!")

    def getBinaryNotationForm(self):
        self.binaryNotation = PcnCube.convertToBinaryNotationForm(self.noneDcEntries, self.varNum)
        return self.binaryNotation

    def getNoneDontCareEntryListForm(self):
        self.noneDcEntries = PcnCube.convertToNoneDontCareEntryListForm(self.binaryNotation, self.varNum)
        return self.noneDcEntries

    def convertToBinaryNotationForm(noneDcEntries, varNum):
        binaryNotationList = ['11']*varNum
        for entry in noneDcEntries:
            if entry < 0:
                binaryNotationList[entry*(-1)-1] = '10'
            elif entry > 0:
                binaryNotationList[entry-1] = '01'
            else:
                binaryNotationList = ['00']*varNum
        return binaryNotationList

    def convertToNoneDontCareEntryListForm(binaryNotationList, varNum):
        if varNum != len(binaryNotationList):
            raise Exception("PCN entry number is inconsistent with the given variable number!")
        else:
            noneDcEntries = []
            for i in range(varNum):
                if binaryNotationList[i] == '01':
                    noneDcEntries.append(i+1)
                elif binaryNotationList[i] == '10':
                    noneDcEntries.append(-1*(i+1))
                elif binaryNotationList[i] == '00':
                    return [0]
                elif binaryNotationList[i] != '11':
                    raise Exception("PCN entry must be one of '01', '10' and '11'.")
            return noneDcEntries

    def _refreshNoneDcEntryNum(self):
        self.noneDcEntryNum = self.varNum - self._countDontCare()

    def _isAllDontCare(self):
        return True if self._countDontCare() == self.varNum else False

    def _countDontCare(self):
        count = 0
        for e in self.binaryNotation:
            if e == '11':
                count = count + 1
        return count

    def _isZero(self):
        return True if '00' in self.binaryNotation else False

    def getXn(self, n):
        return self.binaryNotation[n-1]

    def getCofactor(self, n):
        tempBn = self.binaryNotation.copy()
        if n>0:
            if tempBn[n-1] == '01':
                tempBn[n-1] = '11'
                return PcnCube(binaryNotation=tempBn)
            elif tempBn[n-1] == '10':
                return PcnCube(binaryNotation=(['00']*self.varNum))
            elif tempBn[n-1] == '11' or tempBn[n-1] == '00':
                return PcnCube(binaryNotation=tempBn)
        elif n<0:
            n = n*(-1)
            if tempBn[n-1] == '01':
                return PcnCube(binaryNotation=['00']*self.varNum)
            elif tempBn[n-1] == '10':
                tempBn[n-1] = '11'
                return PcnCube(binaryNotation=tempBn)
            elif tempBn[n-1] == '11' or tempBn[n-1] == '00':
                return PcnCube(binaryNotation=tempBn)
        else:
            raise Exception("ValueError: n must be a postive or negative integer.")

    def andWith(self, n):
        tempBn = self.binaryNotation.copy()
        if n>0:
            if tempBn[n-1] == '01':
                return PcnCube(binaryNotation=tempBn)
            elif tempBn[n-1] == '10' or tempBn[n-1] == '00':
                return PcnCube(binaryNotation=(['00']*self.varNum))
            elif tempBn[n-1] == '11':
                tempBn[n-1] = '01'
                return PcnCube(binaryNotation=tempBn)
        elif n<0:
            n = n*(-1)
            if tempBn[n-1] == '01' or tempBn[n-1] == '00':
                return PcnCube(binaryNotation=['00']*self.varNum)
            elif tempBn[n-1] == '10':
                return PcnCube(binaryNotation=tempBn)
            elif tempBn[n-1] == '11':
                tempBn[n-1] = '10'
                return PcnCube(binaryNotation=tempBn)
        else:
            raise Exception("ValueError: n must be a postive or negative integer.")

    def getComplementaryPcnCubes(self):
        # returns a list (containing 1 or more elements)
        if self._isZero():
            return [PcnCube(binaryNotation=['11']*self.varNum)]
        elif self._isAllDontCare():
            return [PcnCube(binaryNotation=['00']*self.varNum)]
        else:
            cubeList = []
            for i in range(self.varNum):
                if self.binaryNotation[i] == '10' or self.binaryNotation[i] == '01':
                    b= ['11']*self.varNum
                    b[i] = self.binaryNotation[i][::-1]
                    cubeList.append(PcnCube(binaryNotation=b))
            return cubeList
