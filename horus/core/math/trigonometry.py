import math
class Trigonometry():

    def getXCateto(self, hypotenuse, angle):
        cateto = math.cos(angle)*hypotenuse
        return cateto
    
    def getYCateto(self, hypotenuse, angle):
        cateto = math.sin(angle)*hypotenuse
        return cateto