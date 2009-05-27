import math

class Trigonometry():
    
    def getXCateto(self, hypotenuse, angle):
        cateto = math.cos(math.radians(angle))*hypotenuse
        return cateto

    def getYCateto(self, hypotenuse, angle):
        cateto = math.sin(math.radians(angle))*hypotenuse
        return cateto

class LinearRegression:

    def __init__(self, pointlist):
        # pointlist deve ser uma lista de pares (x, y)
        self.pointlist = pointlist
        self.alpha = None
        self.beta = None
        self.error = None
        self.sumX = None    # somatorio dos valores de x em pointlist
        self.sumXX = None   #somatorio dos valores de x**2 em pointlist
        self.sumY = None    #somatorio de y em pointlist
        self.sumXY = None   #somatorio de x*y em pointlist
        self.confidenceIntervals = None
        self.__calculateSum()

    def __calculateSum(self):
        """ Calculo dos somatorios """
        self.sumX = sum([e[0] for e in self.pointlist])
        self.sumXX = sum([e[0] ** 2 for e in self.pointlist])
        self.sumY = sum([e[1] for e in self.pointlist])
        self.sumXY = sum ([e[0] * e[1] for e in self.pointlist])

    def getBeta(self):
        """
            E outra constante, que representa o declive da reta;
            e o valor de `b` na funcao f(x) = ax + b
        """
        if self.beta is None:
          # sumy * sumxx - sumx*y * sumx
          num = self.sumY * self.sumXX - self.sumXY * self.sumX
          # sizelist * sumx**2 - (sumx)**2
          den = len(self.pointlist) * self.sumXX - self.sumX**2
          self.beta = 0
          if den is not 0:
            self.beta = num / den

        return self.beta

    def getAlpha(self):
        """
            E uma constante, que representa a interceptacao da reta com o eixo vertical;
            e o valor de `a` na funcao f(x) = ax + b
        """
        if self.alpha is None:
          # sizelist * sumY*X - sumX * sumY
          num = len(self.pointlist) * self.sumXY - self.sumX * self.sumY
          # sizelist * sumXX - sumX**2
          den = len(self.pointlist) * self.sumXX - self.sumX**2
          self.alpha = 0
          if den is not 0:
            self.alpha = num / den

        return self.alpha 

    def getError(self):
        """
           Soma dos quadrados dos erros 
        """
        if self.error is None:
          alpha = self.getAlpha()
          beta = self.getBeta()
          self.error = sum([((alpha * e[0] + beta) - e[1])**2 for e in self.pointlist])

        return self.error

    def getConfidenceIntervals(self, point):
        """
          em fase de teste
        """
        if self.confidenceIntervals is None:
          pointlist = self.pointlist
          extimateBeta = self.getBeta() - point
          averageX = self.sumX / len(self.pointlist)
          n = math.sqrt(len(self.pointlist) - 2)
          #somatorio do quadrado da diferenca entre x e medianX
          differenceXaverageX = sum([(e[0] - averageX)**2 for e in pointlist])
          erro = math.sqrt(self.getError())
          confidence = 0
          if erro is not 0 :
            confidence = (extimateBeta * n * differenceXaverageX) / erro
          self.confidenceIntervals = confidence

        return self.confidenceIntervals

    def getErrorRatePoint(self, point):
        """
           taxa de errro de um ponto
        """
        alpha = self.getAlpha()
        beta = self.getBeta()
        erro = self.getError()
        averateErro = erro/len(self.pointlist)
        rateErroPoint = point[0]*alpha + beta
        erroPoint = rateErroPoint - point[1]
        return abs(erroPoint) + averateErro
