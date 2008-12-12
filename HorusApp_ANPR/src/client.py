import os
import platedetected as PlateDetected

import report as Report

if __name__ == "__main__":
    plate_detected = PlateDetected.PlateDetected()
    
    abspath = os.path.abspath('..')
    path_load = os.path.join(abspath,"imagens")
    path_save = os.path.join(abspath,"placas")
    file_list = os.listdir(path_load)
    file_list.sort()
    
    import pdb; pdb.set_trace()
    for file_name in file_list[1:][:5]:
        car_image = Report.CarImage(file_name, path_load, path_save)
        report = Report.Report(path_save, car_image) 
        
        plate_detected.locatePlate(report)