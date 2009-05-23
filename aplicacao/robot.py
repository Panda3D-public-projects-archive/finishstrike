from direct.actor.Actor import Actor
from framework.Agent import Agent
from pandac.PandaModules import *
import math

class Robot(Agent):
    """ this class leads with the actor, the robot """
    
    def __init__(self):
        hyp = 10
        catetoX = lambda angle: math.cos(math.radians(angle))*hyp
        catetoY = lambda angle: math.sin(math.radians(angle))*hyp
        #create lasers
        # the lasers creation
        laser = CollisionSegment(0, 0, 2, catetoX(210), catetoY(210), 2)
        laser2 = CollisionSegment(0, 0, 2, catetoX(215), catetoY(215), 2)
        laser3 = CollisionSegment(0, 0, 2, catetoX(220), catetoY(220), 2)
        laser4 = CollisionSegment(0, 0, 2, catetoX(225), catetoY(225), 2)
        laser5 = CollisionSegment(0, 0, 2, catetoX(230), catetoY(230), 2)
        laser6 = CollisionSegment(0, 0, 2, catetoX(235), catetoY(235), 2)
        laser7 = CollisionSegment(0, 0, 2, catetoX(240), catetoY(240), 2)
        laser8 = CollisionSegment(0, 0, 2, catetoX(245), catetoY(245), 2)
        laser9 = CollisionSegment(0, 0, 2, catetoX(250), catetoY(250), 2)
        laser10  = CollisionSegment(0, 0, 2, catetoX(255), catetoY(255), 2)
        laser11 = CollisionSegment(0, 0, 2, catetoX(260), catetoY(260), 2)
        laser12 = CollisionSegment(0, 0, 2, catetoX(265), catetoY(265), 2)
        laser13 = CollisionSegment(0, 0, 2, catetoX(270), catetoY(270), 2)
        laser14 = CollisionSegment(0, 0, 2, catetoX(275), catetoY(275), 2)
        laser15 = CollisionSegment(0, 0, 2, catetoX(280), catetoY(280), 2)
        laser16 = CollisionSegment(0, 0, 2, catetoX(285), catetoY(285), 2)
        laser17 = CollisionSegment(0, 0, 2, catetoX(290), catetoY(290), 2)
        laser18 = CollisionSegment(0, 0, 2, catetoX(295), catetoY(295), 2)
        laser19 = CollisionSegment(0, 0, 2, catetoX(300), catetoY(300), 2)
        laser20 = CollisionSegment(0, 0, 2, catetoX(305), catetoY(305), 2)
        laser21 = CollisionSegment(0, 0, 2, catetoX(310), catetoY(310), 2)
        laser22 = CollisionSegment(0, 0, 2, catetoX(315), catetoY(315), 2)
        laser23 = CollisionSegment(0, 0, 2, catetoX(320), catetoY(320), 2)
        laser24 = CollisionSegment(0, 0, 2, catetoX(325), catetoY(325), 2)
        laser25 = CollisionSegment(0, 0, 2, catetoX(330), catetoY(330), 2)
        
        
        self.sensors["laser"] = (laser, laser2, laser3, laser4, laser5, laser6,
                                laser7, laser8, laser9, laser10, laser11, 
                                laser12, laser13, laser14, laser15, laser16, 
                                laser17, laser18, laser19, laser20, laser21, 
                                laser22, laser23, laser24, laser25)

        self.sensors["odometer"] = [0.0, 0.0]
        
        # load the actor
        self.character = Actor("./modelos/r2d2.egg")
        self.tex = loader.loadTexture("modelos/r2.png")
        # set the texture loaded
        self.character.setTexture(self.tex, 1)
#----------------
#        self.character.actual_position = (0, 0, 0)
#---------------
        self.position = (0, 0, 0)
        
    def setPos(self, tuple):
        self.character.actual_position = tuple
    
    def getSensor(self, sensor_type, id):
        return self.sensors[sensor_type][id]
    
    def setSensor(self, sensor_type, id, value):
        self.sensors[sensor_type][id] = value
