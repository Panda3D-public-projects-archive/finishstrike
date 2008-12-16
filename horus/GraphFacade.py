from Graph import *

class GraphFacade():
	""" makes easy to use the Graph class """
	def getGraph(self, vertex_path, edge_path):
		""" returns a new graph """
		return Graph(vertex_path, edge_path)
