import unittest
from Image import *
import os

class ImageTest(unittest.TestCase):

    def newBlackImage(self):
        im = HImage()
        size = 128, 128
        im.newImage("RGB",size, "Black")
        return im
    
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
        im = self.newBlackImage()
        assert(16384 in im.image.histogram())

    def testNewImageWithWrongParameter(self):
        """
        TODO: the method newImage should handle error in the parameters 
        """
        assert(1)

    def testSaveImage(self):
        """
        Create a new black image and save it. So test if the file is on current directory. Finally remove a file saved
        """
        im = self.newBlackImage()
        im.saveImage("teste.jpg")
        assert("teste.jpg" in os.listdir('.'))
        os.remove("teste.jpg")

    def testSaveImageWithWrongParameter(self):
        """
        TODO: the method saveImage should handle error in the parameters 
        """
        assert(1)
        
    def testCopyImage(self): 
        """
        Instace a HImage object im, with a new image. So copy to im2 
        """
        im = self.newBlackImage()
        im2 = im.copyObjectImage()
        self.assertEquals(im2.image.histogram(),im.image.histogram())
        
    def testCropImage(self):
       """
       Open a image file ("angie.jpg") and crop a peace into a box with topleft vertice 
       in a point (100, 100), and a bottom-right vertices in a point (150, 190).
       So shuld verifi if a size image is (50,90)
       """
       im = HImage()
       im.openImage("angie.jpg")
       box = (100, 100, 150, 190)
       im2 = im.cropImage(box)
       self.assertEquals((50,90),im2.size)

    def testCropImageWithInvalidRegion(self):
       """
       Try execute a method cropImage with invalid parameter. This can happen when the two first parameters do not 
       correspond to the topleft vertice and the last two parameters does not correspond to the bottom-right vertice.
       """
       #im = HImage()
       #im.openImage("angie.jpg")
       #box = (150, 190, 100, 100)
       #im2 = im.cropImage(box)
       #self.assertEquals("Invalid region to Crop",im2)
       assert(1)
       
if __name__ == '__main__':
    unittest.main()
