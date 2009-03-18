# -*- coding: cp1252 -*-
from direct.gui.OnscreenText import OnscreenText
from framework.GraphFacade import *
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *
import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.task import Task
from direct.interval.IntervalGlobal import *
from robot import *

#Cria o Traverser, no "base"
base.cTrav = CollisionTraverser()
#Cria o Pusher, no "base"
base.pusher = CollisionHandlerPusher()
#Cria o Floor, "base" também
base.floor = CollisionHandlerFloor()
base.floor.setMaxVelocity(1)
#Cria o Laser
base.laser = CollisionHandlerQueue()

class Environment(DirectObject):
	""" This class works with environments details """

	def __init__(self):
		# show the text on screen
		self.title = OnscreenText(pos=(0.8, -0.85), fg=(255, 255, 0, 90))
		self.title2 = OnscreenText(pos=(0.8, -0.95), fg=(255, 255, 0, 90))
		# load the environment model
		self.environment = loader.loadModel("./modelos/[modelo] novo galpao.egg")
		# load the actor from module Robot
		self.robot = Robot().robot
		self.odometer = 0
		self.distanceLaser = self.robot
		self.threshold = 0.9852941
		# adjusting scale and position of the model
		self.environment.setScale(10, 10, 10)
		self.environment.setPos(0, 0, 2.01)
		self.robot.setScale(5, 5, 5)
		self.robot.setPos(0, 0, 0)
		# render
		self.environment.reparentTo(render)
		self.robot.reparentTo(render)
		# building a graph with GraphFacade
		self.graph = \
		GraphFacade().getGraph("./modelos/nos.txt", "./modelos/arestas.txt")	
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
		self.accept("p",      self.walkAway,["no1", "no9"])
	#--------------------------------------------------
		# game's aspect in initial state
		self.prevtime = 0
		self.isMoving = False
		self.floater = NodePath(PandaNode("floater"))
		self.floater.reparentTo(render)	
		base.disableMouse()
		base.camera.setPos(self.robot.getX(), self.robot.getY()+200, 500)
		taskMgr.add(self.printXYZ, "printXYZTask")
		# add a movement event in the environment
		taskMgr.add(self.move,"moveTask")
		# build a sequence of movements 
		self.walk = Sequence()


                self.createColliders()
	#--------------------------------------------------
	# collision

        def createColliders(self):
                #create the collision sphere
                self.robotSphereCN = CollisionNode('robotSphere')
                self.robotSphereCN.addSolid(CollisionSphere(0,0,3,2) )
                self.robotEsfNP = self.robot.attachNewNode(self.robotSphereCN)
                self.robotEsfNP.show()
                base.cTrav.addCollider(self.robotEsfNP, base.pusher)
                base.pusher.addCollider(self.robotEsfNP, self.robot)
                        
                #configuracao do ray de colisao do robo
                self.robotGroundRay = CollisionRay()
                self.robotGroundRay.setOrigin(0,0,10)
                self.robotGroundRay.setDirection(0,0,-1)
                self.robotGroundCol = CollisionNode('robotRay')
                self.robotGroundCol.addSolid(self.robotGroundRay)
                self.robotGroundColNp = self.robot.attachNewNode(self.robotGroundCol)
                self.robotGroundColNp.show()
                base.cTrav.addCollider(self.robotGroundColNp, base.floor)
                base.floor.addCollider(self.robotGroundColNp, self.robot)
                
                #para o laser    
                self.laser  = CollisionSegment (0, 0, 0, 0,-30,0) 
                self.laserNode = CollisionNode ('laserNode')
                self.laserNodePath = self.robot.attachNewNode(self.laserNode)
                self.laserNodePath.node().addSolid(self.laser)
                self.laserNodePath.show()
                base.cTrav.addCollider(self.laserNodePath, base.laser)
            

                base.cTrav.showCollisions(render)
                base.cTrav.traverse(render)



	def addInterval(self, posInicial, posFinal):
		"""
			This method adds a time interval between two vertexes for the sequence
			movement
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
		"""	set a value within the key into keyMap """

		self.keyMap[key] = value
	#--------------------------------------------------

	def move(self, task):
		""" allow the keyboard movement """

		elapsed = task.time - self.prevtime
                beforePosition = {"X":self.robot.getX(), "Y":self.robot.getY(), "Z":self.robot.getZ()}
		# If a move-key is pressed, move robot in the specified direction.

		if (self.keyMap["left"]!=0):
				self.robot.setH(self.robot.getH() + elapsed*200)
		if (self.keyMap["right"]!=0):
				self.robot.setH(self.robot.getH() - elapsed*200)
		if (self.keyMap["forward"]!=0):
				backward = self.robot.getNetTransform().getMat().getRow3(1)
				backward.normalize()
				self.robot.setPos(self.robot.getPos() - backward*(elapsed*50))
				#The odometer accumulates the value of the distance
				#between its previous position until his current position.
				self.odometer += self.threshold*sqrt((self.robot.getX()-beforePosition["X"])**2 + (self.robot.getY()-beforePosition["Y"])**2 + (self.robot.getZ()-beforePosition["Z"])**2)

		# If robot is moving, loop the run animation.
		# If he is standing still, stop the animation.
		if (self.keyMap["forward"]!=0) or (self.keyMap["left"]!=0) or \
		(self.keyMap["right"]!=0):
				if self.isMoving is False:
						self.robot.loop("run")
						self.isMoving = True
		else:
				if self.isMoving:
						self.robot.stop()
						self.robot.pose("walk", 5)
						self.isMoving = False

		self.floater.setPos(self.robot.getPos())
		self.floater.setZ(self.robot.getZ() + 10)
		base.camera.lookAt(self.floater)
                entries=[]
                entry=0
                base.laser.sortEntries()
                for i in range(base.laser.getNumEntries()):
                        entry = base.laser.getEntry(i)
                        entries.append(entry)

                if (len(entries)>1):
   			self.distanceLaser = entries[1].getSurfacePoint(render)
			self.getXYZ()
                else:
                        self.distanceLaser = "INFINITO"

		# Store the task time and continue.
		self.prevtime = task.time
		return Task.cont
	#--------------------------------------------------

	def printXYZ(self, task):
		""" prints the X, Y, Z position of the actor """

		self.title.setText(self.getXYZ())
		self.title2.setText(self.getInfos())
		return Task.cont
	#--------------------------------------------------

	def getXYZ(self):
		"""
			returns a string of the actual position like 'x: value, y: value, z:
			value'
		"""

		return "X: %.2f Y: %.2f Z: %.2f "\
		% (self.robot.getX(), self.robot.getY(), self.robot.getZ())
	#--------------------------------------------------
        def getInfos(self):
                """
                        returns a string of the actual position like 'x: value, y: value, z:
                        value'
                """
                if (self.distanceLaser == "INFINITO"):
                        return "Odometer: %.2f Laser: %s"\
                        %( self.odometer, self.distanceLaser)
                else:
                        return "Odometer: %.2f Laser: %.1f"\
                        %( self.odometer, sqrt( (self.robot. getPos().getX() - self.distanceLaser.getX())**2 +(self.robot. getPos().getY() - self.distanceLaser.getY())**2+( self.robot. getPos().getZ() - self.distanceLaser.getZ())**2)-10)

a = Environment()
run()
