# -*- coding: utf-8 -*-

from PIL import ImageFilter
from PIL import Image as PilImage

import mathematic as Math
import math

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
    """
        TODO
    """
    return [[image.getpixel((index[0],index[1])), 
             image.getpixel((index[0]+1, index[1]))],
            [image.getpixel((index[0], index[1]+1)), 
             image.getpixel((index[0]+1, index[1]+1))]]
             
class Image(object):    
    """
        This class implements all content's methods required in anpr modules
    """
    
    def __init__(self, content = None, path = None, 
                 mode = None, size = None, color = None):
        """
            TODO
        """
        self.__matrix_content = None   
        self.path = path        
        # if the parameter is not None (ie content refers a PilImage object) 
        # then Image object refers this content
        if content:
            self.content = content
        # if content is None, but the parameter path refers a image file then 
        # open the image
        elif path:
            self.content = PilImage.open(path)
            
        # If there aren't content and path is necessary create a new Image
        # based on parameters mode size and color
        if not (content or path):
            self.content = self.new(mode, size, color)

        self.mysize = self.content.size
        self.mode = self.content.mode


    def new(self, mode = "L", size = (100.100), color = 0):
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
        return PilImage.new(mode, size, color)
            
       
    @property    
    def size(self):        
        """
            TODO
        """        
        return self.mysize     
    
    def load(self):
        self.content.load()
    def crop(self, bbox):
        """
            TODO
        """
        return Image( content = self.content.crop(bbox) )

    def save(self, path):
        """
            TODO
        """
        self.content.save(path)


    # Acho que os proximos metodos podem ser alocados em uma classe e 
    # relacionados com Image via composicao. A presenca deles esta
    # sobrecarregando essa classe
    def get8Neiborhood(self,xy):
        n8List = []        
        if(self.topNeibor(xy) != None):
            n8List.append(self.topNeibor(xy))                
        if(self.topRightNeibor(xy) != None):
            n8List.append(self.topRightNeibor(xy))        
        if(self.rightNeibor(xy) != None):
            n8List.append(self.rightNeibor(xy))
        if(self.backRightNeibor(xy) != None):
            n8List.append(self.backRightNeibor(xy))         
        if(self.backNeibor(xy) != None):
            n8List.append(self.backNeibor(xy))            
        if(self.backLeftNeibor(xy) != None):
            n8List.append(self.backLeftNeibor(xy))
        if(self.leftNeibor(xy) != None):
            n8List.append(self.leftNeibor(xy))
        if(self.topLeftNeibor(xy) != None):
            n8List.append(self.topLeftNeibor(xy))                
        return n8List   
         
    def topNeibor(self, xy):
        if(xy[1]-1 >= 0):
#            self.content.putpixel((xy[0],xy[1]-1),128)
            return self.content.getpixel((xy[0],xy[1]-1))
        else:
            return None
    
    def backNeibor(self, xy):
        if(xy[1]+1 < self.size[1]):
#            self.content.putpixel((xy[0],xy[1]+1),128)
            return self.content.getpixel((xy[0],xy[1]+1))            
    def topRightNeibor(self, xy):
        if(xy[0]+1 < self.size[0]) & (xy[1]-1 >= 0):
#            self.content.putpixel((xy[0]+1, xy[1]-1),128)                      
            return self.content.getpixel((xy[0]+1, xy[1]-1))        
    def rightNeibor(self, xy):
        if(xy[0]+ 1 < self.size[0]):
#            self.content.putpixel((xy[0]+1,xy[1]),128)
            return self.content.getpixel((xy[0]+1,xy[1]))        
    def backRightNeibor(self, xy):               
        if(xy[0]+1 < self.size[0]) & (xy[1]+1 < self.size[1]):
#            self.content.putpixel((xy[0]+1, xy[1]+1),128)            
            return self.content.getpixel((xy[0]+1, xy[1]+1))
    def leftNeibor(self, xy):
        if(xy[0]-1 >= 0): 
#            self.content.putpixel((xy[0]-1, xy[1]),128)
            return self.content.getpixel((xy[0]-1, xy[1]))
    def backLeftNeibor(self, xy):
        if(xy[0]-1 >= 0 ) & ( xy[1]+1 < self.size[1]):
#            self.content.putpixel((xy[0]-1, xy[1]+1),128) 
            return self.content.getpixel((xy[0]-1, xy[1]+1))
    def topLeftNeibor(self, xy):
        if(xy[0]-1 >= 0 ) & ( xy[1]-1 >= 0 ):
#            self.content.putpixel((xy[0]-1, xy[1]-1),128)
            return self.content.getpixel((xy[0]-1, xy[1]-1))        
        
    def getpixel(self,xy):
        """
            TODO
        """
        return self.content.getpixel(xy)       
    
    def putpixel(self, xy, value):
        self.content.putpixel(xy, value)   
        
    @property
    def matrix_content(self):
        """
            This method returns a matrix with values of wich content's pixels.
        """
        #############################
        #### Alterar esse metodo ####
        #############################

        if not self.__matrix_content:
            self.__matrix_content = [[0 for i in range(self.content.size[1])] \
                                    for j in range(self.content.size[0]) ]
            
            for i in range(len(self.__matrix_content)):
                for j in range(len(self.__matrix_content[0])):
                    self.__matrix_content[i][j] = self.content.getpixel((i,j))
        
        return self.__matrix_content
        

class ProcessingImage(object):
    """
        This class contains the methods for processings of image.
    """
    
    def __init__(self, image):
        self.image = image
        
    def applyFilter(self, type_filter):
        """
            TODO
        """
        return Image( content = self.image.content.filter(type_filter) )
        
    def convertRgbToGrayscale(self):
        """
            Esse metodo pode ser retirado e substituido pelo metodo abaixo
        """
        return Image( content = self.image.content.convert("L") )

    def convertMode(self, new_mode):
        """
            This method convert the mode of the image refers by self.image. If a
            self.image.mode is equlas a new_mode this method keeps the mode
            
            Possible modes:
            'L': grayscale; 
            'RGB': color image, based on Red, green and blue colors; 
            'CMYK': color image based on cyan, magenta, yellow and black colors.
        """
        return Image( content = self.image.content.convert(new_object) )
            
    
    
    def fullEdgeDetection(self):
        """
            TODO
        """
        new_image = self.convertRgbToGrayscale()
        processing = ProcessingImage(new_image)
        
        vertical_edges = processing.applyFilter(VERTICAL_EDGE_DETECTED)
        horizontal_edges = processing.applyFilter(HORIZONTAL_EDGE_DETECTED)

        # fazer um breve comentario sobre esses fors
        for i in range( self.image.content.size[0] ):
            for j in range( self.image.content.size[1] ):
                pixel_value = vertical_edges.content.getpixel( (i,j) ) + \
                              horizontal_edges.content.getpixel( (i,j) )
                new_image.content.putpixel( (i,j), pixel_value )    
        
        return new_image        

    def __projection(self, matrix):
        """
            This method calculates the horizontal projection of image passed
            by parameter image. To calculate vertical projection just
            call this method passing pass as parameter image its transpose.
        """
        projection = Math.List([0 for i in range( len(matrix) ) ])
        for i in range( len(matrix) ):
            projection[i] = Math.List( matrix[i] ).sumValues()
        return projection

    # Transformar esses dois proximos metodos em property e calcular a projecao  
    # qdo necessario (caso ja tenha sido calculada sera um atributo) baseado no 
    # getpixel (ao inves do matrix_content).
    # Retirar o matrix_content de Image e o _projection de ProcessingImage
    def verticalProjection(self):
        """
            TODO
        """
        matrix = Math.Math().calculateTranspose( self.image.matrix_content )
        return Math.List( [0,0] + self.__projection( matrix )[2:][:-2] + [0,0] )
        
    def horizontalProjection(self):
        """
            TODO
        """
        return Math.List( self.__projection( self.image.matrix_content ) )
        
    # Qual nome eh melhor highlightLuminance ou enhancementLuminance ?
    # Eh necessario verificar se esta funcionando e testar valores para U
    # Faco isso no fds.
    def highlightLuminance(self, u = 1):
        """            The highlight luminance is doing by:
            I(x, y) = 100 + 20U log[Is (x, y) + 1] 
            where:
            Is is luminance of self.image
            I and the highlight of the luminance of the image
            U is a constant (NAO SEI QUAL POR ENQUANTO)
        """    
        image = Image( mode = self.image.mode, 
                        size = self.image.size, color = self.image.color )
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                # Este math eh nativo do python. Incorporar a funcao log em horus.mathematic
                new_value = 100 + 20 * u * math.log(self.image.getpixel((i,j)) + 1)
                image.putpixel((i,j), new_value)
        return image
        
     
