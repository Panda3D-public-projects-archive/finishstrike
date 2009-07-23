class Math(object):
    """
        TODO
    """

    def calculateTranspose(self, matrix):
        """
            This method calculates the transpose of a matrix.
            
            For example:
            matrix = [[1, 2, 3], [4, 5, 6]]
            new_matrix = [[1, 4], [2, 5], [3, 6]]
        """
        new_matrix = [[0 for i in range(len(matrix))] \
                         for j in range(len(matrix[0])) ]
        
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                new_matrix[j][i] = matrix[i][j]
                
        return new_matrix

    def calculateDerivative(self, projection, h):
        """
            TODO
        """   
        derivative = [0 for i in range(len(projection))]

        for i in range(len(projection)):
            derivative[i] = (projection[i] - projection[i-h]) / h

        return derivative

class List(list):
    """
        This class add method in list objects
    """

    def maxValue(self):
        """
            Return the first index of maximal value of a value's list 
        """   
        return max(self)

    def minValue(self):
        """
            Return the first index of minimal value of a value's list 
        """   
        return min(self)

    def sumValues(self):
        """
            Return the sum of values of list passed by parameter
        """ 
        return sum(self)

    def calculateAvarage(self):
        """
            Return the avarage of values
        """   
        return sum(self) / len(self)
    
   
    def applyThreshold(self, threshold):
        """
            Values below the threshold is reset with zero.
        """   
        def choice(number):
            if number < threshold:
                return 0
            else:
                return number

        return List(map(choice, self))

    def applyBlur(self, sensibility = 0.01):
        """
            Smooth the variation of values of list
        """
        for i in range(len(self)):
            neighboors = List( self[ (i - int(len(self) * sensibility / 2) ): ]\
                                     [ :int( len(self) * sensibility ) ] )
            self[i] = neighboors.calculateAvarage()
        return self

    def locateNonZeroIntervals(self):
        """
            cria uma lista distacando os intervalos (os pares com o indice
            inicial e final definem o intervalo) diferentes de zeros.
        """
        import copy
        value_list = copy.copy(self)
        value_list[0] = value_list[-1] = 0
        
        nonzero_interval_list = []
        inf = 0
        # cria uma lista de candidatos a placas
        # intervalos de valores diferentes de zero
        for i in range(len(value_list)):
            if value_list[i] != 0:
                if inf == 0:
                    if value_list[i-1] == 0:
                        inf = i
                else:
                    if i+1 < len(value_list) and value_list[i+1] == 0:
                        nonzero_interval_list.append((inf, i))
                        inf = 0
        return nonzero_interval_list
    
    def removeSmallIntervals(self, lenght):             
        for intervals in self:
            if intervals[1] - intervals[0] < lenght:
                self.remove(intervals)
        return self