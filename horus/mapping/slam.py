from horus.core.math.math_module import Trigonometry,  LinearRegression
from ransac import *
from landmark import *

class Slam():

    def __init__(self):
        self.robot_rotation = 0
        self.infinity_point = 150
        self.bigger_key = None
        self.bigger_value = None
        self.laser_dic = {}
        self.trigonometry_obj = Trigonometry()
        self.extraction_obj = Ransac()
        self.landmark_list = []
        self.circuference_radius = 45
        self.mark_point_list = [(0, 0)]
        #max try number before stop searching mark points
        self.max_point_try = 5
        
        self.graph_dic = {}
        
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
            #print 'curve not found!'
            pass

    def getRobotPosition(self, walk_distance, rotation, position):
    
        """ 
            calculates X, Y position based on robot`s coordnates
            angle must be in degrees
        """
        rotation = rotation % 360
        print "Walk distance "+ str(walk_distance )+"  Rotation "+ str(rotation )+ " Position " + str(position)
        x = position[0] + self.trigonometry_obj.getXCateto(walk_distance, rotation)
        y = position[1] + self.trigonometry_obj.getYCateto(walk_distance, rotation)
        x = round(x)
        y = round(y)
        return (x , y)
        
    def tryAMarkPoint(self, robot_position,  robot_rotation):
        """
            target_point is the (X, Y) witch this method will test before create a MarkPoint 
            MarkPoint is a circuference in the ground where the robot has passed by
        """   
        append_condition = False
        for mark_point in self.mark_point_list:
            result = self.trigonometry_obj.isPointInCircle(mark_point, robot_position,  self.circuference_radius)
            if (result is False):
                append_condition = True
            else:
                self.max_point_try = self.max_point_try - 1
        if append_condition:
            self.max_point_try += 2
            self.mark_point_list.append(robot_position) 
            
            #buiding graph
            index = len(self.graph_dic)
            self.graph_dic[index] = robot_position,  robot_rotation
            
        return self.max_point_try
    
    def isPointInMarkPointList(self, point):
        """
            Returns True if point is in mark_point_list, else returns False.
        """

        for mark_point in self.mark_point_list:
            result = self.trigonometry_obj.isPointInCircle(mark_point, point,  self.circuference_radius)
            if (result is False):
                condition = True
            else:
                condition = False
        return condition


    def dataAssociation(self, last_position, distance_traveled, rotantion_angle):
        """ based on triangulation """
        pass
