#XXX: Add Copyright

import os
import copy
import ImageFilter
import math
import horus.core.processingimage.imagefilter as filter
import horus.core.processingimage.processingimage as processingimage
import horus.utils.graphics as graphics

from horus.core.processingimage.image import Image
from horus.vision.ocr import apply_ocr

SAVE = os.path.join(os.path.abspath(os.path.dirname(__file__)),"placa")

class ImpossiblePlateExtraction(Exception): 
  pass

class PlateDetection(object):
    """
        Returns the plate string extracted from a car image
        
        parameters
            carImage: the car image to be recognized, this object must be an
                      horus image. 
    """
    index = 0
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
        self.index += 1
        band_list = []
        content = car_image.convert('L')
        content.save(SAVE+"STEP01-01grayscale%s.jpg" % self.index)

        content = processingimage.applyFilter(content, 
                                               filter.VERTICAL_EDGE_DETECTED)
        content.save(SAVE+"STEP01-02vertical_edge_detection%s.jpg" % self.index)

        median_filtered_image = processingimage.applyFilter(content, filter.MEDIAN)
        content.save(SAVE+"STEP01-03filterMedian%s.jpg" % self.index)
        projection_list = processingimage.verticalProjection(median_filtered_image)
                                                    
        # removing the first and the last peak
        projection_list[0] = 0
        projection_list[1] = 0
        projection_list[-1] = 0
        projection_list[-2] = 0
        graphics.generateGraph( SAVE, "STEP02-04GraphProjection.jpg", projection_list ) 

        # empirical parameters obtained by calibration
        blur_list = copy.copy(projection_list).applyBlur(0.04)
        graphics.generateGraph( SAVE, "STEP02-04GraphBlur.jpg", blur_list ) 
        
        threshold = projection_list.calculateAvarage()
        threshold_list = blur_list.applyThreshold(threshold)
        graphics.generateGraph( SAVE, "STEP02-04GraphBandProjection.jpg", threshold_list )        

        band_index_list = threshold_list.locateNonZeroIntervals()

        sorted_band_index_list = self.sortBand(projection_list, 
                                               band_index_list)
                                             
        i = 0
        for band_index in sorted_band_index_list:
            i += 1
            range_to_crop = (0, band_index[0], car_image.size[0], 
                                                           band_index[1])
            band_image = car_image.crop(range_to_crop)
            band_image.content.file_name = "/STEP03-05generateBandList-%s-%s.jpg" % (self.index, str(i))
            band_list.append(Band(band_image, range_to_crop))
            band_image.save(SAVE+band_image.content.file_name)
            
        return band_list

    def getPlate(self, car_image):
        """
          It returns the plate.
        """
        self.index += 1
        band_object_list = self.generateBandList(car_image)
        if not len(band_object_list):
            message = 'The plate could not be extracted.'
            raise ImpossiblePlateExtraction, message

        band = band_object_list[0]
        band.band_image.save(os.path.join(SAVE, "STEP04-%s_select_band.jpg" % self.index))
        return band.getPlate()


class Band(object):
    """
        This class contains a band image.
    """
    index = 0
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
        graphics.generateGraph( SAVE, "STEP06_plate_proj.jpg", projection_list )    
        threshold = projection_list.calculateAvarage()
        blur_list = projection_list.applyBlur(0.04)#.03
                
        threshold_list = copy.copy(blur_list).applyThreshold(threshold*0.7)
        candidate_list = threshold_list.locateNonZeroIntervals()
        candidate_list =  self.sortPlate(candidate_list)
        if ((candidate_list[0][1] - candidate_list[0][0])>len(projection_list)/3):
            threshold_list = copy.copy(blur_list).applyThreshold(threshold)
            candidate_list = threshold_list.locateNonZeroIntervals()
            candidate_list =  self.sortPlate(candidate_list)
        graphics.generateGraph( SAVE, "STEP06_plate_thresh.jpg", threshold_list )               
        return candidate_list


    def generatePlateList(self):
        self.index += 1
        content = self.band_image.convert('L')
        content.save(SAVE+'STEP05-01-grayScale%s.jpg' % self.index)
#        content = processingimage.applyFilter(content, filter.HORIZONTAL_EDGE_DETECTED)
        content = processingimage.fullEdgeDetection(content)
        content.save(SAVE+'/STEP05-02-fullEdgeDetection%s.jpg' % self.index)
        content = processingimage.applyFilter(content, filter.MEDIAN)
        content.save(SAVE+'/STEP05-03-medianFilter%s.jpg' % self.index)
        #content.save( os.path.join(SAVE, self.band_image.content.file_name[-14:-4]+"_edge.jpg") )
        vertical_filtered_image = Image(content=content)
  
        content = vertical_filtered_image.convert('L')
        grayscale_filtered_image = Image(content=content)
        grayscale_filtered_image.save(SAVE+'/STEP05-04-grayScale%s.jpg'%self.index)
        projection_list = processingimage.horizontalProjection(
                                                    grayscale_filtered_image)
#        graphics.generateGraph( SAVE, self.band_image.content.file_name[-14:-4]+"_plate_proj.jpg", projection_list )    

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
        image = self.plate_image.convert('L')
        bin_image = processingimage.localThreshold(image, 5, 7)
        bin_image.save(SAVE+'/Plate-getPlateAsText-plate-localThreshold.jpg')
        X = []
        for x in range(bin_image.size[0]):
          for y in range(bin_image.size[1]):
            if bin_image.getPixel((x,y)) == 0:
              X.append((x,y))
        X.sort()
      
        group_list = []
        for i in X:
          group_index_list = []
          for group in group_list:
            neighbour_list = bin_image.getEightNeighbourhoodCoordinate(i)
            if neighbour_list[0] in group or\
               neighbour_list[1] in group or\
               neighbour_list[2] in group or\
               neighbour_list[3] in group or\
               neighbour_list[4] in group or\
               neighbour_list[5] in group or\
               neighbour_list[6] in group or\
               neighbour_list[7] in group :
              group_index_list.append(group_list.index(group))
      
          group_index_list.sort()
          if group_index_list:
            if len(group_index_list) > 1:
              new_list = []
              for index in group_index_list:
                new_list.extend(group_list[index])
      
              for index in reversed(group_index_list):
                group_list.remove(group_list[index])
      
              group_list.append(new_list)
            else:
              group_list[group_index_list[0]].append(i)
          else:
            group_list.append([i])
      
        # calculate the bbox average
        # generate all image objects from group_list, drawning all the black pixels
        width_sum = 0
        height_sum = 0
        image_candidate_list = []
        image_size = bin_image.size
        media = 0
        for group in group_list:
          if len(group) >= 43 and len(group) < 140:
            new_image = Image(mode='L', size=image_size, color=255)
            for black_pixel in group:
              new_image.putPixel(black_pixel, 0)
            image_bbox = new_image.negative().content.getbbox()
            if (image_bbox[2] - image_bbox[0]) < 43 or \
               (image_bbox[3] - image_bbox[1]) > 4:
              width_sum = width_sum + (image_bbox[2] - image_bbox[0])
              height_sum = height_sum + (image_bbox[3] - image_bbox[1])
              media += 1
              image_candidate_list.append((new_image, image_bbox))
        avg_width = width_sum/media
        avg_heigth = height_sum/media
        
        character_list = []
        for img, bbox in image_candidate_list:
          if (bbox[2] - bbox[0]) <= avg_width+int(avg_width*0.4) and\
            (bbox[2] - bbox[0]) >= avg_width-int(avg_width*0.4) and\
            (bbox[3] - bbox[1]) <= avg_heigth+int(avg_heigth*0.2) and\
            (bbox[3] - bbox[1]) >= avg_heigth-int(avg_heigth*0.2):      
            character_list.append(img)
        
        plate_text_list = []
        index = -1
        unique_image = Image(mode='L', size=image_size, color=255)
        for char_image in character_list:
          index +=1
          char_image.save(SAVE+'/char%s.jpg' % index)
          median_image = char_image.content.filter(ImageFilter.MedianFilter)
          for x in range(median_image.size[0]):
            for y in range(median_image.size[1]):
              if median_image.getpixel((x,y)) == 0:
                unique_image.putPixel((x,y), 0)

          median_image.save(SAVE+'/char%s-medianfilter.jpg' % index)
          character_text = apply_ocr(median_image)
          if character_text in ['\n', None]:
            character_text = apply_ocr(char_image)
          plate_text_list.append(character_text.replace('\n', '').replace(' ', ''))
        unique_image.save('xxx.jpg')
        return ''.join(plate_text_list)
 
def main(car_image):
  car_image = Image(content=car_image)
  platedetection = PlateDetection()
  plate_text = platedetection.getPlate(car_image).getPlateAsText()
  return plate_text

