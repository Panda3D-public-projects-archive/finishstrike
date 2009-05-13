

class PlateDetection(object):
    def locateBandList(self):
        pass
    def sortBandList(self, bandList):
        pass
    def getPlate(self):
        pass
    
class Region(object):
    def locateCandidateList(self, values_list, report):
       pass    
    def sortCandidateList(self):
        pass        
    def locateCandidateList(self):
        pass
    def getRegion(self):
        pass    
    
class Band(object):
    def locatePlateList(self):
        pass
    def sortPlateList(self):
        pass
    def getPlate(self):
        pass

class Plate(object):
    def segment(self):
        pass
    def isPlate(self):
        pass

class Character(object):
    def recognize(self):
        pass