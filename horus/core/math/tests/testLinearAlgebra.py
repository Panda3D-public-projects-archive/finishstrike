import unittest
import mathematic

from mathematic import isVector
from mathematic import isMatrix

from mathematic import NonNumericError
from mathematic import DifferentDimensionError

from mathematic import Vector
from mathematic import NonVectorError
from mathematic import NonVectorComparableError
from mathematic import NonVectorOperableError

from mathematic import Matrix
from mathematic import NonMatrixError
from mathematic import NonMatrixComparableError
from mathematic import NonMatrixOperableError

class IsFunctionsMathematicTest(unittest.TestCase):

    def test_is_vector(self):
        """
            This test case verify if the verifing of a instance is a Vector
            object or it can be a candidate to vector.
        """
        self.assertRaises(NonVectorError, isVector, 'a' )
        self.assertRaises(NonVectorError, isVector, Matrix([[1,2],[3,4]]) )
        self.assertRaises(NonNumericError, isVector, [1, 'a'] )
        assert( isVector([1,2,3]) )
        assert( isVector( Vector([1,2,3]) ) )


    def test_is_matrix(self):
        """
            This test case verify if the verifing of a instance is a Matrix
            object or it can be a candidate to matrix.
        """
        self.assertRaises(NonMatrixError, isMatrix, 'a' )
        self.assertRaises(NonMatrixError, isMatrix, Vector([1,2,3]) ) 
        self.assertRaises(NonMatrixError, isMatrix, [[1,2],[2]] )       
        self.assertRaises(NonNumericError, isMatrix,[[1,'a'],['a',1]] )
        assert( isMatrix( [[1,2],[2,1]] ) )
        assert( isMatrix( Matrix([[1,2],[2,1]]) ) )
        assert( isMatrix( Matrix([[1,2,3],[3,2,1]]) ) )



class VectorsMathematicTest(unittest.TestCase):

    def setUp(self):
        self.vector = Vector( [1, 2, 3] )
    
    def test_instanciation_of_object_vectors(self):
        """
            This test case verify the instanciation of object vector. In this is
            verify all Exception (if coordinates is not a list, or is a non 
            numeric  list)
        """
        self.assertRaises( NonVectorError, Vector, 'a' )
        self.assertRaises( NonNumericError, Vector, [1, 2.5 , 'a'] )
        a = Vector( [1, 2, 2.5] ) 
        self.assertEquals( a.coordinates, [1.0, 2.0, 2.5] )
        self.assertEquals( [1, 2, 3],  Vector( [1, 2, 3] ).coordinates )

    def test_set_and_get_values_of_coordinates_of_vectors(self):
        """
            This test case verify if the access of values of vector's 
            coordinates is correctly done.
        """
        self.assertEquals(self.vector.getCoordinates(0), 1.0)
        self.assertEquals(self.vector.getCoordinates(1), 2.0)
        self.assertEquals(self.vector.getCoordinates(2), 3.0)        
        self.vector.setCoordinates(1, 5)
        self.assertEquals(self.vector.getCoordinates(1), 5.0)
        
        self.vector.coordinates[2] = 7
        self.assertEquals(self.vector.getCoordinates(2), 7.0)

    def test_string_showed_by_vector(self):
        """
            This test case verify if the text showed in print vector is 
            correctly done.
        """
        self.assertEquals("[1, 2, 3]", str(self.vector))



    def test_getitem(self):
        """
            This test case verify if the return of item of vector in method 
            getitem is correctly done.
        """
        self.assertEquals(3, self.vector[2])

   
    def test_comparation_vectors(self):
        """
            This test case verify if the method __eq__ (so the built-in of 
            operator ==) is correctly done.
        """
        assert( self.vector == Vector( [1, 2, 3] ) )
        assert( self.vector == [1, 2, 3] )
        assert( [1, 2, 3] == self.vector )
        assert( not (Vector([3,2,1]) == self.vector) )
        assert( not ([3,2,1] == self.vector) )
        self.assertRaises(DifferentDimensionError, self.vector.__eq__, [1,2])
        self.assertRaises(NonVectorError, self.vector.__eq__, 'a')


    def test_vector_lenght(self):
        """
            This test case verify if the method __len__ (so the built-in len())
            is correctly done.
        """
        self.assertEquals( len( Vector() ), 0 )
        self.assertEquals( len( Vector( [3] ) ), 1 )
        self.assertEquals( len( Vector( [1, 3, 89] ) ), 3 )
        self.assertEquals( len( Vector( range(10) ) ), 10 )


    def test_normal(self):
        """
            TODO
        """
        vector = Vector([3,4])
        self.assertEquals( vector.norma(), 5)
        self.assertEquals( Vector().norma(), 0)
            


    def test_sum_of_vectors(self):
        """
            This test case verify if the sum of the object vector with other 
            is correctly done.
        """
        self.assertEquals( [4, 4, 4], self.vector + Vector([3,2,1]) )
        self.assertEquals( [4, 4, 4], self.vector + [3,2,1] )
        self.assertRaises(NonNumericError, self.vector.__add__, [1, 2, 'a'] )
        self.assertRaises(NonVectorError, self.vector.__add__, 'a')
        self.assertRaises(DifferentDimensionError, self.vector.__add__, [1, 2] )


    def test_increment_self_with_sum_vector(self):
        """
            This test case verify if the increment sum of the object vector with
            other is correctly done.
        """
        self.vector += Vector([3,2,1])
        self.assertEquals( [4, 4, 4], self.vector )
        self.vector += [1, 1, 1]
        self.assertEquals( [5, 5, 5], self.vector )
        self.assertRaises(NonNumericError, self.vector.__iadd__, [1, 2, 'a'] )
        self.assertRaises(NonVectorError, self.vector.__iadd__, 'a')
        self.assertRaises(DifferentDimensionError, self.vector.__iadd__, [1, 2])

        

    def test_diff_of_vectors(self):
        """
            This test case verify if the diff of the object vector with other 
            is correctly done.
        """
        self.assertEquals( [1,1,1], self.vector - Vector([0,1,2]) )
        self.assertEquals( [1,1,1], self.vector - [0,1,2] )
        self.assertRaises(NonNumericError, self.vector.__sub__, [1, 2, 'a'] )
        self.assertRaises(NonVectorError, self.vector.__sub__, 'a')
        self.assertRaises(DifferentDimensionError, self.vector.__sub__, [1, 2] )



    def test_increment_self_with_diff_vector(self):
        """
            This test case verify if the increment diff of the object vector 
            with other is correctly done.
        """
        self.vector -= Vector([0,1,2])
        self.assertEquals( [1,1,1], self.vector )
        self.vector -= [1, 1, 0]
        self.assertEquals( [0,0,1], self.vector )
        self.assertRaises(NonNumericError, self.vector.__isub__, [1, 2, 'a'] )
        self.assertRaises(NonVectorError, self.vector.__isub__, 'a')
        self.assertRaises(DifferentDimensionError, self.vector.__isub__, [1, 2])


    def test_multiplication_vector_by_scalar(self):
        """
            This test case verify if the multiplication of the vector by scalar 
            is correctly done.
        """
        vector = self.vector * 3
        self.assertEquals(vector, [3.0, 6.0, 9.0])        
        vector = self.vector * 0
        self.assertEquals(vector, [0.0, 0.0, 0.0]) 
        vector = self.vector * -1
        self.assertEquals(vector, [-1.0, -2.0, -3.0])
        self.assertRaises(NonNumericError, self.vector.__mul__, 'a')  

    def test_increment_self_with_multiplication_by_scalar(self):
        """
            This test case verify if the increment multiplication of the object  
            vector by scalar is correctly done.
        """
        self.vector *= 3
        self.assertEquals(self.vector, [3.0, 6.0, 9.0])        
        self.vector *= -1
        self.assertEquals(self.vector, [-3.0, -6.0, -9.0])
        self.vector *= 0
        self.assertEquals(self.vector, [0.0, 0.0, 0.0]) 

        self.assertRaises(NonNumericError, self.vector.__imul__, 'a')


    def test_multiplication_by_matrix(self):
        """
            TODO
        """
        matrix = Matrix([[1,2],[2,3],[3,1]])
        assert (self.vector * matrix ==  [14.0, 11.0])
        self.assertRaises( DifferentDimensionError, 
                                  self.vector.__mul__, Matrix( [[1,2],[2,3]] ) )
        self.assertRaises( DifferentDimensionError, 
                                  self.vector.__mul__, [[1,2],[2,3]] )
        self.assertRaises( DifferentDimensionError, 
                     self.vector.multiplicationMatrix, Matrix( [[1,2],[2,3]] ) )
        self.assertRaises( DifferentDimensionError, 
                                self.vector.multiplicationMatrix,[[1,2],[2,3]] ) 
        self.assertRaises( NonMatrixError, 
                                  self.vector.multiplicationMatrix,[[1,2],[2]] ) 
        self.assertRaises( NonNumericError, 
                             self.vector.multiplicationMatrix,[[1,2],[2, 'a']] ) 


    def test_increment_self_with_multiplication_by_matrix(self):
        """
            This test case verify if the increment multiplication of the object  
            vector by a matrix is correctly done.
        """
        self.vector *= Matrix([[1,2],[2,3],[3,1]])
        assert (self.vector ==  [14.0, 11.0])
        self.assertRaises( DifferentDimensionError, 
                             Vector([1,2,3]).__imul__, Matrix( [[1,2],[2,3]] ) )
        self.assertRaises( DifferentDimensionError, 
                                Vector( [1, 2, 3] ).__imul__, [[1,2],[2,3]] ) 
        self.assertRaises( NonMatrixError, 
                                  self.vector.__imul__,[[1,2],[2]] ) 
        self.assertRaises( NonNumericError, 
                             self.vector.__imul__,[[1,2],[2, 'a']] )
        

    def test_multiplication_vector_by_vector_or_cross_product(self):
        """
            TODO
        """
        pass


    def test_increment_multiplication_vector_by_vector_or_cross_product(self):
        """
            TODO
        """
        pass


    def test_inner_product(self):
        """
            This test case verify if the inner product (or scalar product) is
            correctly done.
        """
        self.assertEquals(27, self.vector.innerProduct(Vector([8, 5, 3])))
        self.assertEquals(27, self.vector.innerProduct([8, 5, 3]))        
        self.assertRaises(  DifferentDimensionError, 
                                              self.vector.innerProduct, [1,2] )
        self.assertRaises(NonVectorError, self.vector.innerProduct, 'a')
        self.assertRaises(NonNumericError, self.vector.innerProduct, [1, 'a'] )


    def test_division_vector_by_scalar(self):
        """
            This test case verify if the multiplication of the vector by scalar 
            is correctly done.
        """
        vector = Vector([9,12,15])
        vector2 = vector / 3
        self.assertEquals( vector2.coordinates, [3.0, 4.0, 5.0] )
        self.assertRaises(ZeroDivisionError, self.vector.__div__, 0.0)
        vector2 = vector / -1
        self.assertEquals( vector2.coordinates, [-9.0, -12.0, -15.0] )
        self.assertRaises(NonNumericError, self.vector.__div__, 'a')


    def test_increment_self_with_division_by_scalar(self):
        """
            This test case verify if the increment division of the object  
            vector by a scalar is correctly done.
        """
        vector = Vector([9,12,15])
        vector /= 3
        self.assertEquals( vector.coordinates, [3.0, 4.0, 5.0] )
        self.assertRaises(ZeroDivisionError, self.vector.__idiv__, 0.0)
        vector = Vector([9,12,15])
        vector /= -1
        self.assertEquals( vector.coordinates, [-9.0, -12.0, -15.0] )
        self.assertRaises(NonNumericError, self.vector.__idiv__, 'a')


class MatrixMathematicTest(unittest.TestCase):

    def setUp(self):
        self.matrix = Matrix( [[1, 2], [4, 3]] )
    
    def test_instanciation_of_object_matrix(self):
        """
            This test case verify the instanciation of object vector. In this is
            verify all erros (if the matrix is not a list, and the elements of 
            matrix aren't a list, or is a non numeric matrix)
        """
        self.assertRaises( NonMatrixError, Matrix, 'a' )
        self.assertRaises( NonMatrixError, Matrix, [1, 2] )
        self.assertRaises( NonMatrixError, Matrix,  [[1], [4, 3]] )
        self.assertRaises( NonNumericError, Matrix,  [[1, 'a'], [4, 3]] )
        self.assertEquals( self.matrix.elements, [[1, 2], [4, 3]])

    def test_set_and_get_values_of_coordinates_of_matrix(self):
        """
            This test case verify if the access of values of vector's 
            coordinates is correctly done.
        """
        self.assertEquals(self.matrix.getElement(0, 0), 1.0)
        self.assertEquals(self.matrix.getElement(0, 1), 2.0)
        self.assertEquals(self.matrix.getElement(1, 0), 4.0)        
        self.assertEquals(self.matrix.getElement(1, 1), 3.0)        

        self.matrix.setElement(0, 0, 5)
        self.assertEquals(self.matrix.getElement(0, 0), 5.0)
        
        self.matrix.elements[1][1] = 7
        self.assertEquals(self.matrix.getElement(1, 1), 7.0)

    def test_string_showed_by_matrix(self):
        """
            This test case verify if the text showed in print matrix is 
            correctly done.
        """
        self.assertEquals("[1, 2]\n[4, 3]\n", str(self.matrix))


    def test_getitem(self):
        """
            This test case verify if the return of item of matrix in method 
            getitem is correctly done.
        """
        self.assertEquals([1,2], self.matrix[0])
        self.assertEquals(1, self.matrix[0][0])


    def test_dimensions_of_matrix(self):
        """
            This test case verify if the dimensions of the matrix is 
            correctly done.
        """     
        self.assertEquals((2, 2), self.matrix.dimensions())
        self.assertEquals((2, 3), Matrix( [[1, 2, 3], [4, 3, 3]] ).dimensions())
        self.assertEquals((3, 2), Matrix( [[4,5], [4,7], [4,9]] ).dimensions())



    def test_comparation_matrix(self):
        """
            This test case verify if the method __eq__ (so the built-in of 
            operator ==) is correctly done.
        """
        assert( self.matrix == Matrix([[1, 2], [4, 3]])  )
        assert( self.matrix == [[1, 2], [4, 3]]  )
        assert( [[1, 2], [4, 3]]  != self.matrix )
        assert( [[1, 2], [4, 3]]  == self.matrix.elements )
        assert( not(self.matrix == [[1, 1], [1, 1]]) )
        self.assertRaises(DifferentDimensionError, self.matrix.__eq__, [[1, 2]])
        self.assertRaises(NonMatrixError, self.matrix.__eq__, 'a')


    def test_sum_of_matrix(self):
        """
            This test case verify if the sum of the object matrix with other 
            is correctly done.
        """
        matrix = Matrix([[1,2,3], [4,3,2]])
        self.assertEquals([[4,4,4],[5,7,9]], matrix + Matrix([[3,2,1],[1,4,7]]))
        self.assertEquals([[4,4,4],[5,7,9]], matrix + [[3,2,1],[1,4,7]])
        self.assertRaises(DifferentDimensionError, matrix.__add__, 
                                                               [[3,2], [1,4]] )
        self.assertRaises(NonNumericError, matrix.__add__, [[3,2,'a'], [1,4,7]])
        self.assertRaises(NonMatrixError, matrix.__add__, 'a')
        

    def test_increment_self_with_sum_matrix(self):
        """
            This test case verify if the increment sum of the matrix with other 
            is correctly done.
        """
        matrix = Matrix([[1,2,3], [4,3,2]])
        matrix += Matrix([[3,2,1],[1,4,7]])
        self.assertEquals([[4,4,4],[5,7,9]], matrix)
        self.assertRaises(DifferentDimensionError, matrix.__iadd__, 
                                                               [[3,2], [1,4]] )
        self.assertRaises(NonNumericError, matrix.__iadd__, [[3,2,'a'], [1,4,7]])
        self.assertRaises(NonMatrixError, matrix.__iadd__, 'a')        
        

    def test_diff_of_matrix(self):
        """
            This test case verify if the diff of the object matrix with other 
            is correctly done.
        """
        matrix = Matrix([[1,2,3], [4,3,2]])
        self.assertEquals( [[-2,0,2], [3,-1,-5]], 
                                        matrix - Matrix( [[3,2,1], [1,4,7]] ) )
        self.assertEquals( [[-2,0,2], [3,-1,-5]], matrix - [[3,2,1], [1,4,7]] )
        self.assertRaises(DifferentDimensionError, matrix.__sub__, 
                                                               [[3,2], [1,4]] )
        self.assertRaises(NonNumericError, matrix.__sub__, [[3,2,'a'], [1,4,7]])
        self.assertRaises(NonMatrixError, matrix.__sub__, 'a')        


    def test_increment_self_with_diff_matrix(self):
        """
            This test case verify if the increment diff of the matrix with other 
            is correctly done.
        """
        matrix = Matrix([[1,2,3], [4,3,2]])
        matrix -= Matrix([[3,2,1],[1,4,7]])
        self.assertEquals([[-2,0,2], [3,-1,-5]], matrix)
        self.assertRaises(DifferentDimensionError, matrix.__isub__, 
                                                               [[3,2], [1,4]] )
        self.assertRaises(NonNumericError, matrix.__isub__, [[3,2,'a'], [1,4,7]])
        self.assertRaises(NonMatrixError, matrix.__isub__, 'a')


    def test_multiplication_matrix_by_scalar(self):
        """
            This test case verify if the multiplication of a matrix by scalar  
            is correctly done.
        """    
        non_matrix_numeric = [['a', 'bb', 'c'], [[1], 2, 'foo bar ']]
        non_matrix = [[2, 4, 6], [8, 10], [12]]
        self.assertRaises( NonMatrixError, self.matrix.__mul__, non_matrix )
        self.assertRaises( NonNumericError, 
                           self.matrix.__mul__, non_matrix_numeric )        
        self.assertRaises( NonNumericError,self.matrix.__mul__, 'a' )
        
        self.assertEquals( [[2, 4], [8, 6]] , self.matrix * 2 )
        self.assertEquals( [[2, 4], [8, 6]] , self.matrix * 2.0 ) 
        self.assertEquals( [[3,6,9], [6,6,6]], Matrix([[1,2,3], [2,2,2]]) * 3 )


    def test_multiplication_matrix_by_vector(self):
        """
            This test case verify if the multiplication of a matrix by vector  
            is correctly done.
        """
        vector = Vector( [1,2] )
        assert( [5,10] == (self.matrix * vector ) )
        assert( [5, 8, 11] == Matrix( [[1,2],[2,3],[3,4]] ) * vector)
        self.assertRaises( DifferentDimensionError,                            \
                           self.matrix.vectorMultiplication, Vector( [1,2,3] ) )
        self.assertRaises(NonVectorError, self.matrix.vectorMultiplication, 'a')
        self.assertRaises( NonNumericError,                                    \
                                   self.matrix.vectorMultiplication, [1,2,'a'] )
        

    def test_multiplication_matrix_by_matrix(self):
        """
            This test case verify if the multiplication of a matrix by matrix  
            is correctly done.
        """
        matrix = Matrix( [[1,2,3], [2,2,2]] )
        assert( self.matrix * matrix == [[5,6,7], [10,14,18]] )
        assert( self.matrix * [[1,2,3], [2,2,2]] == [[5,6,7], [10,14,18]] )
        self.assertRaises( DifferentDimensionError,                            \
               self.matrix.matrixMultiplication, Matrix( [[1,2],[2,3],[3,4]] ) )
        self.assertRaises( NonMatrixError, self.matrix.matrixMultiplication,'a')
        self.assertRaises( NonNumericError,
                              self.matrix.matrixMultiplication,[[1,2],[1,'a']] )
      
        
    def test_increment_self_with_multiplication_by_matrix(self):
        """
            This test case verify if the increment multiplication of the matrix 
            with other is correctly done.
        """
        matrix = Matrix( [[1,2,3], [2,2,2]] )
        self.matrix *= matrix
        assert( self.matrix == [[5,6,7], [10,14,18]] )
        self.assertRaises( DifferentDimensionError,                            \
               self.matrix.matrixMultiplication, Matrix( [[1,2],[2,3]] ) )
        self.assertRaises( NonMatrixError, self.matrix.matrixMultiplication,'a')
        self.assertRaises( NonNumericError,
                              self.matrix.matrixMultiplication,[[1,2],[1,'a']] )


    def test_transpose_matrix(self):
        """
            This test case verify if the method transpose of the matrix 
            is correctly done.
        """
        matrixA = Matrix( [[2, 3, 4], [3, 4, 5]] )
        matrixB = Matrix( [[1, 2], [2, 3], [3, 4]] )
        matrixC = Matrix( [[1, 2, 3]] )
        self.assertEquals( [[2, 3], [3, 4], [4, 5]], matrixA.transpose() )
        self.assertEquals( [[1, 2, 3], [2, 3, 4]],   matrixB.transpose() )
        self.assertEquals( [[1], [2], [3]],          matrixC.transpose() )

        
class MathematicTest(unittest.TestCase):

    def setUp(self):
        self.non_matrix = [[1, 2, 3], [4, 5], [6]]
        self.matrixA = [[2, 3, 4], [3, 4, 5]]
        self.matrixB = [[1, 2], [2, 3], [3, 4]]
        self.matrixC = [[1, 2, 3]]
        self.vectorA = [1, 2, 3]
        self.vectorB = [5, 4, 3]
        
    def test_transpose_matrix(self):
        transpose_matrix = [[2, 3], [3, 4], [4, 5]]
        self.assertEquals(transpose_matrix, mathematic.transpose(self.matrixA))
        self.assertEquals([[1], [2], [3]], mathematic.transpose(self.matrixC))
        self.assertRaises(mathematic.NotIsMatrixException, mathematic.transpose, self.non_matrix)

    def test_multiplication_scalar_vector(self):
        vector_heterogeneous = [[1], 2, 'foo bar ']
        self.assertEquals( [2, 4, 6], mathematic.multiplicationScalarVector(2, self.vectorA))
        self.assertEquals( [[1, 1], 4, 'foo bar foo bar '], 
                           mathematic.multiplicationScalarVector(2, vector_heterogeneous))

    def test_multiplication_vector(self):
        self.assertEquals( 22, mathematic.multiplicationVector(self.vectorA, self.vectorB))
        self.assertEquals( [2, 4, 6], mathematic.multiplicationVector(2, self.vectorA))  
        self.assertRaises( mathematic.ImpossibilityMultiplicationVectorsException,\
                           mathematic.multiplicationVector, [2, 3], self.vectorA) 

    def test_multiplication_scalar_by_matrix(self):
        matrix_heterogeneous = [['a', 'bb', 'c'], [[1], 2, 'foo bar ']]
        double_non_matrix = [[2, 4, 6], [8, 10], [12]]
        self.assertEquals( [[4, 6, 8], [6, 8, 10]], 
                    mathematic.multiplicationScalarMatrix(2, self.matrixA))
        self.assertEquals( [['aa', 'bbbb', 'cc'], 
                           [[1, 1], 4, 'foo bar foo bar ']],
                    mathematic.multiplicationScalarMatrix(2, matrix_heterogeneous))
                    
        self.assertEquals( double_non_matrix, 
                    mathematic.multiplicationScalarMatrix(2, self.non_matrix))   

    def test_multiplication_vector_by_matrix(self):
        self.assertEquals( [14, 20], mathematic.multiplicationVectorMatrix(self.vectorA, self.matrixB))
        self.assertRaises( mathematic.IncompatibleLenghtVectorMatrixException,\
                           mathematic.multiplicationVectorMatrix, [2, 3], self.matrixB) 
        self.assertRaises( mathematic.ElementNonNumericError,\
                           mathematic.multiplicationVectorMatrix, [2, 3, 'a'], self.matrixB) 
        
        self.assertRaises( mathematic.ElementNonNumericError,\
                           mathematic.multiplicationVectorMatrix, self.vectorA, [[1, 2], [2, 'o'], [3, 4]])       
        self.assertRaises( mathematic.NotIsMatrixException,\
                           mathematic.multiplicationVectorMatrix, self.vectorA, self.non_matrix) 

    def test_multiplication_matrix_vector(self):
        self.assertEquals( [20, 26], mathematic.multiplicationMatrixVector(self.matrixA, self.vectorA))
        
        self.assertRaises( mathematic.IncompatibleLenghtVectorMatrixException,\
                           mathematic.multiplicationMatrixVector, self.matrixA, [2, 3]) 
        self.assertRaises( mathematic.ElementNonNumericError,\
                           mathematic.multiplicationMatrixVector, self.matrixA, [2, 3, 'a']) 
        
        self.assertRaises( mathematic.ElementNonNumericError,\
                           mathematic.multiplicationMatrixVector, [[1, 22, 'o'], [1, 3, 4]], self.vectorA)       
        self.assertRaises( mathematic.NotIsMatrixException,\
                           mathematic.multiplicationMatrixVector, self.non_matrix, self.vectorA) 
    
    def test_multiplication_matrix(self):
        self.assertEquals([[20, 29], [26, 38]], mathematic.multiplicationMatrix(self.matrixA, self.matrixB))
        self.assertEquals( [2, 4, 6], mathematic.multiplicationMatrix(2, self.vectorA))
        self.assertEquals( [14, 20], mathematic.multiplicationMatrix(self.vectorA, self.matrixB))        
        self.assertEquals( [20, 26], mathematic.multiplicationMatrix(self.matrixA, self.vectorA))
        
        self.assertRaises( mathematic.ImpossibilityMultiplicationMatrixException,\
                           mathematic.multiplicationMatrix, self.matrixA, self.matrixA)
        self.assertRaises( mathematic.NotIsMatrixException,\
                           mathematic.multiplicationMatrix, self.matrixA, self.non_matrix)
        self.assertRaises( mathematic.NotIsMatrixException,\
                           mathematic.multiplicationMatrix, self.non_matrix, self.matrixB)                    
        self.assertRaises( mathematic.ElementNonNumericError,\
                           mathematic.multiplicationMatrix, [['d', 3, [7]], [1, 3, 'q']], self.matrixB)
        self.assertRaises( mathematic.ElementNonNumericError,\
                           mathematic.multiplicationMatrix, self.matrixA, [['d', 3], [[7], 1], [3, 'q']])

    def test_singular_variance(self):
        value_list = [2, 5, 7, 1, 5, 4, 1, 2, 15, 2]
        variance_values = [-2.4000000000000004, 0.59999999999999964, 
                            2.5999999999999996, -3.4000000000000004, 
                            0.59999999999999964, -0.40000000000000036, 
                            -3.4000000000000004, -2.4000000000000004, 
                            10.6, -2.4000000000000004]
        math = mathematic.Statistical()
        self.assertEquals(math.avarage(value_list), 4.4)
        self.assertEquals(math.singularVariance(value_list), variance_values)
        self.assertEquals(math.variance(value_list), variance_values)
        self.assertEquals(math.covariance(value_list), 160.39999999999998)

    def test_multidimensional_variance(self):
        value_list = [[2, 5, 7, 0], [1, 5, 4, 0], [1, 2, 15, 0], 
                      [2, 5, 9, 0], [9, 5, 4, 0], [7, 5, 3, 0] ]
        math = mathematic.Statistical()
        centroide = [3.6666666666666665, 4.5, 7.0, 0.0] 
        self.assertEquals(math.centroide(value_list), centroide )
        #print math.multidimensionalVariance(value_list)
        #print "covariance"
        #print math.covariance(value_list)

if __name__ == "__main__":
    unittest.main()
    
