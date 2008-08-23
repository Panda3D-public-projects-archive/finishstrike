from PIL import Image

class HIImage:
   def openImage(self, name):
       """ Open an image source """

   def saveImage(self, name):
       """ Save an image source """

   def newImage(self, mode, size, color):
       """ Create a new image """

   def copyObjectImage(self):
       """ Copy an instance of HImage """

   def copyImage(self):
       """ Copy an image """

   def generateHistogram(self):
       """ genererate the histogram of image """

   def cropImage(self, box):
       """ Execute a crop on Image """


class HImage(HIImage):
    """
    RETIRAR O TODO APOS PRONTO E VERIFICAR SEMPRE SE NAO HA NADA DEFINITIVO - OU QUASE - ESCRITO EM PORTUGUES
    TODO1: refatorar a classe para esconder o atributo image do tipo PIL.Image.
    TODO2: remover o metodo copyImage, para que o cliente nao tenha acesso ao atributo 'image'
    TODO3: modificar o retorno de cropImage para que o cliente nao tenha acesso a uma imagem do tipo PIL.Image
    TODO4: criar os atributos para filename e size, acessiveis ao cliente (acessivel atraves de get)
    TODO5: modify the method copyObjectImage to use copy.copy
    TODO6: retornar um erro quando conhecido quando o box passado ao metodo cropImage for invalido.
    REFATORAR OS TESTES APOS REALIZAR AS CITADAS MODIFICACOES
    """
    
    def openImage(self, name):
        self.image = Image.open(name)
        return self.image

    def saveImage(self, name):
        self.image.save(name)

    def newImage(self, mode, size, color):
        self.image = Image.new(mode, size, color)

    def copyObjectImage(self):
        im = HImage()
        im.image = self.image.copy()
        return im

    def copyImage(self):
        return self.image.copy()

    def generateHistogram(self):
        return self.image.histogram()

    def cropImage(self, box):
        im = self.image.crop(box)
        if im.size==(0,0):
            return self.image.crop(box)
        else:
            return "Invalid region to Crop"

   






