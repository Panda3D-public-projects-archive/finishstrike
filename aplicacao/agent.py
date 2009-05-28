#abstract class
class Agent():
    #lasers, odometer, sonar, camera...
    sensors = {}
    # (x, y)
    position = (0, 0)
    rotation = 0
    #max robot steps
    step = 25
    graph_steps_dic = {}
    
    #abstract method
    def getSensor(self, sensor_type, id):
        pass
        
    #abstract method
    def setSensor(self, sensor_type, id, value):
        pass    
