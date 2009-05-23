# XXX: Add copyright
import os
import horus.featureExtraction as FeatureExtraction
from PIL import Image as PilImage
import horus.image as Image

import report as Report

def binarizeImage(path):
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
    charPath = os.path.join(abspath,"characters/t.PNG")
    """
        Imagens do paint nao sao binarias 0 ou 255,
        se a imagem for gerada pelo paint, descomente a linha de baixo     
    """
#    binarizeImage(charPath)    
    image = Image.Image(None, charPath)
    FeatureExtraction.hildtchSkeletonize(image)
    image.save(os.path.join(abspath,"characters/skeletonizedChar.PNG"))
