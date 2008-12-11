import copy

from PIL import ImageFilter
from PIL import Image as PilImage
from graphGeneration import generateGraph

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
        This class implements all image's methods required in anpr modules
    """
    
    def __init__(self, **kargs):
        """
            TODO
        """
        self.__matrix_image = None   
        
        if kargs.has_key('image'):
            self.__image = kargs['image']
        if kargs.has_key('path'):    
            self.__image = PilImage.open(kargs['path'])
            
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
        #######################################################
        #### Verificar se esse procedimento ja e feito em  ####
        #### alguma api python com uma melhor performance  ####
        #######################################################
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


    def calculateProjection2(self, matrix):
        """
            This method calculates the horizontal projection of image passed
            by parameter image. To calculate vertical projection just
            call this method passing pass as parameter image its transpose.
        """
        projection = [0 for i in range(len(matrix))]
        for i in range(len(matrix)):
            projection[i] = self.sumValues(matrix[i])
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
        """
            TODO
        """   
        return self.sumValues(values_list) / len(values_list)


class RegionDetected(object):

    def __init__(self):
        """
            TODO
        """   
        self.math = ImageMath()

    def calculatePeak(self, projection):
        """
            This method return de maximum value in projection list
            
            PS: the extremes values of projection's list are very high, 
                because the projection is based in edge detection and 
                there are a edge in images border
        """   
        projection = [0,0]+projection[2:][:-2]+[0,0]
        return self.math.maxValue(projection)


    def calculateRegion(self, projection_list, cut_sensibility):
        """
            TODO
        """   
        peak = self.calculatePeak(projection_list)

        blur_list = self.applyBlur(copy.copy(projection_list), 0.07)
        threshold = self.math.calculateAvarage(projection_list)

        candidate_list = []
        sensibility = 1
        while not candidate_list or sensibility==0:
            sensibility -= 0.1
            threshold_list = self.applyThreshold(blur_list, threshold*sensibility)
            candidate_list = []    
            candidate_list = self.locateCandidates(threshold_list)
            report.write("sens: %s\tCandidate List  %s\n"%(str(sensibility),str(candidate_list)))
            if candidate_list:
                for elem in candidate_list:
                    if elem[1] - elem[0] > len(projection_list)*0.6 \
                    or elem[1] - elem[0] < len(projection_list)*0.3:
                        candidate_list.remove(elem)

        generateGraph(PATH_SAVE,file[:-4]+"_Band_Thresh.jpg", threshold_list, \
				([peak],[ projection_list[peak]]))        
        generateGraph(PATH_SAVE,file[:-4]+"_Proj_Vert.jpg", projection_list, \
				([peak],[ projection_list[peak]]))
        
        inf_list = [i for i in range(len(projection_list))[:peak] \
		    if projection_list[i]<= cut_sensibility*projection_list[peak]]
        sup_list = [i for i in range(len(projection_list))[peak:] \
		    if projection_list[i]<= cut_sensibility*projection_list[peak]]
        
        interval = (inf_list[-1], sup_list[0])
        del(blur_list, threshold_list, candidate_list, inf_list, sup_list)
        return interval

    def applyThreshold(self, values_list, threshold):
        """
            TODO
        """   
        def choice(number):
            if number < threshold:
                return 0
            else:
                return number

        return map(choice, values_list)

    def applyBlur(self, values_list, sensibility = 0.01):
        """
            TODO
        """
        list_lenght = len(values_list)
        for i in range(list_lenght):
            neighboors = values_list[(i- int(list_lenght*sensibility/2)):]\
				          [: int(list_lenght*sensibility)]
            values_list[i] = self.math.calculateAvarage(neighboors)
        return values_list

    
    def locateCandidates(self, values_list):
        candidate_list = []
        inf = 0
        sup = 0

        # cria uma lista de candidatos a placas
        # intervalos de valores diferentes de zero
        # TODO: melhorar algoritmo
        for i in range(len(values_list)):
            if values_list[i] != 0:
                if inf == 0:
                    if values_list[i-1] == 0:
                        inf = i
                else:
                    if i+1 < len(values_list) and values_list[i+1] == 0:
                        sup = i
                        candidate_list.append((inf, sup))
                        inf = 0
                        sup = 0
        #print "Candidate List  %s"%str(candidate_list)
        report.write("Candidate List  %s\n"%str(candidate_list))
        return candidate_list        
    
    
    def findCandidatePlates(self, projection_list):
        blur_list = self.applyBlur(projection_list, 0.05)

        threshold = self.math.calculateAvarage(projection_list)

        candidate_list = []
        sensibility = 1

        while not candidate_list or sensibility==0:
            sensibility -= 0.1
            threshold_list = self.applyThreshold(blur_list, threshold*sensibility)
            candidate_list = []            
            candidate_list = self.locateCandidates(threshold_list)
            report.write("sens: %s\tCandidate List  %s\n"%(str(sensibility),str(candidate_list)))
            if candidate_list:
                for elem in candidate_list:
                    if elem[1] - elem[0] > len(projection_list)*0.6 \
                    or elem[1] - elem[0] < len(projection_list)*0.2:
                        report.write("elem rem: %s\n"%str(elem))
                        candidate_list.remove(elem)
                        report.write("New cand: %s\n"%(str(candidate_list)))
        
        report.write("Candidate Plate: %s\n"%str(candidate_list))
        generateGraph(PATH_SAVE,file[:-4]+"_Plate_Thresh.jpg", threshold_list)        
        generateGraph(PATH_SAVE,file[:-4]+"_Proj_horiz.jpg", projection_list)

        inf = 0
        sup = 0
        
        
        # Escolhe o maior intervalo dentre os candidatos
        lenght = 0
        for elem in candidate_list:
            lenght_elem = elem[1] - elem[0]
            if lenght_elem > lenght:
                lenght = lenght_elem
                inf = elem[0]
                sup = elem[1]

        if sup == projection_list[-1] or inf == projection_list[-1]:
            report.write( "inf e sup ultimos: (%s, %s)\n"%( str(inf), str(sup) ) )
        
        report.write("inf e sup: (%s, %s)\n"%(str(inf), str(sup)))
        
        del(blur_list, threshold_list, candidate_list)

        return inf, sup   

        
        
import os

PATH_LOAD = "/home/gabriel/leandro/Workspaces/python-workspaces/anpr/imagens"
PATH_SAVE = "/home/gabriel/leandro/Workspaces/python-workspaces/anpr/placas"

lista = os.listdir(PATH_LOAD)
lista.sort()

lista2 = lista

report = open(os.path.join(PATH_SAVE, 'report.txt'),"w+")

for file in lista2:
    try:
        print "File: %s"%file
        report.write("File: %s\n"%file)
        report.write("Band detector\n")

        image = Image(path = os.path.join(PATH_LOAD,file))
        image.save(os.path.join(PATH_SAVE,file))

        verticalFilteredImage = image.applyFilter(VERTICAL_EDGE_DETECTED)
        grayscaleFilteredImage = verticalFilteredImage.convertRgbToGrayscale()

        imageMath = ImageMath()
        new_matrix = imageMath.calculateTranspose\
	        (grayscaleFilteredImage.matrix_image)
        verticalProjection = imageMath.calculateProjection2(new_matrix)
        verticalProjection = [0,0]+verticalProjection[2:][:-2]+[0,0]

        regionDetected = RegionDetected()
        inf_band, sup_band = regionDetected.calculateRegion\
		         (verticalProjection, 0.55)

        bbox = (0, inf_band, image.size[0], sup_band)
        #print "BBox:  %s"%str(bbox)
        report.write("BBox: %s\n"%str(bbox))

        band = image.crop(bbox)
        band.save(os.path.join(PATH_SAVE,file[:-4]+"_band.jpg"))

        report.write("Plate detector\n")
        filteredBand = band.fullEdgeDetection()
        grayscaleFilteredBand = filteredBand.convertRgbToGrayscale()


        horizontalProjection = imageMath.calculateProjection2\
		           (grayscaleFilteredBand.matrix_image)

        inf_Plate, sup_Plate = regionDetected.findCandidatePlates\
		           (horizontalProjection)

        if sup_Plate == 0:
            sup_Plate = image.size[0]

        bbox = (inf_Plate, inf_band, sup_Plate, sup_band)
        #print "BBox: %s\n"%str(bbox)
        report.write("BBox: %s\n\n"%str(bbox))

        band = image.crop(bbox)
        band.save(os.path.join(PATH_SAVE,file[:-4]+"_plate.jpg"))
        del(image, verticalFilteredImage, grayscaleFilteredImage, imageMath, bbox, band,new_matrix)
        del(verticalProjection, regionDetected, filteredBand, grayscaleFilteredBand, horizontalProjection)
    except:
        pass
