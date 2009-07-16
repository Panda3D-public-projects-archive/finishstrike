import commands
import StringIO
import os

def apply_ocr(img):
  result_file = '/tmp/temp'  
  image_source = '/tmp/image_temp.jpg'
  img.save(image_source)
  image_name = image_source.split('.')[0]
  image_converted = image_name+".tif"
  convert_args = 'convert %s %s'%( image_source, image_converted)
  ocr_args = 'tesseract %s %s'%(image_converted, result_file)
  del_tif_args = 'rm %s'%(image_converted)
  del_txt_args = 'rm %s.txt'%(result_file)
  del_imgtmp_args = 'rm %s'%(image_source)
  print "------Convertion Process-----"
  print commands.getoutput(convert_args)
  print "---------Ocr Process---------"
  print commands.getoutput(ocr_args)
  print "-----Deletion Process--------"
  print commands.getoutput(del_tif_args)  
  result_file = file(result_file+".txt", 'r')
  result_text = result_file.readline()
  result_file.close()
  commands.getoutput(del_txt_args)
  commands.getoutput(del_imgtmp_args)
  return result_text  
                 

