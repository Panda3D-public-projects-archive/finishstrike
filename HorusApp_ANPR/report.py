import os

class CarImage(object):
    def __init__(self, file_name, path_load, path_save):
        self.file_name = file_name
        self.path_load = path_load
        self.path_save = path_save

class Report(object):
    def __init__(self, path_save, car_image):
        self.path_save = path_save
        file_name = os.path.join( path_save, "report"+car_image.file_name )[:-4]
        self.file_report = open( file_name, "w+")
        self.car_image = car_image
        
    def write(self, content):
        self.file_report.write(content)
        
    def __del__(self):
        self.file_report.close()

