import math

from PyQt6.QtCore import *
from PyQt6.QtGui import * 
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGraphicsItem, QGraphicsView, QGraphicsScene, QHBoxLayout,QGraphicsLineItem, QGraphicsPathItem, QVBoxLayout, QGraphicsEllipseItem
import sys


"""
class Widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.btn = QPushButton("Add Line")

        self.gv = QGraphicsView()
        self.scene = QGraphicsScene(self)
        self.gv.setScene(self.scene) 
        #self.gv.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        lay = QHBoxLayout(self)
        lay.addWidget(self.btn)
        lay.addWidget(self.gv)

        self.p_item = self.scene.addPixmap(QPixmap("lena.png"))
        self.btn.clicked.connect(self.add_line)

    def add_line(self):
        p1 = self.p_item.boundingRect().topLeft()
        p2 = self.p_item.boundingRect().center()
        line = QGraphicsLineItem(QLineF(p1, p2), self.p_item)
        line.setPen(QPen(Qt.GlobalColor.red, 5))
        line.setFlag(QGraphicsItem.ItemIsMovable, True)
        line.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.gv.fitInView(self.scene.sceneRect())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec())
"""


class Widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.btn = QPushButton("Press Me")

        self.gv = QGraphicsView()
        self.scene = QGraphicsScene(self)
        self.gv.setScene(self.scene) 
        #self.gv.setRenderHint(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        lay = QVBoxLayout(self)
        lay.addWidget(self.btn)
        lay.addWidget(self.gv)

        self.p_item = self.scene.addPixmap(QPixmap("image3.png"))
        self.p_item.setPos(100, 100)

        self.btn.clicked.connect(self.print_)
        self.emulate_drawing()

    def emulate_drawing(self):
        rect = self.p_item.boundingRect()

        path = QPainterPath()
        A = rect.height()

        for i in range(0, int(rect.width())-10):
            path.lineTo(i, A/2*(1-math.cos(i*math.pi/40)))

        item = QGraphicsPathItem(path, self.p_item)
        item.setPen(QPen(Qt.GlobalColor.red, 10))

        r = QRectF(QPointF(), rect.size()*0.5)

        item = QGraphicsEllipseItem(r, self.p_item)
        item.setPos(rect.center()-r.center())
        item.setPen(QPen(Qt.GlobalColor.blue, 10))

    def print_(self):

        image = QImage(self.gv.viewport().size(), QImage.Format.Format_RGB888)
        image.fill(Qt.GlobalColor.transparent)

        painter = QPainter(image)
        self.gv.render(painter)
        painter.end()

        image.save("output.png")

    def showEvent(self, event):
        QWidget.showEvent(self, event)
        self.gv.fitInView(self.scene.sceneRect())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec())
