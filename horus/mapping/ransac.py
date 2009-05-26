import sys
import random
from horus.core.math.math_module import *

class Ransac():

    def __init__(self):
        self.data = None
        self.minValuesPoint = 3 # o valor ideal e 8
        self.maxInterations = 20 # ideal 40
        self.valueGoodFit = 0.9  # valor ideal e 0.5
        self.iterations = 0
        self.bestfit = None # modelo de melhor ajuste. class: LinearRegression()
        self.destError = None # valor do erro do modelo com menor taxa de erro

    def getBestFitModel(self, listPoint):
        self.data = listPoint
        self.destError = sys.maxint
        while self.iterations < self.maxInterations and self.destError >= self.valueGoodFit:
            maybeinliers = self.randomlySelectedValues(self.data)
            maybemodel = self.modelBestFits(maybeinliers)
            alsoinliers = []
            rejectedlist = filter(lambda x: x not in maybeinliers, self.data)
            alsoinliers = self.searchItemsFitModel(rejectedlist, maybemodel)

            if len(alsoinliers) > self.minValuesPoint:
              newlist = maybeinliers.__iadd__(alsoinliers)
              betterModel = self.modelBestFits(newlist)

              modelError = betterModel.getError()

              if modelError < self.destError:
                self.bestfit = betterModel
                self.destError = modelError

            self.iterations+=1

        return self.bestfit

    def randomlySelectedValues(self, listPoint):
        randomValues = random.sample(listPoint, self.minValuesPoint)
        return randomValues

    def modelBestFits(self, listPoint):
        """ uses LinearRegression to identify a model"""
        
        model = LinearRegression(listPoint)
        return model

    def searchItemsFitModel(self, listPoint, model):
        itemsFitModel = []
        for point in listPoint:
            if model.getErrorRatePoint(point) <= self.valueGoodFit:
              itemsFitModel.append(point)
        return itemsFitModel
        
