import unittest
from PIL import Image as PilImage
import horus.core.computervision.featureExtraction as featureExtraction
import horus.core.computervision.image as image
from os.path import abspath, join, dirname

PREFIX = join(abspath(dirname(__file__)))

class FeatureExtractionTest(unittest.TestCase):

    def setUp(self):
        self.imagePath = join(PREFIX, "testImages/region_test_image.png")
        self.edPath = join(PREFIX,"testImages/edge_detection_test.png")
        self.edPath2 = join(PREFIX,"testImages/edge_detection_test2.png")
        self.edImage = image.Image(self.edPath)
        self.edImage2 = image.Image(self.edPath2)
        self.regionTestImage = image.Image(self.imagePath)
    
    #XXX: Where is the doc string?
    def test_01_getRegionList(self):     
        """

        """
        r0 = [[0, 0 ,0, 0], 
              [0, 0, 0, 0]]

        r3 = [[50, 50, 50, 50], 
              [50, 50, 50, 50]]

        r1 = [[100, 100, 100, 100],
               [100, 100, 100, 100]]

        r4 = [[150, 150, 150, 150],
              [150, 150, 150, 150]]

        r2 = [[200, 200, 200, 200],
              [200, 200, 200, 200]]

        r5 = [[250, 250, 250, 250],
              [250, 250, 250, 250]]
        self.assertEquals(self.regionTestImage.size, (8,6))

        image_list = self.regionTestImage.getRegionList(3, 2)
        self.assertEquals(len(image_list), 6)
        self.assertEquals(r0, image_list[0].pixel_matrix())
        self.assertEquals(r1, image_list[1].pixel_matrix())
        self.assertEquals(r2, image_list[2].pixel_matrix())
        self.assertEquals(r3, image_list[3].pixel_matrix())
        self.assertEquals(r4, image_list[4].pixel_matrix())
        self.assertEquals(r5, image_list[5].pixel_matrix())
        
#   def test_02_extractFeatureByEdgeDetection(self):
#       featureMatrix = featureExtraction.extractFeatureByEdgeDetection(self.edImage)
#       self.assertEquals(6, len(featureMatrix[0]))
#       self.assertEquals(10, len(featureMatrix))
#       self.assertEquals(1, featureMatrix[2][0], featureMatrix[0])
#       self.assertEquals(1, featureMatrix[3][0], featureMatrix[0])
#       self.assertEquals(1, featureMatrix[6][1], featureMatrix[6])
#       self.assertEquals(1, featureMatrix[7][2], featureMatrix[7])
#       self.assertEquals(1, featureMatrix[5][3], featureMatrix[5])
#       self.assertEquals(1, featureMatrix[0][4], featureMatrix[0])
#       self.assertEquals(1, featureMatrix[4][5], featureMatrix[4])

#     def test_03_extractFeatureByEdgeDetection2(self):
#         featureMatrix = featureExtraction.extractFeatureByEdgeDetection(self.edImage2)
#         assert 6 == len(featureMatrix[0])
#         assert 10 == len(featureMatrix)
#         
#         assert 1 == featureMatrix[2][0], featureMatrix[0]
#         assert 2 == featureMatrix[3][0], featureMatrix[0]
#         assert 1 == featureMatrix[6][1], featureMatrix[6]
#         assert 1 == featureMatrix[7][2], featureMatrix[7]
#         assert 1 == featureMatrix[6][2], featureMatrix[6]
#         assert 1 == featureMatrix[5][3], featureMatrix[5]
#         assert 1 == featureMatrix[0][4], featureMatrix[0]
#         assert 1 == featureMatrix[4][5], featureMatrix[4]

    def test_04_getTwoLoops(self):
        """

        """
        imagePath = join(PREFIX, 'testImages/two_squares.png')
        imageP = image.Image(image_path=imagePath)
        self.assertEquals(2, featureExtraction.getNumLoops(imageP))
         
    def test_05_getThreeLoops(self):
        """

        """
        imagePath = join(PREFIX, 'testImages/three_squares.png')
        imageP = image.Image(image_path= imagePath)
        self.assertEquals(3, featureExtraction.getNumLoops(imageP))
         
    def test_06_getTwoLoopsFromBCharacter(self):
        """

        """
        image_path = join(PREFIX, 'testImages/b_character_skeletonized.png')
        image_b_character = image.Image(image_path=image_path)
        self.assertEquals(2, featureExtraction.getNumLoops(image_b_character))

    def test_07_blackIntensityInFourRegions(self):
        image_path = join(PREFIX, 'testImages/black_intensity_test.png')
        image_path = image.Image(image_path)
        output_expected = [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0,
                           0, 0, 0, 2, 1, 0, 3, 1, 0, 0, 0, 0, 0]
        self.assertEquals(featureExtraction.blocksIntensity(image_path),
                                            output_expected)
        
    def testBlackIntensityFourNumber(self):
        abspath = os.path.abspath('.')
        imagePath = os.path.join(abspath,"testImages/black_intensity_test_number_four.png")
        imageP = image.Image(imagePath)
        output_expected = [1, 0, 0, 0, 1, 4, 0, 0, 0, 4, 4, 0,
                     0, 0, 4, 1, 3, 3, 3, 5, 0, 0, 0, 0, 4]
        self.assertEquals(featureExtraction.blocksIntensity(imageP), \
                                 output_expected)

if __name__=='__main__':
    unittest.main()

