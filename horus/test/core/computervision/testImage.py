import unittest
from PIL import Image as PilImage
import horus.core.computervision.image as image
from os.path import join, abspath, dirname

PREFIX = join(abspath(dirname(__file__)))

class ImageTest(unittest.TestCase):
    def setUp(self):
        self.imagePath = join(PREFIX,"testImages/image_test.png")
        self.test_image = image.Image(self.imagePath)

    def test_01_image(self):
        imCroped = self.test_image.crop((0,0,3,3))
        im = image.Image(img_to_mix = imCroped)
        self.assertTrue(im)
        self.assertEqual(list(im.getdata()), list(imCroped.getdata()))
        
    def test_02_getdata(self):
        expected_output = [255, 255, 255, 255,  0,
                           255,  0,   0,   0,  255,
                           255,  0,   0,   0,  255,
                           255,  0,   0,   0,  255,
                           255, 255, 255, 255, 255]
        self.assertEqual(list(self.test_image.getdata()), expected_output)

    def test_column_row(self):
        self.assertEqual(self.test_image.getpixel((4,0)), 0)
        self.assertEqual(self.test_image.getpixel((0,4)), 255)

    def test_get8Neiborhood(self):
        expected_output = [0, 0, 0, 0, 0, 0, 0, 0]
        result_list = self.test_image.getEightNeighbourhood((2,2))
        self.assertEqual(expected_output, result_list)

    def test_topNeibor(self):
        self.assertEqual(self.test_image.topNeighbour((0,1)), 255)
        self.assertEqual(self.test_image.topNeighbour((2,2)), 0)
        self.assertEqual(self.test_image.topNeighbour((4,1)), 0)
        
    def test_topRightNeibor(self):
        self.assertEqual(self.test_image.topRightNeighbour((0,1)), 255)
        self.assertEqual(self.test_image.topRightNeighbour((2,2)), 0)
        self.assertEqual(self.test_image.topRightNeighbour((4,1)), None)
        
    def test_rightNeibor(self):
        self.assertEqual(self.test_image.rightNeighbour((0,1)), 0)
        self.assertEqual(self.test_image.rightNeighbour((2,2)), 0)
        self.assertEqual(self.test_image.rightNeighbour((3,2)), 255)
        
    def test_bottomRightNeibor(self):
        self.assertEqual(self.test_image.bottomRightNeighbour((0,1)), 0)
        self.assertEqual(self.test_image.bottomRightNeighbour((2,2)), 0)
        self.assertEqual(self.test_image.bottomRightNeighbour((3,2)), 255)
        
    def test_bottomNeibor(self):
        self.assertEqual(self.test_image.bottomNeighbour((0,1)), 255)
        self.assertEqual(self.test_image.bottomNeighbour((2,2)), 0)
        self.assertEqual(self.test_image.bottomNeighbour((3,2)), 0)
        
    def test_bottomLeftNeibor(self):
        self.assertEqual(self.test_image.bottomLeftNeighbour((0,1)), None)
        self.assertEqual(self.test_image.bottomLeftNeighbour((2,2)), 0)
        self.assertEqual(self.test_image.bottomLeftNeighbour((3,2)), 0)
        
    def test_leftNeibor(self):
        self.assertEqual(self.test_image.leftNeighbour((0,1)), None)
        self.assertEqual(self.test_image.leftNeighbour((1,3)), 255)
        self.assertEqual(self.test_image.leftNeighbour((3,2)), 0)
        
    def test_topLeftNeibor(self):
        self.assertEqual(self.test_image.topLeftNeighbour((0,1)), None)
        self.assertEqual(self.test_image.topLeftNeighbour((1,3)), 255)
        self.assertEqual(self.test_image.topLeftNeighbour((3,2)), 0)
    
    def test_getFourNeighborhood(self):
       expected_output = [[0, 0],
                          [0, 0]]
       result_list = self.test_image.getFourNeighbourhood((2,2))
       self.assertEqual(expected_output, result_list)

    def test_mixinFromPath(self):
        img = image.Image(image_path=self.imagePath)
        self.assertTrue(str(type(img)).endswith("ImagePilMixedIn'>"))

    def test_mixin_from_path(self):
        img = PilImage.open(self.imagePath)
        imagemixed = image.Image(img_to_mix=img)
        self.assertTrue(str(type(imagemixed)).endswith("ImagePilMixedIn'>"))
        self.assertEqual(imagemixed.size, img.size)
        self.assertEqual(imagemixed.mode, img.mode)
        self.assertTrue(imagemixed.pixel_matrix)

if __name__ == '__main__':
    unittest.main()

