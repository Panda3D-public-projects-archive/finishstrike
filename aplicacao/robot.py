from direct.actor.Actor import Actor
from agent import Agent
from pandac.PandaModules import *
import math

class Robot(Agent):
    """ this class leads with the actor, the robot """
    
    def __init__(self):

        # the lasers creation
        self.createLasers(25,  5,  210,  15)
        #odometer is a list witch first element is actual odometer
        # and second is last odomenter
        self.sensors["odometer"] = [0.0, 0.0]
        
        # load the actor
        self.character = Actor("./modelos/r2d2.egg")
        self.tex = loader.loadTexture("modelos/r2.png")
        # set the texture loaded
        self.character.setTexture(self.tex, 1)
        self.position = (0, 0, 0)
        self.credits_to_walk = 0
        
    def setPos(self, tuple):
        self.character.actual_position = tuple
    
    def getSensor(self, sensor_type, id):
        return self.sensors[sensor_type][id]
    
    def setSensor(self, sensor_type, id, value):
        self.sensors[sensor_type][id] = value
