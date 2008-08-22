from PIL import Image

class HIImage:
   def openImage(self, name):
       """ Open an image source """

   def saveImage(self, name):
       """ Save an image source """

   def newImage(self, mode, size, color):
       """ Create a new image """

   def copyObjectImage(self):
       """ Copy an instance of HImage """

   def copyImage(self):
       """ Copy an image """

   def generateHistogram(self):
       """ genererate the histogram of image """

   def cropImage(self, box):
       """ Execute a crop on Image """


class HImage(HIImage):

    def openImage(self, name):
        self.image = Image.open(name)
        return self.image

    def saveImage(self, name):
        self.image.save(name)

    def newImage(self, mode, size, color):
        self.image = Image.new(mode, size, color)

    def copyObjectImage(self):
        """ TODO: modify to copy.copy """
        im = HImage()
        im.image = self.image.copy()
        return im

    def copyImage(self):
        return self.image.copy()

    def generateHistogram(self):
        return self.image.histogram()

    def cropImage(self, box):
        return self.image.crop(box)

   






