# XXX: Add copyright

def extractFeatureByEdgeDetection(image):
    """
        This method extract features of an image counting the occurrences of
        a specific edge type in the regions of the image.
        
        image: the image to extract features.
        return: a matrix with dimensions = (number of edges x number of regions),
        each value of the matrix contains the number of occurrences of an
        edge type in a region of the image (matrix[edgeType][region])
    """
    regionList = image.getRegionList(col=2, row=3)
    edgeTypeList = getRegionTypeList()
     
    featureMatrix = [[0 for i in range(len(regionList))] \
                                    for j in range(len(edgeTypeList)) ]    
    for region in regionList:        
        for i in range(region.size[0]-1):
            for j in range(region.size[1]-1):
                region2x2 = region.getFourNeighbourhood((i,j))                                
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
                if(image.getPixel((i,j)) == 0):                    
                    n8 = image.getEightNeighbourhood((i,j))                                       
                    if(n8.count(255) > 0):                        
                        boundaryPixelList.append((i,j))                        
        for pixel in boundaryPixelList:
            n8 = image.getEightNeighbourhood(pixel)
            if((image.topNeighbour(pixel) + image.rightNeighbour(pixel) + 
                image.leftNeighbour(pixel)) == 0):
                continue            
            if((image.topNeighbour(pixel) + image.rightNeighbour(pixel) + 
                image.bottomNeighbour(pixel)) == 0):
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
        if(not letContinue):            
            break                                 
    return image

def getNumJunctions(image):
    pass

def getNumLineEnds(image):
    pass


def getNumLoops(image):
    numRegions = 0;    
    
    for j in range( image.size[1] ):
        transition = 0;
        for i in range(image.size[0] ):            
                flag = 0;
                pixelValue = image.getPixel((i,j))
                if(i+1 < image.size[0]):
                    if(pixelValue == 0) & (image.getPixel((i+1, j)) == 255):
                        if((image.topLeftNeighbour((i+1, j)) == 0) and   
                               (image.topNeighbour((i+1,j)) == 0)):

                        # XXX: useless comments should not be commited as well.   
                        #if(image.topLeftNeighbour((i+1, j)) * image.topNeighbour((i+1,j)) * 
                        # image.rightTopNeighbour((i+1, j)) == 0):                            
                            count = i + 1;                            
                            while(count < image.size[0]):                                
                                if(image.getPixel((count, j)) == 0): 
                                    line_count = j + 1
                                    while(line_count < image.size[1]):
                                        if(image.getPixel((i + 1, line_count)) == 0):
                                            numRegions += 1
                                            break
                                        line_count += 1
                                    if(image.getPixel((i + 1, line_count)) == 0):
                                            break 
                                count += 1
    return numRegions
                        
                     
                
def countTransitions(image, pixel):
    """
        count the number of 0 to 255 transitions in the 8 neighborhood of a pixel 
        in a clock-wise order.      
    """   
    count = 0
    if(image.topNeighbour(pixel) == 0)&(image.topRightNeighbour(pixel) == 255):        
        count += 1
    if(image.topRightNeighbour(pixel) == 0)&(image.rightNeighbour(pixel) == 255):        
        count += 1
    if(image.rightNeighbour(pixel) == 0)&(image.bottomRightNeighbour(pixel) == 255):
        count += 1
    if(image.bottomRightNeighbour(pixel) == 0)&(image.bottomNeighbour(pixel) == 255):
        count += 1
    if(image.bottomNeighbour(pixel) == 0)&(image.bottomLeftNeighbour(pixel) == 255):        
        count += 1
    if(image.bottomLeftNeighbour(pixel) == 0)&(image.leftNeighbour(pixel) == 255):
        count += 1
    if(image.leftNeighbour(pixel) == 0)&(image.topLeftNeighbour(pixel) == 255):
        count += 1
    if(image.topLeftNeighbour(pixel) == 0)&(image.topNeighbour(pixel) == 255):
        count += 1
    return count


def blocksIntensity(image, row=5, col=5):   
    """
      This method consists in two steps. The first one, splits the image in rowXCol sub-images.
      The last step counts the number of black pixels in each sub-image.
      Return a list which is the number of black pixels in each sub-image.
    """
    sub_image_list = image.getRegionList(row, col)
    pattern_list = []
    for sub_image in sub_image_list:
        pixel_matrix = sub_image.pixel_matrix()
        black_itensity = 0
        for line in pixel_matrix:
            black_itensity += line.count(0)
        pattern_list.append(black_itensity)

    return pattern_list

