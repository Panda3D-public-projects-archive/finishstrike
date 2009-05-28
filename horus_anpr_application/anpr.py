#XXX: Add Copyright

import os
import copy
import horus.core.processingimage.imagefilter as filter
import horus.core.processingimage.processingimage as processingimage
import horus.utils.graphics as graphics

from horus.core.processingimage.image import Image

import pytesser

SAVE = os.path.join(os.path.abspath(os.path.dirname(__file__)),"placa")
SAVE = os.path.join(os.path.abspath('.'),"placa")


class PlateDetection(object):
    """
        Returns the plate string extracted from a car image
        
        parameters
            carImage: the car image to be recognized, this object must be an
                      horus image. 
    """
    
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

        peak_sort = copy.copy(peak_list)
        peak_sort.sort()

        for peak in peak_sort[::-1]:
            band_sort.append(band_list[peak_list.index(peak)])
        
        return band_sort
            

    def generateBandList(self, car_image):
        """
          It generates a list of all the candidate bands.
        """
        band_list = []
        content = processingimage.applyFilter(car_image, 
                                              filter.VERTICAL_EDGE_DETECTED)
        vertical_filtered_image = Image(content=content)

        content = vertical_filtered_image.convert('L')
        grayscale_filtered_image = Image(content=content)
        projection_list = processingimage.horizontalProjection(
                                                    grayscale_filtered_image)

        # removing the first and the last peak
        projection_list[0] = 0
        projection_list[1] = 0
        projection_list[-1] = 0
        projection_list[-2] = 0

        # empirical parameters obtained by calibration
        blur_list = projection_list.applyBlur(0.07)
        
        threshold = projection_list.calculateAvarage()
        threshold_list = blur_list.applyThreshold(threshold)

        band_index_list = locateNonZeroIntervals(threshold_list)


        sorted_band_index_list = self.sortBand(projection_list, 
                                               band_index_list)
        for band_index in sorted_band_index_list:
            range_to_crop = (0, band_index[0], car_image.size[0], 
                                                           band_index[1])
            band_image = car_image.crop(range_to_crop)
            band_list.append(Band(band_image))
            
        return band_list

    def getPlateAsImage(self, car_image):
        """
          It returns the image of the plate.
        """
        band_object_list = self.generateBandList(car_image)
        # For now, we are just using the first band.
        if not len(band_object_list):
            message = 'The plate could not be extracted.'
            raise ImpossiblePlateExtraction, message

        first_band = band_object_list[0]

        first_band.getPlate().plate_image.save('./placa/bianin.jpg')

        return None


    def getPlate(self, car_image):
        pass


class Band(object):
    """
      This class contains a band image.
    """
    def __init__(self, band_image=None):
        if band_image is None:
            raise AttributeError, 'Band image can not be None.'
        else:
            self.band_image = band_image


    def getPlate(self):
        """
            It will look for a plate into the band image.
        """
        band_list = []
        content = processingimage.applyFilter(self.band_image, 
                                              filter.HORIZONTAL_EDGE_DETECTED)
        horizontal_filtered_image = Image(content=content)
  
        content = horizontal_filtered_image.convert('L')
        grayscale_filtered_image = Image(content=content)
        projection_list = processingimage.verticalProjection(
                                                    grayscale_filtered_image)
  
        # removing the first and the last peak
        projection_list[0] = 0
        projection_list[1] = 0
        projection_list[-1] = 0
        projection_list[-2] = 0
  
        # empirical parameters obtained by calibration
        blur_list = projection_list.applyBlur(0.05)

        threshold = projection_list.calculateAvarage()
        #TODO: melhorar algoritmo
        candidate_list = []
        sensibility = 1
        while not candidate_list or sensibility==0:
            sensibility -= 0.1
            threshold_list = blur_list.applyThreshold(threshold*sensibility)
            candidate_list = locateNonZeroIntervals(threshold_list)
            for elem in candidate_list:
                # Estes parametros foram calculados empiricamente
                # Em outras palavras: chute...
                if elem[1] - elem[0] > len(projection_list)*0.6 \
                   or elem[1] - elem[0] < len(projection_list)*0.2:
                    candidate_list.remove(elem)
        
        # Escolhe o maior intervalo dentre os candidatos
        inferior_index = superior_index = lenght = 0
        for elem in candidate_list:
            lenght_elem = elem[1] - elem[0]
            if lenght_elem > lenght:
                lenght = lenght_elem
                inferior_index = elem[0]
                superior_index = elem[1]
  
        range_to_crop = (inferior_index, 0, superior_index, self.band_image.size[1])
        plate_image = self.band_image.crop(range_to_crop)
        self.band_image.save('./placa/band_placa.jpg')
        print range_to_crop
        return Plate(plate_image)

class Plate(object):
    """
      This class contains a plate image.
    """
    def __init__(self, plate_image=None):
        if plate_image is None:
            raise AttributeError, 'Plate image can not be None.'
        else:
            self.plate_image = plate_image

    def getPlateImage(self):
        """
            It returns the plate image
        """
        pass

    def getPlateAsText(self):
        """
            It returns the plate as string
        """
        pass

class Character(object):
    def recognize(self):
        pass

class ImpossiblePlateExtraction(Exception): pass
  
def locateNonZeroIntervals(value_list):
    """
        Cria uma lista distacando os intervalos (os pares com o indice
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

  
def binarizeImage(path):

    from PIL import Image as PilImage
    image = PilImage.open(path)
    image = image.convert("L")
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if(image.getpixel((i,j)) < 128):
                image.putpixel((i,j), 0)
            else:
                image.putpixel((i,j), 255)
    image.save(path)
 
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
        plate = platedetection.getPlateAsImage(car_image)
        #from horus.core.processingimage.processingimage import hildtchSkeletonize
        break

    img = binarizeImage('./placa/bianin.jpg')


    #img_filtered = hildtchSkeletonize(img)
    #img_filtered.save('./placa/bianin_sk2.jpg')
    #print pytesser.image_to_string(img)
    import sys
    sys.exit(0)
