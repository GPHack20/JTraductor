import sys

"""
from PySide2.QtWidgets import (QApplication, QLabel, QWidget)
from PySide2.QtGui import QPainter, QColor, QPen
from PySide2.QtCore import Qt
"""

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
        self.label = QLabel(self)
        self.label.resize(500, 40)

        pixmap=QPixmap("ll.png")
        self.fondo=QLabel(self)
        self.fondo.setPixmap(pixmap)


        self.show()
        self.posI = None
        self.posF = None

    def mouseMoveEvent(self, event):
        distance_from_center = round(((event.y() - 250)**2 + (event.x() - 500)**2)**0.5)
        self.label.setText('Coordinates: ( %d : %d )' % (event.x(), event.y()) + "Distance from center: " + str(distance_from_center))       
        #self.pos = event.pos()
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
        if self.posI != None and self.posF != None:
            q = QPainter(self)            
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
#ex.showFullScreen()
sys.exit(app.exec_())