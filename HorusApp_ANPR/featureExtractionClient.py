import os
import featureExtraction as FeatureExtraction
from PIL import Image as PilImage
import image as Image

import report as Report

if __name__ == "__main__":
    abspath = os.path.abspath('..')
    image = PilImage.open(os.path.join(abspath,
                                     "HorusAPP_ANPR/characters/s.JPG"))
    image = image.convert("L")
    for i in range(image.size[0]):
        for j in range(image.size[1]):            
            if(image.getpixel((i,j)) < 128):
                image.putpixel((i,j), 0)
            else:
                image.putpixel((i,j), 255)    
    image.save(os.path.join(abspath,
                                     "HorusAPP_ANPR/characters/s.JPG"))
    
    image = Image.Image(None, os.path.join(abspath,
                                     "HorusAPP_ANPR/characters/s.JPG"))    
    print FeatureExtraction.extractFeatureByEdgeDetection(image)