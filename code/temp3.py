from email.charset import QP
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QMainWindow, QVBoxLayout, QLineEdit
from PyQt6.QtGui import QIcon, QFont, QAction, QPixmap, QPainter, QColor, QPen, QBrush
import sys
from PyQt6.QtCore import Qt, QRect,QPoint



class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        widget = QLabel("Hello")
        font = widget.font()
        font.setPointSize(30)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.setCentralWidget(widget)

        # widget.setPixmap(QPixmap('cutout.jpg'))

        # widget2 = QLineEdit()
        # widget2.setMaxLength(10)
        # widget2.setPlaceholderText("Enter your text")

        # #widget.setReadOnly(True) # uncomment this to make readonly

        # widget2.returnPressed.connect(self.return_pressed)
        # widget2.selectionChanged.connect(self.selection_changed)
        # widget2.textChanged.connect(self.text_changed)
        # widget2.textEdited.connect(self.text_edited)

        # self.setCentralWidget(widget2)


    def return_pressed(self):
        print("Return pressed!")
        self.centralWidget().setText("BOOM!")

    def selection_changed(self):
        print("Selection changed")
        print(self.centralWidget().selectedText())

    def text_changed(self, s):
        print("Text changed...")
        print(s)

    def text_edited(self, s):
        print("Text edited...")
        print(s)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()