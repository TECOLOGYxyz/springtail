import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30,30,600,400)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        br = QtGui.QBrush(QtGui.QColor(300, 50, 50, 400))  
        qp.setBrush(br)   
        qp.drawRect(QtCore.QRect(self.begin, self.end))       

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    # def mouseReleaseEvent(self, event):
    #     self.begin = event.pos()
    #     self.end = event.pos()
    #     self.update()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec())

"""
import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt
class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    
    
    self.label = QLabel()
    canvas = QPixmap(400, 300)
    canvas.fill(Qt.GlobalColor.white)
    self.label.setPixmap(canvas)
    self.setCentralWidget(self.label)
    self.draw_something()    


  def draw_something(self):
    pixmap = self.label.pixmap()
    painter = QPainter()
    painter.begin(pixmap) 
    painter.drawLine(10, 10, 300, 200)
    painter.end()

    self.label.setPixmap(pixmap)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
"""