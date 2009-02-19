import unittest
import os
from PIL import Image as PilImage
import featureExtraction
import image
class FeatureExtractionTest(unittest.TestCase):    
    def setUp(self):
        abspath = os.path.abspath('.')
        self.imagePath = os.path.join(abspath,"testImages/regionTestImage.PNG")
        self.edPath = os.path.join(abspath,"testImages/edgeDetectionTest.PNG")
        self.edPath2 = os.path.join(abspath,"testImages/edgeDetectionTest2.PNG")        
#        image1 = PilImage.open(self.edPath2)
#        image1 = image1.convert("L") 
#        image1.save(self.edPath2)
        self.edImage = image.Image(path = self.edPath)
        self.edImage2 = image.Image(path = self.edPath2)
        self.regionTestImage = image.Image(path = self.imagePath)               
    
    def testGetSixRegionList(self):
        print
        r0 = [0,0,0,0,0,0,0,0]
        r1 = [50,50,50,50,50,50,50,50]
        r2 = [100,100,100,100,100,100,100,100]
        r3 = [150,150,150,150,150,150,150,150]
        r4 = [200,200,200,200,200,200,200,200]
        r5 = [250,250,250,250,250,250,250,250]
        assert (8,6) == self.regionTestImage.size, "The image size must be: " + str(self.regionTestImage.size)        
        sixRegionList = featureExtraction.getSixRegionList(self.regionTestImage)                
        assert 6 == len(sixRegionList)        
        assert r0 == list(sixRegionList[0].content.getdata())
        assert r1 == list(sixRegionList[1].content.getdata())
        assert r2 == list(sixRegionList[2].content.getdata())
        assert r3 == list(sixRegionList[3].content.getdata())
        assert r4 == list(sixRegionList[4].content.getdata())
        assert r5 == list(sixRegionList[5].content.getdata())
        
    def testExtractFeatureByEdgeDetection(self):
        print
        featureMatrix = featureExtraction.extractFeatureByEdgeDetection(
                                                                self.edImage)        
        assert 6 == len(featureMatrix[0])
        assert 10 == len(featureMatrix)     
        
        assert 1 == featureMatrix[2][0], featureMatrix[0]
        assert 1 == featureMatrix[3][0], featureMatrix[0]
        assert 1 == featureMatrix[6][1], featureMatrix[6]
        assert 1 == featureMatrix[7][2], featureMatrix[7]
        assert 1 == featureMatrix[5][3], featureMatrix[5]
        assert 1 == featureMatrix[0][4], featureMatrix[0]
        assert 1 == featureMatrix[4][5], featureMatrix[4]
        
    def testExtractFeatureByEdgeDetection2(self):
        print
        featureMatrix = featureExtraction.extractFeatureByEdgeDetection(
                                                                self.edImage2)        
        assert 6 == len(featureMatrix[0])
        assert 10 == len(featureMatrix)
        
        assert 1 == featureMatrix[2][0], featureMatrix[0]
        assert 2 == featureMatrix[3][0], featureMatrix[0]
        assert 1 == featureMatrix[6][1], featureMatrix[6]
        assert 1 == featureMatrix[7][2], featureMatrix[7]
        assert 1 == featureMatrix[6][2], featureMatrix[6]
        assert 1 == featureMatrix[5][3], featureMatrix[5]
        assert 1 == featureMatrix[0][4], featureMatrix[0]
        assert 1 == featureMatrix[4][5], featureMatrix[4]