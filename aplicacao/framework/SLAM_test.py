import unittest
from SLAM import *

class SlamTest(unittest.TestCase):

    def test_biggerDictionaryKey(self):
        slam_obj = Slam()
        laser_dic= {'180':28, '170':8, '160':44}
        slam_obj.biggerDictionaryKey(laser_dic)
        bigger_value = slam_obj.bigger_value
        bigger_key = slam_obj.bigger_key
        #test bigger value calculation
        self.assertEqual(44, bigger_value)
        #test bigger key calculation
        self.assertEqual('160', bigger_key)

    def test_landmarkUpdate(self):
        slam_obj = Slam()
        slam_obj.landmarkUpdate('+30', 45)
        slam_obj.landmarkUpdate('-30', 90)
        slam_obj.landmarkUpdate('0', 5)
        self.assertEqual(45, slam_obj.landmark_dic['+30'])
        self.assertEqual(90, slam_obj.landmark_dic['-30'])
        self.assertEqual(5, slam_obj.landmark_dic['0'])

def main():
    unittest.main()

if __name__ == '__main__':
    main()

        