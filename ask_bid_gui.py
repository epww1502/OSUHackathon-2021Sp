import sys
from PyQt5 import QtWidgets, QtGui, uic, QtCore
import pyupbit
import time

class AskBidThread(QtCore.QThread):
        data_sent = QtCore.pyqtSignal(list)

        def __init__(self, ticker):
                super().__init__()
                self.ticker = ticker
                self.alive = True

        def run(self):
                while self.alive:
                        data = pyupbit.get_orderbook(self.ticker)
                        time.sleep(0.05)
                        self.data_sent.emit(data)
        def close(self):
                self.alive = False

class AskBidWidget(QtWidgets.QWidget):
        def __init__(self, parent=None, ticker="KRW-BTC"):
                super().__init__(parent)
                uic.loadUi("./qt_ui/ask_bid.ui", self)
                self.ticker = ticker

                self.asksAnime = [ ]
                self.bidsAnime = [ ]

                for i in range(self.tableBids.rowCount()):
                        # ask book
                        ask_item_1 = QtWidgets.QTableWidgetItem(str(""))
                        ask_item_1.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tableAsks.setItem(i, 0, ask_item_1)

                        ask_item_2 = QtWidgets.QTableWidgetItem(str(""))
                        ask_item_2.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tableAsks.setItem(i, 1, ask_item_2)
                        
                        ask_item_3 = QtWidgets.QProgressBar(self.tableAsks)
                        ask_item_3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        ask_item_3.setStyleSheet("""
                                QProgressBar {background-color : rgba(0, 0, 0, 0%);border : 1}
                                QProgressBar::Chunk {background-color : rgba(255, 0, 0, 50%);border : 1}
                                """)
                        self.tableAsks.setCellWidget(i, 2, ask_item_3)
                        # add animation to make smooth
                        ask_anime = QtCore.QPropertyAnimation(ask_item_3, b"value")
                        ask_anime.setDuration(200)
                        self.asksAnime.append(ask_anime)

                        # bid book
                        bid_item_1 = QtWidgets.QTableWidgetItem(str(""))
                        bid_item_1.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tableBids.setItem(i, 0, bid_item_1)

                        bid_item_2 = QtWidgets.QTableWidgetItem(str(""))
                        bid_item_2.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        self.tableBids.setItem(i, 1, bid_item_2)
                        
                        bid_item_3 = QtWidgets.QProgressBar(self.tableAsks)
                        bid_item_3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        bid_item_3.setStyleSheet("""
                                QProgressBar {background-color : rgba(0, 0, 0, 0%);border : 1}
                                QProgressBar::Chunk {background-color : rgba(0, 255, 0, 40%);border : 1}
                                """)
                        self.tableBids.setCellWidget(i, 2, bid_item_3)
                        # add animation to make smooth
                        bid_anime = QtCore.QPropertyAnimation(bid_item_3, b"value")
                        bid_anime.setDuration(200)
                        self.bidsAnime.append(bid_anime)
                
                self.ab_w = AskBidThread(self.ticker)
                self.ab_w.data_sent.connect(self.update_data)
                self.ab_w.start()
        
        def update_data(self, data):
                tradingValues = []
                row_counter = 0
                for v in data[0]['orderbook_units']:
                        tradingValues.append(int(v['bid_price'] * v['bid_size']))
                        maxtradingValue = max(tradingValues)
                        row_counter += 1
                        if row_counter == 10:
                                row_counter = 0
                                break
                
                for i, v in enumerate(data[0]['orderbook_units']):
                        ask_item_1 = self.tableAsks.item(i, 0)
                        ask_item_1.setText(f"{v['ask_price']:,}")
                        ask_item_2 = self.tableAsks.item(i, 1)
                        ask_item_2.setText(f"{v['ask_size']:,}")
                        ask_item_3 = self.tableAsks.cellWidget(i, 2)
                        ask_item_3.setRange(0, maxtradingValue)
                        ask_item_3.setFormat(f"{tradingValues[i]:,}")

                        self.asksAnime[i].setStartValue(ask_item_3.value() if ask_item_3.value() > 0 else 0)
                        self.asksAnime[i].setEndValue(tradingValues[i])
                        self.asksAnime[i].start()


                        bid_item_1 = self.tableBids.item(i, 0)
                        bid_item_1.setText(f"{v['bid_price']:,}")
                        bid_item_2 = self.tableBids.item(i, 1)
                        bid_item_2.setText(f"{v['bid_size']:,}")
                        bid_item_3 = self.tableBids.cellWidget(i, 2)
                        bid_item_3.setRange(0, maxtradingValue)
                        bid_item_3.setFormat(f"{tradingValues[i]:,}")
                        bid_item_3.setValue(tradingValues[i])

                        self.bidsAnime[i].setStartValue(bid_item_3.value() if bid_item_3.value() > 0 else 0)
                        self.bidsAnime[i].setEndValue(tradingValues[i])
                        self.bidsAnime[i].start()

                        row_counter += 1
                        if row_counter == 10:
                                break
        
        def closeEvent(self, event):
                self.ab_w.close()



if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        ab_w = AskBidWidget()
        ab_w.show()
        exit(app.exec_())