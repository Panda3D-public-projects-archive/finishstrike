# -*- coding: cp1252 -*-
from direct.gui.OnscreenText import OnscreenText
from framework.GraphFacade import *
from framework.SLAM import *
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *
import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.task import Task
from direct.interval.IntervalGlobal import *
from robot import *


#Create o Traverser in the "base"
base.cTrav = CollisionTraverser()
#Create Pusher in the "base"
base.pusher = CollisionHandlerPusher()
#Create Floor in the "base"
base.floor = CollisionHandlerFloor()
base.floor.setMaxVelocity(1)
#Create lasers
base.laser = CollisionHandlerQueue()
base.laser2 = CollisionHandlerQueue()
base.laser3 = CollisionHandlerQueue()
base.laser4 = CollisionHandlerQueue()
base.laser5 = CollisionHandlerQueue()
base.laser6 = CollisionHandlerQueue()
base.laser7 = CollisionHandlerQueue()
base.laser8 = CollisionHandlerQueue()
base.laser9 = CollisionHandlerQueue()
base.laser10 = CollisionHandlerQueue()
base.laser11 = CollisionHandlerQueue()
base.laser12 = CollisionHandlerQueue()
base.laser13 = CollisionHandlerQueue()
base.laser14 = CollisionHandlerQueue()
base.laser15 = CollisionHandlerQueue()
base.laser16 = CollisionHandlerQueue()
base.laser17 = CollisionHandlerQueue()
base.laser18 = CollisionHandlerQueue()
base.laser19 = CollisionHandlerQueue()


class PandaSlam(Slam):

    def startAutomaticWalk(self):
        """  """
        envi.setKey("forward", 1)
    
    def stopAutomaticWalk(self):
        """  """
        envi.setKey("forward", 0)

class Environment(DirectObject):
    """ This class works with environments details """

    def __init__(self):
        # this is the robot dictionary lasers - keys is degrees
        
        self.slam_obj = PandaSlam()
        self.slam_obj.landmarkUpdate('+90', 0)
        self.slam_obj.landmarkUpdate('+80', 0)
        self.slam_obj.landmarkUpdate('+70', 0)
        self.slam_obj.landmarkUpdate('+60', 0)
        self.slam_obj.landmarkUpdate('+50', 0)
        self.slam_obj.landmarkUpdate('+40', 0)
        self.slam_obj.landmarkUpdate('+30', 0)
        self.slam_obj.landmarkUpdate('+20', 0)
        self.slam_obj.landmarkUpdate('+10', 0)
        self.slam_obj.landmarkUpdate('0', 0)
        self.slam_obj.landmarkUpdate('-10', 0)
        self.slam_obj.landmarkUpdate('-20', 0)
        self.slam_obj.landmarkUpdate('-30', 0)
        self.slam_obj.landmarkUpdate('-40', 0)
        self.slam_obj.landmarkUpdate('-50', 0)
        self.slam_obj.landmarkUpdate('-60', 0)
        self.slam_obj.landmarkUpdate('-70', 0)
        self.slam_obj.landmarkUpdate('-80', 0)
        self.slam_obj.landmarkUpdate('-90', 0)

        # show the text on screen
        self.title = OnscreenText(pos=(0.8, -0.85), fg=(255, 255, 0, 90))
        self.title_odometer = \
            OnscreenText(pos=(0.8, -0.95), fg=(255, 255, 0, 90))
        self.title_lasers = OnscreenText(pos=(-1, 0.9), fg=(255, 255, 0, 90))
        # load the environment model
        self.environment = \
            loader.loadModel("./modelos/[modelo] novo galpao.egg")
        # load the actor from module Robot
        self.robot = Robot().robot
        self.odometer = 0
        self.last_odometer = 0
        self.distance_laser = self.robot
        self.threshold = 0.96
        # adjusting scale and position of the model
        self.environment.setScale(10, 10, 10)
        self.environment.setPos(0, 0, 2.01)
        self.robot.setScale(10, 10, 10)
        self.robot.setPos(0, 0, 0)
        # render
        self.environment.reparentTo(render)
        self.robot.reparentTo(render)
        # building a graph with GraphFacade
        self.graph = \
        GraphFacade().getGraph("nos.txt", "arestas.txt")
    #--------------------------------------------------
        # the key map dictionary
        self.keyMap = {"left":0, "right":0, "forward":0, "down":0}
        # the control
        self.accept("arrow_left", self.setKey, ["left", 1])
        self.accept("arrow_right", self.setKey, ["right", 1])
        self.accept("arrow_up", self.setKey, ["forward", 1])
        self.accept("arrow_left-up", self.setKey, ["left", 0])
        self.accept("arrow_right-up", self.setKey, ["right", 0])
        self.accept("arrow_up-up", self.setKey, ["forward", 0])
        self.accept("m", self.playMusic, ['./modelos/missaoimpossivel.mp3'])
        #self.accept("p", self.walkAway,["no1", "no9"])
        self.accept("s", self.slam_obj.startAutomaticWalk)
        self.accept("o", self.slam_obj.stopAutomaticWalk)
        self.accept("t", self.doTest)
    #--------------------------------------------------
        # game's aspect in initial state
        self.prevtime = 0
        self.isMoving = False
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

        base.disableMouse()
        base.camera.setPos(self.robot.getX(), self.robot.getY()+160, 500)
        taskMgr.add(self.printXYZ, "printXYZTask")
        # add a movement event in the environment
        taskMgr.add(self.move,"moveTask")
        # build a sequence of movements
        self.walk = Sequence()
        self.createColliders()
        self.printLasersResult()
    #--------------------------------------------------

    def playMusic(self, music):
        """ music for test """
        self.musicBoxSound = base.loadMusic(music)
        self.musicBoxSound.setVolume(1)
        self.musicBoxSound.setLoopCount(200) 
        self.musicBoxSound.play()

    def createColliders(self):
            #create the collision sphere
            self.robotSphereCN = CollisionNode('robotSphere')
            self.robotSphereCN.addSolid(CollisionSphere(0,0,2,1))
            self.robotEsfNP = self.robot.attachNewNode(self.robotSphereCN)
            #self.robotEsfNP.show()
            base.cTrav.addCollider(self.robotEsfNP, base.pusher)
            base.pusher.addCollider(self.robotEsfNP, self.robot)

            #robot Collision Ray
            self.robotGroundRay = CollisionRay()
            self.robotGroundRay.setOrigin(0,0,10)
            self.robotGroundRay.setDirection(0,0,-1)
            self.robotGroundCol = CollisionNode('robotRay')
            self.robotGroundCol.addSolid(self.robotGroundRay)
            self.robotGroundColNp=self.robot.attachNewNode(self.robotGroundCol)
            #self.robotGroundColNp.show()
            base.cTrav.addCollider(self.robotGroundColNp, base.floor)
            base.floor.addCollider(self.robotGroundColNp, self.robot)

            # the lasers creation
            #90
            self.laser = CollisionSegment (0, 0, 2, 0, -30/2.25, 2)
            #170
            self.laser2 = CollisionSegment (0, 0, 2, -29.55/2.25, -5.21/2.25, 2)
            #160
            self.laser3 = CollisionSegment (0, 0, 2, -28.19/2.25, -10.26/2.25, 2)
            #150
            self.laser4 = CollisionSegment (0, 0, 2, -25.98/2.25, -15/2.25, 2)
            #140
            self.laser5 = CollisionSegment (0, 0, 2, -22.98/2.25, -19.28/2.25, 2)
            #130
            self.laser6 = CollisionSegment (0, 0, 2, -19.28/2.25, -22.98/2.25, 2)
            #120
            self.laser7 = CollisionSegment (0, 0, 2, -15/2.25, -25.98/2.25, 2)
            #110
            self.laser8 = CollisionSegment (0, 0, 2, -10.26/2.25, -28.19/2.25, 2)
            #100
            self.laser9 = CollisionSegment (0, 0, 2, -6.21/2.25, -29.54/2.25, 2)
            #180
            self.laser10  = CollisionSegment (0, 0, 2, -30/2.25, 0, 2)
            #80
            self.laser11 = CollisionSegment (0, 0, 2, 5.21/2.25, -29.54/2.25, 2)
            #70
            self.laser12 = CollisionSegment (0, 0, 2, 10.26/2.25, -28.19/2.25, 2)
            #60
            self.laser13 = CollisionSegment (0, 0, 2, 15/2.25, -25.98/2.25, 2)
            #50
            self.laser14 = CollisionSegment (0, 0, 2, 19.28/2.25, -22.98/2.25, 2)
            #40
            self.laser15 = CollisionSegment (0, 0, 2, 22.98/2.25, -19.28/2.25, 2)
            #30
            self.laser16 = CollisionSegment (0, 0, 2, 25.98/2.25, -15/2.25, 2)
            #20
            self.laser17 = CollisionSegment (0, 0, 2, 28.19/2.25, -10.26/2.25, 2)
            #10
            self.laser18 = CollisionSegment (0, 0, 2, 29.54/2.25, -5.21/2.25, 2)
            #0
            self.laser19 = CollisionSegment (0, 0, 2, 30/2.25, 0, 2)

            # attach a node for each laser NodePath
            self.laserNodePath = \
                self.robot.attachNewNode(CollisionNode('laserNode'))
            self.laserNodePath2 = \
                self.robot.attachNewNode(CollisionNode ('laserNode2'))
            self.laserNodePath3 = \
                self.robot.attachNewNode(CollisionNode ('laserNode3'))
            self.laserNodePath4 = \
                self.robot.attachNewNode(CollisionNode ('laserNode4'))
            self.laserNodePath5 = \
                self.robot.attachNewNode(CollisionNode ('laserNode5'))
            self.laserNodePath6 = \
                self.robot.attachNewNode(CollisionNode ('laserNode6'))
            self.laserNodePath7 = \
                self.robot.attachNewNode(CollisionNode ('laserNode7'))
            self.laserNodePath8 = \
                self.robot.attachNewNode(CollisionNode ('laserNode8'))
            self.laserNodePath9 = \
                self.robot.attachNewNode(CollisionNode ('laserNode9'))
            self.laserNodePath10 = \
                self.robot.attachNewNode(CollisionNode ('laserNode10'))
            self.laserNodePath11 = \
                self.robot.attachNewNode(CollisionNode ('laserNode11'))
            self.laserNodePath12 = \
                self.robot.attachNewNode(CollisionNode ('laserNode12'))
            self.laserNodePath13 = \
                self.robot.attachNewNode(CollisionNode ('laserNode13'))
            self.laserNodePath14 = \
                self.robot.attachNewNode(CollisionNode ('laserNode14'))
            self.laserNodePath15 = \
                self.robot.attachNewNode(CollisionNode ('laserNode15'))
            self.laserNodePath16 = \
                self.robot.attachNewNode(CollisionNode ('laserNode16'))
            self.laserNodePath17 = \
                self.robot.attachNewNode(CollisionNode ('laserNode17'))
            self.laserNodePath18 = \
                self.robot.attachNewNode(CollisionNode ('laserNode18'))
            self.laserNodePath19 = \
                self.robot.attachNewNode(CollisionNode ('laserNode19'))

            # each laser have its NodePath
            self.laserNodePath.node().addSolid(self.laser)
            self.laserNodePath2.node().addSolid(self.laser2)
            self.laserNodePath3.node().addSolid(self.laser3)
            self.laserNodePath4.node().addSolid(self.laser4)
            self.laserNodePath5.node().addSolid(self.laser5)
            self.laserNodePath6.node().addSolid(self.laser6)
            self.laserNodePath7.node().addSolid(self.laser7)
            self.laserNodePath8.node().addSolid(self.laser8)
            self.laserNodePath9.node().addSolid(self.laser9)
            self.laserNodePath10.node().addSolid(self.laser10)
            self.laserNodePath11.node().addSolid(self.laser11)
            self.laserNodePath12.node().addSolid(self.laser12)
            self.laserNodePath13.node().addSolid(self.laser13)
            self.laserNodePath14.node().addSolid(self.laser14)
            self.laserNodePath15.node().addSolid(self.laser15)
            self.laserNodePath16.node().addSolid(self.laser16)
            self.laserNodePath17.node().addSolid(self.laser17)
            self.laserNodePath18.node().addSolid(self.laser18)
            self.laserNodePath19.node().addSolid(self.laser19)

            #each laser is now collidible
            base.cTrav.addCollider(self.laserNodePath, base.laser)
            base.cTrav.addCollider(self.laserNodePath2, base.laser2)
            base.cTrav.addCollider(self.laserNodePath3, base.laser3)
            base.cTrav.addCollider(self.laserNodePath4, base.laser4)
            base.cTrav.addCollider(self.laserNodePath5, base.laser5)
            base.cTrav.addCollider(self.laserNodePath6, base.laser6)
            base.cTrav.addCollider(self.laserNodePath7, base.laser7)
            base.cTrav.addCollider(self.laserNodePath8, base.laser8)
            base.cTrav.addCollider(self.laserNodePath9, base.laser9)
            base.cTrav.addCollider(self.laserNodePath10, base.laser10)
            base.cTrav.addCollider(self.laserNodePath11, base.laser11)
            base.cTrav.addCollider(self.laserNodePath12, base.laser12)
            base.cTrav.addCollider(self.laserNodePath13, base.laser13)
            base.cTrav.addCollider(self.laserNodePath14, base.laser14)
            base.cTrav.addCollider(self.laserNodePath15, base.laser15)
            base.cTrav.addCollider(self.laserNodePath16, base.laser16)
            base.cTrav.addCollider(self.laserNodePath17, base.laser17)
            base.cTrav.addCollider(self.laserNodePath18, base.laser18)
            base.cTrav.addCollider(self.laserNodePath19, base.laser19)

            base.cTrav.traverse(render)

    def addInterval(self, posInicial, posFinal):
        """
            This method adds a time interval between 
            two vertexes for the sequence movement
        """

        robotPosInter1= \
        self.robot.posInterval(5,Point3(posFinal[0], posFinal[1], posFinal[2]),
            startPos=Point3(posInicial[0], posInicial[1], posInicial[2]))
        self.walk.append(robotPosInter1)
    #--------------------------------------------------

    def goTo(self):
        """
            Starts the sequence of movements, called walk
        """
        self.robot.loop("run")
        self.walk.start()
    #--------------------------------------------------

    def walkAway(self, initial, final):
        """
            Builds the vertexes dictionary and executes Dijkstra (from GraphFacade)
        """

        self.graph.buildVertexDic()
        adjacency_matrix = self.graph.buildAdjMatrix()
        # way is the shortest path between two vertexes
        way = self.graph.shortestPath(adjacency_matrix, initial, final)
        i = 0
        while (i <= (len(way)-2)):
            aux = self.graph.getPositionVertex(way[i])
            aux1 = self.graph.getPositionVertex(way[i+1])
            self.addInterval(aux, aux1)
            i += 1
        self.goTo()
    #--------------------------------------------------

    def setKey(self, key, value):
        """ set a value within the key into keyMap """

        self.keyMap[key] = value
    #--------------------------------------------------

    def move(self, task):
        """ allow the keyboard movement """

        elapsed = task.time - self.prevtime
        beforePosition = \
          {"X":self.robot.getX(), "Y":self.robot.getY(), "Z":self.robot.getZ()}
        # If a move-key is pressed, move robot in the specified direction.

        if (self.keyMap["left"]!=0):
                self.robot.setH(self.robot.getH() + elapsed*160)
        if (self.keyMap["right"]!=0):
                self.robot.setH(self.robot.getH() - elapsed*160)
        if (self.keyMap["forward"]!=0):
                backward = self.robot.getNetTransform().getMat().getRow3(1)
                backward.normalize()
                self.robot.setPos(self.robot.getPos() - backward*(elapsed*50))
                #The odometer accumulates the value of the distance
                #between its previous position until his current position.
                self.odometer += self.threshold*sqrt(
                    (self.robot.getX()-beforePosition["X"])**2 + 
                    (self.robot.getY()-beforePosition["Y"])**2 + 
                    (self.robot.getZ()-beforePosition["Z"])**2)

                #Use odometer to active/desactive laser scan and others tasks
                if (self.odometer - self.last_odometer >= 25.0):
                    self.last_odometer = self.odometer
                    base.cTrav.showCollisions(render)
                    self.getLasersDistance()
                    self.printLasersResult()
                    self.seeTheWay()
                    #self.slam_obj.createLandmarkGraph()
                else:
                    base.cTrav.hideCollisions()

        # If robot is moving, loop the run animation.
        # If he is standing still, stop the animation.
        if (self.keyMap["forward"]!=0) or (self.keyMap["left"]!=0) or \
        (self.keyMap["right"]!=0):
                if self.isMoving is False:
                        self.isMoving = True
        else:
                if self.isMoving:
                        self.robot.stop()
                        self.isMoving = False

        self.floater.setPos(self.robot.getPos())
        self.floater.setZ(self.robot.getZ() + 10)
        base.camera.lookAt(self.floater)

        # Store the task time and continue.
        self.prevtime = task.time

        return Task.cont

    #--------------------------------------------------
    def getDistance(self, laser, degree):
        entries=[]
        entry=0
        laser.sortEntries()
        for i in range(laser.getNumEntries()):
            entry = laser.getEntry(i)
            entries.append(entry)

        if (len(entries)>1):
            self.distance_laser = entries[1].getSurfacePoint(render)
            value = sqrt((self.robot.getPos().getX()
            - self.distance_laser.getX())**2+(self.robot.getPos().getY()
            - self.distance_laser.getY())**2+(self.robot.getPos().getZ()
            - self.distance_laser.getZ())**2)-18
            self.slam_obj.landmarkUpdate(degree, value)
        else:
            self.slam_obj.landmarkUpdate(degree, self.slam_obj.infinity_point)

    def getLasersDistance(self):
        self.getDistance(base.laser, "0")
        self.getDistance(base.laser2, "-80")
        self.getDistance(base.laser3, "-70")
        self.getDistance(base.laser4, "-60")
        self.getDistance(base.laser5, "-50")
        self.getDistance(base.laser6, "-40")
        self.getDistance(base.laser7, "-30")
        self.getDistance(base.laser8, "-20")
        self.getDistance(base.laser9, "-10")
        self.getDistance(base.laser10, "-90")
        self.getDistance(base.laser11, "+10")
        self.getDistance(base.laser12, "+20")
        self.getDistance(base.laser13, "+30")
        self.getDistance(base.laser14, "+40")
        self.getDistance(base.laser15, "+50")
        self.getDistance(base.laser16, "+60")
        self.getDistance(base.laser17, "+70")
        self.getDistance(base.laser18, "+80")
        self.getDistance(base.laser19, "+90")

    
    def printXYZ(self, task):
        """ prints the X, Y, Z position of the actor """

        self.title.setText(self.getXYZ())
        self.title_odometer.setText(self.getInfos())
        return Task.cont
    #--------------------------------------------------

    def printLasersResult(self):
        self.title_lasers.setText("+90: %.2f \n +80: %.2f \n +70: %.2f \n \
+60: %.2f \n +50: %.2f \n +40: %.2f \n +30: %.2f \n +20: %.2f \n \
+10: %.2f \n 0: %.2f \n -10: %.2f \n -20: %.2f \n -30: %.2f \n \
-40: %.2f \n -50: %.2f \n -60: %.2f \n -70: %.2f \n -80: %.2f \n \
-90: %.2f" %
        (self.slam_obj.landmark_dic["+90"], self.slam_obj.landmark_dic["+80"],
        self.slam_obj.landmark_dic["+70"], self.slam_obj.landmark_dic["+60"], 
        self.slam_obj.landmark_dic["+50"], self.slam_obj.landmark_dic["+40"], 
        self.slam_obj.landmark_dic["+30"], self.slam_obj.landmark_dic["+20"],
        self.slam_obj.landmark_dic["+10"], self.slam_obj.landmark_dic["0"], 
        self.slam_obj.landmark_dic["-10"], self.slam_obj.landmark_dic["-20"], 
        self.slam_obj.landmark_dic["-30"], self.slam_obj.landmark_dic["-40"],
        self.slam_obj.landmark_dic["-50"], self.slam_obj.landmark_dic["-60"],
        self.slam_obj.landmark_dic["-70"],
        self.slam_obj.landmark_dic["-80"], self.slam_obj.landmark_dic["-90"]))

    def getXYZ(self):
        """
            returns a string of the actual position like 
            'x: value, y: value, z : value'
        """

        return "X: %.2f Y: %.2f Z: %.2f "\
        % (self.robot.getX(), self.robot.getY(), self.robot.getZ())
    #--------------------------------------------------
    def getInfos(self):
        """ returns odometer data """
        if (self.distance_laser == None):
            return "Odometer: %.2f Laser: %s"\
            %( self.odometer, self.distance_laser)
        else:
            return "Odometer: %.2f" %self.odometer

    def seeTheWay(self):
        """ see the way to walk """
        actualH = self.robot.getH()
        newH = self.slam_obj.biggerDictionaryKey(self.slam_obj.landmark_dic)
        newH = actualH + float(newH)
        self.robot.setHpr(newH, 0, 0)
        
    def buildGraphOfLandmarks(self):
        """ builds a landmark graph """
        for key in self.slam_obj.landmark_dic.iterkeys():
            self.slam_obj.createLandmarkGraph(key)
    
    def doTest(self):
        angle = '+60'
        self.buildGraphOfLandmarks()
        print self.slam_obj.landmark_graph
        print self.slam_obj.landmark_graph.__len__()


envi = Environment()
run()