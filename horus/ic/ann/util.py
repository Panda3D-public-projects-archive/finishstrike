import os
from pyfann import libfann
from horus.core.processingimage import image, processingimage


outputs = {
	"direita":1,
	"esquerda":0
}

pattern_size = (250, 219)



def is_image(file):
  types = ['.png','.jpg', '.bmp', '.jpeg', '.gif']
  for i in types:
    if file.find(i) >=0:
      return True
  return False
  
def write_train_file_from_dir(path, method_object, target_file='../default.train'):
  images = os.listdir(path)
  images = [i for i in images if is_image(i)]
  img = image.Image(path=path+images[0])
  train_file = open(target_file, 'w')
  lines = []
  head = " ".join([str(len(images)), str(img.size[0]), str(1)])
  lines.append(head+"\n")
  
  for i in images:
    img = image.Image(path=path+i)
    img = img.convert('L')
    pattern = method_object(img)
    pattern_str = ""
    for j in pattern:
      pattern_str += " "+str(j) 
    lines.append(pattern_str+"\n")
    for k in outputs.keys():      
	if i.find(k) >= 0:
            lines.append("%d\n"%(outputs[k]))
            break
  
  for i in lines:
    train_file.write(i)
  train_file.close()

def get_pattern_from_image(img, original_size=pattern_size):
  """
     This method extracts the pattern used to train and run the net.         
  """  
  new_img = img.convert('L')
  new_img = processingimage.globalThreshold(new_img)
  box = new_img.negative().content.getbbox()  
  new_img = new_img.crop((box[0]-2, box[1]-2, box[2]+2, box[3]+2))
  new_img = new_img.resize(original_size)
  new_img_sk = processingimage.hildtchSkeletonize(new_img)  
  new_img_sk = new_img_sk.negative()
  pattern = processingimage.verticalProjection(new_img_sk)
  return pattern
  
if __name__ == "__main__":
  write_train_file_from_dir('/tmp/train/', get_pattern_from_image)


