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
    regionList = getSixRegionList(image)
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
     
"""
    This method divide a given image in six regions.
    
    image: the original image to be divided in six regions.
     
    return: a list of six images, each one represents a part of the original
    image.
"""
def getSixRegionList(image):
    size = image.size
    r0_dimension = (0, 0, ((size[0]/2) ),((size[1]/3)))
    r1_dimension = (size[0]/2, 0, size[0] ,(size[1]/3))
    r2_dimension = (0, (size[1]/3), (size[0]/2), (2*size[1]/3))
    r3_dimension = (size[0]/2, size[1]/3, size[0], 2*size[1]/3)
    r4_dimension = (0, (2*size[1]/3), (size[0]/2),size[1])
    r5_dimension = ((size[0]/2), 2*size[1]/3, size[0], size[1])
    regionList = []
    print Image.Image(img_to_mix = image.crop(r0_dimension))
    regionList.append(Image.Image(img_to_mix = image.crop(r0_dimension)))
    regionList.append(Image.Image(img_to_mix = image.crop(r1_dimension)))
    regionList.append(Image.Image(img_to_mix = image.crop(r2_dimension)))
    regionList.append(Image.Image(img_to_mix = image.crop(r3_dimension)))
    regionList.append(Image.Image(img_to_mix = image.crop(r4_dimension)))
    regionList.append(Image.Image(img_to_mix = image.crop(r5_dimension)))
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
    edgeTypes.append([[255,255],[0,0]])
    """
    Horizontal Upper
    0,0
    1,1
    """    
    edgeTypes.append([[0, 0],[255, 255]])
    """
    Vertical left
    0,1
    0,1
    """
    edgeTypes.append([[0,255],[0,255]])
    """
    Vertical Right
    1,0
    1,0
    """
    edgeTypes.append([[255,0],[255,0]])
    """
    Diagonal center left
    0,1
    1,0
    """
    edgeTypes.append([[0,255],[255, 0]])
    """
    Diagonal upper left
    0,0
    1,0
    """
    edgeTypes.append([[0,0],[255, 0]])
    """
    Diagonal bottom left
    0,1
    0,0
    """
    edgeTypes.append([[0,255],[0, 0]])
    """
    Diagonal center right
    1,0
    0,1
    """
    edgeTypes.append([[255,0],[0, 255]])
    """
    Diagonal upper right
    1,0
    0,0
    """
    edgeTypes.append([[255,0],[0, 0]])
    """
    Diagonal bottom right
    0,0
    0,1
    """
    edgeTypes.append([[0,0],[0, 255]])
    return edgeTypes

"""
    Skeletonize an image with the Hilditch's algorithm. 
"""
def hildtchSkeletonize(image):        
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
    import pdb    
    numRegions = 0;    
    
    for j in range( image.size[1] ):
        transition = 0;
        #if j == 5: pdb.set_trace()
        for i in range(image.size[0] ):            
                flag = 0;
                pixelValue = image.getpixel((i,j));
                if(i+1 < image.size[0]):
                    if(pixelValue == 0) & (image.getpixel((i+1, j)) == 255):
                        if((image.topLeftNeibor((i+1, j)) == 0) and   
                               (image.topNeibor((i+1,j)) == 0)):
                            
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
                        
                     
                
"""
    count the number of 0 to 255 transitions in the 8 neighborhood of a pixel 
    in a clock-wise order.      
"""   
def countTransitions(image, pixel):
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


def blocksIntensity(image):
    """
         
    """
       
    pixelMatrix = image.pixel_matrix()  
    hSize = image.size[1]/5#image.size[1]/5
    wSize = image.size[0]/5#image.size[0]/5
    height_position = 0
    width_position = 0     
    pattern_list = []   
    while height_position < image.size[1]:
        while width_position < image.size[0]:
            if (height_position + hSize) <= image.size[1] and (wSize + width_position) <= image.size[0]:
                matrixCroped = [i[height_position:(height_position+hSize)] for i in pixelMatrix[width_position:width_position+wSize]]
                blackItensity = 0
                for line in matrixCroped:
                    blackItensity += line.count(0)  
                pattern_list.append(blackItensity)
            width_position += wSize
        height_position += hSize
        width_position = 0           
        
    return pattern_list
    
    
            
