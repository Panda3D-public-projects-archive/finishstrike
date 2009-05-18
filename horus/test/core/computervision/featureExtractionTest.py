import unittest
import os
from PIL import Image as PilImage
import horus.core.computervision.featureExtraction as featureExtraction
import horus.core.computervision.image as image

class FeatureExtractionTest(unittest.TestCase):
    def setUp(self):
        abspath = os.path.abspath('.')
        self.imagePath = os.path.join(abspath,"testImages/region_test_image.png")
        self.edPath = os.path.join(abspath,"testImages/edge_detection_test.png")
        self.edPath2 = os.path.join(abspath,"testImages/edge_detection_test2.png")
        self.edImage = image.Image(self.edPath)
        self.edImage2 = image.Image(self.edPath2)
        self.regionTestImage = image.Image(self.imagePath)
    
    def testGetRegionList(self):     
        import pdb;pdb.set_trace()
        r0 = [0,0,0,0,0,0,0,0]
        r1 = [50,50,50,50,50,50,50,50]
        r2 = [100,100,100,100,100,100,100,100]
        r3 = [150,150,150,150,150,150,150,150]
        r4 = [200,200,200,200,200,200,200,200]
        r5 = [250,250,250,250,250,250,250,250]
        self.assertEquals(self.regionTestImage.size, (8,6))
        sixRegionList = self.regionTestImage.getRegionList(3, 2)
        self.assertEquals(len(sixRegionList), 6)
        assert r0 == list(sixRegionList[0].pixel_matrix())
        assert r1 == list(sixRegionList[1].pixel_matrix())
        assert r2 == list(sixRegionList[2].pixel_matrix())
        assert r3 == list(sixRegionList[3].pixel_matrix())
        assert r4 == list(sixRegionList[4].pixel_matrix())
        assert r5 == list(sixRegionList[5].pixel_matrix())
        
##    def testExtractFeatureByEdgeDetection(self):
##        featureMatrix = featureExtraction.extractFeatureByEdgeDetection(self.edImage)
##        assert 6 == len(featureMatrix[0])
##        assert 10 == len(featureMatrix)
##        
##        assert 1 == featureMatrix[2][0], featureMatrix[0]
##        assert 1 == featureMatrix[3][0], featureMatrix[0]
##        assert 1 == featureMatrix[6][1], featureMatrix[6]
##        assert 1 == featureMatrix[7][2], featureMatrix[7]
##        assert 1 == featureMatrix[5][3], featureMatrix[5]
##        assert 1 == featureMatrix[0][4], featureMatrix[0]
##        assert 1 == featureMatrix[4][5], featureMatrix[4]
##        
##    def testExtractFeatureByEdgeDetection2(self):
##        featureMatrix = featureExtraction.extractFeatureByEdgeDetection(self.edImage2)
##        assert 6 == len(featureMatrix[0])
##        assert 10 == len(featureMatrix)
##        
##        assert 1 == featureMatrix[2][0], featureMatrix[0]
##        assert 2 == featureMatrix[3][0], featureMatrix[0]
##        assert 1 == featureMatrix[6][1], featureMatrix[6]
##        assert 1 == featureMatrix[7][2], featureMatrix[7]
##        assert 1 == featureMatrix[6][2], featureMatrix[6]
##        assert 1 == featureMatrix[5][3], featureMatrix[5]
##        assert 1 == featureMatrix[0][4], featureMatrix[0]
##        assert 1 == featureMatrix[4][5], featureMatrix[4]
##        
##    def testGet2Loops(self):
##        abspath = os.path.abspath('.')
##        imagePath = os.path.join(abspath,"testImages/two_squares.png")
##        imageP = image.Image(image_path= imagePath)
##        assert 2 == featureExtraction.getNumLoops(imageP), featureExtraction.getNumLoops(imageP)
##        
##    def testGet3Loops(self):
##        abspath = os.path.abspath('.')
##        imagePath = os.path.join(abspath,"testImages/three_squares.png")
##        imageP = image.Image(image_path= imagePath)
##        assert 3 == featureExtraction.getNumLoops(imageP), featureExtraction.getNumLoops(imageP)
##        
##    def testGet2LoopsFromBChar(self):
##        abspath = os.path.abspath('.')
##        imagePath = os.path.join(abspath,"testImages/b_character_skeletonized.png")
##        imageP = image.Image(image_path= imagePath)
##        assert 2 == featureExtraction.getNumLoops(imageP), \
##                                    featureExtraction.getNumLoops(imageP)
##        
##    def testBlackIntensityFourRegions(self):
##        abspath = os.path.abspath('.')
##        imagePath = os.path.join(abspath,"testImages/black_intensity_test.png")
##        imageP = image.Image(imagePath)        
##        
##        output_expected = [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0,
##                        0, 0, 0, 2, 1, 0, 3, 1, 0, 0, 0, 0, 0]
##        self.assertEquals(featureExtraction.blocksIntensity(imageP),\
##                                            output_expected)
##        
##    def testBlackIntensityFourNumber(self):
##        abspath = os.path.abspath('.')
##        imagePath = os.path.join(abspath,"testImages/black_intensity_test_number_four.png")
##        imageP = image.Image(imagePath)
##        output_expected = [1, 0, 0, 0, 1, 4, 0, 0, 0, 4, 4, 0,
##                     0, 0, 4, 1, 3, 3, 3, 5, 0, 0, 0, 0, 4]
##        self.assertEquals(featureExtraction.blocksIntensity(imageP), \
##                                 output_expected)
def suite():
    suite = unittest.makeSuite(FeatureExtractionTest,'test')     
    return suite
if __name__ == '__main__':    
    ##suite.addTest(doctest.DocTestSuite())
    ##suite.debug()
    unittest.TextTestRunner(verbosity=2).run(suite())

    
        
