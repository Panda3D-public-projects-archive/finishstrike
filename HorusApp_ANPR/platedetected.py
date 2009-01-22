import copy
import os

import graphics as Graphics
import mathematic as Math
import image as Image

class RegionDetected(object):

    def __init__(self):
        """
            TODO
        """   
        self.image_math = Math.ImageMath()
        self.math = Math.Math()

    def calculatePeak(self, projection):
        """
            This method return de maximum value in projection list
            
            PS: the extremes values of projection's list are very high, 
                because the projection is based in edge detection and 
                there are a edge in images border
        """   
        projection = [0,0]+projection[2:][:-2]+[0,0]
        return self.math.maxValue(projection)


    def calculateRegion(self, projection_list, cut_sensibility, report):
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
            candidate_list = self.locateCandidates(threshold_list, report)
            report.write("sens: %s\tCandidate List  %s\n"%(str(sensibility),str(candidate_list)))
            if candidate_list:
                for elem in candidate_list:
                    if elem[1] - elem[0] > len(projection_list)*0.6 \
                    or elem[1] - elem[0] < len(projection_list)*0.3:
                        candidate_list.remove(elem)

        Graphics.generateGraph(report.path_save, report.car_image.file_name[:-4]+"_Band_Thresh.png", \
                               threshold_list, ([peak],[ projection_list[peak]]))        
        Graphics.generateGraph(report.path_save, report.car_image.file_name[:-4]+"_Proj_Vert.png", \
                               projection_list, ([peak],[ projection_list[peak]]))
        
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

    
    def locateCandidates(self, values_list, report):
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
    
    
    def findCandidatePlates(self, projection_list, report):
        blur_list = self.applyBlur(projection_list, 0.05)

        threshold = self.math.calculateAvarage(projection_list)

        candidate_list = []
        sensibility = 1

        while not candidate_list or sensibility==0:
            sensibility -= 0.1
            threshold_list = self.applyThreshold(blur_list, threshold*sensibility)
            candidate_list = []            
            candidate_list = self.locateCandidates(threshold_list, report)
            report.write("sens: %s\tCandidate List  %s\n"%(str(sensibility),str(candidate_list)))
            if candidate_list:
                for elem in candidate_list:
                    if elem[1] - elem[0] > len(projection_list)*0.6 \
                    or elem[1] - elem[0] < len(projection_list)*0.2:
                        report.write("elem rem: %s\n"%str(elem))
                        candidate_list.remove(elem)
                        report.write("New cand: %s\n"%(str(candidate_list)))
        
        report.write("Candidate Plate: %s\n"%str(candidate_list))
        Graphics.generateGraph(report.path_save, report.car_image.file_name[:-4]+"_Plate_Thresh.png",\
                               threshold_list)        
        Graphics.generateGraph(report.path_save, report.car_image.file_name[:-4]+"_Proj_horiz.png",\
                               projection_list)

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
    

class PlateDetected(object):
    
    def locatePlate(self, report):
        try:
            file_name = report.car_image.file_name
            path_load = report.car_image.path_load
            path_save = report.car_image.path_save
            
            print "File: %s" % file_name
            report.write("File: %s\n" % file_name)
            report.write("Band detector\n")
        
            image = Image.Image(os.path.join(path_load, file_name))
            image.save(os.path.join(path_save, file_name))
        
            verticalFilteredImage = image.applyFilter(Image.VERTICAL_EDGE_DETECTED)
            grayscaleFilteredImage = verticalFilteredImage.convertRgbToGrayscale()
        
            image_math = Math.ImageMath()
            math = Math.Math()
            new_matrix = math.calculateTranspose(grayscaleFilteredImage.matrix_image)
            verticalProjection = image_math.calculateProjection2(new_matrix)
            verticalProjection = [0,0]+verticalProjection[2:][:-2]+[0,0]
        
            regionDetected = RegionDetected()
            inf_band, sup_band = regionDetected.calculateRegion\
                     (verticalProjection, 0.55, report)
        
            bbox = (0, inf_band, image.size[0], sup_band)
            #print "BBox:  %s"%str(bbox)
            report.write("BBox: %s\n"%str(bbox))
        
            band = image.crop(bbox)
            band.save(os.path.join(path_save, file_name[:-4]+"_band.jpg"))
        
            report.write("Plate detector\n")
            filteredBand = band.fullEdgeDetection()
            grayscaleFilteredBand = filteredBand.convertRgbToGrayscale()
        
        
            horizontalProjection = image_math.calculateProjection2\
                       (grayscaleFilteredBand.matrix_image)
        
            inf_Plate, sup_Plate = regionDetected.findCandidatePlates\
                       (horizontalProjection, report)
        
            if sup_Plate == 0:
                sup_Plate = image.size[0]
        
            bbox = (inf_Plate, inf_band, sup_Plate, sup_band)
            #print "BBox: %s\n"%str(bbox)
            report.write("BBox: %s\n\n"%str(bbox))
        
            band = image.crop(bbox)
            band.save(os.path.join(path_save, file_name[:-4]+"_plate.jpg"))
            del(image, verticalFilteredImage, grayscaleFilteredImage, image_math, bbox, band,new_matrix)
            del(verticalProjection, regionDetected, filteredBand, grayscaleFilteredBand, horizontalProjection)
        except:
            pass
