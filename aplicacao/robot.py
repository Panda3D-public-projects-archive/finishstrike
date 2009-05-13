from direct.actor.Actor import Actor
from framework.Agent import Agent
from pandac.PandaModules import *

class Robot(Agent):
    """ this class leads with the actor, the robot """
    
    def __init__(self):
        #create lasers
        # the lasers creation
        #90
        laser = CollisionSegment(0, 0, 2, 0, -30/2.25, 2)
        #170
        laser2 = CollisionSegment(0, 0, 2, -29.55/2.25, -5.21/2.25, 2)
        #160
        laser3 = CollisionSegment(0, 0, 2, -28.19/2.25, -10.26/2.25, 2)
        #150
        laser4 = CollisionSegment(0, 0, 2, -25.98/2.25, -15/2.25, 2)
        #140
        laser5 = CollisionSegment(0, 0, 2, -22.98/2.25, -19.28/2.25, 2)
        #130
        laser6 = CollisionSegment(0, 0, 2, -19.28/2.25, -22.98/2.25, 2)
        #120
        laser7 = CollisionSegment(0, 0, 2, -15/2.25, -25.98/2.25, 2)
        #110
        laser8 = CollisionSegment(0, 0, 2, -10.26/2.25, -28.19/2.25, 2)
        #100
        laser9 = CollisionSegment(0, 0, 2, -6.21/2.25, -29.54/2.25, 2)
        #180
        laser10  = CollisionSegment(0, 0, 2, -30/2.25, 0, 2)
        #80
        laser11 = CollisionSegment(0, 0, 2, 5.21/2.25, -29.54/2.25, 2)
        #70
        laser12 = CollisionSegment(0, 0, 2, 10.26/2.25, -28.19/2.25, 2)
        #60
        laser13 = CollisionSegment(0, 0, 2, 15/2.25, -25.98/2.25, 2)
        #50
        laser14 = CollisionSegment(0, 0, 2, 19.28/2.25, -22.98/2.25, 2)
        #40
        laser15 = CollisionSegment(0, 0, 2, 22.98/2.25, -19.28/2.25, 2)
        #30
        laser16 = CollisionSegment(0, 0, 2, 25.98/2.25, -15/2.25, 2)
        #20
        laser17 = CollisionSegment(0, 0, 2, 28.19/2.25, -10.26/2.25, 2)
        #10
        laser18 = CollisionSegment(0, 0, 2, 29.54/2.25, -5.21/2.25, 2)
        #0
        laser19 = CollisionSegment(0, 0, 2, 30/2.25, 0, 2)
        
        self.sensors["laser"] = (laser, laser2, laser3, laser4, laser5, laser6,
                                laser7, laser8, laser9, laser10, laser11, 
                                laser12, laser13, laser14, laser15, laser16, 
                                laser17, laser18, laser19)

        self.sensors["odometer"] = [0.0, 0.0]
        
        # load the actor
        self.character = Actor("./modelos/r2d2.egg")
        self.tex = loader.loadTexture("modelos/r2.png")
        # set the texture loaded
        self.character.setTexture(self.tex, 1)
        self.character.actual_position = (0, 0, 0)
        self.position = (0, 0, 0)
        
    def setPos(self, tuple):
        self.character.actual_position = tuple
    
    def getSensor(self, sensor_type, id):
        return self.sensors[sensor_type][id]
    
    def setSensor(self, sensor_type, id, value):
        self.sensors[sensor_type][id] = value