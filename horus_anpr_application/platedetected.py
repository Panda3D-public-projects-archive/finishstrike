# -*- coding: utf-8 -*-

import os

import horus.graphics as Graphics
import horus.mathematic as ath
import horus.image as Image

class RegionDetected(object):

    def calculatePeak(self, projection):
        """
            This method return de maximum value in projection list
            
            PS: the extremes values of projection's list are very high, 
                because the projection is based in edge detection and 
                there are a edge in images border
        """
        projection = ath.List([0,0]+projection[2:][:-2]+[0,0])
        return projection.maxValue()


    def calculateRegion(self, projection_list, cut_sensibility, report):
        """
            TODO
        """   
        peak = projection_list.index(self.calculatePeak(projection_list))
        
        blur_list = projection_list.applyBlur(0.07)
        threshold = projection_list.calculateAvarage()

        #TODO: melhorar essa escolha
        candidate_list = []
        sensibility = 1
        while not candidate_list or sensibility==0:
            sensibility -= 0.1
            threshold_list = blur_list.applyThreshold(threshold*sensibility)
            candidate_list = []    
            candidate_list = self.locateCandidates(threshold_list, report)
            report.write("sens: %s\tCandidate List  %s\n"%(str(sensibility),str(candidate_list)))
            if candidate_list:
                for elem in candidate_list:
                    if elem[1] - elem[0] > len(projection_list)*0.6 \
                    or elem[1] - elem[0] < len(projection_list)*0.3:
                        candidate_list.remove(elem)

#        Graphics.generateGraph( report.path_save, 
#                       report.car_image.file_name[:-4]+"_Band_Thresh.png", 
#                       threshold_list, 
#                       ( [peak],[ projection_list[peak] ] )       )
#        
#        
#        Graphics.generateGraph(report.path_save, 
#                       report.car_image.file_name[:-4]+"_Proj_Vert.png", 
#                       projection_list, 
#                       ( [peak], [ projection_list[peak] ] )     )
        
        inf_list = [ i for i in range( len(projection_list) )[:peak] 
                 if projection_list[i]<= cut_sensibility*projection_list[peak] ]
        sup_list = [ i for i in range( len(projection_list) )[peak:]  
                 if projection_list[i]<= cut_sensibility*projection_list[peak] ]
        
        
        interval = (inf_list[-1], sup_list[0])
        
        del(blur_list, threshold_list, candidate_list, inf_list, sup_list)
        
        return interval
    
    # descobrir porque descarta automaticamente os intervalos extremos
    # isso costuma ser util, mas pode haver algum momento que os extremos sejam importantes
    def locateCandidates(self, values_list, report):
        candidate_list = []
        inf = 0

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
                        candidate_list.append( (inf, i) )
                        inf = 0
        report.write("Candidate List  %s\n"%str(candidate_list))
        return candidate_list        
    
    
    def findCandidatePlates(self, projection_list, report):
        blur_list = projection_list.applyBlur(0.05)
        threshold = projection_list.calculateAvarage()

        #TODO: melhorar algoritmo
        candidate_list = []
        sensibility = 1
        while not candidate_list or sensibility==0:
            sensibility -= 0.1
            threshold_list = blur_list.applyThreshold(threshold*sensibility)
            candidate_list = []            
            candidate_list = self.locateCandidates(threshold_list, report)
            report.write("sens: %s\tCandidate List  %s\n"%(str(sensibility),str(candidate_list)))
            if candidate_list:
                for elem in candidate_list:
                    # Estes parametros foram calculados empiricamente
                    # Em outras palavras: chute...
                    if elem[1] - elem[0] > len(projection_list)*0.6 \
                    or elem[1] - elem[0] < len(projection_list)*0.2:
                        report.write("elem rem: %s\n"%str(elem))
                        candidate_list.remove(elem)
                        report.write("New cand: %s\n"%(str(candidate_list)))
        
        report.write("Candidate Plate: %s\n"%str(candidate_list))
#        Graphics.generateGraph( report.path_save, 
#                    report.car_image.file_name[:-4]+"_Plate_Thresh.png",
#                    threshold_list )        
#        Graphics.generateGraph( report.path_save, 
#                     report.car_image.file_name[:-4]+"_Proj_horiz.png",
#                     projection_list )

        # Escolhe o maior intervalo dentre os candidatos
        inf = sup = lenght = 0
        for elem in candidate_list:
            lenght_elem = elem[1] - elem[0]
            if lenght_elem > lenght:
                lenght = lenght_elem
                inf = elem[0]
                sup = elem[1]

        if sup == projection_list[-1] or inf == projection_list[-1]:
            report.write("inf e sup ultimos: (%s, %s)\n" % (str(inf),str(sup)) )
        
        report.write( "inf e sup: (%s, %s)\n" % (str(inf),str(sup)) )
        
        del(blur_list, threshold_list, candidate_list)

        return inf, sup   
    
class Plate(object):
    
    def __init__(self, report):
        self.report = report
       
        self.file_name = report.car_image.file_name
        self.path_load = report.car_image.path_load
        self.path_save = report.car_image.path_save
        
        self.image = Image.Image(path = os.path.join(self.path_load, self.file_name))
        self.processing = Image.ProcessingImage(self.image)
        
        self.regionDetected = RegionDetected()
        
        print "File: %s" % self.file_name
        self.report.write("File: %s\n" % self.file_name)
        
        self.band = None

        
    def locateBand(self):
        self.report.write("Band detector\n")

        self.image.save( os.path.join(self.path_save, self.file_name) )

        verticalFilteredImage = self.processing.applyFilter(
                                                  Image.VERTICAL_EDGE_DETECTED )
        grayscaleFilteredImage = Image.ProcessingImage( 
                                 verticalFilteredImage ).convertRgbToGrayscale()

        verticalProjection = Image.ProcessingImage( 
                                 grayscaleFilteredImage ).verticalProjection()

        
        inf_band, sup_band = self.regionDetected.calculateRegion( 
                                  verticalProjection, 0.55, self.report )

        self.bbox = (0, inf_band, self.image.size[0], sup_band)
        self.report.write("BBox: %s\n"%str(self.bbox))

        self.band = self.image.crop(self.bbox)
#        self.band.save( os.path.join( self.path_save, 
#                                      self.file_name[:-4] + "_band.jpg") )

        del(verticalFilteredImage, grayscaleFilteredImage, verticalProjection)
    
        return self.band
    
    def locatePlate(self):        
        self.report.write("Plate detector\n")

        filteredBand = Image.ProcessingImage( self.band ).fullEdgeDetection()
        grayscaleFilteredBand = Image.ProcessingImage( 
                                     filteredBand ).convertRgbToGrayscale()
    
        horizontalProjection = Image.ProcessingImage(
                                  grayscaleFilteredBand ).horizontalProjection()

        inf_Plate, sup_Plate = self.regionDetected.findCandidatePlates( 
                                             horizontalProjection, self.report )
    
        if sup_Plate == 0:
            sup_Plate = image.size[0]
    
        self.bbox = (inf_Plate, self.bbox[1], sup_Plate, self.bbox[3])
        self.report.write( "BBox: %s\n\n" % str( self.bbox ) )
    
        plate = self.image.crop(self.bbox)
        plate.save( os.path.join( self.path_save, self.file_name[:-4] + "_plate.jpg" ) )

        del(filteredBand, grayscaleFilteredBand, horizontalProjection)

        return plate

    def plateDetect(self):
        self.locateBand()
        return self.locatePlate()
        
        
class Characters(object):
    """
        After locate a region which containing the plate is necessary to divide 
        it to obtain the images with characters.
    """
    
    def __init__(self, plate, report):
        self.report = report
       
        self.file_name = report.car_image.file_name
        self.path_load = report.car_image.path_load  
        self.path_save = report.car_image.path_save

        self.plate = plate
        
        
    def preProcessing(self):
        gs_plate = Image.ProcessingImage(self.plate).convertRgbToGrayscale()
        gs_plate.save(os.path.join( self.path_save, self.file_name[:-4] + "_GS_plate.jpg" ))
        projection = Image.ProcessingImage(gs_plate).horizontalProjection()

#        Graphics.generateGraph( self.path_save,
#                                self.file_name[:-4]+"_Proj_horiz.png",
#                                projection )        
#        
        avarage = projection.calculateAvarage()
        projection = projection.applyThreshold(avarage)
#        Graphics.generateGraph( self.path_save,
#                                self.file_name[:-4]+"_cut_horiz.png",
#                                projection )

        intervals =  RegionDetected().locateCandidates(projection, self.report)

        peaks = ath.List()
        for interval in intervals:
            lenght = interval[1] - interval[0]
            inter = ath.List(projection[interval[0]:][:lenght])
            peaks.append(interval[0] + inter.index(inter.maxValue()))
        
        print peaks
        for i in range(len(peaks) - 1):
            char = self.plate.crop((peaks[i], 0, peaks[i+1], self.plate.size[1]))
            char.save( os.path.join( self.path_save, "char%d.jpg"%i ) )

            
