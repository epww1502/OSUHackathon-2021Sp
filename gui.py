import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore

form_class = uic.loadUiType("bull.ui")[0]

class MyWindow(QtWidgets.QMainWindow, form_class):
        def __init__(self):
                super().__init__()
                self.setGeometry(800,300,400,400)
                self.setWindowIcon(QtGui.QIcon(".\image\kimchicoin.png"))
                self.setupUi(self)
                
                btn = QtWidgets.QPushButton("btn 1", self)
                btn.move(10,10)

                btn2 = QtWidgets.QPushButton("btn 2", self)
                btn2.move(10,40)

                btn.clicked.connect(self.btn_clicked)
                self.setWindowTitle("Kimchicoin bot")

                timer = QtCore.QTimer(self)
                timer.start(5000)
                timer.timeout.connect(self.timeout)

        def timeout(self):
                print("it is bull market! time to sell!")

        def btn_clicked(self):
                print("btn clikced!")

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
# btn = QtWidgets.QPushButton("bitcoin!")
# btn.show()
# label = QtWidgets.QLabel("Hello")
# label.show()
# app.exec_()