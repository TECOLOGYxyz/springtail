from email.charset import QP
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QMainWindow, QVBoxLayout, QFileDialog
from PyQt6.QtGui import QIcon, QFont, QAction, QPixmap, QPainter, QColor, QPen, QBrush
import sys
from PyQt6.QtCore import Qt, QRect,QPoint


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interactive Springtail Counter")
        self.setWindowIcon(QIcon("icons/flower.png"))
        self.setGeometry(50, 30, 600, 400)

        self.central_widget = QWidget()               
        self.setCentralWidget(self.central_widget)    
        lay = QGridLayout(self.central_widget)
 
        self.label = QLabel(self)
        self.pixmap = QPixmap('cutout.jpg')
        self.label.setPixmap(self.pixmap)


        self.createMenu()
        lay.addWidget(self.label)
        self.show()

  

        # def open_dialog(self):
        #     fname = QFileDialog.getOpenFileName(
        #         self,
        #         "Open File",
        #         "${HOME}",
        #         "All Files (*);; Python Files (*.py);; PNG Files (*.png)",
        #     )


        # grid = QGridLayout()

        # btnLoadImg = QPushButton("Load image")
        # btnDetect = QPushButton("Detect")
        # btnClose = QPushButton("Exit")
        # grid.addWidget(btnLoadImg,0,0)
        # grid.addWidget(btnDetect,1,0)
        # grid.addWidget(btnClose,0,10)

        # self.setLayout(grid)

    def createMenu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        actionMenu = mainMenu.addMenu("Action")


        newAction = QAction(QIcon("icons/image.png"), "Open image...", self)
        newAction.setShortcut("Ctrl+N")
        fileMenu.addAction(newAction)
        self.menu.addAction(self.action)
        self.action.triggered.connect(self.my_function)

        saveAction = QAction(QIcon("icons/save.png"), "Save...", self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        
        fileMenu.addSeparator()
        exitAction = QAction(QIcon("icons/exit.png"), "Exit", self)
        exitAction.triggered.connect(self.closeWindow)
        fileMenu.addAction(exitAction)

        detectAction = QAction(QIcon("icons/detect.png"), "Run detection...", self)
        detectAction.setShortcut("Ctrl+D")
        actionMenu.addAction(detectAction)


    def closeWindow(self):
        self.close()

        # grid = QGridLayout()

        # btnLoadImg = QPushButton("Load image")
        # btnDetect = QPushButton("Detect")
        # btnClose = QPushButton("Exit")

        # grid.addWidget(btnLoadImg,0,0)
        # grid.addWidget(btnDetect,1,0)
        # grid.addWidget(btnClose,0,10)

        # self.setLayout(grid)

    # def createWidget(self):
    #     btn = QPushButton("Load image", self)
    #     btn.move(10,10)
    #     btn.setStyleSheet('background-color:white')
    #     btn.setFont(QFont("Courier New", 15))
    #     btn.clicked.connect(self.btnClick)
        
    #     self.label = QLabel("Ja da", self)

    # def btnClick(self):
    #     self.label.setText("Clicked")
    #     self.label.setStyleSheet('background-color:red')


app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec())



# app = QApplication(sys.argv)

# window = QWidget()


# window.show()

# sys.exit(app.exec())