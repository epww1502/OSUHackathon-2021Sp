import sys
from pyupbit import WebSocketManager
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class SummaryView(QtCore.QThread):

    data24H = QtCore.pyqtSignal(int, float, float, int, float, int, int, int)
    

    def __init__(self, ticker="KRW-BTC"):
        super().__init__()
        self.ticker = ticker
        self.running = True

# {'type': 'ticker', 'code': 'KRW-BTC', 
# 'opening_price': 78531000.0, 
# 'high_price': 79389000.0, 
# 'low_price': 77881000.0, 
# 'trade_price': 78905000.0, 
# 'prev_closing_price': 78530000.0, 
# 'acc_trade_price': 65978730871.70746, 
# 'change': 'RISE', 'change_price': 375000.0, 
# 'signed_change_price': 375000.0, 
# 'change_rate': 0.0047752451, 
# 'signed_change_rate': 0.0047752451, 
# 'ask_bid': 'ASK', 'trade_volume': 0.00014367, 
# 'acc_trade_volume': 836.64747003, 
# 'trade_date': '20210411', 
# 'trade_time': '010740', 
# 'trade_timestamp': 1618103260000, 
# 'acc_ask_volume': 382.746141, 
# 'acc_bid_volume': 453.90132903, 
# 'highest_52_week_price': 79600000.0, 
# 'highest_52_week_date': '2021-04-10', 
# 'lowest_52_week_price': 7929000.0, 
# 'lowest_52_week_date': '2020-04-16', 
# 'trade_status': None, 'market_state': 'ACTIVE', 
# 'market_state_for_ios': None, 'is_trading_suspended': False, 
# 'delisting_date': None, 'market_warning': 'NONE', 
# 'timestamp': 1618103260894, 
# 'acc_trade_price_24h': 750858334924.5751, 
# 'acc_trade_volume_24h': 9568.67265675, 
# 'stream_type': 'SNAPSHOT'}

    def run(self):
        websocket = WebSocketManager("ticker", [f"{self.ticker}"])
        while self.running:
            socket_data = websocket.get()
            #print(socket_data)

            self.data24H.emit(
                            int(socket_data['trade_price']),
                            float(socket_data['signed_change_rate'] * 100),
                            float(socket_data['acc_trade_volume_24h']),
                            int(socket_data['high_price']),
                            float(socket_data['acc_trade_price_24h']),
                            int(socket_data['low_price']),
                            int(socket_data['signed_change_price']),
                            int(socket_data['prev_closing_price'])
            )

        websocket.terminate()

    def close(self):
        self.running = False


class SummaryWidget(QWidget):
    def __init__(self, parent=None, ticker="KRW-BTC"):
        super().__init__(parent)
        uic.loadUi("./qt_ui/summary_view.ui", self)

        self.ticker = ticker
        self.sum_view = SummaryView(ticker)
        self.sum_view.data24H.connect(self.use_data24)
        self.sum_view.start()

    def end_event(self, event):
        self.sum_view.close()

    def use_data24(self, trade_price, change_rate, acc_trade_volume_24h, high_price, acc_trade_price_24h, low_price, change_price, prev_closing_price):
        self.label_1.setText(f"{trade_price:,}")
        self.label_2.setText(f"{change_rate:,.2f}%")
        self.label_4.setText(f"{acc_trade_volume_24h:,.3f} {self.ticker[4:]}")
        self.label_6.setText(f"{high_price:,}")
        self.label_8.setText(f"{acc_trade_price_24h:,.0f} KRW")
        self.label_10.setText(f"{low_price:,}")
        self.label_12.setText(f"{change_price:,}")
        self.label_14.setText(f"{prev_closing_price:,}")
        self.__updateStyle()


    def __updateStyle(self):
        if '-' in self.label_2.text():
            self.label_1.setStyleSheet("color:blue;")
            self.label_2.setStyleSheet("background-color:blue;color:white;")
            self.label_12.setStyleSheet("color:blue;")
        else:
            self.label_1.setStyleSheet("color:red;")
            self.label_2.setStyleSheet("background-color:red;color:white;")
            self.label_12.setStyleSheet("color:red;")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ob = SummaryWidget()
    ob.show()
    exit(app.exec_())