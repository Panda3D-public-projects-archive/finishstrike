
def extractFeatureByEdgeDetection(image):
    """
        This method extract features of an image counting the occurrences of
        a specific edge type in the regions of the image.
        
        image: the image to extract features.
        return: a matrix with dimensions = (number of edges x number of regions),
        each value of the matrix contains the number of occurrences of an
        edge type in a region of the image (matrix[edgeType][region])
    """
    regionList = image.getRegionList(col=6, row=6)
    edgeTypeList = getRegionTypeList()
     
    featureMatrix = [[0 for i in range(len(regionList))] \
                                    for j in range(len(edgeTypeList)) ]    
    for region in regionList:        
        for i in range(region.size[0]-1):
            for j in range(region.size[1]-1):
                region2x2 = region.getFourNeighborhood((i,j))                                
                for edgeType in edgeTypeList:
                    if edgeType == region2x2:
                        regionIndex = regionList.index(region)
                        edgeIndex = edgeTypeList.index(edgeType)
                        featureMatrix[edgeIndex][regionIndex] += 1      
    return featureMatrix
     

def getRegionTypeList():
    """
        returns a list of distinct edge types. Each edge type is represented by
        one matrix 2 x 2.
    """

    edgeTypes = []
    # XXX: Why did you as multiline instead of comments?
    """
    Horizontal bottom
    1,1
    0,0
    """
    edgeTypes.append([[255,255],[0,0]])

    # XXX: Why did you as multiline instead of comments?
    """
    Horizontal Upper
    0,0
    1,1
    """    
    edgeTypes.append([[0, 0],[255, 255]])

    # XXX: Why did you as multiline instead of comments?
    """
    Vertical left
    0,1
    0,1
    """
    edgeTypes.append([[0,255],[0,255]])

    # XXX: Why did you as multiline instead of comments?
    """
    Vertical Right
    1,0
    1,0
    """
    edgeTypes.append([[255,0],[255,0]])

    # XXX: Why did you as multiline instead of comments?
    """
    Diagonal center left
    0,1
    1,0
    """
    edgeTypes.append([[0,255],[255, 0]])

    # XXX: Why did you as multiline instead of comments?
    """
    Diagonal upper left
    0,0
    1,0
    """
    edgeTypes.append([[0,0],[255, 0]])

    # XXX: Why did you as multiline instead of comments?
    """
    Diagonal bottom left
    0,1
    0,0
    """
    edgeTypes.append([[0,255],[0, 0]])

    # XXX: Why did you as multiline instead of comments?
    """
    Diagonal center right
    1,0
    0,1
    """
    edgeTypes.append([[255,0],[0, 255]])

    # XXX: Why did you as multiline instead of comments?
    """
    Diagonal upper right
    1,0
    0,0
    """
    edgeTypes.append([[255,0],[0, 0]])

    # XXX: Why did you as multiline instead of comments?
    """
    Diagonal bottom right
    0,0
    0,1
    """
    edgeTypes.append([[0,0],[0, 255]])
    return edgeTypes

def hildtchSkeletonize(image):        
    """
        Skeletonize an image with the Hilditch's algorithm. 
    """
    while (True):
        letContinue = False
        boundaryPixelList = []
        pixelsToDelete = []
        for i in range( image.size[0] ):
            for j in range(image.size[1] ):
                if(image.getpixel((i,j)) == 0):                    
                    n8 = image.get8Neiborhood((i,j))                                       
                    if(n8.count(255) > 0):                        
                        boundaryPixelList.append((i,j))                        
        for pixel in boundaryPixelList:
            n8 = image.get8Neiborhood(pixel)
            if((image.topNeibor(pixel) + image.rightNeibor(pixel) + 
                image.leftNeibor(pixel)) == 0):
                continue            
            if((image.topNeibor(pixel) + image.rightNeibor(pixel) + 
                image.backNeibor(pixel)) == 0):
                continue                
            if not((n8.count(0) >= 2) & (n8.count(0) <= 6)):                
                continue
            numTransitions = countTransitions(image, pixel)
            if numTransitions <> 1:                
                continue                        
            pixelsToDelete.append(pixel)            
            letContinue = True
        for pixelToDelete in pixelsToDelete:                      
            image.putpixel(pixelToDelete, 255)
        print letContinue                        
        if(not letContinue):            
            break                                 
    return image

def getNumJunctions(image):
    pass

def getNumLineEnds(image):
    pass


def getNumLoops(image):
    #XXX: Please, do not commit the code with pdb.
    numRegions = 0;    
    
    for j in range( image.size[1] ):
        transition = 0;
        # XXX: useless comments should not be commited.
        #if j == 5: pdb.set_trace()
        for i in range(image.size[0] ):            
                flag = 0;
                pixelValue = image.getpixel((i,j));
                if(i+1 < image.size[0]):
                    if(pixelValue == 0) & (image.getpixel((i+1, j)) == 255):
                        if((image.topLeftNeibor((i+1, j)) == 0) and   
                               (image.topNeibor((i+1,j)) == 0)):

                        # XXX: useless comments should not be commited as well.   
                        #if(image.topLeftNeibor((i+1, j)) * image.topNeibor((i+1,j)) * 
                        # image.topRightNeibor((i+1, j)) == 0):                            
                            count = i + 1;                            
                            while(count < image.size[0]):                                
                                if(image.getpixel((count, j)) == 0): 
                                    line_count = j + 1
                                    while(line_count < image.size[1]):
                                        if(image.getpixel((i + 1, line_count)) == 0):
                                            numRegions += 1
                                            break
                                        line_count += 1
                                    if(image.getpixel((i + 1, line_count)) == 0):
                                            break 
                                count += 1
    return numRegions
                        
                     
                
def countTransitions(image, pixel):
    """
        count the number of 0 to 255 transitions in the 8 neighborhood of a pixel 
        in a clock-wise order.      
    """   
    count = 0
    if(image.topNeibor(pixel) == 0)&(image.topRightNeibor(pixel) == 255):        
        count += 1
    if(image.topRightNeibor(pixel) == 0)&(image.rightNeibor(pixel) == 255):        
        count += 1
    if(image.rightNeibor(pixel) == 0)&(image.backRightNeibor(pixel) == 255):
        count += 1
    if(image.backRightNeibor(pixel) == 0)&(image.backNeibor(pixel) == 255):
        count += 1
    if(image.backNeibor(pixel) == 0)&(image.backLeftNeibor(pixel) == 255):        
        count += 1
    if(image.backLeftNeibor(pixel) == 0)&(image.leftNeibor(pixel) == 255):
        count += 1
    if(image.leftNeibor(pixel) == 0)&(image.topLeftNeibor(pixel) == 255):
        count += 1
    if(image.topLeftNeibor(pixel) == 0)&(image.topNeibor(pixel) == 255):
        count += 1
    return count


def blocksIntensity(image, row, col):
    #XXX: We have to test this method.
    """ This method consists in two steps. The first one, splits the image in rowXCol subimages.
        The last step counts the number of black pixels in each subimage.
        Return a list wich is the number of black pixel in each subimage."""
   
    pattern_list = []
    subImage_list = image.getRegionList(row, col)
        
    for subImage in subImage_list:
        pixelMatrix = subImage.pixel_matrix()
        blackItensity = 0
        for line in matrixCroped:
            blackItensity += line.count(0)
        pattern_list.append(blackItensity)

    return pattern_list

