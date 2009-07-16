# XXX: Add Copyright

from horus.core.processingimage import imagefilter
from PIL import Image as PilImage 
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
    vertical_edges = applyFilter(new_image, imagefilter.VERTICAL_EDGE_DETECTED)
    horizontal_edges = applyFilter(new_image, 
                                          imagefilter.HORIZONTAL_EDGE_DETECTED)

    # fazer um breve comentario sobre esses fors
    for i in range( image.size[0] ):
        for j in range( image.size[1] ):
            pixel_value = vertical_edges.getPixel( (i,j) ) +                \
                          horizontal_edges.getPixel( (i,j) )
            new_image.putPixel( (i,j), pixel_value )
    
    return horusImage.Image(content=new_image)

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
# getPixel (ao inves do matrix_content).
# Retirar o matrix_content de Image e o _projection de ProcessingImage
def verticalProjection(image):
    """
        TODO
    """
    matrix = mathematic.Math().calculateTranspose(image.pixel_matrix())
    r =  mathematic.List( [0,0] + projection(matrix)[2:][:-2] + [0,0] )
    return r
    
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
    enhanced_image = horusImage.Image( mode = image.mode, 
                    size = image.size)
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            # Este math eh nativo do python. Incorporar a funcao log em horus.mathematic
            new_value = 100 + 20 * u * math.log(image.getPixel((i,j)) + 1)
            enhanced_image.putPixel((i,j), new_value)
    return enhanced_image

def hildtchSkeletonize(image):        
    while (True):
        letContinue = False
        boundaryPixelList = []
        pixelsToDelete = []
        for i in range( image.size[0] ):
            for j in range(image.size[1]):
                if(image.getPixel((i,j)) == 0):                    
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
            image.putPixel(pixelToDelete, 255)
#        print letContinue                        
        if(not letContinue):            
            break                                 
    return image

def localThreshold(image, size, con):
    """
        This method binarize an image using the mean local adaptive threshold
        algorithm.
        for more information access: 
        http://homepages.inf.ed.ac.uk/rbf/HIPR2/adpthrsh.htm
        
        params:
            image: a grayscale horus image to be thresholded.
            size: the size of the pixel's neighborhood.
            con: a constant to subtracted from the mean of the neighborhood. 
    """
    thresholdedImage = PilImage.new(image.mode, image.size)
    for i in range( image.size[0] ):
        for j in range( image.size[1] ):
            mean = 0
            count = 0
            for k in range(size):
                for l in range(size):
                    try:
                        index = ((i - (int(size/2))+ k),(j - int(size/2)+ l))                        
                        mean = mean + image.getPixel(index)                        
                        count += 1
                    except:
                        pass            
            mean = int(mean/count) - con
            if(image.getPixel((i,j)) > mean):                
                thresholdedImage.putpixel((i,j), 255)
            else:
                thresholdedImage.putpixel((i,j), 0)    
    return horusImage.Image(content = thresholdedImage)
                    
def applyFilter(image, filter):
    return horusImage.Image(content=image.content.filter(filter))

def globalThreshold(img, threshold=128):
    new_img = horusImage.Image(mode=img.mode, size=img.size)
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if img.getPixel((i,j)) > threshold:
                new_img.putPixel((i,j), 255) 
            else:
                new_img.putPixel((i,j), 0)
    return new_img




def locateNonZeroIntervals(value_list):
    """
        cria uma lista distacando os intervalos (os pares com o indice
        inicial e final definem o intervalo) diferentes de zeros.
    """
    nonzero_interval_list = []
    inf = 0
    # cria uma lista de candidatos a placas
    # intervalos de valores diferentes de zero
    for i in range(len(value_list)):
        if value_list[i] != 0:
            if inf == 0:
                if value_list[i-1] == 0:
                    inf = i
            else:
                if i+1 < len(value_list) and value_list[i+1] == 0:
                    nonzero_interval_list.append((inf, i))
                    inf = 0
    return nonzero_interval_list

