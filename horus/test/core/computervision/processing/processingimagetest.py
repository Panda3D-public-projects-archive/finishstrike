'''
Created on 08/05/2009

@author: thiagorinu
'''
import horus.core.computervision.processing.processingimage as processingimage
import os
import unittest
import horus.core.computervision.image as image
class ProcessingImageTest(unittest.TestCase):
    def setUp(self):
        abspath = os.path.abspath('..')
        self.imagePath = os.path.join(abspath,"testImages/image_test.png")                
        self.test_image = image.Image(self.imagePath)
    
    def test_fullEdgeDetection(self):
        filtered_img = processingimage.fullEdgeDetection(self.test_image)        
        assert None != filtered_img, list(filtered_img.getdata())
    
    def test_projection(self):
        input_matrix = [[0,1,1,0],
                        [2,3,4,0],
                        [0,0,0,1]]
        expected_output = [2,9,1]
        
        result_list = processingimage.projection(input_matrix)
        assert result_list == expected_output, result_list
    
    def test_verticalProjection(self):
        result_list = processingimage.verticalProjection(self.test_image)
        print result_list
        assert result_list != None
    
    def test_horizontalProjection(self):
        result_list = processingimage.horizontalProjection(self.test_image)
        print result_list
        assert result_list != None
    
    def test_highlightLuminance(self):        
        image = processingimage.highlightLuminance(self.test_image)
        assert None != image
    
    def test_hildtchSkeletonize(self):
        abspath = os.path.abspath('..')
        imagePath = os.path.join(abspath,"testImages/skeletonization_test_img.png")                
        sktestimage = image.Image(imagePath)
        
        expected_output = [255, 255, 255, 255, 255, 255, 255, 255, 
                           255, 255, 255, 255, 255, 255, 255, 255, 
                           0, 255, 255, 255, 255, 0, 255, 255, 255,
                           255, 0, 255, 255, 255, 255, 255, 0, 255,
                           255, 255, 255, 255, 255, 255, 255, 255,
                           255, 255, 255]
         
        result_img = processingimage.hildtchSkeletonize(sktestimage)
        
        assert list(result_img.getdata()) == expected_output, \
                list(result_img.getdata()) 