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

class Image(object):	
    """
        TODO
    """

	##########################################################
	#1 - Criar metodo __init__ desta classe, recebendo como parametro **kargs.
	#	    Verificar se o usuario passou um path ou um image.
	#
	#    	Deletar loadFromPath e loadFromImage
	#	
	#2 - Verificar se a alteracao feita no metodo applyFilter esta correta.
	#3 - Verificar se a alteracao feita no metodo convertRgbToGrayscale esta correta.
	#4 - Verificar se a alteracao feita no metodo crop esta correta.3 - Verificar se a alteracao feita no metodo convertRgbToGrayscale esta correta.
	#5 - Pensar e alterar 'as alteracoes' feitas nos metodos: applyFilter, convertRgbToGrayscale e crop
	#	    Estes metodos devem retornar instancias da classe Image deste modulo. 	 	 
	##########################################################
    def __init__(self):
        """
            TODO
        """
        self.__matrix_image = None    
    

    def loadFromPath(self, path):
        self.__image = PilImage.open(path)
        
    def loadFromImage(self, image):
        self.__image = image

    @property
    def image(self):
        """
            TODO
        """
        return self.__image
        

    def applyFilter(self, type_filter):
        image = Image()
        image.loadFromImage(self.__image.filter(type_filter))
        return image
    
    
    def convertRgbToGrayscale(self):
        """
            TODO
        """
        image = Image()
        image.loadFromImage(self.__image.convert("L"))
        return image

    
    def size(self):        
        return self.__image.size

    def crop(self, bbox):
        image = Image()
        image.loadFromImage(self.__image.crop(bbox))
        return image

    def save(self, path):
        self.__image.save(path)

    def getpixel(self,xy):
        return self.__image.getpixel(xy)
        
    @property
    def matrix_image(self):
        #######################################
        # Alterar esse metodo #####
        """
            This method returns a matrix with values of wich image's pixels.
        """
        if not self.__matrix_image:
            self.__matrix_image = [[0 for i in range(self.__image.size[1])] \
                             for j in range(self.__image.size[0]) ]
            
            for i in range(len(self.__matrix_image)):
                for j in range(len(self.__matrix_image[0])):
                    self.__matrix_image[i][j] = self.__image.getpixel((i,j))
        
        return self.__matrix_image
		
    def fullEdgeDetection(self):
            grayS_image = self.convertRgbToGrayscale()
            image_vertical_filtered = grayS_image.applyFilter(VERTICAL_EDGE_DETECTED)
            image_horizontal_filtered = grayS_image.applyFilter(HORIZONTAL_EDGE_DETECTED)
            #print image_vertical_filtered.getpixel((0,0))
            
            sum = 0
            for i in range(self.__image.size[0]):
                    for j in range(self.__image.size[1]):
                                    sum = 0
                               # print image_vertical_filtered.getpixel((i,j))
                                    sum += image_vertical_filtered.__image.getpixel((i,j))
                                    sum += image_horizontal_filtered.__image.getpixel((i,j))
                                    self.__image.putpixel((i,j), sum)	
            return self

    
        
        
class ImageMath(object):
    """
        TODO
    """

    def calculateTranspose(self, matrix):
        """
            This methid calculates the transpose of a matrix.
            
            For example:
            matrix = [[1, 2, 3], [4, 5, 6]]
            new_matrix = [[1, 4], [2, 5], [3, 6]]
        """
        new_matrix = [[0 for i in range(len(matrix))] \
                         for j in range(len(matrix[0])) ]
        
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                new_matrix[j][i] = matrix[i][j]
                
        return new_matrix

    def calculateProjection(self, matrix):
        """
            This method calculates the vertical projection of image passed 
            by parameter image. To calculate horizontal projection just
            call this method passing pass as parameter image its transpose.
        """
        projection = [0 for i in range(len(matrix[0]))]
        for i in range(len(matrix[0])):
            for j in range(len(matrix)):
                projection[i] += matrix[j][i]
        return projection

    def maxValue(self, values_list):
        """
            Return the first index of maximal value of a value's list 
        """   
        max_value = max(values_list)
        index_max_value = values_list.index(max_value)
        return index_max_value

    def minValue(self, values_list):
        """
            Return the first index of minimal value of a value's list 
        """   
        min_value = min(values_list)
        index_min_value = values_list.index(min_value)
        return index_min_value

    def sumValues(self, values_list):
        """
            Return the sum of values of list passed by parameter
        """ 
        return sum(values_list)

    def calculateDerivative(self, projection, h):
        """
            TODO
        """   
        derivative = [0 for i in range(len(projection))]

        for i in range(len(projection)):
            derivative[i] = (projection[i] - projection[i-h]) / h

        return derivative
        
    def calculateAvarage(self, values_list):
        return self.sumValues(values_list) / len(values_list)
        



class RegionDetected(object):

    def __init__(self):
        self.math = ImageMath()

    def calculatePeak(self, projection):
        """
            TODO
        """   
        projection = [0,0]+projection[2:][:-2]+[0,0]
        return self.math.maxValue(projection)
        
    def calculateRegion(self, projection, sensibility):
        """
            TODO
        """   
        peak = self.calculatePeak(projection)

        inf_list = [i for i in range(len(projection))[:peak] if projection[i]<= sensibility*projection[peak]]
        sup_list = [i for i in range(len(projection))[peak:] if projection[i]<= sensibility*projection[peak]]

        return inf_list[-1], sup_list[0]
    

    def applyThreshold(self, values_list, threshold):
        print threshold
        for i in range(len(values_list)):
            if values_list[i] < threshold:
                values_list[i] = 0
        return values_list

    def applyBlur(self, values_list):
        for i in range(len(values_list)):
            neighboors = values_list[(i-3):][:5]
            values_list[i] = self.math.calculateAvarage(neighboors)
        return values_list

    def findCandidatePlates(self, projection_list):
        projection_list = regionDetected.applyBlur(projection_list)

        threshold = self.math.calculateAvarage(projection_list)
        projection_list = regionDetected.applyThreshold(projection_list, threshold*0.5)


        candidate_list = []
        inf = 0
        sup = 0

        # cria uma lista de candidatos a placas
        # intervalos de valores diferentes de zero
        # TODO: melhorar algoritmo
        for i in range(len(projection_list)):
            if projection_list[i] != 0:
                if inf == 0:
                    if projection_list[i-1] == 0:
                        inf = i
                else:
                    if i+1 < len(projection_list) and projection_list[i+1] == 0:
                        sup = i
                        candidate_list.append((inf, sup))
                        inf = 0
                        sup = 0
                
        print candidate_list

        # Escolhe o maior intervalo dentre os candidatos
        lenght = 0
        for elem in candidate_list:
            lenght_elem = elem[1] - elem[0]
            if lenght_elem > lenght:
                lenght = lenght_elem
                inf = elem[0]
                sup = elem[1]


        print "\n\n%d\t%d"%(inf, sup)
        #ax = subplot(111)
        #ax.plot(range(len(projection_list)),projection_list)
        #show()

        return inf, sup
	   
import sys
from pylab import *


import os

lista = os.listdir("C:\\snapshots")

lista2 = []
lista2 = lista[33:]

# ERRO NO ALGORITMO 1: da erro no out of range para test__00X.jpg, para X = 5, 6, 15, 26, 27, 35, 50, 58, 82, 88
# Resultado Inapropriado no Algoritmo1: 17, 23, 34, 40, 41, 53, 56, 57, 66, 67, 75, 84, 85, 94
# imagens testadas 97; erros 24
# Porcenteagem de acerto: 75%

# Erro no algoritmo 2: 34, 57
# Resultado Inapropriado no Algoritmo2: 8, 9, 12, 18, 19, 24, 31, 33, 36, 42, 43, 45, 49, 52, 54, 55, 59, 60, 62,
# 63, 64, 65, 76, 83, 90, 97
# imagens testadas 97 - 24 = 73; erros 28
# Porcenteagem de acerto: 62%


for file in lista2:
	print file
	image = Image()
	image.loadFromPath("c:\\snapshots\\%s"%file)

	verticalFilteredImage = image.applyFilter(VERTICAL_EDGE_DETECTED)
	grayscaleFilteredImage = verticalFilteredImage.convertRgbToGrayscale()

	imageMath = ImageMath()
	verticalProjection = imageMath.calculateProjection(grayscaleFilteredImage.matrix_image)

	regionDetected = RegionDetected()
	inf, sup = regionDetected.calculateRegion(verticalProjection, 0.55)

	bbox = (0, inf, image.size()[0], sup)

	band = image.crop(bbox)
	band.save("C:\\snapshots\\teste\\%sband.jpg"%file)

	#grayscaleFilteredBand = verticalEdgeFilteredBand.convertRgbToGrayscale()
	filteredBand = band.fullEdgeDetection()
	grayscaleFilteredBand = filteredBand.convertRgbToGrayscale()
	
	
	import pdb
	#pdb.set_trace()
	new_matrix = imageMath.calculateTranspose(grayscaleFilteredBand.matrix_image)	
	
	grayscaleFilteredBand.save("c:\\snapshots\\teste\\blabla.jpg")
	horizontalProjection = imageMath.calculateProjection(new_matrix)
	 
	#horizontalProjection = regionDetected.applyBlur(horizontalProjection)
	#threshold = imageMath.calculateAvarage(horizontalProjection)
	#horizontalProjection = regionDetected.applyThreshold(horizontalProjection, threshold)
	#print horizontalProjection

	inf_Plate, sup_Plate = regionDetected.findCandidatePlates(horizontalProjection)

	print "\n\n%d\t%d"%(inf_Plate, sup_Plate)
	bbox = (inf_Plate, inf, sup_Plate, sup)
	print bbox
	band = image.crop(bbox)
	band.save("C:\\snapshots\\teste\\plate_%s"%file)	
	#ax = subplot(111)
	#ax.plot(range(len(horizontalProjection)),horizontalProjection)
	#show()


	
	
	
	
	

