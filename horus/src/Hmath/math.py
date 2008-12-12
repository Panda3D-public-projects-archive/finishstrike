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
        #######################################################
        #### Verificar se esse procedimento ja e feito em  ####
        #### alguma api python com uma melhor performance  ####
        #######################################################
        new_matrix = [[0 for i in range(len(matrix))] \
                         for j in range(len(matrix[0])) ]
        
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                new_matrix[j][i] = matrix[i][j]
                
        return new_matrix

    def maxValue(self, values_list):
        """
            Return the first index of maximal value of a value's list 
        """   
        max_value = max(values_list)
        index_max_value = values_list.index(max_value)
        return index_max_value

    def minValue(self, values_list):
        """
            Return the first index of minimal value of a value's list 
        """   
        min_value = min(values_list)
        index_min_value = values_list.index(min_value)
        return index_min_value

    def sumValues(self, values_list):
        """
            Return the sum of values of list passed by parameter
        """ 
        return sum(values_list)

    def calculateDerivative(self, projection, h):
        """
            TODO
        """   
        derivative = [0 for i in range(len(projection))]

        for i in range(len(projection)):
            derivative[i] = (projection[i] - projection[i-h]) / h

        return derivative
        
    def calculateAvarage(self, values_list):
        """
            TODO
        """   
        return self.sumValues(values_list) / len(values_list)
    
    
class ImageMath(object):
    
    def __init__(self):
        self.math = Math()
    
    def calculateProjection(self, matrix):
        """
            This method calculates the vertical projection of image passed 
            by parameter image. To calculate horizontal projection just
            call this method passing pass as parameter image its transpose.
        """
        projection = [0 for i in range(len(matrix[0]))]
        for i in range(len(matrix[0])):
            for j in range(len(matrix)):
                projection[i] += matrix[j][i]
        return projection


    def calculateProjection2(self, matrix):
        """
            This method calculates the horizontal projection of image passed
            by parameter image. To calculate vertical projection just
            call this method passing pass as parameter image its transpose.
        """
        projection = [0 for i in range(len(matrix))]
        for i in range(len(matrix)):
            projection[i] = self.math.sumValues(matrix[i])
        return projection
