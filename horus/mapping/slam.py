from horus.core.math.math_module import Trigonometry,  LinearRegression
from ransac import *
from landmark import *

class Slam():

    def __init__(self):
        self.robot_rotation = 0
        self.infinity_point = 110
        self.bigger_key = None
        self.bigger_value = None
        self.laser_dic = {}
        self.trigonometry_obj = Trigonometry()
        self.extraction_obj = Ransac()
        self.landmark_list = []
        self.circuference_radius = 300
        self.mark_point_list = [(0, 0)]
        
    def biggerDictionaryKey(self, dictionary):
        """ gets bigger key in dictionary """
        #bigger value calculation
        self.bigger_value = max(dictionary.values())
        #bigger key calculation
        self.bigger_key = [key for key in dictionary.iterkeys() if 
                            dictionary[key] == self.bigger_value]
        self.bigger_key = self.bigger_key.pop()

        return self.bigger_key
    
#-------------------------------------
#self.slam_obj.landmarkExtraction
#-------------------------------------

    def startAutomaticWalk():
        pass

    def stopAutomaticWalk():
        pass

    def laserUpdate(self, key, value):
        self.laser_dic[key] = value
    
    def createCollisionTuple(self, angle, position_tuple):
        """
            creates a collision list using mathematical 
            calculations of rectangle triangle
        """
        hypotenuse = self.laser_dic[angle]
        angle = float(angle)
        #note: position_tuple parameter is robot`s (x, y)
        x = position_tuple[0] + self.trigonometry_obj.getXCateto(hypotenuse, angle)
        y = position_tuple[1] + self.trigonometry_obj.getYCateto(hypotenuse, angle)
        x = round(x,1)
        y = round(y,1)
        tuple = (x, y)
#        if tuple not in self.collision_graph and hypotenuse != self.infinity_point:
#            self.collision_graph.append(tuple)
        return tuple
        
        
    def landmarkExtraction(self, robot_position):
        """ builds a landmark graph """
        
        collision_list = []
        for key in self.laser_dic.iterkeys():
            tuple = self.createCollisionTuple(key, robot_position)
            collision_list.append(tuple)
        
        try:
            oid = self.landmark_list.__len__()
            landmark = self.extraction_obj.getBestFitModel(collision_list,  oid)
            self.landmark_list.append(landmark)
        except:
            print 'curve not found!'
            pass

    def getRobotPosition(self, walk_distance, rotation, position):
    
        """ 
            calculates X, Y position based on robot`s coordnates
            angle must be in degrees
        """
        rotation = rotation % 360
        x = position[0] + self.trigonometry_obj.getXCateto(walk_distance, rotation)
        y = position[1] + self.trigonometry_obj.getYCateto(walk_distance, rotation)
        x = round(x, 1)
        y = round(y, 1)
        
        return (x , y)
        
    def createMarkPoint(self, robot_position):
        """
            target_point is the (X, Y) witch this method will test before create a MarkPoint 
            MarkPoint is a circuference in the ground where the robot has passed by
        """   
        for mark_point in self.mark_point_list:
            result = self.trigonometry_obj.isPointInCircle(mark_point, robot_position,  self.circuference_radius)
            if (result is False):
                self.mark_point_list.append(robot_position)
                break

#---------------------------------------------------------------------        
# verifying this
#   def linearRegression(self):
#      """ overrides linear regression from LinearRegression module """ 
#       lr = LinearRegression(self.collision_graph)
#        return lr
#---------------------------------------------------------------------    

    def dataAssociation(self, last_position, distance_traveled, rotantion_angle):
        """ based on triangulation """
        pass
