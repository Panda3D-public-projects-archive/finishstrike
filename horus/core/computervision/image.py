# -*- coding: utf-8 -*-
# XXX: Add Copyright
from PIL import Image as PILImage
       
class ImageMixIn(object):
    """
        This class implements all content's methods required in anpr modules
    """
           
    # XXX: over_group should be explained into the doc string   
    def getRegionList(self, row, col, over_group=None):
        """
            This method split a given image in NxM regions.
            In other words,
             - if we have an image with 30x30 pixels it should return a list
            containing 25 sub-images.

            image: the original image to be divided in six regions.
             
            return: a list of six images, each one represents a part of the original
            image.
        """
        width, height = self.size
        height_block_size = height/row
        width_block_size = width/col
        cut_list = [(x, y) for x in range(0, width) for y in range(0, height)]
        cut_list = [i for i in cut_list if i[0] % width_block_size == 0 and i[1] % height_block_size == 0]
        subimage_list = []
        for i in cut_list:
            # Getting indexes
            x0, y0 = i
            x1 = (i[0]+width_block_size)
            y1 = (i[1]+height_block_size)
            if x1 > width: 
              if over_group is None:
                  continue
              x1 = width - 1
            if y1 > height:
                if over_group is None:
                    continue
                y1 = height -1
            subimage_list.append(Image(img_to_mix=self.crop((x0, y0, x1, y1))))
        for i in subimage_list:
            i.show()
        return subimage_list


    def getEightNeighbourhood(self, xy):
        # XXX: This variable name is not so good
        # XXX: neighbourhood_list
        n8List = []        
        if self.topNeighbour(xy) != None:
            n8List.append(self.topNeighbour(xy))
        if self.rightTopNeighbour(xy) != None:
            n8List.append(self.rightTopNeighbour(xy))
        if self.rightNeighbour(xy) != None:
            n8List.append(self.rightNeighbour(xy))
        if self.rightBottomNeighbour(xy) != None:
            n8List.append(self.rightBottomNeighbour(xy))
        if self.bottomNeighbour(xy) != None:
            n8List.append(self.bottomNeighbour(xy))
        if self.leftBottomNeighbour(xy) != None:
            n8List.append(self.leftBottomNeighbour(xy))
        if self.leftNeighbour(xy) != None:
            n8List.append(self.leftNeighbour(xy))
        if self.leftTopNeighbour(xy) != None:
            n8List.append(self.leftTopNeighbour(xy))
        return n8List   
         
    def topNeighbour(self, xy):
        if(xy[1]-1 >= 0):
            return self.getpixel((xy[0],xy[1]-1))
        else:
            return None
    
    def bottomNeighbour(self, xy):
        if(xy[1]+1 < self.size[1]):
            return self.getpixel((xy[0],xy[1]+1))

    def rightTopNeighbour(self, xy):
        if(xy[0]+1 < self.size[0]) & (xy[1]-1 >= 0):
            return self.getpixel((xy[0]+1, xy[1]-1))

    def rightNeighbour(self, xy):
        if(xy[0]+ 1 < self.size[0]):
            return self.getpixel((xy[0]+1,xy[1]))

    def rightBottomNeighbour(self, xy):
        if(xy[0]+1 < self.size[0]) & (xy[1]+1 < self.size[1]):
            return self.getpixel((xy[0]+1, xy[1]+1))

    def leftNeighbour(self, xy):
        if(xy[0]-1 >= 0): 
            return self.getpixel((xy[0]-1, xy[1]))

    def leftBottomNeighbour(self, xy):
        if(xy[0]-1 >= 0 ) & ( xy[1]+1 < self.size[1]):
            return self.getpixel((xy[0]-1, xy[1]+1))

    def leftTopNeighbour(self, xy):
        if(xy[0]-1 >= 0 ) & ( xy[1]-1 >= 0 ):
            return self.getpixel((xy[0]-1, xy[1]-1))

    def pixel_matrix(self):
        """
            This method returns a matrix with values of wich content's pixels.
        """
        matrix = [[]]
        matrix = [[0 for i in range(self.size[1])] for j in range(self.size[0]) ]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                    matrix[i][j] = self.getpixel((i,j))
        return matrix

    # XXX: The doc string should be added.
    def getFourNeighbourhood(self, index):
      """
         TODO
      """
      return [[self.getpixel((index[0],index[1])),
               self.getpixel((index[0]+1, index[1]))],
              [self.getpixel((index[0], index[1]+1)),
               self.getpixel((index[0]+1, index[1]+1))]]

def Image(image_path=None, img_to_mix=None):
    """
      This method should return a PIL Image object mixed with ImageMixIn
    """
    newimg = None
    if img_to_mix is not None and \
       image_path is None:
        im = PILImage.new(img_to_mix.mode, img_to_mix.size)
        NewClassImage = type('ImagePilMixedIn', (im.__class__, ImageMixIn,), {})
        newimg = NewClassImage()
        newimg._new(img_to_mix)
        newimg.__dict__.update(img_to_mix.__dict__)
        newimg.putdata(img_to_mix.getdata())        
    else:   
        im = PILImage.open(image_path)
        NewClassImage = type('ImagePilMixedIn', (im.__class__, ImageMixIn,), {})
        newimg = NewClassImage(fp=image_path) 
        newimg.__dict__.update(im.__dict__)  
    return newimg

def new(mode = None, size = None, color = None):    
    return Image(img_to_mix = PILImage.new(mode, size, color)) 

if __name__=='__main__':
    x=Image(image_path='/home/lucas/lenna.jpg')
    y=x.getRegionList(6,6)
    for i in y:
        i.save('/home/lucas/img/%s.jpg' % y.index(i))

