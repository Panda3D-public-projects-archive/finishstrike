#abstract class
class Agent():
    sensors = {} #lasers, odometer, sonar, camera...
    position = (0, 0, 0)
        
    #abstract method
    def getSensor(self, sensor_type, id):
        pass
        
    #abstract method
    def setSensor(self, sensor_type, id, value):
        pass
