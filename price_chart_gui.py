import sys
from PyQt5 import QtWidgets, QtGui, uic, QtCore, QtChart
import pyupbit
import time

class ChartThread(QtCore.QThread):
        data_sent = QtCore.pyqtSignal(float)

        def __init__(self, ticker):
                super().__init__()
                self.ticker = ticker
                self.alive = True

        def run(self):
                while self.alive:
                        data = pyupbit.get_current_price(self.ticker)
                        time.sleep(1)
                        self.data_sent.emit(data)
        def close(self):
                self.alive = False

class ChartWidget(QtWidgets.QWidget):
        def __init__(self, parent=None, ticker="KRW-BTC"):
                super().__init__(parent)
                uic.loadUi("./qt_ui/chart.ui", self)
                self.ticker = ticker

                self.viewLimit = 128

                self.priceData = QtChart.QLineSeries()
                self.priceChart = QtChart.QChart()
                self.priceChart.addSeries(self.priceData)
                self.priceChart.legend().hide()

                x_axis = QtChart.QDateTimeAxis()
                x_axis.setFormat("hh:mm:ss")
                x_axis.setTickCount(4)
                dt = QtCore.QDateTime.currentDateTime()
                x_axis.setRange(dt, dt.addSecs(self.viewLimit))

                y_axis = QtChart.QValueAxis()
                y_axis.setVisible(False)

                self.priceChart.addAxis(x_axis, QtCore.Qt.AlignBottom)
                self.priceChart.addAxis(y_axis, QtCore.Qt.AlignRight)
                self.priceData.attachAxis(x_axis)
                self.priceData.attachAxis(y_axis)
                self.priceChart.layout().setContentsMargins(0, 0, 0, 0)
                

                # add anti-aliasing effect on chart
                self.priceView.setChart(self.priceChart)
                self.priceView.setRenderHints(QtGui.QPainter.Antialiasing)

                self.thread = ChartThread(ticker)
                self.thread.data_sent.connect(self.appendData)
                self.thread.start()

        def appendData(self, cur_price):
                if len(self.priceData) == self.viewLimit:
                        self.priceData.remove(0)

                dt = QtCore.QDateTime.currentDateTime()
                self.priceData.append(dt.toMSecsSinceEpoch(), cur_price)
                self.__AxisUpdate()

        def __AxisUpdate(self):
                pvs = self.priceData.pointsVector()
                dt_start = QtCore.QDateTime.fromMSecsSinceEpoch(int(pvs[0].x()))

                if len(self.priceData) == self.viewLimit:
                        dt_last = QtCore.QDateTime.fromMSecsSinceEpoch(int(pvs[-1].x()))
                else:
                        dt_last = dt_start.addSecs(self.viewLimit)

                ax = self.priceChart.axisX()
                ax.setRange(dt_start, dt_last)

                ay = self.priceChart.axisY()
                y_data = [v.y() for v in pvs]
                ay.setRange(min(y_data), max(y_data))
        
        def closeEvent(self, event):
                self.thread.close()

if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        chart = ChartWidget()
        chart.show()
        exit(app.exec_())