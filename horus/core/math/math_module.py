import math

class Trigonometry():
    
    def getXCateto(self, hypotenuse, angle):
        cateto = math.cos(math.radians(angle))*hypotenuse
        return cateto

    def getYCateto(self, hypotenuse, angle):
        cateto = math.sin(math.radians(angle))*hypotenuse
        return cateto

class LinearRegression():
    """ 
        this class gets X, Y points and makes a line between this points
        structure: LinearRegression(list), where list is a tuple of values
        like [(x1, y1),(x2,y2),...,(xn,yn)]
    """
    def __init__(self, pointlist):
        # pointlist must be pairs (x, y)
        self.pointlist = pointlist
        self.alpha = None
        self.beta = None
        self.error = None
        self.sumX = None    # sum x in pointlist
        self.sumXX = None   #sum x**2 in pointlist
        self.sumY = None    #sum y in pointlist
        self.sumXY = None   #sum x*y in pointlist

    def __calculateSum(self):
        """ Calculo dos somatorios """
        self.sumX = sum([e[0] for e in self.pointlist])
        self.sumXX = sum([e[0] ** 2 for e in self.pointlist])
        self.sumY = sum([e[1] for e in self.pointlist])
        self.sumXY = sum ([e[0] * e[1] for e in self.pointlist])

    def getBeta(self):
        """
            get beta value.
            contant 'b' in function f(x) = ax + b
        """
        if self.beta is None:
          self.__calculateSum()
          # sumy * sumxx - sumx*y * sumx
          num = self.sumY * self.sumXX - self.sumXY * self.sumX
          # sizelist * sumx**2 - (sumx)**2
          den = len(self.pointlist) * self.sumXX - self.sumX**2
          self.beta = num / den

        return self.beta

    def getAlpha(self):
        """
            get alpha value.
            contant 'a' in function f(x) = ax + b
        """
        if self.alpha is None:
          self.__calculateSum()
          # sizelist * sumY*X - sumX * sumY
          num = len(self.pointlist) * self.sumXY - self.sumX * self.sumY
          # sizelist * sumXX - sumX**2
          den = len(self.pointlist) * self.sumXX - self.sumX**2        
          self.alpha = num / den

        return self.alpha 

    def getError(self):
        """
           i dont know how to explain 
        """
        if self.error is None:
          pointlist = self.pointlist
          alpha = self.getAlpha()
          beta = self.getBeta()
          comprehension = [((alpha * e[0] + beta) - e[1])**2 for e in pointlist]
          self.error = sum(comprehension)

        return self.error
    
    def getConfidenceIntervals(self, point):
        """
          in test phase
        """
        if self.confidenceIntervals is None:
          self.__calculateSum()
          pointlist = self.pointlist
          extimateBeta = self.getBeta() - point
          averageX = self.sumX / len(self.pointlist)
          n = sqrt(len(self.pointlist) - 2)
          #somatorio do quadrado da diferenca entre x e medianX
          differenceXaverageX = sum([(e[0] - averageX)**2 for e in pointlist])
          erro = sqrt(self.getError())
          confidence = 0
          if erro > 0 :
            confidence = (extimateBeta * n * differenceXaverageX) / erro
          self.confidenceIntervals = confidence

        return self.confidenceIntervals

    def getErrorRatePoint(self, point):
        """
           error rate
        """
        alpha = self.getAlpha()
        beta = self.getBeta()
        erro = self.getError()
        averateErro = erro/len(self.pointlist)
        rateErroPoint = (point[0]*alpha + beta)
        erroPoint = rateErroPoint - point[1]
        return abs(erroPoint) + averateErro