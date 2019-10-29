import sys

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


class MouseTracker(QWidget):
    distance_from_center = 0
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Mouse Tracker')

        


        self.show()
        self.posI = None
        self.posF = None

    def mouseMoveEvent(self, event):
        self.update()
    def mousePressEvent(self,event):
        if self.posI != None and self.posF != None:
            self.posI=None
            self.posF=None
        if self.posI == None:
            self.posI = event.pos()
        else:
            if self.posF == None:
                self.posF = event.pos()

    def paintEvent(self, event):
        pixmap=QPixmap("ll.png")
        q = QPainter(self)  
        q.drawPixmap(self.rect(),pixmap)
        if self.posI != None and self.posF != None:
                      
            #q.drawLine(self.posI.x(), self.posI.y(), self.posF.x(), self.posF.y()) #posicion inicial de la coordenada
            
            
            
            q.drawLine(self.posI.x(), self.posI.y(), self.posF.x(), self.posI.y())
            q.drawLine(self.posF.x(), self.posI.y(), self.posF.x(), self.posF.y())
            q.drawLine(self.posF.x(), self.posF.y(), self.posI.x(), self.posF.y())
            q.drawLine(self.posI.x(), self.posI.y(), self.posI.x(), self.posF.y())
            

"""
(pix,piy)
(pfx,pfy)

"""

app = QApplication(sys.argv)
ex = MouseTracker()
ex.showFullScreen()
sys.exit(app.exec_())