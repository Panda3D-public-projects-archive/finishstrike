import sys
import random
from horus.core.math.math_module import *
from exceptions import Exception

class Ransac():

    def __init__(self, regression = LinearRegression):

        self.minValuesPoint = 3 # o valor ideal e 8
        self.maxInterations = 20 # ideal 40
        self.valueGoodFit = 0.9  # valor ideal e 0.5
        self.regression = regression

    def getBestFitModel(self, listPoint,  landmark_oid):

        data = listPoint
        bestError = sys.maxint # valor do erro do modelo com menor taxa de erro
        bestfit = None # modelo de melhor ajuste. class: LinearRegression()
        iterations = 0

        while iterations < self.maxInterations and bestError >= self.valueGoodFit:
            maybeinliers = self.randomlySelectedValues(data)
            maybemodel = self.modelBestFits(maybeinliers)
            alsoinliers = []
            rejectedlist = filter(lambda x: x not in maybeinliers, data)
            alsoinliers = self.searchItemsFitModel(rejectedlist, maybemodel)

            if len(alsoinliers) > self.minValuesPoint:
              maybeinliers.__iadd__(alsoinliers)
              betterModel = self.modelBestFits(maybeinliers)

              modelError = betterModel.getError()

              if modelError < bestError:
                bestfit = betterModel
                bestError = modelError

            iterations+=1

        if bestfit is None:
            raise CurveNotFound()

        return Landmark(landmark_oid,  bestfit)

    def randomlySelectedValues(self, listPoint):
        randomValues = random.sample(listPoint, self.minValuesPoint)
        return randomValues

    def modelBestFits(self, listPoint):
        """ uses Regression to identify a model"""
        model = self.regression(listPoint)
        return model

    def searchItemsFitModel(self, listPoint, model):
        itemsFitModel = []
        for point in listPoint:
            if model.getErrorRatePoint(point) <= self.valueGoodFit:
              itemsFitModel.append(point)
        return itemsFitModel


class CurveNotFound(Exception):
  	
   	def __str__(self):
   		print "","modify the type of regression and try again"
