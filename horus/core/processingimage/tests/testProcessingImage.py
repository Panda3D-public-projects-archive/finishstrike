from horus.core.processingimage import processingimage, image  
import unittest
from os.path import join, abspath, dirname

PREFIX = join(abspath(dirname(__file__)))

class ProcessingImageTest(unittest.TestCase):
    def setUp(self):
        self.image_path = join(PREFIX,'data/image.png')
        self.test_image = image.Image(path=self.image_path)

    def test_01_fullEdgeDetection(self):
        filtered_img = processingimage.fullEdgeDetection(self.test_image)
        self.assertTrue(filtered_img)

    def test_02_projection(self):
        input_matrix = [[0, 1, 1, 0],
                        [2, 3, 4, 0],
                        [0, 0, 0, 1]]
        
        expected_output = [2, 9, 1]

        result_list = processingimage.projection(input_matrix)
        self.assertEqual(result_list, expected_output)
    
    def test_03_verticalProjection(self):
        result_list = processingimage.verticalProjection(self.test_image)
        self.assertTrue(result_list)
    
    def test_04_horizontalProjection(self):
        result_list = processingimage.horizontalProjection(self.test_image)
        self.assertTrue(result_list)
    
    def test_05_highlightLuminance(self):
        image = processingimage.highlightLuminance(self.test_image)
        self.assertTrue(image)
    
    def test_06_hildtchSkeletonize(self):
        image_path = join(PREFIX,"data/skeletonization_image.png")
        sktestimage = image.Image(path=image_path)
        
        expected_output = [255, 255, 255, 255, 255, 255,
                           255, 255, 255, 255, 255, 255, 
                           255, 255, 255, 255, 255, 0, 
                           255, 255, 255, 255, 255, 255, 
                           255, 255, 255, 255, 255, 255]
        result_img = processingimage.hildtchSkeletonize(sktestimage)
        self.assertEqual(result_img.getData(), expected_output)

if __name__ == '__main__':
    unittest.main()
