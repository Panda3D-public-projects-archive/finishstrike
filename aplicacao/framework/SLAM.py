from math_module import *

class Slam():

    def __init__(self):
        self.infinity_point = 9999
        self.bigger_key = None
        self.bigger_value = None
        self.landmark_dic = {}
        self.projection = ()
        # this is a list of tuples like [(x1,y1),...,(xn,yn)]
        self.collision_graph = []
        self.trigonometry_obj = Trigonometry()
    def biggerDictionaryKey(self, dictionary):
        """ gets bigger key in dictionary """
        #bigger value calculation
        self.bigger_value = max(dictionary.values())
        #bigger key calculation
        self.bigger_key = [key for key in dictionary.iterkeys() if 
                            dictionary[key] == self.bigger_value]
        self.bigger_key = self.bigger_key.pop()

        return self.bigger_key

    #abstractmethod
    def startAutomaticWalk():
        pass

    #abstractmethod
    def stopAutomaticWalk():
        pass

    def landmarkUpdate(self, key, value):
        self.landmark_dic[key] = value
    
    def doProjection(self, rotation, robotX, robotY):
        #fazer calculo de projecao para o angulo X e Y
        self.projection = (rotation % 360, robotX, robotY)

    def createLandmarkGraph(self, robot, angle, position_tuple):
        """
            creates a landmark Graph using mathematical 
            calculations of rectangle triangle
        """
        #note: position_tuple parameter is robot`s (x, y)
        hypotenuse = self.landmark_dic[angle]
        angle = float(angle)
        x = position_tuple[0] + self.trigonometry_obj.getXCateto(hypotenuse, angle)
        y = position_tuple[1] + self.trigonometry_obj.getYCateto(hypotenuse, angle)
        tuple = (x, y)
        if tuple not in self.collision_graph and hypotenuse != self.infinity_point:
            self.collision_graph.append(tuple)
        
        
    def getRobotPosition(self, walk_distance, angle):
        """ calculates X, Y position based on robot`s coordnates """

        x = self.trigonometry_obj.getXCateto(walk_distance, angle)
        y = self.trigonometry_obj.getYCateto(walk_distance, angle)
        return (x , y)
        
    def linearRegression(self):
        """ overrides linear regression from LinearRegression module """ 
        lr = LinearRegression(self.collision_graph)
        return lr
    
    def dataAssociation(self, last_position, distance_traveled, rotantion_angle):
        """ based on triangulation """
        pass