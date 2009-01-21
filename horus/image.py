from PIL import ImageFilter
from PIL import Image as PilImage
class HORIZONTAL_EDGE_DETECTED(ImageFilter.BuiltinFilter):
    name = "HorizontalEdgeDetected"
    filterargs = (3, 3), 1, 0, (
       -1, -1, -1,
        0,  0,  0,
        1,  1,  1,
        )

class VERTICAL_EDGE_DETECTED(ImageFilter.BuiltinFilter):
    name = "VerticalEdgeDetected"
    filterargs = (3, 3), 1, 0, (
       -1,  0,  1,
       -1,  0,  1,
       -1,  0,  1,
        )
def getFourNeighborhood(index, image):
    return [[image.getpixel((index[0],index[1])), 
             image.getpixel((index[0]+1, index[1]))],
            [image.getpixel((index[0], index[1]+1)), 
             image.getpixel((index[0]+1, index[1]+1))]]
class Image(object):    
    """   
        This class implements all image's methods required in anpr modules
    """
    
    def __init__(self, image = None, path = None):
        """
            TODO
        """
        self.__matrix_image = None   
        
        if image:
            self.__image = image
        if path:
            self.__image = PilImage.open(path)
            
        
    @property
    def image(self):
        """
            TODO
        """
        return self.__image
        
    def applyFilter(self, type_filter):
        """
            TODO
        """
        return Image(image = self.__image.filter(type_filter))
        
    def convertRgbToGrayscale(self):
        """
            TODO
        """
        return Image(image = self.__image.convert("L"))

    @property    
    def size(self):        
        """
            TODO
        """        
        return self.__image.size     
        
    def crop(self, bbox):
        """
            TODO
        """
        return Image(image = self.__image.crop(bbox))

    def save(self, path):
        """
            TODO
        """
        self.__image.save(path)

    def getpixel(self,xy):
        """
            TODO
        """
        return self.__image.getpixel(xy)       
        
        
    @property
    def matrix_image(self):
        """
            This method returns a matrix with values of wich image's pixels.
        """
        #############################
        #### Alterar esse metodo ####
        #############################

        if not self.__matrix_image:
            self.__matrix_image = [[0 for i in range(self.__image.size[1])] \
                                    for j in range(self.__image.size[0]) ]
            
            for i in range(len(self.__matrix_image)):
                for j in range(len(self.__matrix_image[0])):
                    self.__matrix_image[i][j] = self.__image.getpixel((i,j))
        
        return self.__matrix_image
        
    def fullEdgeDetection(self):
        """
            TODO
        """
        ###################################################################
        #### Esse metodo deve alterar realmente o estado da imagem, ou ####
        #### seria melhor criar uma nova imagem e retornar essa outra  ####
        ###################################################################
        gray_image = self.convertRgbToGrayscale()
        image_vertical_filtered = gray_image.applyFilter(VERTICAL_EDGE_DETECTED)
        image_horizontal_filtered = gray_image.applyFilter(HORIZONTAL_EDGE_DETECTED)

        for i in range(self.__image.size[0]):
            for j in range(self.__image.size[1]):
                pixel_value = image_vertical_filtered.__image.getpixel((i,j))
                pixel_value += image_horizontal_filtered.__image.getpixel((i,j))
                self.__image.putpixel((i,j), pixel_value)    
        return self        
        