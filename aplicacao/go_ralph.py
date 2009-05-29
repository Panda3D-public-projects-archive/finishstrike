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

base.node_path_list = []
base.collision_node_list = []
base.laser_list = []

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
        
        base.bufferViewer.setCardSize(0.8, 0)
        mainWindow = base.win
        base.altBuffer = mainWindow.makeTextureBuffer("hello", 256, 256)
        

        base.first_vision_camera = base.makeCamera(base.altBuffer)
        base.first_vision_camera.reparentTo(render)
     
     #Create lasers
        for i in range(25):
            base.laser_list.append(CollisionHandlerQueue())
    
        # this is the robot dictionary lasers - keys is degrees
        # -60 to -5
        self.slam_obj = PandaSlam()
        for i in range(60, 0, -5):
            self.slam_obj.laserUpdate('+' + str(i), 0)
        
        # 0
        self.slam_obj.laserUpdate('0', 0)
        
        # -5 to -60
        for i in range(5,  61,  5):
            self.slam_obj.laserUpdate('-' + str(i), 0)
        
        # show the text on screen
        self.title = OnscreenText(pos=(0.8, -0.85), fg=(255, 255, 0, 90))
        self.title_odometer = \
            OnscreenText(pos=(0.8, -0.95), fg=(255, 255, 0, 90))
        self.title_lasers = OnscreenText(pos=(-1, 0.9), fg=(255, 255, 0, 90)) 
        self.title_lasers.setScale(.05)
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
        self.environment.setScale(20, 20, 20)
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
        self.accept("v", base.bufferViewer.toggleEnable)
    #--------------------------------------------------
        # game's aspect in initial state
        self.printLasersResult()
        self.prevtime = 0
        self.isMoving = False
        self.floater = NodePath(PandaNode("floater"))
        self.first_vision_floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)
        self.first_vision_floater.reparentTo(render)

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
            for i in range(25):
                node_name = 'laserNode' + str(i)
                base.node_path_list.append(self.character.attachNewNode(CollisionNode(node_name)))

             # each laser have its node_path
                node_path = base.node_path_list[i]
                node_path.node().addSolid(self.robot.getSensor("laser",i))
                
            #each laser is now collidible
                base.cTrav.addCollider(base.node_path_list[i], base.laser_list[i])

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
        #first_vision_camera adjusting
        hyp = 140
        catetoX = lambda angle: math.cos(math.radians(angle))*hyp
        catetoY = lambda angle: math.sin(math.radians(angle))*hyp
        self.first_vision_floater.setX(self.character.getX() + catetoX(self.character.getH()-90))
        self.first_vision_floater.setY(self.character.getY() + catetoY(self.character.getH()-90))
        self.first_vision_floater.setZ(self.character.getZ() + 20)
        base.first_vision_camera.setPos(self.character.getX(),  self.character.getY(),  45)
                
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
                if (odometer - last_odometer >= self.robot.step):
                    self.robot.setSensor("odometer", 1, odometer)
                    #base.cTrav.showCollisions(render)
                    self.getLasersDistance()
                    self.printLasersResult()
                    self.robot.rotation += self.seeTheWay()
                    self.robot.position = self.slam_obj.getRobotPosition(
                        odometer - last_odometer, self.robot.rotation, self.robot.position)
                    
                    self.slam_obj.landmarkExtraction(self.robot.position)
                    self.robot.graph_steps_dic[self.robot.position] = self.character.getPos()
                    self.robot.step = min(self.slam_obj.laser_dic.values())
               
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
        base.first_vision_camera.lookAt(self.first_vision_floater)

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
        # get negatives lasers reads (-60 to -5)
        j = 0
        for i in range(-60,  0,  5):
            d = self.getDistance(base.laser_list[j], str(i))
            j += 1
        
        # get zero laser read ( 0 )
        self.getDistance(base.laser_list[12] ,"0")
        
        # get positives lasers reads (+5 to +60)
        j = 13
        for i in range(5,  61,  5):
            self.getDistance(base.laser_list[j], '+'+str(i))
            j += 1
            
        
    
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
-30: %.2f \n -35: %.2f \n -40: %.2f \n -45: %.2f \n -50: %.2f \n -55: %.2f \n -60: %.2f"   % 
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
        if self.slam_obj.laser_dic[newH] <= 6:
            newH = float(newH) - 180
        #newH = self.slam_obj.closestDictionaryKey(self.slam_obj.laser_dic)
        rotation = float(newH)
        newH = actualH + float(newH)
        self.character.setHpr(newH, 0, 0)
        return rotation

       
    def doTest(self):
        #print self.character.getH() % 360
        # angle = '+60'
        base.camera.zoomCam(2)
        #print self.robot.graph_steps_dic

envi = Environment()
run()
