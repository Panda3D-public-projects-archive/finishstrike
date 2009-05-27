import unittest
from horus.core.math import math_module  

class TrigonometryTest(unittest.TestCase):
    
    def test_getXCateto(self):
        hypotenuse = 1
        angle = 60
        angle2 = 30
        to = math_module.Trigonometry()
        self.assertAlmostEqual(to.getXCateto(hypotenuse, angle), .5)
        self.assertAlmostEqual(to.getYCateto(hypotenuse, angle2), .5)

class LinearRegressionTest(unittest.TestCase):
        
    def test_getAlpha(self):
        #to this list alpha must be 0
        list = [(1,3),(2,3),(3,3),(4,3)]
        #to this list alpha must be 2
        list2 = [(1,3),(2,5),(3,7),(4,9)]

        lr = math_module.LinearRegression(list)
        self.assertEqual(0, lr.getAlpha())

        lr = math_module.LinearRegression(list2)
        self.assertEqual(2, lr.getAlpha())

    def test_getBeta(self):
        #to this list beta must be 3
        list = [(1,3),(2,3),(3,3),(4,3)]
        #to this list beta must be 1
        list2 = [(1,3),(2,5),(3,7),(4,9)]

        lr = math_module.LinearRegression(list)
        self.assertEqual(3, lr.getBeta())

        lr = math_module.LinearRegression(list2)
        self.assertEqual(1, lr.getBeta())

    def test_getError(self):
        list = [(1,3),(2,3),(3,3),(4,3)]
        lr = math_module.LinearRegression(list)
        self.assertEqual(0, lr.getError())


if __name__ == '__main__':
    unittest.main()

        
