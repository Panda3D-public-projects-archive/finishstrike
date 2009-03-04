# -*- coding: cp1252 -*-
from priodict import PriorityDictionary

def Dijkstra(graph, start, end=None):
	"""
		Finds the best way between two vertexes
	"""
	distance_dic = {}
	previous_dic = {}
	priority_dic = PriorityDictionary()
	priority_dic[start] = 0
	
	for value in priority_dic:
		distance_dic[value] = priority_dic[value]
		if value == end:
			break
		
		for w in graph[value]:
			vw_length = distance_dic[value] + graph[value][w]
			if w in distance_dic:
				if vw_length < distance_dic[w]:
					raise ValueError, """Dijkstra"""
				elif w not in priority_dic or vw_length < priority_dic[w]:
					priority_dic[w] = vw_length
					previous_dic[w] = value
		
		return (distance_dic, previous_dic)
	
	
	def findAllPaths(graph, start, end, path=[]):
		"""
			Finds all possibles paths
		"""
		path = path + [start]
		if start == end:
			return [path]
		if not graph.has_key(start):
			return []
		paths = []
		for node in graph[start]:
			if node not in path:
				newpaths = findAllPaths(graph, node, end, path)
				for newpath in newpaths:
					paths.append(newpath)
		return paths
	
	def shortestPath(graph, start, end):
		"""
			Finds the shortest path based on Dijkstra
		"""  
		distance_dic, previous_dic = Dijkstra(graph, start, end)
		path_dic = []
		while 1:
			path_dic.append(end)
			if end == start:
				break
			end = previous_dic[end]
		path_dic.reverse()
		return path_dic
