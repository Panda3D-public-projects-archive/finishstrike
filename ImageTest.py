import unittest
from Image import *
import os

class ImageTest(unittest.TestCase):

    def testInstanceImage(self):
        im = HImage()
        assert('openImage'in dir(im))

    def testOpenImageTest(self):
        """
        Open a image's source "angie.jpg", and verify the file name of the atribute image of im (instance of HImage)
        """
        im = HImage()
        im.openImage("angie.jpg")
        self.assertEquals('angie.jpg',im.image.filename)

    def testOpenImageWithWrongName(self):
        """
        TODO: the method openImage should handle error in the parameter 'name' (file missing; invalid type)
        """
        assert(1)

    def testNewImage(self):
        """ 
        Create a black image, which size is height = 128 and width = 128. 
        So, the histogram have 16384 points correspondent to black pixel.
        """
        im = HImage()
        size = 128, 128
        im.newImage("RGB",size, "Black")
        assert(16384 in im.image.histogram())

    def testNewWithWrongParameter(self):
        """
        TODO: the method newImage should handle error in the parameters 
        """
        assert(1)

    def testSaveImage(self):
        """
        Create a new black image and save it. So test if the file is on current directory
        """
        im = HImage()
        size = 128, 128
        im.newImage("RGB",size, "Black")
        im.saveImage("teste.jpg")
        assert("teste.jpg" in os.listdir('.'))
        os.remove("teste.jpg")
        



if __name__ == '__main__':
    unittest.main()
