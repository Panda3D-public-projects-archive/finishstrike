#-*- coding: utf-8 -*-
# XXX: Add Copyright
from PIL import Image as PILImage
       
class Image(object):    
    """
        This class implements all content's methods required in anpr modules
    """
    
    def __init__(self, content = None, path = None, 
                 mode = None, size = None, color = None):
        """
            TODO
        """
        self.matrix = None   
        self.path = path        
        
        # if the parameter is not None (ie content refers a PilImage object) 
        # then Image object refers this content
        if content:
            if isinstance(content, Image):
                self.content = content.content
            else:
                self.content = content
        # if content is None, but the parameter path refers a image file then 
        # open the image
        elif path:
            self.content = PILImage.open(path)
            
        # If there aren't content and path is necessary create a new Image
        # based on parameters mode size and color, or case this parameter was
        # none this is seted with default values
        else:
            if not color:
                if not mode:
                    mode = "L" 
                    color = 0
                else:
                    if mode == "L":
                        color = 0
                    elif mode == "RGB":
                        color = (0, 0, 0)
                    elif mode == "CMYK":
                        color = (0, 0, 0, 0)
            else:
                if not mode:
                    if isinstance(color, int):
                        mode = "L"
                    elif len(color) == 3:
                        mode == "RGB"
                    elif len(color) == 4:
                        mode == "CMYK"
            if not size:
                size = (255, 255)

            self.content = self.new(mode, size, color).content

        


    def new(self, mode = "L", size = (100,100), color = 0):
        """
            Create a new Image as follow:
            
            mode: 
            'L': grayscale; 
            'RGB': color image, based on Red, green and blue colors; 
            'CMYK': color image based on cyan, magenta, yellow and black colors.
            
            size: tuple with width and height image
            
            color: the color of image. The image created is homogeneous 
            (the image has a unique color). This parameter can be a integer 
            (for greyscale image), a tuple is three (for RGB images) or four 
            (for CMYK images) values between 0 and 255.
        """
        return Image(content=PILImage.new(mode, size, color))
            
       
    @property    
    def size(self):        
        """
            This method return a tuple with the size of image: (width, height) 
        """        
        return self.content.size    
        
    @property    
    def mode(self):        
        """
            Possible modes: 
            'L': grayscale; 
            'RGB': color image, based on Red, green and blue colors; 
            'CMYK': color image based on cyan, magenta, yellow and black colors.
        """        
        return self.content.mode    
     
    
    def convert(self, mode):
        """
            This method convert the mode of the image
        """
        return Image(content=self.content.convert(mode))
    
    def resize(self, size):
        """
            This method resizes an image.
        """ 
        return Image(content=self.content.resize(size))
    
    def load(self):
        """
            Load the image
        """
        self.content.load()
        
    def crop(self, region):
        """
            Crop the image based on rectangle passed on parameter region
        """
        return Image( content = self.content.crop(region) )

    def save(self, path):
        """
            Save the image
        """
        self.content.save(path)

    def getPixel(self,xy):
        """
            Return the color of pixel (x, y)
            
            ps: the parameter xy should be a tuple
        """
        return self.content.getpixel(xy)       
    
    #TODO: Write test
    def putPixel(self, xy, value):
        """
            Define the color of pixel xy (tuple with value of row and collumn 
            of pixel map) with value.
            
            ps: value must have the specifc structure of the mode of image
        """
        self.content.putpixel(xy, value)   
    
    # the Pil pattern is getdata, but dehorus pattern is getData.    
    def getData(self):
        """
            This method return a list of values of color of image. This list 
            is orderly placing column after column.
        """
        return list(self.content.getdata())
        

    # modify the name of this method to getmatrixdata or getmatrix.
    # Is not @property better? If yes, pixel_matrix is OK.
    def pixel_matrix(self):
        """
            This method returns a matrix with values of wich content's pixels.
        """
        data = self.getData()
        self.matrix = [[data[(self.size[0]*j)+i] for i in range(self.size[0])]
                                                 for j in range(self.size[1]) ]

        return self.matrix

        

    def getEightNeighbourhood(self, xy):
        # XXX: This variable name is not so good
        # XXX: neighbourhood_list
        n8List = []        
        if self.topNeighbour(xy) is not None:
            n8List.append(self.topNeighbour(xy))

        if self.topRightNeighbour(xy) is not None:
            n8List.append(self.topRightNeighbour(xy))        

        if self.rightNeighbour(xy) is not None:
            n8List.append(self.rightNeighbour(xy))

        if self.bottomRightNeighbour(xy) is not None:
            n8List.append(self.bottomRightNeighbour(xy))         

        if self.bottomNeighbour(xy) is not None:
            n8List.append(self.bottomNeighbour(xy))            

        if self.bottomLeftNeighbour(xy) is not None:
            n8List.append(self.bottomLeftNeighbour(xy))

        if self.leftNeighbour(xy) is not None:
            n8List.append(self.leftNeighbour(xy))

        if self.topLeftNeighbour(xy) is not None:
            n8List.append(self.topLeftNeighbour(xy))                
        return n8List   
         
    def topNeighbour(self, xy):
        if(xy[1]-1 >= 0):
            return self.getPixel((xy[0],xy[1]-1))
        else:
            return None
    
    def bottomNeighbour(self, xy):
        if(xy[1]+1 < self.size[1]):
            return self.getPixel((xy[0],xy[1]+1))            

    def topRightNeighbour(self, xy):
        if(xy[0]+1 < self.size[0]) & (xy[1]-1 >= 0):
            return self.getPixel((xy[0]+1, xy[1]-1))        

    def rightNeighbour(self, xy):
        if(xy[0]+ 1 < self.size[0]):
            return self.getPixel((xy[0]+1,xy[1]))        

    def bottomRightNeighbour(self, xy):               
        if(xy[0]+1 < self.size[0]) & (xy[1]+1 < self.size[1]):
            return self.getPixel((xy[0]+1, xy[1]+1))

    def leftNeighbour(self, xy):
        if(xy[0]-1 >= 0): 
            return self.getPixel((xy[0]-1, xy[1]))

    def bottomLeftNeighbour(self, xy):
        if(xy[0]-1 >= 0 ) & ( xy[1]+1 < self.size[1]):
            return self.getPixel((xy[0]-1, xy[1]+1))

    def topLeftNeighbour(self, xy):
        if(xy[0]-1 >= 0 ) & ( xy[1]-1 >= 0 ):
            return self.getPixel((xy[0]-1, xy[1]-1))         


    # XXX: The doc string should be added.
    def getFourNeighbourhood(self, index):
      """
         TODO
      """
      return [[self.getPixel((index[0],index[1])),
               self.getPixel((index[0]+1, index[1]))],
              [self.getPixel((index[0], index[1]+1)),
               self.getPixel((index[0]+1, index[1]+1))]]
               
               
    def getRegionList(self, row, col, over_group=None):
        """
            This method split a given image in NxM regions.
            In other words,
             - if we have an image with 30x30 pixels it should return a list
            containing 25 sub-images.

            image: the original image to be divided in six regions.
             
            return: a list of six images, each one represents a part of the original
            image.
        """        
        width, height = self.size
        height_block_size = height/row
        width_block_size = width/col
        x = [(y,x) for x in range(0, height+1) for y in range(0, width+1)]
        x = [i for i in x if i[0] % width_block_size == 0 and i[1] % height_block_size == 0]
        subimage_list = []
        for i in x:           
            # Getting indexes
            x0, y0 = i
            x1 = i[0]+width_block_size
            y1 = i[1]+height_block_size
             
            if x1 > width:
              if over_group is None:
                  continue
              x1 = width

            if y1 > height:
                if over_group is None:
                    continue
                y1 = height
            subimage_list.append(Image(content=self.crop((x0, y0, x1, y1))))
        return subimage_list               

    def negative(self):
        """
            This method calculate the negative image. The source image must be Grayscale.
            XXX: TODO: To make this method accept as many modes as possible.
        """
        new_img = Image(mode=self.mode, size=self.content.size)
        for col in range(new_img.size[0]):
            for line in range(new_img.size[1]):
               
                new_img.putPixel((col,line), (255 - self.getPixel((col, line))))
        return new_img

if __name__ == '__main__':
    from horus.core.processingimage import image, processingimage
    ni = image.Image(path='/home/ucam/dev/projetofinal/sk/direita5.png')
    ni = ni.negative()
    ni.content.show()
    print processingimage.verticalProjection(ni)
