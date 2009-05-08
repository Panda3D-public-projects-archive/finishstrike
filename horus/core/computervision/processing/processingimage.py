# XXX: Add Copyright

import core.computervision.image as Image
import horusimagefilter as filter
import utils.mathematic as Math
import math

def fullEdgeDetection(image):
    """
        TODO
    """    
    new_image = image
    if(image.mode != "L"):
        new_image = image.convert("L")       
    vertical_edges = new_image.filter(filter.VERTICAL_EDGE_DETECTED)
    horizontal_edges = new_image.filter(filter.HORIZONTAL_EDGE_DETECTED)

    # fazer um breve comentario sobre esses fors
    for i in range( image.size[0] ):
        for j in range( image.size[1] ):
            pixel_value = vertical_edges.getpixel( (i,j) ) + \
                          horizontal_edges.getpixel( (i,j) )
            new_image.putpixel( (i,j), pixel_value )
    
    return Image.Image(img_to_mix = new_image)

# XXX: Why __ ??
def projection(matrix):
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
def verticalProjection(image):
    """
        TODO
    """
    matrix = Math.Math().calculateTranspose(image.pixel_matrix())
    return Math.List( [0,0] + projection(matrix)[2:][:-2] + [0,0] )
    
def horizontalProjection(image):
    """
        TODO
    """
    return Math.List(projection(image.pixel_matrix()))
    
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
    enhanced_image = Image.new( mode = image.mode, 
                    size = image.size)
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            # Este math eh nativo do python. Incorporar a funcao log em horus.mathematic
            new_value = 100 + 20 * u * math.log(image.getpixel((i,j)) + 1)
            enhanced_image.putpixel((i,j), new_value)
    return enhanced_image

