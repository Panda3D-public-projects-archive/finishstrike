#abstract class
class Agent():
    sensors = {} #lasers, odometer, sonar, camera...
    position = (0, 0) # (x, y)
    rotation = 0    
    graph_steps_dic = {}
    
    #abstract method
    def getSensor(self, sensor_type, id):
        pass
        
    #abstract method
    def setSensor(self, sensor_type, id, value):
        pass    
