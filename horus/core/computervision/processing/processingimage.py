# XXX: Add Copyright

from core.computervision.image import Image
import mathematic as Math
import math

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

    # XXX: Why __ ??
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
        """The highlight luminance is doing by:
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

