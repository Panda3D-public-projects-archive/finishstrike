from horus.core.math.math_module import Trigonometry,  LinearRegression
from ransac import *
from landmark import *

class Slam():

    def __init__(self,  infinity_point=150,  circuference_radius=30):
        self.quadrant_dic = {'1': [], '2': [], '3': [], '4': [],  '0': []  }
        self.robot_rotation = 0
        self.infinity_point = infinity_point
        self.bigger_key = None
        self.bigger_value = None
        self.laser_dic = {}
        self.trigonometry_obj = Trigonometry()
        self.extraction_obj = Ransac()
        self.landmark_list = []
        self.circuference_radius = circuference_radius
        self.mark_point_list = [(0, 0)]
        #max try number before stop earching mark points
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
    
    def seeFarthestPoint(self,  actual_robot_rotation=0):
        """ returns farthest laser direction """
        
        actualH = actual_robot_rotation
        new_h = self.biggerDictionaryKey(self.laser_dic)
        if self.laser_dic[new_h] <= 6:
            new_h = float(new_h) - 180
        rotation = float(new_h)
        finalH = actualH + rotation
        return new_h
        
    def seeNewWay(self,  actual_robot_rotation=0):
        """ see a new way to walk """
        
        actualH = actual_robot_rotation
        catetoX = lambda angle: math.cos(math.radians(angle))*hyp
        catetoY = lambda angle: math.sin(math.radians(angle))*hyp
        right_dic = {}
        left_dic = {}
        left_count = 0
        right_count = 0
       
        for  key in self.laser_dic.keys():
            
            if float(key) < 0.0:
                left_dic[key] = self.laser_dic[key]
                hyp = left_dic[key]
                angle = float(key)
                x = catetoX(angle)
                y = catetoY(angle)
                coordLaser = (x, y)
                if self.isPointInMarkPointList(coordLaser):
                    left_count += 1
            elif float(key) > 0.0:
                right_dic[key] = self.laser_dic[key]
                hyp = right_dic[key]
                angle = float(key)
                x = catetoX(angle)
                y = catetoY(angle)
                coordLaser = (x, y)
                if self.isPointInMarkPointList(coordLaser):
                    right_count += 1
                
        if left_count < right_count:
            new_h = self.biggerDictionaryKey(left_dic)
        elif right_count > left_count:
            new_h = self.biggerDictionaryKey(right_dic)
        else:
            new_h = self.seeFarthestPoint(actualH)
        
        rotation = float(new_h)     
        finalH = actualH + rotation
        
        return finalH

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

    def pointsByQuadrants(self, center_tuple):
        """
        
        """
        for mark_point in self.mark_point_list:
            if whatQuadrant(center_tuple, mark_point) == '1': self.quadrant_dic['1'].append(mark_point)
            elif whatQuadrant(center_tuple, mark_point) == '2': self.quadrant_dic['2'].append(mark_point)
            elif whatQuadrant(center_tuple, mark_point) == '3': self.quadrant_dic['3'].append(mark_point)
            elif whatQuadrant(center_tuple, mark_point) == '4': self.quadrant_dic['4'].append(mark_point)
            else: self.quadrant_dic['0'].append(mark_point)
    
    def dataAssociation(self, last_position, distance_traveled, rotantion_angle):
        """ based on triangulation """
        pass
