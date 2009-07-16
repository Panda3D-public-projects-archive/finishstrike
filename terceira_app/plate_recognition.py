from horus.core.processingimage import processingimage, image
from horus.ic.ann import ann, util
from horus.vision import ocr

def recognize(img, offset=3):
  if img.mode != 'L':
    plate = img.convert('L')
  plate = processingimage.globalThreshold(plate)
  plate_negative = plate.negative()
  vertical_proj = processingimage.horizontalProjection(plate_negative)  
  y_cord_list = processingimage.locateNonZeroIntervals(vertical_proj)
  word_list = []
  arrow_list = []
 
  horizontal_proj = processingimage.verticalProjection(plate_negative)
  horizontal_proj = horizontal_proj.applyBlur(0.01)
  x_cord_list = processingimage.locateNonZeroIntervals(horizontal_proj) 

  for line in y_cord_list:
    word_list.append(img.crop((x_cord_list[0][0]-offset, line[0]-offset, x_cord_list[0][1]+offset, line[1]+offset)))
    arrow_list.append(img.crop((x_cord_list[1][0]-offset, line[0]-offset, x_cord_list[1][1]+offset, line[1]+offset)))
  
  neural_network = ann.load('/tmp/ann.net')
  
  keys = []
  values = []
  #Arrows Recognition
  for arrow in arrow_list:
    arrow_pattern = util.get_pattern_from_image(arrow)
    values.append(neural_network.run(arrow_pattern))
  
  for word in word_list:
    keys.append(ocr.apply_ocr(word.convert('L')))
    
  output_dict = {}
  for i in range(len(keys)):
    output_dict[keys[i]] = values[i]

  print output_dict
  return output_dict

    
       
  


 

if __name__ == '__main__':
  img = image.Image(path='/home/ucam/Desktop/placa3.png')
  recognize(img)
  
    
