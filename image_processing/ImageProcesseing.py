# -*- coding: utf-8 -*-

import sys  
import os
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QAction

import horus.image as Image

class MainWindow (QtGui.QMainWindow):
    """
        Class responsible by construct a main GUI
    """    
    def __init__(self, parent=None):
        """
            Create the GUI
        """
        self.image = QtGui.QImage()
        self.processed_image = QtGui.QImage()
        self.filename = None
        self.tmp_name = "/tmp/temp.jpg"
       
        super(MainWindow, self).__init__(parent)
        
        self.setObjectName("MainWindow")
        self.resize(1010, 465)
        
        self.setWindowTitle( QtGui.QApplication.translate( "MainWindow", 
                                "HORUS_APP: Processamento de Imagem",  
                                None, QtGui.QApplication.UnicodeUTF8) )

    
        self.centralwidget = QtGui.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(5, 30, 1000, 415))

        self.left_widget = QtGui.QWidget(self.widget)
        self.left_widget.setGeometry(QtCore.QRect(5, 5, 400, 410))
        
        self.center_widget = QtGui.QWidget(self.widget)
        self.center_widget.setGeometry(QtCore.QRect(410, 5, 180, 410))
        
        self.right_widget = QtGui.QWidget(self.widget)
        self.right_widget.setGeometry(QtCore.QRect(595, 5, 400, 410))        

        self.widget_layout = QtGui.QHBoxLayout()
        self.widget_layout.addWidget(self.left_widget)
        self.widget_layout.addWidget(self.center_widget)
        self.widget_layout.addWidget(self.right_widget)  
 
        self.zoomSpinBox = QtGui.QSpinBox(self.left_widget)
        self.zoomSpinBox.setGeometry(QtCore.QRect(100, 5, 200, 25))
        self.zoomSpinBox.setRange(1, 200)
        self.zoomSpinBox.setSuffix(" %")
        self.zoomSpinBox.setValue(100)
        self.zoomSpinBox.setToolTip("    Zoom the image")
        self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
        self.zoomSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.connect(self.zoomSpinBox,
                     QtCore.SIGNAL("valueChanged(int)"), self.showImageLeft)

        self.graphicsView = QtGui.QLabel(self.left_widget)
        self.graphicsView.setGeometry(QtCore.QRect(5, 35, 390, 340))

        self.zoomSpinBox_2 = QtGui.QSpinBox(self.right_widget)
        self.zoomSpinBox_2.setGeometry(QtCore.QRect(100, 5, 200, 25))
        self.zoomSpinBox_2.setRange(1, 200)
        self.zoomSpinBox_2.setSuffix(" %")
        self.zoomSpinBox_2.setValue(100)
        self.zoomSpinBox_2.setToolTip("Zoom the image")
        self.zoomSpinBox_2.setStatusTip(self.zoomSpinBox_2.toolTip())
        self.zoomSpinBox_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.connect(self.zoomSpinBox_2,
                     QtCore.SIGNAL("valueChanged(int)"), self.showImageRight)       

        self.graphicsView_2 = QtGui.QLabel(self.right_widget)
        self.graphicsView_2.setGeometry(QtCore.QRect(5, 35, 390, 340))
        
        self.comboBox = QtGui.QComboBox(self.center_widget)
        self.comboBox.setGeometry(QtCore.QRect(5, 5, 170, 25))
        self.comboBox.addItems( ["Filtro", 
                                 "-------------",
                                 "Horizontal Edge Detector", 
                                 "Vertical Edge Detector",
                                 "Full Edge Detector",
                                 "Highlight Luminance"] )
        self.connect( self.comboBox, QtCore.SIGNAL("currentIndexChanged(int)"), 
                      self.applyFilter )
        
        self.comboBox_2 = QtGui.QComboBox(self.center_widget)
        self.comboBox_2.setGeometry(QtCore.QRect(5, 35, 170, 25))
        self.comboBox_2.addItems( ["Mode", 
                                   "-------------",
                                   "RGB", 
                                   "Gray Scale",
                                   "Binary"] )
        self.connect( self.comboBox_2, QtCore.SIGNAL("currentIndexChanged(int)"), 
                      self.convertMode )

        self.comboBox_3 = QtGui.QComboBox(self.center_widget)
        self.comboBox_3.setGeometry(QtCore.QRect(5, 65, 170, 25))
        self.comboBox_3.addItems( ["Projection", 
                                   "-------------",
                                   "Horizontal", 
                                   "Vertical"] )
        self.connect( self.comboBox_3, QtCore.SIGNAL("currentIndexChanged(int)"), 
                      self.project )

                                               
        self.browser = QtGui.QTextBrowser(self.center_widget)
        self.browser.setGeometry(QtCore.QRect(5, 95, 170, 270))
        
        self.radio_buttom_origin = QtGui.QRadioButton(self.center_widget)
        self.radio_buttom_origin.setGeometry(QtCore.QRect(5, 340, 170, 20))
        self.radio_buttom_origin.setText("Change Left Image")

        self.radio_buttom_modified = QtGui.QRadioButton(self.center_widget)
        self.radio_buttom_modified.setGeometry(QtCore.QRect(5, 360, 170, 20))
        self.radio_buttom_modified.setText("Change Right Image")
        self.radio_buttom_modified.setChecked(True)
        
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.setTitle( QtGui.QApplication.translate( "MainWindow",
                                "&File", None, QtGui.QApplication.UnicodeUTF8) )
                                
        self.actionOpen = QtGui.QAction(self)
        self.actionOpen.setObjectName("actionOpen")
        self.fileMenu.addAction(self.actionOpen)
        self.actionOpen.setText(QtGui.QApplication.translate( "MainWindow",
                                "&Open", None, QtGui.QApplication.UnicodeUTF8) )

        self.actionQuit = QtGui.QAction(self)
        self.actionQuit.setObjectName("actionQuit")
        self.fileMenu.addAction(self.actionQuit)
        self.actionQuit.setText(QtGui.QApplication.translate( "MainWindow",
                                "&Quit", None, QtGui.QApplication.UnicodeUTF8) )

        self.sizeLabel = QtGui.QLabel()
        self.sizeLabel.setFrameStyle( QtGui.QFrame.StyledPanel | 
                                      QtGui.QFrame.Sunken ) 

        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.statusbar.addPermanentWidget(self.sizeLabel)

        QtCore.QMetaObject.connectSlotsByName(self)

      
    def on_actionQuit_triggered(self):
        """
            This metod is called when the action actionQuit is triggered, 
            ie when the Quit menu entry is triggered.

            The control of the called is doing by QT.
        """
        exit()

    def on_actionOpen_triggered(self):
        """
            This metod is called when the action actionOpen is triggered, 
            ie when the Open menu entry is triggered.

            The control of the called is doing by QT.
        """
        dir = os.path.dirname(self.filename) if self.filename is not None else "."

        # Lista de formatos de Imagens suportados
        formats = ["*.%s" % unicode(format).lower() \
                     for format in QtGui.QImageReader.supportedImageFormats() ]
        
        # Seleciona um arquivo e configura a caixa de dialogo para abertura deste
        filename = unicode(QtGui.QFileDialog.getOpenFileName(self,
                            "Open File", dir,
                            "File types: %s" % " ".join(formats)))
        
        # Se um arquivo for selecionado chama o metodo para le-lo
        if filename:
            self.loadFile(filename)


    def loadFile(self, filename=None):
        # Não entendi
        if filename is None:
            action = self.sender()
            if isinstance(action, QAction):
                filename = unicode(action.data().toString())
            else:
                return
        
        # Procedimento para abrir o arquivo
        if filename:
            self.filename = None
            image = QtGui.QImage(filename)
            if image.isNull():
                message = "Failed to read %s" % filename
            else:
                self.image = QtGui.QImage()
                self.image = image
                self.processed_image = image
                self.filename = filename
                self.showImageLeft()
                self.showImageRight()
                self.sizeLabel.setText("%d x %d" % (image.width(), image.height()))
                message = "Loaded %s" % os.path.basename(filename)
            
            self.updateStatus(message)
            self.browser.append("Open: %s (%s)"%(os.path.basename(filename), filename))
            self.comboBox.setCurrentIndex(0)
       
    def showImageLeft(self, percent = None):
        """
            This method show the origin image on component graphicsView (on left).
            
            When a zoomSpinBox_X is changed automatically this method is
            called passing the parameter percent how the value of the zoomSpinBox
        """
        if self.image.isNull():
            return
        # Altera a imagem atraves do percentual de seu tamanho (seu percentual é 
        # determinado pelo valor do componente zoomSpinBox)
        if percent is None:
            percent = self.zoomSpinBox.value()
        # valor real do percentual da imagem (por exemplo 10% = 0,10)
        factor = percent / 100.0
        
        # Escalamento da imagem
        width = self.image.width() * factor
        height = self.image.height() * factor
        image = self.image.scaled(width, height, QtCore.Qt.KeepAspectRatio)
        
        #exibe a imagem
        self.graphicsView.setPixmap(QtGui.QPixmap.fromImage(image))
        
    
    def showImageRight(self, percent = None):
        """
            This method show the origin image on component graphicsView (on left).
            
            When a zoomSpinBox_X is changed automatically this method is
            called passing the parameter percent how the value of the zoomSpinBox
        """
        if self.image.isNull():
            return
        # Altera a imagem atraves do percentual de seu tamanho (seu percentual é 
        # determinado pelo valor do componente zoomSpinBox)
        if percent is None:
            percent = self.zoomSpinBox_2.value()
        # valor real do percentual da imagem (por exemplo 10% = 0,10)
        factor = percent / 100.0
        
        # Escalamento da imagem
        width = self.processed_image.width() * factor
        height = self.processed_image.height() * factor
        image = self.processed_image.scaled(width, height, QtCore.Qt.KeepAspectRatio)
        
        #exibe a imagem
        self.graphicsView_2.setPixmap(QtGui.QPixmap.fromImage(image))

    def updateStatus(self, message):
        """
           This method changes the values of window to reference the image showed.
        """
        # Exibe a mensagem recebida por parametro na barra de status (parte de 
        # baixo da janela) por 5 segundos (5000 milisegundos)
        self.statusBar().showMessage(message, 5000)

        if self.filename is not None:
            self.setWindowTitle("HORUS_APP: Processamento de Imagem - %s[*]" % \
                                os.path.basename(self.filename))
        elif not self.image.isNull():
            self.setWindowTitle("HORUS_APP: Processamento de Imagem - Unnamed[*]")
        else:
            self.setWindowTitle("HORUS_APP: Processamento de Imagem[*]")
        
        # Adicionar o nome da imagem no log
        self.browser.clear()

    def applyFilter(self):
        """
            This method choice the filter that will applyed according to comboBox 
        """
        if self.image.isNull():
            return
        combo_box_index = self.comboBox.currentIndex()
        if combo_box_index > 1:
            self.browser.append("Apply Filter: %s"%(unicode(self.comboBox.currentText())))
            
            image = Image.Image(path = self.filename)
            processer_image = Image.ProcessingImage(image)
            if combo_box_index == 2:
                image = processer_image.applyFilter(Image.HORIZONTAL_EDGE_DETECTED)
            elif combo_box_index == 3:
                image = processer_image.applyFilter(Image.VERTICAL_EDGE_DETECTED)
            elif combo_box_index == 4:
                image = processer_image.fullEdgeDetection()
            elif combo_box_index == 5:    
                image = processer_image.highlightLuminance()
                
            image.save(self.tmp_name)
            
            self.processed_image = QtGui.QImage(self.tmp_name)
            self.graphicsView_2.setPixmap(QtGui.QPixmap.fromImage(self.processed_image))

    def convertMode(self):
        """
            This method convert the mode of image (modify the processed image).            
        """
        if self.image.isNull():
            return
        combo_box_index = self.comboBox_2.currentIndex()
        if combo_box_index > 1:
            self.browser.append("Mode: %s"%(unicode(self.comboBox.currentText())))
            
            image = Image.Image(path = self.filename)
            processer_image = Image.ProcessingImage(image)
            if combo_box_index == 2:
                image = processer_image.convertMode("RGB")
            elif combo_box_index == 3:
                image = processer_image.convertMode("L")
            elif combo_box_index == 4:
                 image = processer_image.simpleThreshold(128)

            image.save(self.tmp_name)
            
            self.processed_image = QtGui.QImage(self.tmp_name)
            self.graphicsView_2.setPixmap(QtGui.QPixmap.fromImage(self.processed_image))

    def project(self):
        """
            This method show the graphics of projection (vertical or horizontal)
            of the image.
        """
        if self.image.isNull():
            return
        combo_box_index = self.comboBox_3.currentIndex()
        if combo_box_index > 1:
            self.browser.append("%s Projection"%(unicode(self.comboBox_3.currentText())))
            
            image = Image.Image(path = self.filename)
            processer_image = Image.ProcessingImage(image)
            image = processer_image.convertMode("L")
            processer_image = Image.ProcessingImage(image)
            
            if combo_box_index == 2:
                projection = processer_image.horizontalProjection()
            elif combo_box_index == 3:
                projection = processer_image.verticalProjection()

            from horus import graphics
            graphics.generateGraph('/tmp', 'proj', projection, None, 'png')
            image = Image.Image(path = "/tmp/proj.png")
            
            image.save(self.tmp_name)
            
            self.processed_image = QtGui.QImage(self.tmp_name)
            self.graphicsView_2.setPixmap(QtGui.QPixmap.fromImage(self.processed_image))
            
            
               
app = QtGui.QApplication(sys.argv)
form = MainWindow ()
form.show()
app.exec_()        
