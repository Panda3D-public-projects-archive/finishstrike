# -*- coding: utf-8 -*-
# XXX: Add Copyright
from PIL import Image as PILImage
       
class ImageMixIn(object):
    """
        This class implements all content's methods required in anpr modules
    """
    # Acho que os proximos metodos podem ser alocados em uma classe e 
    # relacionados com Image via composicao. A presenca deles esta
    # sobrecarregando essa classe
    def get8Neiborhood(self,xy):
        n8List = []        
        if(self.topNeibor(xy) != None):
            n8List.append(self.topNeibor(xy))                
        if(self.topRightNeibor(xy) != None):
            n8List.append(self.topRightNeibor(xy))        
        if(self.rightNeibor(xy) != None):
            n8List.append(self.rightNeibor(xy))
        if(self.backRightNeibor(xy) != None):
            n8List.append(self.backRightNeibor(xy))         
        if(self.backNeibor(xy) != None):
            n8List.append(self.backNeibor(xy))            
        if(self.backLeftNeibor(xy) != None):
            n8List.append(self.backLeftNeibor(xy))
        if(self.leftNeibor(xy) != None):
            n8List.append(self.leftNeibor(xy))
        if(self.topLeftNeibor(xy) != None):
            n8List.append(self.topLeftNeibor(xy))                
        return n8List   
         
    def topNeibor(self, xy):
        if(xy[1]-1 >= 0):
            return self.getpixel((xy[0],xy[1]-1))
        else:
            return None
    
    def backNeibor(self, xy):
        if(xy[1]+1 < self.size[1]):
            return self.getpixel((xy[0],xy[1]+1))            

    def topRightNeibor(self, xy):
        if(xy[0]+1 < self.size[0]) & (xy[1]-1 >= 0):
            return self.getpixel((xy[0]+1, xy[1]-1))        

    def rightNeibor(self, xy):
        if(xy[0]+ 1 < self.size[0]):
            return self.getpixel((xy[0]+1,xy[1]))        

    def backRightNeibor(self, xy):               
        if(xy[0]+1 < self.size[0]) & (xy[1]+1 < self.size[1]):
            return self.getpixel((xy[0]+1, xy[1]+1))

    def leftNeibor(self, xy):
        if(xy[0]-1 >= 0): 
            return self.getpixel((xy[0]-1, xy[1]))

    def backLeftNeibor(self, xy):
        if(xy[0]-1 >= 0 ) & ( xy[1]+1 < self.size[1]):
            return self.getpixel((xy[0]-1, xy[1]+1))

    def topLeftNeibor(self, xy):
        if(xy[0]-1 >= 0 ) & ( xy[1]-1 >= 0 ):
            return self.getpixel((xy[0]-1, xy[1]-1))        

    
    def pixel_matrix(self):
        """
            This method returns a matrix with values of wich content's pixels.
        """
        # XXX: TODO
        #############################
        #### Alterar esse metodo ####
        #############################
        self.matrix = [[]]
        if not self.matrix:
            self.matrix = [[0 for i in range(self.size[1])] \
                                    for j in range(self.size[0]) ]

            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    self.matrix[i][j] = self.getpixel((i,j))

        return self.matrix

    #XXX: The doc string should be added.
    def getFourNeighborhood(self, index):
      """
         TODO
      """
      return [[self.getpixel((index[0],index[1])),
               self.getpixel((index[0]+1, index[1]))],
              [self.getpixel((index[0], index[1]+1)),
               self.getpixel((index[0]+1, index[1]+1))]]

def Image(image_path = None, img_to_mix = None):
  """
    This method should return a PIL Image object mixed with ImageMixIn
  """
  newimg = None
  if((img_to_mix != None) & (image_path == None)):      
      im = PILImage.new(img_to_mix.mode, img_to_mix.size)
      NewClassImage = type('ImagePilMixedIn', (im.__class__, ImageMixIn,), {})
      newimg = NewClassImage()
      newimg._new(img_to_mix)
      newimg.__dict__.update(im.__dict__)
      newimg.putdata(img_to_mix.getdata())
  else:   
      im = PILImage.open(image_path)
      NewClassImage = type('ImagePilMixedIn', (im.__class__, ImageMixIn,), {})
      newimg = NewClassImage(fp=image_path) 
      newimg.__dict__.update(im.__dict__)
  return newimg
