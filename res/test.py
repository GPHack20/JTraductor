import os
import sys
from PySide2.QtWidgets import *

from PySide2.QtCore import *

from PySide2.QtGui import *

class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.img_fold = r"/home/gphack20/Imágenes"

        self.widget_layout = QVBoxLayout(self)
        self.widget_layout.setMargin(0)
        img_path = os.path.join(self.img_fold, "ll.png")

        pixmap = QPixmap(img_path)
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        self.widget_layout.addWidget(lbl)


        self.setWindowTitle('Image viewer')
        self.adjustSize()
        self.show()

def main():

    app = QApplication(sys.argv)
    
    ex = Example()
    ex.showFullScreen()
    #ex.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()