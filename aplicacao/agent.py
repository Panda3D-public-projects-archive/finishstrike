from pandac.PandaModules import *
import math
class Agent():
    #lasers, odometer, sonar, camera...
    sensors = {}
    # (x, y)
    position = (0, 0)
    rotation = 0
    #max robot steps
    step = 25
    graph_steps_list = []

   
    def getSensor(self, sensor_type, id):
        pass
    

    def setSensor(self, sensor_type, id, value):
        pass    

    def createLasers(self,  num_lasers,  degree_interval,  first_laser_degree,  hyp):
        laser_list = []
        catetoX = lambda angle: math.cos(math.radians(angle))*hyp
        catetoY = lambda angle: math.sin(math.radians(angle))*hyp 
        for i in range(num_lasers):
             degree = first_laser_degree
             laser = CollisionSegment(0, 0, 2, catetoX(degree), catetoY(degree), 2) 
             first_laser_degree += degree_interval
             laser_list.append(laser)
             self.sensors["laser"] = laser_list
