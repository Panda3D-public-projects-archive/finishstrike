import unittest
from horus.mapping.slam import Slam
from horus.mapping.ransac import *
from horus.core.math.math_module import Trigonometry,  LinearRegression

class SlamTest(unittest.TestCase):
    
    def setUp(self):
        self.robot_rotation = 0
        self.infinity_point = 110
        self.bigger_key = +30
        self.bigger_value = 30
        self.laser_dic = {'+30': 30,  '+25': 25,  '+20': 20,  '+15': 15, '+0': 10,  '+5': 5,  '0':0}
        self.trigonometry_obj = Trigonometry()
        self.extraction_obj = Ransac()
        self.landmark_list = []
        self.mark_point_list = []
                

    def test_biggerDictionaryKey(self):
        dictionary = self.laser_dic
        self.bigger_value = max(dictionary.values())
        self.bigger_key = [key for key in dictionary.iterkeys() if 
                            dictionary[key] == self.bigger_value]
        self.bigger_key = self.bigger_key.pop()

        self.assertEqual(self.bigger_key, '+30')
        
    def test_laserUpdate(self):
        key = '+13'
        value = 13
        self.laser_dic[key] = value
        self.assertEqual(self.laser_dic['+13'], 13)
        
    def test_createCollisionTuple(self):
        robot_position = (0,  0)
        angle = '+30'
        #(0, 0)
        position_tuple = robot_position
        hypotenuse = self.laser_dic[angle]
        angle = float(angle)
        # 0 + cos(30) * 30 ~= 26.0
        x = position_tuple[0] + self.trigonometry_obj.getXCateto(hypotenuse, angle) 
        # 0 + sin(30) * 30 = 15
        y = position_tuple[1] + self.trigonometry_obj.getYCateto(hypotenuse, angle)
        x = round(x,1)
        y = round(y,1)
        tuple = (x, y)
        self.assertAlmostEqual(x, 26.0)
        self.assertEqual(y, 15 )
        
    def test_createMarkPoint(self):
        self.circuference_radius = 10
        robot_position = (0,  0)
        self.mark_point_list = [(2,  3),  (21,  20)]
        
        for mark_point in self.mark_point_list:
            result = self.trigonometry_obj.isPointInCircle(mark_point, robot_position, self.circuference_radius)
            if (result is False):
                self.mark_point_list.append(robot_position)
                break
        
        length = len(self.mark_point_list)
        self.assertTrue(length==3)
        
        self.mark_point_list = [(21,  20)]
        self.circuference_radius = 7
        robot_position = (0,  0)
        for mark_point in self.mark_point_list:
            result = self.trigonometry_obj.isPointInCircle(mark_point, robot_position, self.circuference_radius)
            if (result is False):
                self.mark_point_list.append(robot_position)
                break
        length = len(self.mark_point_list)
        self.assertTrue(length==2)
        
        
        self.mark_point_list = [(0,  6)]
        self.circuference_radius = 7
        robot_position = (0,  0)
        for mark_point in self.mark_point_list:
            result = self.trigonometry_obj.isPointInCircle(mark_point, robot_position, self.circuference_radius)
            if (result is False):
                self.mark_point_list.append(robot_position)
                break
        length = len(self.mark_point_list)
        self.assertTrue(length==1)
        
    def test_landmarkExtraction(self):
        def createCollisionTuple(angle, position_tuple):

            hypotenuse = self.laser_dic[angle]
            angle = float(angle)
            #note: position_tuple parameter is robot`s (x, y)
            x = position_tuple[0] + self.trigonometry_obj.getXCateto(hypotenuse, angle)
            y = position_tuple[1] + self.trigonometry_obj.getYCateto(hypotenuse, angle)
            x = round(x,1)
            y = round(y,1)
            tuple = (x, y)
            return tuple
        
        slam = Slam()
        robot_position = (0, 0)
        collision_list = []
        for key in self.laser_dic.iterkeys():
            tuple = createCollisionTuple(key, robot_position)
            collision_list.append(tuple)
        
        try:
            oid = len(self.landmark_list)
            landmark = self.extraction_obj.getBestFitModel(collision_list,  oid)
            self.landmark_list.append(landmark)
            
        except:
            print 'curve not found!'
            pass
        
        
    
if __name__ == '__main__':
    unittest.main()
