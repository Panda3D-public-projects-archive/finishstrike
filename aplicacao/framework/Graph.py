# -*- coding: cp1252 -*-
from math import sqrt
from priodict import PriorityDictionary

class Graph():
    """
        The graph object has the know-how to work with a graph file.
    """
    def __init__(self, vertexes_file, edge_file):
        """
            A graph object is initialized with a vertex dictionary and two
            files: a vertexes file and an edges file
        """
        self.vertex_dic = {}
        try:
            self.vertexes_file = open(vertexes_file,'r')
            self.edges_file = open(edge_file,'r')

        except IOError:
            print "ATENTION: File not found!!!"

    def buildVertexDic(self):
        """ Method responsable for the contruction of a vertex dictonary  """
        vertex_aux_dic=[]
        line_lists = self.vertexes_file.readlines()
        self.vertexes_file.close()
        for line in line_lists:
            vertex_aux_dic = line.split()
            vertex = vertex_aux_dic[0]
            vertexX = float(vertex_aux_dic[1])
            vertexY = float(vertex_aux_dic[2])
            vertexZ = float(vertex_aux_dic[3])
            self.vertex_dic[vertex]=[vertexX, vertexY, vertexZ]

    def buildAdjMatrix(self):
        """ Method responsable for the contruction of a adjoining matrix """
        adj_matrix_dict = {}
        line_lists = self.edges_file.readlines()
        self.edges_file.close()
        for line in line_lists:
            edgeAux = line.split()
            no1_x = self.vertex_dic[edgeAux[0]][0]
            no1_y = self.vertex_dic[edgeAux[0]][1]
            no1_z = self.vertex_dic[edgeAux[0]][2]
            no2_x = self.vertex_dic[edgeAux[1]][0]
            no2_y = self.vertex_dic[edgeAux[1]][1]
            no2_z = self.vertex_dic[edgeAux[1]][2]
            edge_weight = sqrt(((no1_x-no2_x)**2)+
                ((no1_x-no2_x)**2)+((no1_x-no2_x)**2))
            if not(adj_matrix_dict.has_key(edgeAux[0])):
                adj_matrix_dict[edgeAux[0]] = {edgeAux[1]:edge_weight}
            else:
                adj_matrix_dict_Aux = adj_matrix_dict.pop(edgeAux[0])
                adj_matrix_dict_Aux[edgeAux[1]]=edge_weight
                adj_matrix_dict[edgeAux[0]] = adj_matrix_dict_Aux
        return adj_matrix_dict

    def getPositionVertex(self,vertex):
        """ returns the 'x', 'y' and 'z' position of a specific vertex """

        return self.vertex_dic[str(vertex)]


    def dijkstra(self,graph,start,end=None):
        """
            Finds the minor path between two vertexes
            The graph parameter is a dictionary witch the index is a vertex.
        """

        distance_dic = {}
        previous_dic = {}
        priority_dic = PriorityDictionary()
        priority_dic[start] = 0

        for v in priority_dic:
            distance_dic[v] = priority_dic[v]
            if v == end: break
            for w in graph[v]:
                vwLength = distance_dic[v] + graph[v][w]
                if w in distance_dic:
                    if vwLength < distance_dic[w]:
                        raise ValueError, "dijkstra"
                elif w not in priority_dic or vwLength < priority_dic[w]:
                    priority_dic[w] = vwLength
                    previous_dic[w] = v

        return (distance_dic,previous_dic)

    def getPathListInGraph(self,graph, start, end, path=[]):
        """    Finds all paths in graph """

        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_key(start):
            return []
        path_list = []
        for node in graph[start]:
            if node not in path:
                newpaths = getPathListInGraph(graph, node, end, path)
                for newpath in newpaths:
                    path_list.append(newpath)
        return path_list

    def shortestPath(self, graph, start, end):
        """
            Finds the shortest path using dijkstra.
        """
        distance_dic,previous_dic = self.dijkstra(graph,start,end)
        path_list = []
        while 1:
            path_list.append(end)
            if end == start:
                break
            end = previous_dic[end]
        path_list.reverse()
        return path_list
