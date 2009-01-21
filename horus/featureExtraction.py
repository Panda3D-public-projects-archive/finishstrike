import image as Image

"""
    this method extract features of an image counting the occurrences of
    a specific edge type in the regions of the image.
    
    image: the image to extract features.
    return: a matrix with dimensions = (number of edges x number of regions),
    each value of the matrix contains the number of occurrences of an
    edge type in a region of the image (matrix[edgeType][region])
"""
def extractFeatureByEdgeDetection(image):
    regionList = getSixRegionList(image)(image)
    edgeTypeList = getRegionTypeList()
     
    featureMatrix = [[0 for i in range(len(regionList))] \
                                    for j in range(len(edgeTypeList)) ]    
    for region in regionList:        
        for i in range(region.size[0]-1):
            for j in range(region.size[1]-1):
                region2x2 = Image.getFourNeighborhood((i,j), region)                
                for edgeType in edgeTypeList:
                    if edgeType == region2x2:
                        regionIndex = regionList.index(region)
                        edgeIndex = edgeTypeList.index(edgeType)
                        featureMatrix[edgeIndex][regionIndex] += 1      
    return featureMatrix
     
"""
    This method divide a given image in six regions.
    
    image: the original image to be divided in six regions.
     
    return: a list of six images, each one represents a part of the original
    image.
"""
def getSixRegionList(image):
    size = image.size
    r0_dimension = (0, 0, ((size[0]/2) -1),((size[1]/3) -1))
    r1_dimension = (size[0]/2, 0, size[0]-1 ,(size[1]/3) -1)
    r2_dimension = (0, (size[1]/3), (size[0]/2) -1, (2*size[1]/3) -1)
    r3_dimension = (size[0]/2, size[1]/3, size[0]-1,2*size[1]/3 -1)
    r4_dimension = (0, (2*size[1]/3) -1, (size[0]/2),size[1] -1)
    r5_dimension = ((size[0]/2), 2*size[1]/3, size[0] -1, size[1] -1)
    regionList = []
    regionList.append(image.crop(r0_dimension))
    regionList.append(image.crop(r1_dimension))
    regionList.append(image.crop(r2_dimension))
    regionList.append(image.crop(r3_dimension))
    regionList.append(image.crop(r4_dimension))
    regionList.append(image.crop(r5_dimension))
    return regionList

"""
    returns a list of distinct edge types. Each edge type is represented by
    one matrix 2 x 2.
"""
def getRegionTypeList():
    edgeTypes = []
    """
    Horizontal bottom
    1,1
    0,0
    """
    edgeTypes.append([[1,1],[0,0]])
    """
    Horizontal Upper
    0,0
    1,1
    """    
    edgeTypes.append([[0, 0],[1, 1]])
    """
    Vertical left
    0,1
    0,1
    """
    edgeTypes.append([[0,1],[0,1]])
    """
    Vertical Right
    1,0
    1,0
    """
    edgeTypes.append([[1,0],[1,0]])
    """
    Diagonal center left
    0,1
    1,0
    """
    edgeTypes.append([[0,1],[1, 0]])
    """
    Diagonal upper left
    0,0
    1,0
    """
    edgeTypes.append([[0,0],[1, 0]])
    """
    Diagonal bottom left
    0,1
    0,0
    """
    edgeTypes.append([[0,1],[0, 0]])
    """
    Diagonal center right
    1,0
    0,1
    """
    edgeTypes.append([[1,0],[0, 1]])
    """
    Diagonal upper right
    1,0
    0,0
    """
    edgeTypes.append([[1,0],[0, 0]])
    """
    Diagonal bottom right
    0,0
    0,1
    """
    edgeTypes.append([[0,0],[0, 1]])
    return edgeTypes
 
