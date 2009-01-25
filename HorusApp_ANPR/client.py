# -*- coding: utf-8 -*-

import os

import platedetected
import report as Report

if __name__ == "__main__":
    
    abspath = os.path.abspath('.')
    path_load = os.path.join(abspath,"imagens")
    path_save = os.path.join(abspath,"placa")
    file_list = os.listdir(path_load)
    file_list.sort()
    
    for file_name in file_list[68:][:1]:
        #try:
            car_image = Report.CarImage(file_name, path_load, path_save)
            report = Report.Report(path_save, car_image) 
            plate_detected = platedetected.Plate(report)
            plate = plate_detected.plateDetect()
            characters = platedetected.Characters(plate, report)
            characters.preProcessing()
            print "END!!"
        #except:
            pass
