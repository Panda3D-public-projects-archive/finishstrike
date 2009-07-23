class Statistical(object):

    def centroide(self, value_matrix):
        if not isinstance(value_matrix[0], list):
            return self.avarage(value_matrix)
        else:
            centroide = []
            for i in range(len(value_matrix[0])):
                centroide.append(self.avarage([value_matrix[j][i] for j in range(len(value_matrix))]))
            return centroide
            
    def avarage(self, value_list):
        return float( sum (value_list) ) / len(value_list)
    
    def multidimensionalVariance(self, sampling):
        variance_matrix = []
        for i in range(len(sampling[0])):
            variance_matrix.append( self.singularVariance( [sampling[j][i] for j in range(len(sampling))] ) )
        return transpose(variance_matrix)

    def singularVariance(self, sampling):
        avarage_value = self.avarage(sampling)
        variance_list = []
        for value in sampling:
            variance_list.append(value - avarage_value)
        return variance_list

    def variance(self, sampling):
        if isinstance(sampling[0],list):
            return self.multidimensionalVariance(sampling)
        else:
            return self.singularVariance(sampling)
        
    def covariance(self, value_list):
        variance = self.variance(value_list)
        return multiplicationMatrix(transpose(variance), variance)