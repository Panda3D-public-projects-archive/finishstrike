import unittest
from SLAM import *
from math_module import *

class SlamTest(unittest.TestCase):

    def test_biggerDictionaryKey(self):
        slam_obj = Slam()
        laser_dic= {'180':28, '170':8, '160':44}
        slam_obj.biggerDictionaryKey(laser_dic)
        bigger_value = slam_obj.bigger_value
        bigger_key = slam_obj.bigger_key
        #------------------------------------
        #test bigger value calculation
        self.assertEqual(44, bigger_value)
        #test bigger key calculation
        self.assertEqual('160', bigger_key)
        #------------------------------------
        
    def test_landmarkUpdate(self):
        slam_obj = Slam()
        slam_obj.landmarkUpdate('+30', 45)
        slam_obj.landmarkUpdate('-30', 90)
        slam_obj.landmarkUpdate('0', 5)
        self.assertEqual(45, slam_obj.landmark_dic['+30'])
        self.assertEqual(90, slam_obj.landmark_dic['-30'])
        self.assertEqual(5, slam_obj.landmark_dic['0'])
        
    def test_createLandmarkGraph(self):
        slam_obj = Slam()
        slam_obj.landmarkUpdate('+30', 45)
        slam_obj.landmarkUpdate('-30', 90)
        slam_obj.landmarkUpdate('0', slam_obj.infinity_point)
        
        slam_obj.createLandmarkGraph('+30')
        slam_obj.createLandmarkGraph('-30')
        tuple_test = slam_obj.landmark_graph
        #-----------------------------------
        #it cannot go to the landmark_graph because key '0' has a infinity value
        slam_obj.createLandmarkGraph('0')
        #-----------------------------------
        self.assertEqual(slam_obj.landmark_graph, tuple_test)
    
    def test_linearRegession(self):
        slam_obj = Slam()
        slam_obj.landmarkUpdate('+30', 45)
        slam_obj.landmarkUpdate('-30', 90)
        slam_obj.landmarkUpdate('0', 94)
        slam_obj.createLandmarkGraph('+30')
        slam_obj.createLandmarkGraph('-30')
        slam_obj.createLandmarkGraph('0')
        lr = slam_obj.linearRegression()
        print lr.getAlpha()
        print lr.getBeta()
        print lr.getError()

def main():
    unittest.main()

if __name__ == '__main__':
    main()

        