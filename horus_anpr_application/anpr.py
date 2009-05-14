

class PlateDetection(object):
    """
        returns the plate string extracted from a car image
        
        parameters
            carImage: the car image to be recognized, this object must be an
                      horus image. 
    """    
    def getPlate(self, carImage):
        pass
    
class Region(object):  
    """
        returns a sorted region candidate list. The list is sorted by the
        probability of existence of the searched region in the candidates.
        
        parameters
            candidateList: the candidate list to be sorted.
           
    """
    def sortCandidateList(self, candidateList):
        pass
    
    def getCutSensibility(self):
        pass    
    
    def getFootConstants(self):
        pass
    
    def getBlurredList(self, listToBlur):
        pass
    
    def getProjection(self):
        pass
    
    def calculatePeak(self, projection):
       pass
    
    def locateCandidateList(self, values_list):
       pass
    
    def getRegion(self):
        pass    
    
class Band(Region):
     
    def getCutSensibility(self):
        pass
    
    def getFootConstants(self):
        pass
    
    def getBlurredList(self, listToBlur):
        pass
    
    def getProjection(self):
        pass
    
    def getRegion(self):
        pass

class Plate(Region):
     
    def getCutSensibility(self):
        pass
    
    def getFootConstants(self):
        pass
    
    def getBlurredList(self, listToBlur):
        pass
    
    def getProjection(self):
        pass
    
    def getRegion(self):
        pass
    
    def segment(self):
        pass
    
    def isPlate(self):
        pass

class Character(object):
    def recognize(self):
        pass