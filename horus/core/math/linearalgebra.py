from math import sqrt

NUMERIC_TYPES = [int, float, long, complex]

class ImpossibilityMultiplicationMatrixException(Exception): 
    """
        This Exception is generated when checked two matrix to do a multiply 
        and the columns leght of the first is different of the rows lenght
        of the second.
    """
    pass


class ImpossibilityMultiplicationVectorsException(Exception): 
    """
        This Exception is generated when the vectors checked don't have a
        same lenght.
    """
    pass


class IncompatibleLenghtVectorMatrixException(Exception): 
    """
        TODO
    """
    pass


class ImpossibilityMultiplicationVectorMatrixException(Exception): 
    """
        TODO
    """
    pass

#TODO - remover essa excecao e substitui-la por NonNumericError
class ElementNonNumericError(Exception): 
    """
        This Exception is generated when the element checked is not
        a number (int or float)
    """
    pass


class NotIsMatrixException(Exception): 
    """
        This Exception is generated when the element checked have row with
        lenght different of the others rows.
    """
    pass

class NonVectorError(Exception): 
    """
        This Exception is generated when the element checked is not a vector.
    """
    pass
    
class NonNumericError(Exception): 
    """
        This Exception is generated when the element checked is not
        a number (int or float)
    """
    pass    
    
class DifferentDimensionError(Exception): 
    """
        This Exception is generated when try operate (+, -, *, /, innerProduct,
        vectorialProduct) two vectors of different dimensions.
    """
    pass        

class NonVectorComparableError(Exception): 
    """
        This Exception is generated when try compare a Vector with object that 
        isn't other vector or a list.
    """
    pass      
    
class NonVectorOperableError(Exception): 
    """
        This Exception is generated when try operate (+, -, innerProduct,
        vectorialProduct) a Vector with object that isn't other intance of the 
        Vector or a list.
    """
    pass
    
    
class NonMatrixError(Exception): 
    """
        This Exception is generated when the element checked is not a matrix.
    """
    pass    
    

class NonMatrixComparableError(Exception): 
    """
        This Exception is generated when try compare a Matrix with object that 
        isn't other matrix or a list of list.
    """
    pass
    

class NonMatrixOperableError(Exception): 
    """
        This Exception is generated when try operate (+, -, *) a Matrix with    
        object that isn't other intance of the Matrix or a list of list.
    """
    pass


def isVector(vector):
    """
        This function verifies if a object is an instance of class Vector, or
        can be an instance of that class.
        
        Examples:
        >>> isVector('a')
        NonVectorError
        >>> isVector(Matrix([[1,2],[3,4]])
        NonVectorError
        >>> isVector([1, 'a'])
        NonNumericError
        >>> isVector([1,2,3])
        True
        >>> isVector(Vector([1,2,3]))
        True
    """
    if isinstance(vector, Vector):
        return True
    elif isinstance(vector, list) and (not isinstance(vector, Matrix)):
        for i in range(len(vector)):
            if not type(vector[i]) in NUMERIC_TYPES:
                raise NonNumericError
        return True
    else:
        raise NonVectorError
            
def isMatrix(matrix):
    """
        This function verifies if a object is an instance of class Matrix, or
        can be an instance of that class.
        
        Examples:
        >>> isMatrix('a')
        NonMatrixError
        >>> isMatrix( Vector([1,2,3]) )
        NonMatrixError
        >>> isMatrix( [[1,2],[2]] )
        NonMatrixError
        >>> isMatrix( [[1,'a'],['a',1]] )
        NonNumericError
        >>> isMatrix( [[1,2],[2,1]] )
        True
        >>> isMatrix( Matrix([[1,2],[2,1]]) )
        True
        >>> isMatrix( Matrix([[1,2,3],[3,2,1]]) )
        True
    """
    if isinstance(matrix, Matrix):
        return True
    elif isinstance(matrix, list) and isinstance(matrix[0], list):
        row_size = len(matrix)
        col_size = len(matrix[0])
        for i in range(len(matrix)):
            if col_size != len(matrix[i]):
                raise NonMatrixError
            for column in matrix[i]:
                if not type(column) in NUMERIC_TYPES:
                    raise NonNumericError
        return True
    else:
        raise NonMatrixError

# Implementar a funcao que segue 
def isLinearlyIndependent(self, vector_list):
    pass


class Vector(list):
    """
        This class represents a Vector (on towards mathematical). The values of
        coordinates of this is in a list. So the built-in method of list (how 
        add, diff, len, mul, div, eq) are used, ie was overwritting, on context
        of vectors.
    """

    def __init__(self, coordinates = []):
        try:
            if isVector(coordinates):
                if isinstance(coordinates, Vector):
                    coordinates = coordinates.coordinates
                self.__coordinate_list = coordinates
        except NonVectorError:
            raise NonVectorError
        except NonNumericError:
            raise NonNumericError
               
                    
        
    def setCoordinates(self, index, value):
        self.__coordinate_list[index] = value
    
    def getCoordinates(self, index):
        return self.__coordinate_list[index]
        
    @property
    def coordinates(self):
        return self.__coordinate_list

    def __str__(self):
        """
            This method is called to show this object how string. This is done 
            in built-in method str and print.
            
            Examples:            
            >>> vector = Vector([1, 2, 3])
            >>> print vector
            [1, 2, 3]
            >>> str(vector)
            [1, 2, 3]
        """
        return "%s"%self.__coordinate_list
        
    def __getitem__(self, index):
        """
            This method return the item self.__coordinate_list[index].
            
            This is called by self[index]. For example:
            >>> vector = Vector( [1,2,3] )
            >>> vector[2]
            3
        """
        return self.__coordinate_list[index]


    def __eq__(self, vector):
        """
            This method compares if two vector have coordinates equals.
            
            This method is called when used with object vectors, or a vector
            and a list, the operator ==
            
            Examples:
            >>> vector1 = Vector([1,2,3])
            >>> vector2 = Vector([1,2,3])
            >>> vector3 = Vector([3,2,1])
            >>> vector1 == vector2
            True
            >>> vector1 == [1,2,3]
            True
            >>> [1,2,3] == vector1
            True            
            >>> vector1 == vector3
            False
            >>> vector1 == [1,2]
            DifferentDimensionError
            >>> vector1 == 'a'
            NonVectorError
        """
        try:
            if isVector(vector):
                if isinstance(vector, list) and not isinstance(vector, Vector):
                    vector = Vector(vector)
                if len(self) == len(vector):
                    for i in range( len(self) ):
                        if self.coordinates[i] != vector.getCoordinates(i):
                            return False
                    return True
                else:
                    raise DifferentDimensionError
        except NonVectorError:
            raise NonVectorError
        except NonNumericError:
            raise NonNumericError

    def __len__(self):
        """
            This method return the lenght of list of attribute coordinate_list,
            ie, the dimension of vector. This method is called when used the
            built-in len(). The use is equals than the use for list, tuple,
            strings, etc.
            
            >>> len( Vector() )
            0
            >>> len( Vector( [3] ) )
            1
            >>> len( Vector( [1, 3, 89] ) )
            3
            >>> len( Vector( range(10) ) )
            10
        """
        return len(self.__coordinate_list)


    def norma(self):
        """
            This method return the lenght (norma) of vector.
            
            Examples:
            >>> vector = Vector([3,4])
            >>> vector.norma()
            5
            >>> Vector().norma()
            0
        """
        return sqrt(self.innerProduct(self))


    def __add__(self, vector):
        """
            This method return a new vector whose the attribute coordinate_list 
            is the sum of values of attributes coordinate_list of these two 
            instances of Vector. 
            
            This method is called when used the operator +
            
            Examples: 
            >>> vector = Vector([1,2,3])
            >>> vector + Vector([3,2,1])
            [4,4,4]
            >>> vector + [3,2,1]
            [4,4,4]
            >>> vector + [1, 2, 'a']
            NonNumericError
            >>> vector + 'a'
            NonVectorError
            >>> vector + Vector([1, 2])
            DifferentDimensionError
        """
        try:
            if isVector(vector):
                if isinstance(vector, list) and not isinstance(vector, Vector):
                    vector = Vector(vector)
                if len(self) == len(vector):
                    return Vector( [self.coordinates[i] + vector.coordinates[i] 
                                                for i in range( len(self) )] )
                else:
                    raise DifferentDimensionError 
        except NonVectorError:
            raise NonVectorError
        except NonNumericError:
            raise NonNumericError



    def __iadd__(self, vector):
        """
            This method sums self with other vector. This method is called by 
            operator +=. Its function is call the method __add__ and alters
            the value of self.
   
            Examples:
            >>> vector = Vector([1,2,3])
            >>> vector += Vector([3,2,1])
            >>> vector
            [4,4,4]
            >>> vector += [1,1,1]
            [5, 5, 5]
            >>> vector += [1, 2, 'a']
            NonNumericError
            >>> vector += 'a'
            NonVectorError
            >>> vector += Vector([1, 2])
            DifferentDimensionError
        """
        return self + vector


    def __sub__(self, vector):
        """
            This method return a new vector whose the attribute coordinate_list 
            is the difference of values of attributes coordinate_list of these
            two instances of Vector. 
            
            This method is called when used the operator -
            
            Examples:
            >>> vector = Vector([1,2,3])
            >>> vector - Vector([0,1,2])
            [1,1,1]
            >>> vector - [0,1,2]
            [1,1,1]
            >>> vector - [1, 2, 'a']
            NonNumericError
            >>> vector - 'a'
            NonVectorError
            >>> vector - Vector([1, 2])
            DifferentDimensionError
        """
        try:
            if isVector(vector):
                if isinstance(vector, list) and not isinstance(vector, Vector):
                    vector = Vector(vector)
                if len(self) == len(vector):
                    return Vector( [self.coordinates[i] - vector.coordinates[i] 
                                                for i in range( len(self) )] )
                else:
                    raise DifferentDimensionError 
        except NonVectorError:
            raise NonVectorError
        except NonNumericError:
            raise NonNumericError


    def __isub__(self, vector):
        """
            This method subtract self with other vector. This method is called
            by operator -=. Its function is call the method __diff__ and
            alters the value of self.
            
            Examples:
            >>> vector = Vector([1,2,3])
            >>> vector -= Vector([0,1,2])
            >>> vector
            [1,1,1]
            >>> vector -= [1,1,0]
            [0,0,1]
            >>> vector -= [1, 2, 'a']
            NonNumericError
            >>> vector -= 'a'
            NonVectorError
            >>> vector -= Vector([1, 2])
            DifferentDimensionError
        """
        return self - vector



    def __mul__(self, vector):
        """
            If the parameter vector is a scalar (variable of numeric type) then
            this method return a new vector whose the attribute coordinate_list 
            is the values of attributes coordinate_list multiply by scalar. 
            
            If the parameter vector is an instance of Vector, or a list, then
            this return the inner product of this two Vectors.

            If the paremeter vector is a matrix (instance of class Matrix) then 
            this method will return the vector whose is the multiplication of 
            self by the matrix.
            
            Otherwise is generated a exception if the value is not 
            one of this case (except raised by functions isVector or isMatrix) 
            or raise a exception NonOperableVector if the vector (vector or 
            matrix) has dimensions non operable with self.

            WARNING: the called should be vector * scalar, or vector * list. If
            the called was done how scalar * vector, or list * vector the
            method called is __mult__ of the scalar, or of the list, ie, the
            result is different than expected.
        """
        if type(vector) in NUMERIC_TYPES:
            return self.multiplicationScalar(vector)
        if isinstance(vector, str):
            raise NonNumericError

        try:
             if isMatrix(vector):
                return self.multiplicationMatrix(vector)
        except NonMatrixError:            
            if isinstance(vector, Vector):
                return self.crossProduct(vector)
            else:
                raise NonMatrixError
        except NonNumericError:
            raise NonNumericError       



    def __imul__(self, vector):
        """
            This method multiplicates self with other vector. This method is 
            called by operator *=. Its function is call the method __mul__ and
            alters the value of self.
            
            How there are two types of multiplication, this choice is done by 
            method __mul__.
        """
        try:
            return self * vector
        except NonNumericError:
            raise NonNumericError
        except DifferentDimensionError:
            raise DifferentDimensionError
        except NonMatrixError:
            raise NonMatrixError



    def multiplicationScalar(self, scalar):
        """
            This method return a new vector whose the attribute coordinate_list 
            is the values of attributes coordinate_list multiply by scalar. 

            Examples:
            >>> vector = Vector([1,2,3])
            >>> vector * 3 
            [3.0, 6.0, 9.0]
            >>> vector * 0 
            [0.0, 0.0, 0.0]
            >>> vector * -1 
            [-1.0, -2.0, -3.0]
            >>> vector * 'a'                        
            NonNumericError  
        """
        if type(scalar) in NUMERIC_TYPES:
            return Vector( [ scalar * elem for elem in self.coordinates ] )
        else:
            raise NonNumericError


    def multiplicationMatrix(self, matrix):
        """
            This method return the vecotr resulted by multiplication of vector 
            by matrix. If dimensions of vector is n and the dimendions of matrix
            is n x m, the dimsnsions of vector resulting is m.
            
            How the multiplication of vector by vector is done (inner product)
            this is used in this method. Calculates the transpose of the matrix 
            and each coordinates of the resulting vector is a inner product 
            between the line of matrx transposed (column of origin matrix) by de
            self (the vector).
            
            Examples:
            >>> matrix = Matrix([[1,2],[2,3],[3,1]])
            >>> vector = Vector([1,2,3])
            >>> vector2 = vector * matrix
            >>> vector2.coordinates
            [14.0, 11.0]
            >>> vector * Matrix( [[1,2],[2,3]] )
            DifferentDimensionError
            >>> vector.multiplicationMatrix( Matrix( [[1,2],[2,3]] ) )
            DifferentDimensionError
            >>> vector.multiplicationMatrix( [[1,2],[2,3]] )
            DifferentDimensionError
            >>> vector.multiplicationMatrix( [[1,2],[2]] )
            NonMatrixError
            >>> vector.multiplicationMatrix( [[1,2],[2, 'a']] )
            NonNumericError
        """
        try:
            if isMatrix(matrix):
                if not isinstance(matrix, Matrix):
                    matrix = Matrix(matrix)
                if len(self) == matrix.dimensions()[0]:
                    result = Vector( [0 for colum in              \
                                  range( matrix.dimensions()[1] ) ] )
                    matrix = matrix.transpose()              
                    for i in range(matrix.dimensions()[0]):
                        result.setCoordinates(i, self.innerProduct(matrix[i]))
                    return result   
                else:
                    raise DifferentDimensionError
        except NonMatrixError:
            raise NonMatrixError
        except NonNumericError:
            raise NonNumericError  



    def crossProduct(self, vector):
        """
            TODO
        """
        # Implementar este metodo
        pass



    def innerProduct(self, vector):
        """
            This method calculates the inner products betwen an instance of a 
            vector and othe vector, or other list.
            
            Examples:
            >>> vector1 = Vector([1,2,3])
            >>> vector2 = Vector([8, 5, 3])
            >>> vector1 * vector2
            27
            >>> vector1.innerProduct(vector2)
            27
            >>> vector1.innerProduct([8, 5, 3])
            27
            >>> vector1 * [1,2]
            DifferentDimensionError
            >>> vector1.innerProduct([1,2])
            DifferentDimensionError
            >>> vector1.innerProduct('a')
            NonVectorError
            >>> vector1.innerProduct([1, 'a'])
            NonNumericError            
        """
        try:
            if isVector(vector):
                if isinstance(vector, list) and not isinstance(vector, Vector):
                    vector = Vector(vector)
                if len(self) == len(vector):
                    result = 0.0
                    for i in range(len(vector)):
                        result += self.coordinates[i] * vector.coordinates[i] 
                    return result
                else:
                    raise DifferentDimensionError 
        except NonVectorError:
            raise NonVectorError
        except NonNumericError:
            raise NonNumericError        



    def __div__(self, scalar):
        """
            This method return a new vector whose the attribute coordinate_list 
            is the values of attributes coordinate_list divides by scalar. 
            
            WARNING 1: the called should be vector / scalar. If the called was 
            done how scalar / vector the method called is __mul__ of the 
            scalar, ie, the result is different than expected
            
            WARNING 2: if the scalar is zero is impossible do the division.
            
            Examples:
            >>> vector = Vector([9,12,15])
            >>> vector / 3 
            [3.0, 4.0, 5.0]
            >>> vector / 0 
            ZeroDivisionError
            >>> vector / -1 
            [-9.0, -12.0, -15.0]
            >>> vector / 'a'                        
            NonNumericError  
        """
        if type(scalar) in NUMERIC_TYPES:
            if scalar:
                return Vector( [float(elem) / float(scalar) 
                                                for elem in self.coordinates ] )
            else:
                raise ZeroDivisionError
        else:
            raise NonNumericError


    def __idiv__(self, scalar):
        """
            This method divides self with other vector
            
            Examples:
            >>> vector = Vector([9,12,15])
            >>> vector /= 3 
            [3.0, 4.0, 5.0]
            >>> vector / 0 
            ZeroDivisionError
            >>> vector / -1 
            [-9.0, -12.0, -15.0]
            >>> vector / 'a'                        
            NonNumericError  
            
        vector = Vector([9,12,15])
        vector /= 3
        self.assertEquals( vector.coordinates, [3.0, 4.0, 5.0] )
        self.assertRaises(ZeroDivisionError, self.vector.__idiv__, 0.0)
        vector = Vector([9,12,15])
        vector /= -1
        self.assertEquals( vector.coordinates, [-9.0, -12.0, -15.0] )
        self.assertRaises(NonNumericError, self.vector.__idiv__, 'a')
        """
        try:
            return self / scalar
        except ZeroDivisionError:
            raise ZeroDivisionError
        except NonNumericError:
            raise NonNumericError

class Matrix(list):
    """
        This class represents a Matrix (on towards mathematical). The values of
        coordinates of this is in a list. So the built-in method of list (how 
        add, diff, len, mul, div, eq) are used, ie was overwritting, on context
        of vectors.
        
        WARNING: the type of matrix represented by objects of this class are 
        bidimensionals matrix.
    """
    def __init__(self, matrix = [[]]):
        """
            Ever a object is initialized is verified if the paremeter matrix is 
            a valid matrix. Else is raise a exception according the return of
            function isMatrix (stored in variable is_matrix).
        """
        if isMatrix(matrix):
            if isinstance(matrix, Matrix):
                matrix = matrix.elements
            self.__elements = matrix
        
    def setElement(self, row, column, value):
        self.__elements[row][column] = value
    
    def getElement(self, row, column):
        return self.__elements[row][column]
        
    @property
    def elements(self):
        return self.__elements



    def __str__(self):
        """
            This method is called to show this object how string. This is done 
            in built-in method str and print

            Examples:            
            >>> matrix = Matrix( [[1, 2], [3, 4]] )
            >>> print matrix
            [[1, 2], [3, 4]]
            >>> str(matrix)
            [[1, 2], [3, 4]]            
        """
        matrix_str = ""
        for i in range(len(self.__elements)):
            matrix_str += "%s\n"%self.__elements[i]
        return matrix_str    


    def __getitem__(self, index):
        """
            This method return the list of self.__coordinate_list[index]. So
            the item is caught in the list.


            For example:
            >>> matrix = Matrix( [[1,2],[4,3]] )
            >>> matrix[0]
            [1,2]
            matrix[0][0]
            1
        """
        return self.__elements[index]


    def dimensions(self):
        """
            This method return a tuple wich the first value is lenght of list
            that represents the rows (and then contais other lists) and the
            second is the lenght of all lists that contain the columns, ie, the
            dimensions of matrix.
        
            ps: Is not possible call a same method to calculate the dimensions 
            of a matrix because the method len should return a integer (and not
            a tuple). 
            
            Examples:
            >>> Matrix( [[1,2],[4,3]] ).dimensions()
            (2, 2)
            >>> Matrix( [[1, 2, 3], [4, 3, 3]] ).dimensions()
            (2, 3)
            >>> Matrix( [[4,5], [4,7], [4,9]] ).dimensions()
            (3, 2)
        """
        return ( len(self.__elements), len(self.__elements[0])  )



    def __eq__(self, matrix):
        """
            This method compares if two matrix have elements equals.
            
            This method is called when used with object matrix, or a matrix
            and a list of list, the operator ==
            
            Examples:
            >>> matrix = Matrix([[1, 2], [4, 3]])
            >>> matrix == Matrix([[1, 2], [4, 3]])
            True
            >>> matrix == [[1, 2], [4, 3]]
            True
            >>> [[1, 2], [4, 3]] == matrix
            True
            >>> [[1, 2], [4, 3]] = matrix.elements
            True
            >>> matrix == [[1, 1], [1, 1]]
            False
            >>> matrix == [[1, 2]]
            DifferentDimensionError
            >>> matrix == 'a'
            NonMatrixError
            
            ps: this don't compare instances, compares values of coordinate_list
            attribute.
        """
        if isMatrix(matrix):
            if not isinstance(matrix, Matrix):
                matrix = Matrix(matrix)
            if self.dimensions()[0] == matrix.dimensions()[0] and \
                self.dimensions()[1] == matrix.dimensions()[1]:
                for i in range( self.dimensions()[0] ):
                    for j in range( self.dimensions()[1] ):
                        if self.elements[i][j] != matrix.getElement(i, j):
                            return False
                return True 
            else:
                raise DifferentDimensionError
        


    def __add__(self, matrix):
        """
            This method return a new matrix whose the attribute elements 
            is the sum of values of attributes elements of these and the same 
            attribute of matrix 
                        
            ps: this method is called when used the operator +
            
            Examples:
            >>> matrix = Matrix([[1,2,3], [4,3,2]])
            >>> matrix + Matrix([[3,2,1], [1,4,7]])
            [[4,4,4], [5,7,9]]
            >>> matrix + [[3,2,1], [1,4,7]]
            [[4,4,4], [5,7,9]]
            >>> matrix + [[3,2], [1,4]]
            DifferentDimensionError
            >>> matrix + [[3,2,'a'], [1,4,7]]
            NonNumericError
            >>> matrix1 + 'a'
            NonMatrixError
        """
        if isMatrix(matrix):
            if not isinstance(matrix, Matrix):
                matrix = Matrix(matrix)
            if isinstance(matrix, Matrix):
                if self.dimensions()[0] == matrix.dimensions()[0] and \
                             self.dimensions()[1] == matrix.dimensions()[1]:
                    return Matrix( [[ self.elements[i][j] + 
                                      matrix.elements[i][j] 
                                      for j in range(self.dimensions()[1])]
                                      for i in range(self.dimensions()[0])])
                else:
                    raise DifferentDimensionError



    def __iadd__(self, matrix):
        """
            This method sums self with other matrix. This method is called by 
            operator +=. Its function is call the method __add__ and alters
            the value of self.
            
            Examples:
            >>> matrix = Matrix([[1,2,3], [4,3,2]])
            >>> matrix += Matrix([[3,2,1], [1,4,7]])
            >>> matrix
            [[4,4,4], [5,7,9]]
            >>> matrix += [[3,2], [1,4]]
            DifferentDimensionError
            >>> matrix += [[3,2,'a'], [1,4,7]]
            NonNumericError
            >>> matrix1 += 'a'
            NonMatrixError
        """
        return self + matrix
        
        

    def __sub__(self, matrix):
        """
            This method return a new matrix whose the attribute elements 
            is the diff of values of attributes elements of these and the same 
            attribute of matrix 
            
            ps: this method is called when used the operator -
                        
            Examples:
            >>> matrix = Matrix([[1,2,3], [4,3,2]])
            >>> matrix - Matrix([[3,2,1], [1,4,7]])
            [[-2,0,2], [3,-1,-5]]
            >>> matrix - [[3,2,1], [1,4,7]]
            [[-2,0,2], [3,-1,-5]]
            >>> matrix - [[3,2], [1,4]]
            DifferentDimensionError
            >>> matrix - [[3,2,'a'], [1,4,7]]
            NonNumericError
            >>> matrix - 'a'
            NonMatrixError         
        """
        if isMatrix(matrix):
            if not isinstance(matrix, Matrix):
                matrix = Matrix(matrix)
            if isinstance(matrix, Matrix):
                if self.dimensions()[0] == matrix.dimensions()[0] and \
                   self.dimensions()[1] == matrix.dimensions()[1]:
                    return Matrix( [[ self.elements[i][j] - 
                                      matrix.elements[i][j] 
                                      for j in range(self.dimensions()[1])]
                                      for i in range(self.dimensions()[0])])
                else:
                    raise DifferentDimensionError
    
    def __isub__(self, matrix):
        """
            This method diffs self with other matrix. This method is called by 
            operator -=. Its function is call the method __iadd__ and alters
            the value of self.
            
            Examples:
            >>> matrix = Matrix([[1,2,3], [4,3,2]])
            >>> matrix -= Matrix([[3,2,1], [1,4,7]])
            >>> matrix
            [[-2,0,2], [3,-1,-5]]
            >>> matrix -= [[3,2], [1,4]]
            DifferentDimensionError
            >>> matrix -= [[3,2,'a'], [1,4,7]]
            NonNumericError
            >>> matrix -= 'a'
            NonMatrixError
        """
        return self - matrix


    def scalarMultiplication(self, scalar):
        """
            This method multiply the matrix represented by this for the 
            paremter scalar (variable of numeric type), ie, this return a new 
            matrix whose the attribute elements is the values of attribute
            elements of this multiply by scalar. 
            
            Examples:
            >>> matrix = Matrix( [[1,2],[4,3]] )
            >>> matrix * [[2, 4, 6], [8, 10], [12]]
            NonMatrixError
            >>> matrix * [['a', 'bb', 'c'], [[1], 2, 'foo bar ']]
            NonNumericError
            >>> matrix * 'a'
            NonNumericError
            >>> matrix * 2 
            [[2, 4], [8, 6]]
            >>> matrix * 2.0
            [[2, 4], [8, 6]]
            >>> Matrix([[1,2,3], [2,2,2]]) * 3 
            [[3,6,9], [6,6,6]]
        """    
        if type(scalar) in NUMERIC_TYPES:
            return Matrix( [ [ self[i][j] * scalar 
                               for j in range( self.dimensions()[1] ) ]
                               for i in range( self.dimensions()[0] ) ] )
        else:
            raise NonNumericError

    def vectorMultiplication(self, vector):
        """
            This method multiply a matrix represented by this by a vector. 
            
            The Vector can be a instance of class Vector or a numeric list.
            
            If lenght of the vector (quantity of the coordinates of the vector)
            is different from the quantity of the row of the matrix (resulted 
            of dimensions()[0] ) is generated a exception, because these are 
            not operable.
            
            Examples:
            >>> matrix = Matrix( [[1,2],[4,3]] )
            >>> vector = Vector( [1,2] )
            >>> matrix * vector
            [5,10]
            >>> Matrix( [[1,2],[2,3],[3,4]] ) * vector
            [5, 8, 11]
            >>> matrix * Vector( [1,2,3] )
            DifferentDimensionError
            >>> matrix * 'a'
            NonVectorError
            >>> matrix * [1,2,'a']
            NonNumericError
        """
        if isVector(vector):
            if not isinstance(vector, Vector):
                vector = Vector(vector)
            if self.dimensions()[1] == len(vector):
                result = Vector( [0 for colum in              \
                              range( self.dimensions()[0] ) ] )
                for i in range(self.dimensions()[0]):
                    result.setCoordinates(i, vector.innerProduct(self[i]))
                return result   
            else:
                raise DifferentDimensionError


    def matrixMultiplication(self, matrix):
        """
            This method multiply a matrix by other matrix
            
            The matrix can be a instance of class Matrix or a numeric list of 
            list (vector candidate).
            
            If quantity of columns of this instance of matrix (dimensions()[1])
            is different from the quantity of the row of the matrix passed by
            parameter (dimensions()[0]) is generated a exception, because these
            are not operable (on mathematic towards).
            
            Examples:
            >>> matrix = Matrix( [[1,2],[4,3]] )
            >>> matrix * Matrix([[1,2,3], [2,2,2]])
            [[5,6,7], [10,14,18]]
            >>> matrix * [[1,2,3], [2,2,2]]
            [[5,6,7], [10,14,18]]
            >>> matrix * Matrix( [[1,2],[2,3],[3,4]] )
            DifferentDimensionError
            >>> matrix * 'a'
            NonMatrixError
            >>> matrix * [[1,2],[1,'a']]
            NonNumericError            
        """
        if isMatrix(matrix):
            if not isinstance(matrix, Matrix):
                matrix = Matrix(matrix)
            if self.dimensions()[1] == matrix.dimensions()[0]:
                result = Matrix( [
                           [0 for column in range( matrix.dimensions()[1]) ]
                              for row in range( self.dimensions()[0] ) ] )
                              
                matrix = matrix.transpose()        
                for i in range( self.dimensions()[0] ):
                    for j in range( matrix.dimensions()[0] ):
                        result.elements[i][j] =                           \
                                     Vector(self[i]).innerProduct(matrix[j])
                return result   
            else:
                raise DifferentDimensionError



    def __mul__(self, matrix):
        """
            If the parameter matrix is a scalar (variable of numeric type) then
            this method return a new matrix whose the attribute elements 
            is the values of attribute elements multiply by scalar (call the 
            method scalarMultiplication)
            
            If the parameter matrix is an instance of Vector, or a candidate, 
            then this call the method vectorMultiplication.

            If the parameter matrix is an instance of Matrix, or a candidate, 
            then this call the method matrixMultiplication.

            WARNING: the called should be matrix * scalar, matrix1 * matrix, or 
            matrix * list(of list). If the called was done how scalar * matrix, 
            or list * matrix the method called is __mul__ of the scalar, or of 
            the list, ie, the result is different than expected.
        """
        if isinstance(matrix, str):
            raise NonNumericError 
        elif type(matrix) in NUMERIC_TYPES:
                return self.scalarMultiplication(matrix)
        
        try:    
            if isVector(matrix):
                return self.vectorMultiplication(matrix)
        except Exception:
            pass 

        if isMatrix(matrix):
            return self.matrixMultiplication(matrix)

   
    def __imul__(self, matrix):
        """
            This method multiplicate self by scalar, vector or other matrix 
            according the type of parameter. This method is called by 
            operator *=. 
            
            Its function is call the method __mul__ and alters the value of self
        """
        return self * matrix


    def transpose(self):
        """
            This method return the transpose of the matrix represented by self.
            
            Example:
            >>> matrix = [[2, 3], [3, 4], [5, 6]]
            >>> matrix.transpose 
            [[2, 3, 5], [3, 4, 6]]
        """
        return Matrix( [ [self[j][i] for j in range( self.dimensions()[0])] \
                              for i in range (self.dimensions()[1] ) ] )


    #######################################
    #                                     #
    #  Implementar os metodos que seguem  #
    #                                     #
    #######################################

 
    def isSquare(self):
        """
            TODO
        """
        pass
    
    def isIdentity(self):
        """
            TODO
        """
        pass
        
    def isDiagonal(self):
        """
            TODO
        """
        pass        
    
    def isSymetric(self):
        """
            TODO
        """
        pass
        
    def isSuperiorTriangular(self):
        """
            TODO
        """
        pass

    def isInferiorTriangular(self):
        """
            TODO
        """
        pass
        
    def isTriangular(self):
        """
            TODO
        """
        pass        

    def cofator(self):
        """
            TODO
        """
        pass
        
    def adjoint(self):
        """
            TODO
        """
        pass
    
    def determinant(self):
        """
            TODO
        """
        pass
        
    def inverse(self):
        """
            TODO
        """
        pass
        
    def characteristicPolynomial(self):
        """
            TODO
        """
        pass
    
    def eigenvalues(self):
        """
            TODO
        """
        pass

    def eigenvectors(self):
        """
            TODO
        """
        pass