import os
import horus.featureExtraction as FeatureExtraction
from PIL import Image as PilImage
import horus.image as Image

import report as Report

if __name__ == "__main__":
    abspath = os.path.abspath('.')
    image = PilImage.open(os.path.join(abspath,"characters/t.JPG"))
    image = Image.Image(None, os.path.join(abspath,"characters/t.JPG"))
    image = FeatureExtraction.skeletonize(image)
    image.save(os.path.join(abspath,"characters/skeletonizedChar2.JPG"))
