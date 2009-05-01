class LinearRegression:

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