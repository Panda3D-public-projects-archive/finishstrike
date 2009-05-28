#XXX: Add Copyright

import os

import horus.core.processingimage.imagefilter as filter
import horus.core.processingimage.processingimage as processingimage
import horus.utils.graphics as graphics

from horus.core.processingimage.image import Image

#SAVE = os.path.join(os.path.abspath(os.path.dirname(__file__)),"placa")
SAVE = os.path.join(os.path.abspath('.'),"placa")


class PlateDetection(object):
    """
        Returns the plate string extracted from a car image
        
        parameters
            carImage: the car image to be recognized, this object must be an
                      horus image. 
    """
    
    def locateNonZeroIntervals(self, values_list):
        """
            Cria uma lista distacando os intervalos (os pares com o indice
            inicial e final definem o intervalo) diferentes de zeros.
        """
        nonzero_intervals_list = []
        inf = 0

        # cria uma lista de candidatos a placas
        # intervalos de valores diferentes de zero
        for i in range(len(values_list)):
            if values_list[i] != 0:
                if inf == 0:
                    if values_list[i-1] == 0:
                        inf = i
                else:
                    if i+1 < len(values_list) and values_list[i+1] == 0:
                        nonzero_intervals_list.append( (inf, i) )
                        inf = 0
                        
        return nonzero_intervals_list
        
    # nao esta sendo utilizado porque e necessario definir a menor porcentagem
    # de tamanho de um intervalo, em relacao ao todo, para considera-lo
    def removeSmallIntervals(self, value_list, lenght):             
        for intervals in value_list:
            if intervals[1] - intervals[0] < lenght:
                value_list.remove(intervals)
        return value_list
        
       
    def sortBand(self, projection, band_list):
        """
            Ordena os bands de modo decrescente de acordo com os picos.
        """
        peak_list = []
        band_sort = []
        
        for band in band_list:
            peak_list.append(max(projection[band[0]:band[1]]))

        # a copia e necessaria pois o sort altera a lista ao ordena-la, e o 
        # estado inicial dos pares (indices, picos) e necessario para resgatar 
        # o band inicial
        import copy
        peak_sort = copy.copy(peak_list)
        peak_sort.sort()

        for peak in peak_sort[::-1]:
            band_sort.append(band_list[peak_list.index(peak)])
        
        return band_sort
            

    def locateBandList(self, car_image):
        band_list = []

        content = processingimage.applyFilter(                                
                                     car_image, filter.VERTICAL_EDGE_DETECTED )
        vertical_filtered_image = Image(content=content)

        content = vertical_filtered_image.convert('L')
        grayscale_filtered_image = Image(content=content)
        projection_list = processingimage.horizontalProjection(
                                                    grayscale_filtered_image )

        # removing the first and the last peak
        projection_list[0] = 0
        projection_list[1] = 0
        projection_list[-1] = 0
        projection_list[-2] = 0

        # getting the peak
        peak = projection_list.index(max(projection_list))

        # empirical parameters obtained by calibration
        cut_sensibility = 0.55
        blur_list = projection_list.applyBlur(0.07)
        
        threshold = projection_list.calculateAvarage()
        threshold_list = blur_list.applyThreshold(threshold)

        band_list = self.locateNonZeroIntervals(threshold_list)


        band_list = self.sortBand(projection_list, band_list)
        i = 0
        for band in band_list:
            i+=1
            range_to_crop = (0, band[0], car_image.size[0], band[1])
            im = car_image.crop(range_to_crop)
            im.save(SAVE+"/%s-%s.png" % ( car_image.content.filename[-12:-4],
                                                     str(i) ) )
            
        return band_list

    def getPlate(self, car_image):

        self.locateBandList(car_image)

        #for band in band_list:
        #    plate = band.getRegion()
        #    if plate:
        #        return plate

class Region(object):  
    """
        Returns a sorted region candidate list. The list is sorted by the
        probability of existence of the searched region in the candidates.
        
        parameters
            candidateList: the candidate list to be sorted.
           
    """
    def sortCandidateList(self, candidateList):
        pass
    
    def getCutSensibility(self):
        pass    
    
    def getFootConstants(self):
        pass
    
    def getBlurredList(self, listToBlur):
        pass
    
    def getProjection(self):
        pass
    
    def calculatePeak(self, projection):
       pass
    
    def locateCandidateList(self, values_list):
       pass
    
    def getRegion(self):
        pass    
    
class Band(Region):
     
    def getCutSensibility(self):
        pass
    
    def getFootConstants(self):
        pass
    
    def getBlurredList(self, listToBlur):
        pass
    
    def getProjection(self):
        pass
    
    def getRegion(self):
        pass

class Plate(Region):
     
    def getCutSensibility(self):
        pass
    
    def getFootConstants(self):
        pass
    
    def getBlurredList(self, listToBlur):
        pass
    
    def getProjection(self):
        pass
    
    def getRegion(self):
        pass
    
    def segment(self):
        pass
    
    def isPlate(self):
        pass

class Character(object):
    def recognize(self):
        pass
if __name__ == "__main__":
    
    abspath = os.path.abspath('.')
    path_load = os.path.join(abspath,"imagens")
    path_save = os.path.join(abspath,"placa")
    file_list = os.listdir(path_load)
    file_list.sort()
    
    for file_name in file_list[1:][:20]:
        path_image = os.path.join(path_load, file_name)
        car_image = Image(path=path_image)
        platedetection = PlateDetection()
        plate = platedetection.getPlate(car_image)
