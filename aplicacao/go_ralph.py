# -*- coding: cp1252 -*-
from direct.gui.OnscreenText import OnscreenText
from horus.mapping.slam import *
from horus.core.math.graph import *
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
base.laser20 = CollisionHandlerQueue()
base.laser21 = CollisionHandlerQueue()
base.laser22 = CollisionHandlerQueue()
base.laser23 = CollisionHandlerQueue()
base.laser24 = CollisionHandlerQueue()
base.laser25 = CollisionHandlerQueue()


class PandaSlam(Slam):

    def __init__(self):
        Slam.__init__(self)

    def startAutomaticWalk(self):
        """  """
        envi.getLasersDistance()
        envi.printLasersResult()
        envi.seeTheWay()
        envi.setKey("forward", 1)

    def stopAutomaticWalk(self):
        """  """
        envi.setKey("forward", 0)

class Environment(DirectObject):
    """ This class works with environments details """

    def __init__(self):
        # this is the robot dictionary lasers - keys is degrees
        
        self.slam_obj = PandaSlam()
        self.slam_obj.laserUpdate('+60', 0)
        self.slam_obj.laserUpdate('+55', 0)
        self.slam_obj.laserUpdate('+50', 0)
        self.slam_obj.laserUpdate('+45', 0)
        self.slam_obj.laserUpdate('+40', 0)
        self.slam_obj.laserUpdate('+35', 0)
        self.slam_obj.laserUpdate('+30', 0)
        self.slam_obj.laserUpdate('+25', 0)
        self.slam_obj.laserUpdate('+20', 0)
        self.slam_obj.laserUpdate('+15', 0)
        self.slam_obj.laserUpdate('+10', 0)
        self.slam_obj.laserUpdate('+5', 0)
        self.slam_obj.laserUpdate('0', 0)
        self.slam_obj.laserUpdate('-5', 0)
        self.slam_obj.laserUpdate('-10', 0)
        self.slam_obj.laserUpdate('-15', 0)
        self.slam_obj.laserUpdate('-20', 0)
        self.slam_obj.laserUpdate('-25', 0)
        self.slam_obj.laserUpdate('-30', 0)
        self.slam_obj.laserUpdate('-35', 0)
        self.slam_obj.laserUpdate('-40', 0)
        self.slam_obj.laserUpdate('-45', 0)
        self.slam_obj.laserUpdate('-50', 0)
        self.slam_obj.laserUpdate('-55', 0)
        self.slam_obj.laserUpdate('-60', 0)
        
        
        
        # show the text on screen
        self.title = OnscreenText(pos=(0.8, -0.85), fg=(255, 255, 0, 90))
        self.title_odometer = \
            OnscreenText(pos=(0.8, -0.95), fg=(255, 255, 0, 90))
        self.title_lasers = OnscreenText(pos=(-1, 0.9), fg=(255, 255, 0, 90)) 
        # load the environment model
        self.environment = \
            loader.loadModel("./modelos/[modelo] novo galpao.egg")
        self.robot = Robot()
        # load the character from module Robot
        self.character = self.robot.character
        #self.robot.graphSteps[self.robot.position] = self.character.getPos()
        self.distance_laser = self.character
        self.threshold = 0.96
        # adjusting scale and position of the model
        self.environment.setScale(10, 10, 10)
        self.environment.setPos(0, 0, 2.01)
        self.character.setScale(10, 10, 10)
        
        # render
        self.environment.reparentTo(render)
        self.character.reparentTo(render)
        # building a graph with GraphFacade
        self.graph = Graph("nos.txt", "arestas.txt")
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
        self.printLasersResult()
        self.prevtime = 0
        self.isMoving = False
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

        base.disableMouse()
        base.camera.setPos(self.character.getX(), 
            self.character.getY() + 160, 500)
        taskMgr.add(self.printXYZ, "printXYZTask")
        # add a movement event in the environment
        taskMgr.add(self.move,"moveTask")
        # build a sequence of movements
        self.walk = Sequence()
        self.createColliders()
        
    #--------------------------------------------------

    def playMusic(self, music):
        """ music for test """
        self.musicBoxSound = base.loadMusic(music)
        self.musicBoxSound.setVolume(1)
        self.musicBoxSound.setLoopCount(200) 
        self.musicBoxSound.play()

    def createColliders(self):
            #create the collision sphere
            self.characterSphereCN = CollisionNode('characterSphere')
            self.characterSphereCN.addSolid(CollisionSphere(0,0,2,1))
            self.characterEsfNP = self.character.attachNewNode(self.characterSphereCN)
            #self.characterEsfNP.show()
            base.cTrav.addCollider(self.characterEsfNP, base.pusher)
            base.pusher.addCollider(self.characterEsfNP, self.character)

            #character Collision Ray
            self.characterGroundRay = CollisionRay()
            self.characterGroundRay.setOrigin(0,0,10)
            self.characterGroundRay.setDirection(0,0,-1)
            self.characterGroundCol = CollisionNode('characterRay')
            self.characterGroundCol.addSolid(self.characterGroundRay)
            self.characterGroundColNp=self.character.attachNewNode(self.characterGroundCol)
            #self.characterGroundColNp.show()
            base.cTrav.addCollider(self.characterGroundColNp, base.floor)
            base.floor.addCollider(self.characterGroundColNp, self.character)

            # attach a node for each laser NodePath
            self.laserNodePath = \
                self.character.attachNewNode(CollisionNode('laserNode'))
            self.laserNodePath2 = \
                self.character.attachNewNode(CollisionNode ('laserNode2'))
            self.laserNodePath3 = \
                self.character.attachNewNode(CollisionNode ('laserNode3'))
            self.laserNodePath4 = \
                self.character.attachNewNode(CollisionNode ('laserNode4'))
            self.laserNodePath5 = \
                self.character.attachNewNode(CollisionNode ('laserNode5'))
            self.laserNodePath6 = \
                self.character.attachNewNode(CollisionNode ('laserNode6'))
            self.laserNodePath7 = \
                self.character.attachNewNode(CollisionNode ('laserNode7'))
            self.laserNodePath8 = \
                self.character.attachNewNode(CollisionNode ('laserNode8'))
            self.laserNodePath9 = \
                self.character.attachNewNode(CollisionNode ('laserNode9'))
            self.laserNodePath10 = \
                self.character.attachNewNode(CollisionNode ('laserNode10'))
            self.laserNodePath11 = \
                self.character.attachNewNode(CollisionNode ('laserNode11'))
            self.laserNodePath12 = \
                self.character.attachNewNode(CollisionNode ('laserNode12'))
            self.laserNodePath13 = \
                self.character.attachNewNode(CollisionNode ('laserNode13'))
            self.laserNodePath14 = \
                self.character.attachNewNode(CollisionNode ('laserNode14'))
            self.laserNodePath15 = \
                self.character.attachNewNode(CollisionNode ('laserNode15'))
            self.laserNodePath16 = \
                self.character.attachNewNode(CollisionNode ('laserNode16'))
            self.laserNodePath17 = \
                self.character.attachNewNode(CollisionNode ('laserNode17'))
            self.laserNodePath18 = \
                self.character.attachNewNode(CollisionNode ('laserNode18'))
            self.laserNodePath19 = \
                self.character.attachNewNode(CollisionNode ('laserNode19'))
            self.laserNodePath20 = \
                self.character.attachNewNode(CollisionNode ('laserNode20'))
            self.laserNodePath21 = \
                self.character.attachNewNode(CollisionNode ('laserNode21'))
            self.laserNodePath22 = \
                self.character.attachNewNode(CollisionNode ('laserNode22'))
            self.laserNodePath23 = \
                self.character.attachNewNode(CollisionNode ('laserNode23'))
            self.laserNodePath24 = \
                self.character.attachNewNode(CollisionNode ('laserNode24'))
            self.laserNodePath25 = \
                self.character.attachNewNode(CollisionNode ('laserNode25'))



            # each laser have its NodePath
            self.laserNodePath.node().addSolid(self.robot.getSensor("laser",0))
            self.laserNodePath2.node().addSolid(self.robot.getSensor("laser",1))
            self.laserNodePath3.node().addSolid(self.robot.getSensor("laser",2))
            self.laserNodePath4.node().addSolid(self.robot.getSensor("laser",3))
            self.laserNodePath5.node().addSolid(self.robot.getSensor("laser",4))
            self.laserNodePath6.node().addSolid(self.robot.getSensor("laser",5))
            self.laserNodePath7.node().addSolid(self.robot.getSensor("laser",6))
            self.laserNodePath8.node().addSolid(self.robot.getSensor("laser",7))
            self.laserNodePath9.node().addSolid(self.robot.getSensor("laser",8))
            self.laserNodePath10.node().addSolid(self.robot.getSensor("laser",9))
            self.laserNodePath11.node().addSolid(self.robot.getSensor("laser",10))
            self.laserNodePath12.node().addSolid(self.robot.getSensor("laser",11))
            self.laserNodePath13.node().addSolid(self.robot.getSensor("laser",12))
            self.laserNodePath14.node().addSolid(self.robot.getSensor("laser",13))
            self.laserNodePath15.node().addSolid(self.robot.getSensor("laser",14))
            self.laserNodePath16.node().addSolid(self.robot.getSensor("laser",15))
            self.laserNodePath17.node().addSolid(self.robot.getSensor("laser",16))
            self.laserNodePath18.node().addSolid(self.robot.getSensor("laser",17))
            self.laserNodePath19.node().addSolid(self.robot.getSensor("laser",18))
            self.laserNodePath20.node().addSolid(self.robot.getSensor("laser",19))
            self.laserNodePath21.node().addSolid(self.robot.getSensor("laser",20))
            self.laserNodePath22.node().addSolid(self.robot.getSensor("laser",21))
            self.laserNodePath23.node().addSolid(self.robot.getSensor("laser",22))
            self.laserNodePath24.node().addSolid(self.robot.getSensor("laser",23))
            self.laserNodePath25.node().addSolid(self.robot.getSensor("laser",24))

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
            base.cTrav.addCollider(self.laserNodePath20, base.laser20)
            base.cTrav.addCollider(self.laserNodePath21, base.laser21)
            base.cTrav.addCollider(self.laserNodePath22, base.laser22)
            base.cTrav.addCollider(self.laserNodePath23, base.laser23)
            base.cTrav.addCollider(self.laserNodePath24, base.laser24)
            base.cTrav.addCollider(self.laserNodePath25, base.laser25)

            base.cTrav.traverse(render)

    def addInterval(self, posInicial, posFinal):
        """
            This method adds a time interval between 
            two vertexes for the sequence movement
        """

        character_interval= \
        self.character.posInterval(5,Point3(posFinal[0], posFinal[1], posFinal[2]),
            startPos=Point3(posInicial[0], posInicial[1], posInicial[2]))
        self.walk.append(character_interval)
    #--------------------------------------------------

    def goTo(self):
        """
            Starts the sequence of movements, called walk
        """
        self.character.loop("run")
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
          {"X":self.character.getX(), "Y":self.character.getY(), "Z":self.character.getZ()}
        # If a move-key is pressed, move character in the specified direction.

        if (self.keyMap["left"]!=0):
                self.character.setH(self.character.getH() + elapsed*160)
        if (self.keyMap["right"]!=0):
                self.character.setH(self.character.getH() - elapsed*160)
        if (self.keyMap["forward"]!=0):
                backward = self.character.getNetTransform().getMat().getRow3(1)
                backward.normalize()
                self.character.setPos(self.character.getPos() - backward*(elapsed*50))
                #The odometer accumulates the value of the distance
                #between its previous position until his current position.
                last_odometer = self.robot.getSensor("odometer", 1)
                odometer = self.robot.getSensor("odometer", 0)
                odometer += self.threshold*sqrt(
                    (self.character.getX()-beforePosition["X"])**2 +
                    (self.character.getY()-beforePosition["Y"])**2 + 
                    (self.character.getZ()-beforePosition["Z"])**2)
                
                self.robot.setSensor("odometer", 0, odometer)
    
                #Use odometer to active/desactive laser scan and others tasks
                if (odometer - last_odometer >= 25.0):
                    self.robot.setSensor("odometer", 1, odometer)
                    base.cTrav.showCollisions(render)
                    self.getLasersDistance()
                    self.printLasersResult()
                    self.robot.rotation += self.seeTheWay()
                    self.robot.position = self.slam_obj.getRobotPosition(
                        odometer - last_odometer, self.robot.rotation, self.robot.position)
                    
                    self.slam_obj.landmarkExtraction(self.robot.position)
                    self.robot.graph_steps_dic[self.robot.position] = self.character.getPos()
                    
               
                else:
                    base.cTrav.hideCollisions()

        # If character is moving, loop the run animation.
        # If he is standing still, stop the animation.
        if (self.keyMap["forward"]!=0) or (self.keyMap["left"]!=0) or \
        (self.keyMap["right"]!=0):
                if self.isMoving is False:
                        self.isMoving = True
        else:
                if self.isMoving:
                        self.character.stop()
                        self.isMoving = False

        self.floater.setPos(self.character.getPos())
        self.floater.setZ(self.character.getZ() + 10)
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
            value = sqrt((self.character.getPos().getX()
            - self.distance_laser.getX())**2+(self.character.getPos().getY()
            - self.distance_laser.getY())**2+(self.character.getPos().getZ()
            - self.distance_laser.getZ())**2)-18
            self.slam_obj.laserUpdate(degree, value)

        else:
            self.slam_obj.laserUpdate(degree, self.slam_obj.infinity_point)

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
        """ prints the X, Y, Z position of the character """

        self.title.setText(self.getXYZ())
        self.title_odometer.setText(self.getInfos())
        return Task.cont
    #--------------------------------------------------

    def printLasersResult(self):
        self.title_lasers.setText("+60: %.2f \n +55: %.2f \n +50: %.2f \n \
+45: %.2f \n +40: %.2f \n +35: %.2f \n +30: %.2f \n +25: %.2f \n \
+20: %.2f \n +15: %.2f \n +10: %.2f \n +5: %.2f \n 0: %.2f \n \
-5: %.2f \n -10: %.2f \n -15: %.2f \n -20: %.2f \n -25: %.2f \n \
-30: %.2f \n -35: %.2f \n -40: %.2f \n -45: %.2f \n -50: %.2f \n -55: %.2f \n -60: %.2f \n" %
        (self.slam_obj.laser_dic["+60"], self.slam_obj.laser_dic["+55"],
        self.slam_obj.laser_dic["+50"], self.slam_obj.laser_dic["+45"], 
        self.slam_obj.laser_dic["+40"], self.slam_obj.laser_dic["+35"], 
        self.slam_obj.laser_dic["+30"], self.slam_obj.laser_dic["+25"],
        self.slam_obj.laser_dic["+20"], self.slam_obj.laser_dic["+15"], 
        self.slam_obj.laser_dic["+10"], self.slam_obj.laser_dic["+5"], 
        self.slam_obj.laser_dic["0"], self.slam_obj.laser_dic["-5"],
        self.slam_obj.laser_dic["-10"], self.slam_obj.laser_dic["-15"],
        self.slam_obj.laser_dic["-20"],
        self.slam_obj.laser_dic["-25"], self.slam_obj.laser_dic["-30"],
        self.slam_obj.laser_dic["-35"], self.slam_obj.laser_dic["-40"],
        self.slam_obj.laser_dic["-45"], self.slam_obj.laser_dic["-50"],
        self.slam_obj.laser_dic["-55"], self.slam_obj.laser_dic["-60"]))

    def getXYZ(self):
        """
            returns a string of the actual position like 
            'x: value, y: value, z : value'
        """

        return "X: %.2f Y: %.2f Z: %.2f "\
        % (self.character.getX(), self.character.getY(), self.character.getZ())
    #--------------------------------------------------
    def getInfos(self):
        """ returns odometer data """
        if (self.distance_laser == None):
            return "Odometer: %.2f Laser: %s"\
            %( self.robot.getSensor("odometer", 0), self.distance_laser)
        else:
            return "Odometer: %.2f" % self.robot.getSensor("odometer", 0)

    def seeTheWay(self):
        """ see the way to walk """
        actualH = self.character.getH()
        newH = self.slam_obj.biggerDictionaryKey(self.slam_obj.laser_dic)
        rotation = float(newH)
        newH = actualH + float(newH)
        self.character.setHpr(newH, 0, 0)
        return rotation

       
    def doTest(self):
        #print self.character.getH() % 360
        # angle = '+60'

        print self.robot.graph_steps_dic

envi = Environment()
run()
