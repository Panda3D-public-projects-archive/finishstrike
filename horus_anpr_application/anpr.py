#XXX: Add Copyright

import os
import copy
import math

import horus.core.processingimage.imagefilter as filter
import horus.core.processingimage.processingimage as processingimage
import horus.utils.graphics as graphics

from horus.core.processingimage.image import Image

SAVE = os.path.join(os.path.abspath(os.path.dirname(__file__)),"placa")
SAVE = os.path.join(os.path.abspath('.'),"placa")

class ImpossiblePlateExtraction(Exception): pass

class PlateDetection(object):
    """
        Returns the plate string extracted from a car image
        
        parameters
            carImage: the car image to be recognized, this object must be an
                      horus image. 
    """
    
    def sortBand(self, projection, band_list):
        """
            Ordena os bands de modo decrescente de acordo com os picos.
        """
        peak_list = []
        band_sort = []
        
        for band in band_list:
            peak_list.append(max(projection[band[0]:band[1]]))

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

        grayscale_filtered_image = processingimage.applyFilter(content, filter.MEDIAN)
        projection_list = processingimage.verticalProjection(grayscale_filtered_image)
                                                    
        # removing the first and the last peak
        projection_list[0] = 0
        projection_list[1] = 0
        projection_list[-1] = 0
        projection_list[-2] = 0
#        graphics.generateGraph( SAVE, car_image.content.filename[-12:-4]+"proj.png", projection_list ) 

        # empirical parameters obtained by calibration
        blur_list = copy.copy(projection_list).applyBlur(0.04)
#        graphics.generateGraph( SAVE, car_image.content.filename[-12:-4]+"blur.png", blur_list ) 
        
        threshold = projection_list.calculateAvarage()
        threshold_list = blur_list.applyThreshold(threshold)
#        graphics.generateGraph( SAVE, car_image.content.filename[-12:-4]+"_band_proj.png", threshold_list )        

        band_index_list = threshold_list.locateNonZeroIntervals()

        sorted_band_index_list = self.sortBand(projection_list, 
                                               band_index_list)
                                             
        i = 0
        for band_index in sorted_band_index_list:
            i += 1
            range_to_crop = (0, band_index[0], car_image.size[0], 
                                                           band_index[1])
            band_image = car_image.crop(range_to_crop)
            band_image.content.file_name = "/%s-%s.png" % ( car_image.content.filename[-12:-4], str(i) )
            band_list.append(Band(band_image, range_to_crop))
#            band_image.save(SAVE+band_image.content.file_name)
            
        return band_list

    def getPlate(self, car_image):
        """
          It returns the plate.
        """
        band_object_list = self.generateBandList(car_image)
        if not len(band_object_list):
            message = 'The plate could not be extracted.'
            raise ImpossiblePlateExtraction, message

        band = band_object_list[0]
#        band.band_image.content.save((os.path.join(SAVE, car_image.content.filename[-12:-4]+"_band.png")))
        return band.getPlate()


class Band(object):
    """
        This class contains a band image.
    """
    def __init__(self, band_image=None, bbox = (0.0, 0.0, 0.0, 0.0)  ):
        if band_image is None:
            raise AttributeError, 'Band image can not be None.'
        else:
            self.band_image = band_image
        self.bbox = bbox 

    def sortPlate(self, plate_list):
        """
            Ordena os plates de modo decrescente de acordo com a distancia do
            centro do intervalo com o centro (coordenada horizontal) da imagem.
        """
        center_list = []
        plate_sort = []
        
        center = self.band_image.size[0] / 2.0
        for plate in plate_list:
            center_list.append( math.fabs(((plate[1]+plate[0])/2.0) - center) )

        center_sort = copy.copy(center_list)
        center_sort.sort()

        for center in center_sort:
            plate_sort.append(plate_list[center_list.index(center)])
        return plate_sort


    def segment(self, projection_list):
#        graphics.generateGraph( SAVE, self.band_image.content.file_name[-14:-4]+"_plate_proj.png", projection_list )    
        threshold = projection_list.calculateAvarage()
        blur_list = projection_list.applyBlur(0.04)#.03
                
        threshold_list = copy.copy(blur_list).applyThreshold(threshold*0.7)
        candidate_list = threshold_list.locateNonZeroIntervals()
        candidate_list =  self.sortPlate(candidate_list)
        print candidate_list
        if ((candidate_list[0][1] - candidate_list[0][0])>len(projection_list)/3):
            print "opa1"
            threshold_list = copy.copy(blur_list).applyThreshold(threshold)
            candidate_list = threshold_list.locateNonZeroIntervals()
            candidate_list =  self.sortPlate(candidate_list)
            print candidate_list
         
        print
#        graphics.generateGraph( SAVE, self.band_image.content.file_name[-14:-4]+"_plate_thresh.png", threshold_list )               
        return candidate_list


    def generatePlateList(self):
        content = self.band_image.convert('L')
#        content = processingimage.applyFilter(content, filter.HORIZONTAL_EDGE_DETECTED)
        content = processingimage.fullEdgeDetection(content)
        content = processingimage.applyFilter(content, filter.MEDIAN)
#        content.save( os.path.join(SAVE, self.band_image.content.file_name[-14:-4]+"_edge.png") )
        vertical_filtered_image = Image(content=content)
  
        content = vertical_filtered_image.convert('L')
        grayscale_filtered_image = Image(content=content)
        projection_list = processingimage.horizontalProjection(
                                                    grayscale_filtered_image)
#        graphics.generateGraph( SAVE, self.band_image.content.file_name[-14:-4]+"_plate_proj.png", projection_list )    

        candidate_list = self.segment(projection_list)
        return candidate_list

    def getPlate(self):
        """
            It will look for a plate into the band image.
        """
        candidate_list = self.generatePlateList()
        candidate_list =  self.sortPlate(candidate_list)
        i = 0
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
        return self.plate_image

    def getPlateAsText(self):
        """
            It returns the plate as string
        """
        # Colocar o OCR nesse metodo
        pass
 
if __name__ == "__main__":
    abspath = os.path.abspath('.')
    path_load = os.path.join(abspath,"imagens")
    path_save = os.path.join(abspath,"placa")
    file_list = os.listdir(path_load)
    file_list.sort()
    
    for file_name in file_list:
        try:
            print file_name
            path_image = os.path.join(path_load, file_name)
            car_image = Image(path=path_image)
            platedetection = PlateDetection()        
            plate = platedetection.getPlate(car_image)
            #car_image.save((os.path.join(SAVE, car_image.content.filename[-12:-4]+".png")))
            plate.plate_image.content.save((os.path.join(SAVE, car_image.content.filename[-12:-4]+"_plate.png")))
        except:
            pass
        