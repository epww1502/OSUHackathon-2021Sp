import sys
from PyQt5 import QtWidgets, QtGui, uic, QtCore, QtChart
import pyupbit
import datetime
import time
from auto_function import *

FORM = uic.loadUiType("./qt_ui/main.ui")[0]

class AutoWorker(QtCore.QThread):
    trading_sent = QtCore.pyqtSignal(str, str, str, str)

    def __init__(self, ticker, upbit):
        super().__init__()
        self.ticker = ticker
        self.upbit = upbit
        self.alive = True

    def run(self):
        now = datetime.datetime.now()
        print(now)
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        print(mid)
        print(mid + datetime.timedelta(seconds=10))
        ma5 = get_five_days(self.ticker)
        target_price = get_target(self.ticker)
        print(ma5)
        print(target_price)
        current_price = pyupbit.get_current_price(self.ticker)

        self.trading_sent.emit(f"target price: {target_price}", f"current price: {current_price}", f"MA5: {ma5}", " ")
        wait_flag = False

        while self.alive:
            try:
                now = datetime.datetime.now()
                if mid < now < mid + datetime.timedelta(seconds=10):
                        print("selling !")
                        target_price = get_target(self.ticker)
                        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
                        ma5 = get_five_days(self.ticker)
                        call_sell = sell_crypto(self.ticker, self.upbit)
                        balance = self.upbit.get_balances()

                        if call_sell != False:
                                result = self.upbit.get_order(self.ticker, state="done")
                                print(result[0])

                                timestamp = str(result[0]['created_at'])
                                new_stamp = "date: " + timestamp[0:10] + " time: " + timestamp[11:] 

                                self.trading_sent.emit("sell", str(result[0]['market']), str(result[0]['volume']), new_stamp)
                                for i in range(len(balance)):
                                        self.trading_sent.emit("blance", f"{str(balance[i]['currency'])}", f"{str(balance[i]['balance'])}", " ")
                                wait_flag = False
                        else:
                                wait_flag = False

                if wait_flag == False:
                    print(current_price, target_price, ma5)
                    #target_price = 10000                # changed for demo
                    if (current_price > target_price) and (current_price > ma5):
                        print("buying !")
                        call_buy = buy_crypto(self.ticker, self.upbit)
                        balance = self.upbit.get_balances()

                        if call_buy != False:
                                result = self.upbit.get_order(self.ticker, state="done")
                                print(result[0])

                                timestamp = str(result[0]['created_at'])
                                new_stamp = "date: " + timestamp[0:10] + " time: " + timestamp[11:]

                                self.trading_sent.emit("buy", str(result[0]['market']), str(result[0]['volume']), new_stamp)
                                for i in range(len(balance)):
                                        self.trading_sent.emit("blance", f"{str(balance[i]['currency'])}", f"{str(balance[i]['balance'])}", " ")
                                wait_flag = True
                        else:
                                wait_flag = True
            except:
                print("pass!")
                pass
            time.sleep(1)

    def close(self):
        self.alive = False

class MainWindow(QtWidgets.QMainWindow, FORM):
        def __init__(self):
                super().__init__()
                self.setWindowIcon(QtGui.QIcon(".\image\kimchicoin.png"))
                self.setupUi(self)
                self.ticker = "KRW-BTC"
                self.setWindowTitle("Kimchicoin bot")

                self.auto_trading_bttn.clicked.connect(self.autotrading_btn)
        
        def autotrading_btn(self):
                if self.auto_trading_bttn.text() == "auto trade":
                        api_key = self.api_key.text()
                        secret_key = self.secret_key.text()
                        
                        if len(api_key) != 40 or len(secret_key) != 40:
                                self.textEdit.append("[FAILED] key is not correct! check it please")
                                return
                        else:
                                self.ub = pyupbit.Upbit(api_key, secret_key)
                                self.balance = self.ub.get_balances()
                                if self.balance == None:
                                        self.textEdit.append("[FAILED] key is not correct! check it please")
                                        return

                        self.auto_trading_bttn.setText("stop")
                        self.textEdit.append("------- START -------")
                        for i in range(len(self.balance)):
                                self.textEdit.append(f"{self.balance[i]['currency']}: {self.balance[i]['balance']} ")

                        self.vw = AutoWorker(self.ticker, self.ub)
                        self.vw.trading_sent.connect(self.receiveTradingSignal)
                        self.vw.start()
                else:
                        self.textEdit.append("------- END -------")
                        self.vw.close()
                        self.auto_trading_bttn.setText("auto trade")

        def receiveTradingSignal(self, type, crypto, amount, time):
                self.textEdit.append(f"[{type}] {crypto} : {amount} {time}")

        def closeEvent(self, event):
                self.vw.close()
                self.widget.closeEvent(event)
                self.widget_2.closeEvent(event)
                self.widget_3.closeEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_w = MainWindow()
    main_w.show()
    exit(app.exec_())
