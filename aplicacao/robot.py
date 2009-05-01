from direct.actor.Actor import Actor

class Robot():
    """ this class leads with the actor, the robot """

    def __init__(self):

        self.odometer = 0
        # load the actor
        self.robot = Actor("./modelos/r2d2.egg")
        #self.robot = Actor("./modelos/ralph.egg.pz")
        # self.robot = Actor("./modelos/ralph.egg.pz",
                            # {"run":"./modelos/ralph-run.egg.pz",
                            # "walk":"./modelos/ralph-walk.egg.pz"})
        # load the texture
        #self.tex = loader.loadTexture("modelos/ralph.jpg")
        self.tex = loader.loadTexture("modelos/r2.png")
        # set the texture loaded
        self.robot.setTexture(self.tex, 1)