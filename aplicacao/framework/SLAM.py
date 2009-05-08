from math_module import *

class Slam():

    def __init__(self):
        self.infinity_point = 9999
        self.bigger_key = None
        self.bigger_value = None
        self.landmark_dic = {}
        # this is a list of tuples like [(x1,y1),...,(xn,yn)]
        self.landmark_graph = []
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
     
    def createLandmarkGraph(self, angle):
        """ creates a landmark Graph using mathematical 
            calculations of rectangle triangle
        """
        hypotenuse = self.landmark_dic[angle]
        angle = float(angle)
        x = self.trigonometry_obj.getXCateto(hypotenuse, angle)
        y = self.trigonometry_obj.getYCateto(hypotenuse, angle)
        tuple = (x, y)
        if tuple not in self.landmark_graph and hypotenuse != self.infinity_point:
            self.landmark_graph.append(tuple)

