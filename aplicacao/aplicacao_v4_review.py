from direct.gui.OnscreenText import OnscreenText
from framework.GraphFacade import *
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *
import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.task import Task
from direct.interval.IntervalGlobal import *
from robot import *

class Environment(DirectObject):
	""" This class works with environments details """

	def __init__(self):
	
		# show the text on screen
		self.title = OnscreenText(pos=(0.8, -0.95))
		# load the environment model
		self.environment = loader.loadModel("./modelos/[modelo] novo galpao.egg")
		# load the actor from module Robot
		self.robot = Robot().robot
		# adjusting scale and position of the model
		self.environment.setScale(10, 10, 10)
		self.environment.setPos(0, 0, 0)
		self.robot.setScale(5, 5, 5)
		self.robot.setPos(0, 0, -2)
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
	#--------------------------------------------------
		
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

		# If a move-key is pressed, move robot in the specified direction.

		if (self.keyMap["left"]!=0):
				self.robot.setH(self.robot.getH() + elapsed*200)
		if (self.keyMap["right"]!=0):
				self.robot.setH(self.robot.getH() - elapsed*200)
		if (self.keyMap["forward"]!=0):
				backward = self.robot.getNetTransform().getMat().getRow3(1)
				backward.normalize()
				self.robot.setPos(self.robot.getPos() - backward*(elapsed*50))

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

		# Store the task time and continue.
		self.prevtime = task.time
		return Task.cont
	#--------------------------------------------------
	
	def printXYZ(self, task):
		""" prints the X, Y, Z position of the actor """

		self.title.setText(self.getXYZ())
		return Task.cont
	#--------------------------------------------------

	def getXYZ(self):
		"""
			returns a string of the actual position like 'x: value, y: value, z:
			value'
		"""
		
		return "X: %.2f Y: %.2f Z: %.2f" \
		% (self.robot.getX(), self.robot.getY(), self.robot.getZ())
	#--------------------------------------------------

a = Environment()
run()
