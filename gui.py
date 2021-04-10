import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
import pyupbit
import time

tickers = ["KRW-BTC", "KRW-ETH", "KRW-BCH", "KRW-ETC"]
form_class = uic.loadUiType("./qt_ui/bull.ui")[0]

class Worker(QtCore.QThread):
        finished = QtCore.pyqtSignal(dict)
        
        def run(self):
                while True:
                        data = {}
                        for ticker in tickers:
                                data[ticker] = self.get_market_infos(ticker)
                        
                        self.finished.emit(data)
                        self.msleep(500)


        def get_market_infos(self, ticker):
                try:
                        df = pyupbit.get_ohlcv(ticker)
                        ma5 = df['close'].rolling(window=5).mean()
                        last_ma5 = ma5[-2]
                        price = pyupbit.get_current_price(ticker)
        
                        state = None
                        if price > last_ma5:
                                state = "bull"
                        else:
                                state = "bear"

                        return price, last_ma5, state
                except:
                        return(None, None, None)

class MyWindow(QtWidgets.QMainWindow, form_class):
        def __init__(self):
                super().__init__()
                self.setGeometry(800,300,400,400)
                self.setWindowIcon(QtGui.QIcon(".\image\kimchicoin.png"))
                self.setupUi(self)
                #self.tableWidget.setRowCount(len(tickers))
                
                btn = QtWidgets.QPushButton("btn 1", self)
                btn.move(10,10)

                btn2 = QtWidgets.QPushButton("btn 2", self)
                btn2.move(10,40)

                btn.clicked.connect(self.btn_clicked)
                self.setWindowTitle("Kimchicoin bot")

                self.worker = Worker()
                self.worker.finished.connect(self.update_table_widget)
                self.worker.start()
        @QtCore.pyqtSlot(dict)

                # timer = QtCore.QTimer(self)
                # timer.start(5000)
                # timer.timeout.connect(self.timeout)

        def timeout(self):
                for i, ticker in enumerate(tickers):
                        item = QtWidgets.QTableWidgetItem(ticker)
                        self.tableWidget.setItem(i, 0, item)
 
                        price, last_ma5, state = self.get_market_infos(ticker)
                        self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(price)))
                        self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(last_ma5)))
                        self.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(state))

        def btn_clicked(self):
                print("btn clikced!")
        
        def update_table_widget(self, data):
                try:
                        for ticker, infos in data.items():
                                index = tickers.index(ticker)

                                self.tableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem(ticker))
                                self.tableWidget.setItem(index, 1, QtWidgets.QTableWidgetItem(str(infos[0])))
                                self.tableWidget.setItem(index, 2, QtWidgets.QTableWidgetItem(str(infos[1])))
                                self.tableWidget.setItem(index, 3, QtWidgets.QTableWidgetItem(str(infos[2])))
                except:
                        pass

app = QtWidgets.QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
print(pyupbit.get_tickers(fiat="KRW"))
# btn = QtWidgets.QPushButton("bitcoin!")
# btn.show()
# label = QtWidgets.QLabel("Hello")
# label.show()
# app.exec_()