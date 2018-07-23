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

    def isAllDontCare(self):
        return True if self._countDontCare() == self.varNum else False

    def _countDontCare(self):
        count = 0
        for e in self.binaryNotation:
            if e == '11':
                count = count + 1
        return count

    def isZero(self):
        return True if '00' in self.binaryNotation else False

    def isUnit(self):
        # only 1 literal is not don't care
        if self._countDontCare() == (self.varNum - 1):
            return self.noneDcEntries[0]
        return 0

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
        if self.isZero():
            return [PcnCube(binaryNotation=['11']*self.varNum)]
        elif self.isAllDontCare():
            return [PcnCube(binaryNotation=['00']*self.varNum)]
        else:
            cubeList = []
            for i in range(self.varNum):
                if self.binaryNotation[i] == '10' or self.binaryNotation[i] == '01':
                    b= ['11']*self.varNum
                    b[i] = self.binaryNotation[i][::-1]
                    cubeList.append(PcnCube(binaryNotation=b))
            return cubeList

class PcnCubeList(object):
    def __init__(self, rawCubeList, varNum):
        self.cubeList = [PcnCube(rawCube=c, varNum=varNum) for c in rawCubeList]
        self.varNum = varNum
        self.originalCubeList = self.cubeList.copy()
        self.unsplittedN = [x+1 for x in range(self.varNum)]

    def _trimZeros(self):
        noneZeroList = []
        for c in self.cubeList:
            if not c.isZero():
                noneZeroList.append(c)
        return noneZeroList

    def _isTautology(self):
        isOne = False
        for c in self.cubeList:
            if c.isAllDontCare():
                isOne = True
        if isOne:
            self.cubeList = ['11']*self.varNum
        return isOne

    def _countPosNeg(self, n):
        pos = 0
        neg = 0
        isBinate = True
        for c in self.originalCubeList:
            if c.getXn(n) == '01':
                pos = pos +1
            elif c.getXn(n) == '10':
                neg = neg +1
        if neg==0 or pos==0:
            isBinate = False
        return {'pos': pos, 'neg': neg, 'isBinate': isBinate}

    def howMuchBinate(self, n):
        pnCount = self._countPosNeg(n)
        if pnCount['isBinate']:
            return max(pnCount['pos'],pnCount['neg'])
        else:
            return -1 

    def posNegNumDiff(self, n):
        pnCount = self._countPosNeg(n)
        if pnCount['isBinate']:
            return abs(pnCount['pos']-pnCount['neg'])
        else:
            return -1

    def getMostBinate(self, specifiedNList = None):
        if specifiedNList:
            nList = specifiedNList
        else:
            nList = [i+1 for i in range(self.varNum)]
        maxBinate = -1
        nMax = []
        for n in nList:
            thisBinate = self.howMuchBinate(n)
            if thisBinate > maxBinate:
                maxBinate = thisBinate
                nMax = []
                nMax.append(n)
            elif thisBinate == maxBinate:
                nMax.append(n)
        return (maxBinate, nMax)

    def getLeastPosNegNumDiff(self, specifiedNList = None):
        if specifiedNList:
            nList = specifiedNList
        else:
            nList = [i+1 for i in range(self.varNum)]
        minDiff = -1
        nMin = []
        for n in nList:
            thisDiff = self.posNegNumDiff(n)
            if thisDiff >= 0:
                if minDiff == -1:
                    minDiff = thisDiff
                if thisDiff < minDiff:
                    minDiff = thisDiff
                    nMin = []
                    nMin.append(n)
                elif thisDiff == minDiff:
                    nMin.append(n)
        return (minDiff, nMin)

    def pickMostShownInAllUnate(self, specifiedNList = None):
        if specifiedNList:
            nList = specifiedNList
        else:
            nList = [i+1 for i in range(self.varNum)]
        maxCount = 0
        nMax = []
        for n in nList:
            d = self._countPosNeg(n)
            if not d['isBinate']:
                thisCount = max(d['pos'], d['neg'])
                if thisCount > maxCount:
                    maxCount = thisCount
                    nMax = []
                    nMax.append(n)
                elif thisCount == maxCount:
                    nMax.append(n)
        return (maxCount, nMax)

    def getMinIndex(self, specifiedNList = None):
        if specifiedNList:
            return min(specifiedNList)
        else:
            return 1

    def whichN2Start(self, specifiedNList = None):
        mostBinateTuple = self.getMostBinate(specifiedNList=specifiedNList)
        isUnate = (mostBinateTuple[0] == -1)
        if not isUnate: # exists binate
            if len(mostBinateTuple[1])==1:
                return mostBinateTuple[1][0]
            else:
                leastNumDiffTuple = self.getLeastPosNegNumDiff(specifiedNList = mostBinateTuple[1])
                if len(leastNumDiffTuple[1])==1:
                    return leastNumDiffTuple[1][0]
                else:
                    return self.getMinIndex(specifiedNList = leastNumDiffTuple[1])
        else: # all unate
            mostShownTuple = self.pickMostShownInAllUnate()
            if len(mostShownTuple[1])==1:
                return mostShownTuple[1][0]
            else:
                return self.getMinIndex(specifiedNList = mostShownTuple[1])

    def _oneStepRecursion(self, n):
        self.unsplittedN.pop(self.unsplittedN.index(n))
        existingCubesNum = len(self.cubeList)
        for i in range(existingCubesNum):
            thisCube = self.cubeList.pop(0)
            posCo = thisCube.getCofactor(n)
            negCo = thisCube.getCofactor(n*(-1))
            compPosCo = posCo.getComplementaryPcnCubes()
            compNegCo = negCo.getComplementaryPcnCubes()
            compPosCoAndN = [c.andWith(n) for c in compPosCo]
            compNegCoAndNBar = [c.andWith(n*(-1)) for c in compNegCo]
            self.cubeList.extend(compPosCoAndN)
            self.cubeList.extend(compNegCoAndNBar)

    def _existAllDontCareCube(self):
        for c in self.cubeList:
            if c.isAllDontCare():
                return True
        return False

    def _existComplementaryUnits(self):
        unitList = []
        for c in self.cubeList:
            unitLiteral = c.isUnit()
            if unitLiteral != 0:
                unitList.append(unitLiteral)
        for u in unitList:
            if u*(-1) in unitList:
                return True
        return False
