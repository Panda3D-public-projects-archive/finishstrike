import unittest
import os
from PIL import Image as PilImage
import horus.core.computervision.featureExtraction as featureExtraction
import horus.core.computervision.image as image

class ImageTest(unittest.TestCase):    
    def setUp(self):
        # XXX: from os.path import abspath, join, dirname
        #      PREFIX = join(abspath(dirname(__file__)))
        # Use . is not correct, you should use the code above.
        abspath = os.path.abspath('.')
        self.imagePath = os.path.join(abspath,"testImages/imageTest.PNG")                
#        image1 = PilImage.open(self.edPath2)
#        image1 = image1.convert("L") 
#        image1.save(self.edPath2)
        self.test_image = image.Image(self.imagePath)
                
    def test_Image(self):
        imCroped = self.test_image.crop((0,0,3,3))
        im = image.Image(img_to_mix = imCroped)                  
        assert im != None
        assert list(im.getdata()) == list(imCroped.getdata()), \
                list(im.getdata())
        
    def test_getdata(self):
        expected_output = [255, 255, 255, 255,  0,\
                           255,  0,   0,   0,  255, \
                           255,  0,   0,   0,  255,\
                           255,  0,   0,   0,  255, \
                           255, 255, 255, 255, 255]
        assert list(self.test_image.getdata()) == expected_output, \
        list(self.test_image.getdata())
        
    def test_column_row(self):
        assert 0 == self.test_image.getpixel((4,0))
        assert 255 == self.test_image.getpixel((0,4))
        
    def test_get8Neiborhood(self):
        expected_output = [0, 0, 0, 0, 0, 0, 0, 0]        
        result_list = self.test_image.get8Neiborhood((2,2))
        assert result_list == expected_output, result_list 
        
    def test_topNeibor(self):
        assert 255 == self.test_image.topNeibor((0,1))
        assert 0 == self.test_image.topNeibor((2,2))
        assert 0 == self.test_image.topNeibor((4,1))
        
    def test_topRightNeibor(self):
        assert 255 == self.test_image.topRightNeibor((0,1))
        assert 0 == self.test_image.topRightNeibor((2,2))
        assert None == self.test_image.topRightNeibor((4,1))
        
    def test_rightNeibor(self):
        assert 0 == self.test_image.rightNeibor((0,1))
        assert 0 == self.test_image.rightNeibor((2,2))
        assert 255 == self.test_image.rightNeibor((3,2))
        
    def test_bottomRightNeibor(self):
        assert 0 == self.test_image.backRightNeibor((0,1))
        assert 0 == self.test_image.backRightNeibor((2,2))
        assert 255 == self.test_image.backRightNeibor((3,2))
        
    def test_bottomNeibor(self):
        assert 255 == self.test_image.backNeibor((0,1))
        assert 0 == self.test_image.backNeibor((2,2))
        assert 0 == self.test_image.backNeibor((3,2))
        
    def test_bottomLeftNeibor(self):
        assert None == self.test_image.backLeftNeibor((0,1))
        assert 0 == self.test_image.backLeftNeibor((2,2))
        assert 0 == self.test_image.backLeftNeibor((3,2))
        
    def test_leftNeibor(self):
        assert None == self.test_image.leftNeibor((0,1))
        assert 255 == self.test_image.leftNeibor((1,3))
        assert 0 == self.test_image.leftNeibor((3,2))
        
    def test_topLeftNeibor(self):
        assert None == self.test_image.topLeftNeibor((0,1))
        assert 255 == self.test_image.topLeftNeibor((1,3))
        assert 0 == self.test_image.topLeftNeibor((3,2))
    
    def test_getFourNeighborhood(self):
        
       expected_output = [[0, 0],\
                          [0, 0]]
       result_list = self.test_image.getFourNeighborhood((2,2))
       assert result_list == expected_output, result_list 
        
