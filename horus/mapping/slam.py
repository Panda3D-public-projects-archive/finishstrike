from horus.core.math.math_module import *
from ransac import *
from landmark import *

class Slam():

    def __init__(self):
        self.robot_rotation = 0
        self.infinity_point = 110
        self.bigger_key = None
        self.bigger_value = None
        self.laser_dic = {}
        self.projection = ()
        # this is a list of tuples like [(x1,y1),...,(xn,yn)]
        self.collision_graph = []
        self.trigonometry_obj = Trigonometry()
        self.extraction_obj = Ransac()
        self.landmark_list = []
        
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

    #abstractmethod
    def startAutomaticWalk():
        pass

    #abstractmethod
    def stopAutomaticWalk():
        pass

    def laserUpdate(self, key, value):
        self.laser_dic[key] = value
    
    def createCollisionList(self, angle, position_tuple):
        """
            creates a landmark Graph using mathematical 
            calculations of rectangle triangle
        """
        #note: position_tuple parameter is robot`s (x, y)
        hypotenuse = self.laser_dic[angle]
        angle = float(angle)
        x = position_tuple[0] + self.trigonometry_obj.getXCateto(hypotenuse, angle)
        y = position_tuple[1] + self.trigonometry_obj.getYCateto(hypotenuse, angle)
        x = round(x,1)
        y = round(y,1)
        tuple = (x, y)
        if tuple not in self.collision_graph and hypotenuse != self.infinity_point:
            self.collision_graph.append(tuple)
        return tuple
        
        
    def landmarkExtraction(self, robot_position):
        """ builds a landmark graph """
        
        collision_list = []
        for key in self.laser_dic.iterkeys():
            tuple = self.createCollisionList(key, robot_position)
            collision_list.append(tuple)

        model = self.extraction_obj.getBestFitModel(collision_list)

        if model is not None:
            oid = self.landmark_list.__len__()
            landmark = Landmark(oid, model)
            self.landmark_list.append(landmark)
        else:
            print "model e none"
        
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
