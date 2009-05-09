import unittest
import os
from PIL import Image as PilImage
import horus.core.computervision.featureExtraction as featureExtraction
import horus.core.computervision.image as image
class FeatureExtractionTest(unittest.TestCase):    
    def setUp(self):
        abspath = os.path.abspath('.')
        self.imagePath = os.path.join(abspath,"testImages/regionTestImage.PNG")
        self.edPath = os.path.join(abspath,"testImages/edgeDetectionTest.PNG")
        self.edPath2 = os.path.join(abspath,"testImages/edgeDetectionTest2.PNG")        
        self.edImage = image.Image(self.edPath)
        self.edImage2 = image.Image(self.edPath2)
        self.regionTestImage = image.Image(self.imagePath)               
    
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
        assert r0 == list(sixRegionList[0].getdata())
        assert r1 == list(sixRegionList[1].getdata())
        assert r2 == list(sixRegionList[2].getdata())
        assert r3 == list(sixRegionList[3].getdata())
        assert r4 == list(sixRegionList[4].getdata())
        assert r5 == list(sixRegionList[5].getdata())
        
    def testExtractFeatureByEdgeDetection(self):
        print
        featureMatrix = featureExtraction.extractFeatureByEdgeDetection(self.edImage)        
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
        featureMatrix = featureExtraction.extractFeatureByEdgeDetection(self.edImage2)        
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
        
    def testGet2Loops(self):
        
        abspath = os.path.abspath('.')
        imagePath = os.path.join(abspath,"testImages/two_squares.PNG")
        imageP = image.Image(image_path= imagePath)
        assert 2 == featureExtraction.getNumLoops(imageP), featureExtraction.getNumLoops(imageP)
        
    def testGet3Loops(self):
        
        abspath = os.path.abspath('.')
        imagePath = os.path.join(abspath,"testImages/three_squares.PNG")
        imageP = image.Image(image_path= imagePath)
        assert 3 == featureExtraction.getNumLoops(imageP), featureExtraction.getNumLoops(imageP)
        
    def testGet2LoopsFromBChar(self):
        
        abspath = os.path.abspath('.')
        imagePath = os.path.join(abspath,"testImages/b_SK.PNG")
        imageP = image.Image(image_path= imagePath)
        assert 2 == featureExtraction.getNumLoops(imageP), \
                                    featureExtraction.getNumLoops(imageP)
        
    def testBlackIntensity4Regions(self):
        
        abspath = os.path.abspath('.')
        imagePath = os.path.join(abspath,"testImages/blackItensityTest.PNG")
        imageP = image.Image(imagePath)
        
        output_expected = [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 
                        0, 0, 0, 2, 1, 0, 3, 1, 0, 0, 0, 0, 0]
        assert  output_expected == featureExtraction.blocksIntensity(imageP), \
                                 featureExtraction.blocksIntensity(imageP)
        
    def testBlackIntensityFourNumber(self):
        
        abspath = os.path.abspath('.')
        imagePath = os.path.join(abspath,"testImages/blackItensityTestNumberFour.PNG")
        imageP = image.Image(imagePath)
        output_expected = [1, 0, 0, 0, 1, 4, 0, 0, 0, 4, 4, 0, 
                     0, 0, 4, 1, 3, 3, 3, 5, 0, 0, 0, 0, 4]        
        assert output_expected == featureExtraction.blocksIntensity(imageP), \
                                 featureExtraction.blocksIntensity(imageP)
        