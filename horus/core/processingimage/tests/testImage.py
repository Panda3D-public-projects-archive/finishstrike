import unittest
from PIL import Image as PILImage
from horus.core.processingimage.image import Image
from os.path import join, abspath, dirname

PREFIX = join(abspath(dirname(__file__)))

class ImageTest(unittest.TestCase):
    def setUp(self):
        self.image_path = join(PREFIX,"data/image.png")
        self.test_image = Image(path = self.image_path)
 

    def test_01_image(self):
        img_cropped = self.test_image.crop((0,0,3,3))
        img = Image(content=img_cropped)
        self.assertTrue(img)
        self.assertEqual(img.size, img_cropped.size)
        
    def test_02_getData(self):
        expected_output = [255, 255, 255, 255, 0,
                           255, 0, 0, 0, 255,
                           255, 0, 0, 0, 255,
                           255, 0, 0, 0, 255,
                           255, 255, 255, 255, 255]
        self.assertEqual(list(self.test_image.getData()), expected_output)

    def test_03_column_row(self):
        self.assertEqual(self.test_image.getPixel((4,0)), 0)
        self.assertEqual(self.test_image.getPixel((0,4)), 255)

    def test_04_getEightNeiborhood(self):
        expected_output = [0, 0, 0, 0, 0, 0, 0, 0]
        result_list = self.test_image.getEightNeighbourhood((2,2))
        self.assertEqual(expected_output, result_list)

    def test_05_topNeibor(self):
        self.assertEqual(self.test_image.topNeighbour((0,1)), 255)
        self.assertEqual(self.test_image.topNeighbour((2,2)), 0)
        self.assertEqual(self.test_image.topNeighbour((4,1)), 0)
        
    def test_06_topRightNeibor(self):
        self.assertEqual(self.test_image.topRightNeighbour((0,1)), 255)
        self.assertEqual(self.test_image.topRightNeighbour((2,2)), 0)
        self.assertEqual(self.test_image.topRightNeighbour((4,1)), None)
        
    def test_07_rightNeibor(self):
        self.assertEqual(self.test_image.rightNeighbour((0,1)), 0)
        self.assertEqual(self.test_image.rightNeighbour((2,2)), 0)
        self.assertEqual(self.test_image.rightNeighbour((3,2)), 255)
        
    def test_08_bottomRightNeibor(self):
        self.assertEqual(self.test_image.bottomRightNeighbour((0,1)), 0)
        self.assertEqual(self.test_image.bottomRightNeighbour((2,2)), 0)
        self.assertEqual(self.test_image.bottomRightNeighbour((3,2)), 255)
        
    def test_09_bottomNeibor(self):
        self.assertEqual(self.test_image.bottomNeighbour((0,1)), 255)
        self.assertEqual(self.test_image.bottomNeighbour((2,2)), 0)
        self.assertEqual(self.test_image.bottomNeighbour((3,2)), 0)
        
    def test_10_bottomLeftNeibor(self):
        self.assertEqual(self.test_image.bottomLeftNeighbour((0,1)), None)
        self.assertEqual(self.test_image.bottomLeftNeighbour((2,2)), 0)
        self.assertEqual(self.test_image.bottomLeftNeighbour((3,2)), 0)
        
    def test_11_leftNeibor(self):
        self.assertEqual(self.test_image.leftNeighbour((0,1)), None)
        self.assertEqual(self.test_image.leftNeighbour((1,3)), 255)
        self.assertEqual(self.test_image.leftNeighbour((3,2)), 0)
        
    def test_12_topLeftNeibor(self):
        self.assertEqual(self.test_image.topLeftNeighbour((0,1)), None)
        self.assertEqual(self.test_image.topLeftNeighbour((1,3)), 255)
        self.assertEqual(self.test_image.topLeftNeighbour((3,2)), 0)
    
    def test_13_getFourNeighborhood(self):
       expected_output = [[0, 0],
                          [0, 0]]
       result_list = self.test_image.getFourNeighbourhood((2,2))
       self.assertEqual(expected_output, result_list)


if __name__ == '__main__':
    unittest.main()

