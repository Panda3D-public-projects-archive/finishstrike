# XXX: Add Copyright

from horus.core.processingimage import imagefilter
from horus.core.processingimage import image as horusImage
from horus.vision import featureextraction
from horus.core.math import mathematic
import math

def fullEdgeDetection(image):
    """
        TODO
    """    
    new_image = image
    if(image.mode != "L"):
        new_image = image.convert("L")       
    vertical_edges = new_image.filter(imagefilter.VERTICAL_EDGE_DETECTED)
    horizontal_edges = new_image.filter(imagefilter.HORIZONTAL_EDGE_DETECTED)

    # fazer um breve comentario sobre esses fors
    for i in range( image.size[0] ):
        for j in range( image.size[1] ):
            pixel_value = vertical_edges.getpixel( (i,j) ) + \
                          horizontal_edges.getpixel( (i,j) )
            new_image.putpixel( (i,j), pixel_value )
    
    return horusImage.Image(img_to_mix = new_image)

# XXX: Why __ ??
def projection(matrix):
    """
        This method calculates the horizontal projection of image passed
        by parameter image. To calculate vertical projection just
        call this method passing pass as parameter image its transpose.
    """
    projection = mathematic.List([0 for i in range(len(matrix))])
    for i in range(len(matrix) ):
        projection[i] = mathematic.List(matrix[i]).sumValues()
    return projection

# Transformar esses dois proximos metodos em property e calcular a projecao  
# qdo necessario (caso ja tenha sido calculada sera um atributo) baseado no 
# getpixel (ao inves do matrix_content).
# Retirar o matrix_content de Image e o _projection de ProcessingImage
def verticalProjection(image):
    """
        TODO
    """
    matrix = mathematic.Math().calculateTranspose(image.pixel_matrix())
    return mathematic.List( [0,0] + projection(matrix)[2:][:-2] + [0,0] )
    
def horizontalProjection(image):
    """
        TODO
    """
    return mathematic.List(projection(image.pixel_matrix()))
    
# Qual nome eh melhor highlightLuminance ou enhancementLuminance ?
# Eh necessario verificar se esta funcionando e testar valores para U
# Faco isso no fds.
def highlightLuminance(image, u = 1):
    """The highlight luminance is doing by:
        I(x, y) = 100 + 20U log[Is (x, y) + 1] 
        where:
        Is is luminance of self.image
        I and the highlight of the luminance of the image
        U is a constant (NAO SEI QUAL POR ENQUANTO)
    """    
    enhanced_image = horusImage.new( mode = image.mode, 
                    size = image.size)
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            # Este math eh nativo do python. Incorporar a funcao log em horus.mathematic
            new_value = 100 + 20 * u * math.log(image.getpixel((i,j)) + 1)
            enhanced_image.putpixel((i,j), new_value)
    return enhanced_image

def hildtchSkeletonize(image):        
    while (True):
        letContinue = False
        boundaryPixelList = []
        pixelsToDelete = []
        for i in range( image.size[0] ):
            for j in range(image.size[1]):
                if(image.getpixel((i,j)) == 0):                    
                    n8 = image.getEightNeighbourhood((i,j))
                    if(n8.count(255) > 0):                        
                        boundaryPixelList.append((i,j))                        
        for pixel in boundaryPixelList:
            n8 = image.getEightNeighbourhood(pixel)
            if((image.topNeighbour(pixel) + image.rightNeighbour(pixel) + 
                image.leftNeighbour(pixel)) == 0):
                continue            
            if((image.topNeighbour(pixel) + image.rightNeighbour(pixel) + 
                image.bottomNeighbour(pixel)) == 0):
                continue                
            if not((n8.count(0) >= 2) & (n8.count(0) <= 6)):                
                continue
            numTransitions = featureextraction.countTransitions(image, pixel)
            if numTransitions <> 1:                
                continue                        
            pixelsToDelete.append(pixel)            
            letContinue = True
        for pixelToDelete in pixelsToDelete:                      
            image.putpixel(pixelToDelete, 255)
        print letContinue                        
        if(not letContinue):            
            break                                 
    return image

