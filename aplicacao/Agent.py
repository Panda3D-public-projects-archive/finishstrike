#abstract class
class Agent():
    """  """
    #lasers, odometer, sonar, camera...
    sensors = {}
    #coord (x, y)
    position = (0, 0)
    #angle
    rotation = 0
    graph_steps_dic = {}
    
    def getSensor(self, sensor_type, id):
        pass
        
    def setSensor(self, sensor_type, id, value):
        pass    
