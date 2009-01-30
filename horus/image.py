# -*- coding: utf-8 -*-

from PIL import ImageFilter
from PIL import Image as PilImage

import mathematic as Math

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
    
    def __init__(self, content = None, path = None):
        """
            TODO
        """
        self.__matrix_content = None   
        
        if content:
            self.content = content
        if path:
            self.content = PilImage.open(path)
            
       
    @property    
    def size(self):        
        """
            TODO
        """        
        return self.content.size     
        
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
    def get8Neiborhood(self,xy):
        n8List = []        
        if(xy[0]-1 >= 0)&(xy[1]-1 >= 0):
            n8List.append(self.matrix_content[xy[0]-1][xy[1]-1])
        else:
            print "fdp"        
        if(xy[0]-1 >= 0):
            n8List.append(self.matrix_content[xy[0]-1][xy[1]])
            if(xy[1]+1 < self.size[1]):
                n8List.append(self.matrix_content[xy[0]-1][xy[1]+1])        
        if(xy[1]-1 >= 0):        
            n8List.append(self.matrix_content[xy[0]][xy[1]-1])
            if(xy[0]+1 < self.size[0]):        
                n8List.append(self.matrix_content[xy[0]+1][xy[1]-1])
        if(xy[0]+1 < self.size[0]):
            n8List.append(self.matrix_content[xy[0]+1][xy[1]])         
        if(xy[0]+1 < self.size[0])&(xy[1]+1 < self.size[1]):
            n8List.append(self.matrix_content[xy[0]+1][xy[1]+1])            
        if(xy[1]+1 < self.size[1]):
            n8List.append(self.matrix_content[xy[0]][xy[1]+1])        
        return n8List   
         
    def topNeibor(self, xy):
        if(xy[0]-1 >= 0):
            return self.matrix_content[xy[0]-1][xy[1]]
        else:
            return None
    
    def backNeibor(self, xy):
        if(xy[0]+1 < self.size[0]):
            return self.matrix_content[xy[0]+1][xy[1]]            
    def topRightNeibor(self, xy):
        if(xy[1]+1 < self.size[1]) & (xy[0]-1 >= 0):
            return self.matrix_content[xy[0]-1][xy[1]+1]        
    def rightNeibor(self, xy):
        if(xy[1]+ 1 < self.size[1]):        
            return self.matrix_content[xy[0]][xy[1]+1]        
    def backRightNeibor(self, xy):               
        if(xy[1]+1 < self.size[1]) & (xy[0]+1 < self.size[0]):            
            return self.matrix_content[xy[0]+1][xy[1]+1]
    def leftNeibor(self, xy):
        if(xy[1]-1 >= 0): 
            return self.matrix_content[xy[0]][xy[1]-1]
    def backLeftNeibor(self, xy):
        if(xy[1]-1 >= 0 ) & ( xy[0]+1 < self.size[0]): 
            return self.matrix_content[xy[0]+1][xy[1]-1]
    def topLeftNeibor(self, xy):
        if(xy[1]+1 < self.size[0] ) & ( xy[0]-1 >= 0 ):  
            return self.matrix_content[xy[0]-1][xy[1]+1]
        
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
            TODO
        """
        return Image( content = self.image.content.convert("L") )

    def fullEdgeDetection(self):
        """
            TODO
        """
        new_image = self.convertRgbToGrayscale()
        processing = ProcessingImage(new_image)
        
        vertical_edges = processing.applyFilter(VERTICAL_EDGE_DETECTED)
        horizontal_edges = processing.applyFilter(HORIZONTAL_EDGE_DETECTED)

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
