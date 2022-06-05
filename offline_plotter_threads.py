import pyqtgraph as pg
from PyQt5.QtGui import QPen, QColor
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import sys, time
from loaded_file_parsing import get_columns, get_data


#QtWidgets.QComboBox.setItemText()

class OfflinePlotter(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi("offline_plotter_bmi.ui", self)

        self.setWindowTitle("BMI Offline Plotter")


        # THREADS CONTAINER
        #https://www.youtube.com/watch?v=k5tIk7w50L4&t=4s
        self.thread={}

        # BUTTON CONNECTION
        self.load_file_button.clicked.connect(self.load_file)
        self.plot_button.clicked.connect(self.plot)

        self.graphicsView.showGrid(True,True)

        self.comboBoxes = [
            self.comboBox,
            self.comboBox_2,
            self.comboBox_3,
            self.comboBox_4,
            self.comboBox_5,
            self.comboBox_6,
            self.comboBox_7,
            self.comboBox_8,
        ]

        self.checkBoxes = [
            self.checkBox,
            self.checkBox_2,
            self.checkBox_3,
            self.checkBox_4,
            self.checkBox_5,
            self.checkBox_6,
            self.checkBox_7,
            self.checkBox_8
        ]

        self.checkBox_9.stateChanged.connect(lambda: self.show_all_signals(self.checkBox_9))

        self.colors = [
            (224, 27, 36),  # signal1
            (26, 95, 180),
            (38, 162, 105),
            (246, 211, 45),
            (255, 120, 0),
            (145, 65, 172),
            (14, 255, 0),
            (71, 195, 167)  # signal8
        ]


    # NORMAL FUNCTIONS
    def show_all_signals(self, QCheckBox):
        for i in self.checkBoxes:
            if i.isChecked() == False:
                i.setChecked(True)
            else:
                i.setChecked(False)

    def load_file(self):
        print(type(self))
        options = QFileDialog.Options()
        self.file_name = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileNames()","Load a file",
                    "csv File (*.csv);;All Files (*)", options=options)[0]

        self.loaded_file_name.setText(self.file_name)

        columns = get_columns(self.file_name)

        columns_num = len(columns)
        for n in range(columns_num):
            for i in range(columns_num):
                self.comboBoxes[n].addItem(columns[i])

            self.comboBoxes[n].itemText(n)

        self.data_2 = get_data(self.file_name, columns[1])


    def plot(self):
        self.graphicsView.clear()

        for n in range(len(self.comboBoxes)):
            print(self.comboBoxes[n].currentText, self.comboBoxes[n].currentIndex())
            if self.checkBoxes[n].checkState():
                signal = self.comboBoxes[n].currentText()
                print(signal)
                self.data = get_data(self.file_name, signal)

                y = []

                for i in self.data:
                    y.append(i)
                #print(y)
                color = QColor(
                    self.colors[n][0],
                    self.colors[n][1],
                    self.colors[n][2],
                )
                pen = pg.mkPen(color, width=1)
                self.graphicsView.plot(y, pen=pen)
            else:
                print("checkbox not clicked")

    # THREAD FUNCTIONS
    def play_thread(self):
        self.thread[1] = ThreadClass(parent=None,index=1)
        self.thread[1].start()
        self.thread[1].any_signal.connect(self.my_function)
        self.play_button.setEnabled(False)
	
	
    def pause_thread(self):
        self.thread[1].stop()
        self.play_button.setEnabled(True)
    

# here you can add other thread        
    def my_function(self):
        index = self.sender().index
        if index==1: # play
            self.graphicsView.clear()
            self.update_xy()
            self.graphicsView.plot(self.x,self.y)
        
    
    

        

class ThreadClass(QtCore.QThread):

    any_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, index=0):

        super(ThreadClass, self).__init__(parent)
        self.index=index
        self.is_running = True

    def run(self):
        print('Starting thread...',self.index)
        cnt = 0
        while True:
            cnt += 1
            if cnt == 99:
                cnt = 0
            time.sleep(0.1)
            self.any_signal.emit(cnt)
    def stop(self):
        self.is_running = False
        print('Stopping thread...', self.index)
        self.terminate()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = OfflinePlotter()
    MainWindow.show()
    sys.exit(app.exec_())