import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QHBoxLayout, QListWidget
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter
from io import BytesIO

workdir = ""


app = QApplication([])
my_win = QWidget()
my_win.show()

btnL = QPushButton('Лево')
btnR = QPushButton('Право')
btnM = QPushButton('Зеркало')
btnS = QPushButton('Резкость')
btnHB = QPushButton('Ч/Б')
btnF = QPushButton('Папка')

FLst = QListWidget()

pct = QLabel()

vLayout = QVBoxLayout()
vLayout2 = QVBoxLayout()
hLayout = QHBoxLayout()
hLayout2 = QHBoxLayout()

vLayout.addWidget(btnF)
vLayout.addWidget(FLst)
hLayout.addWidget(btnL)
hLayout.addWidget(btnR)
hLayout.addWidget(btnM)
hLayout.addWidget(btnS)
hLayout.addWidget(btnHB)
vLayout2.addWidget(pct, 80)
vLayout2.addLayout( hLayout, 20)
hLayout2.addLayout( vLayout, 20)
hLayout2.addLayout( vLayout2, 80)


def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


files = ['a.txt', 'b.png', 'c.jpg']


def filter(files, extensions):
    result = []
    for name in files:
        for ext in extensions:
            if name.endswith(ext):
                result.append(name)
    return result

def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.gif', '.png', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    FLst.clear()
    for name in filenames:
        FLst.addItem(name)

class ImageProcessor :
    def __init__(self):
        self.image = None
        self.name = None
        self.savedir = "modified/"
        self.path = None
        self.image_path = None

    def loadImage(self, path, name):
        self.path = path
        self.name = name
        self.image_path = os.path.join(path, name)
        self.image = Image.open(self.image_path)
    
    def showImage(self):
        pct.hide()
        image_pixmap = QPixmap(self.image_path)
        image_pixmap = image_pixmap.scaled(\
            pct.width(),
            pct.height(),
            Qt.KeepAspectRatio)
        pct.setPixmap(image_pixmap)
        pct.show()

    def saveImage(self):
        save_path = os.path.join(self.path, self.savedir)
        if not (os.path.exists(save_path) or os.path.isdir(save_path)):
            os.mkdir(save_path)
        save_name = os.path.join(save_path, self.name)
        self.image.save(save_name)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        self.image_path = os.path.join(self.path, self.savedir)
        self.image_path = os.path.join(self.image_path, self.name)
        self.showImage()

    def do_mirrow(self):

        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        self.image_path = os.path.join(self.path, self.savedir)
        self.image_path = os.path.join(self.image_path, self.name)
        self.showImage()

    def do_s(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        self.image_path = os.path.join(self.path, self.savedir)
        self.image_path = os.path.join(self.image_path, self.name)
        self.showImage()

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        self.image_path = os.path.join(self.path, self.savedir)
        self.image_path = os.path.join(self.image_path, self.name)
        self.showImage()

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        self.image_path = os.path.join(self.path, self.savedir)
        self.image_path = os.path.join(self.image_path, self.name)
        self.showImage()

    


processor = ImageProcessor()

def showChosenImage():
    if FLst.currentRow() >= 0:
        filename = FLst.currentItem().text()
        processor.loadImage(workdir, filename)
        processor.showImage()

FLst.currentRowChanged.connect(showChosenImage)
btnF.clicked.connect(showFilenamesList)
my_win.setLayout(hLayout2)
btnHB.clicked.connect(processor.do_bw)
btnM.clicked.connect(processor.do_mirrow)
btnS.clicked.connect(processor.do_s)
btnL.clicked.connect(processor.do_left)
btnR.clicked.connect(processor.do_right)
app.exec_()
