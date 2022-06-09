import pyqtgraph as pg
from PyQt5.QtGui import QPen, QColor
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
import sys, time
from loaded_file_parsing import get_columns, get_data

#QtWidgets.QComboBox.activated

#QtWidgets.QComboBox.setItemText()

class OfflinePlotter(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi("offline_plotter_bmi.ui", self)

        self.setWindowTitle("BMI Offline Plotter")


        # THREADS CONTAINER
        #https://www.youtube.com/watch?v=k5tIk7w50L4&t=4s
        self.thread={}

        self.comboBox_files.addItem("None")

        # BUTTON CONNECTION
        self.load_file_button.clicked.connect(self.load_file)
        self.plot_button.clicked.connect(self.plot)
        self.clear_graph_button.clicked.connect(self.clear_graph)

        # comboBox_files signal connection
        self.comboBox_files.currentIndexChanged.connect(self.update_comboBox_options)

        # show grid on ptqtgraph graph x,y
        self.graphicsView.showGrid(True,True)

        # self.files will contains file names as keys and lists of str column names as values
        # self.files = {
        #      file_name: [column1,column2,...]}
        self.files = {}
        self.data = None
        self.current_file_name = None


        self.comboBoxes = [
            self.comboBox,
            self.comboBox_2,
            self.comboBox_3,
            self.comboBox_4,
            self.comboBox_5,
            self.comboBox_6,
            self.comboBox_7,
            self.comboBox_8
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
        # getting the file name
        options = QFileDialog.Options()

        try:
            self.current_file_name = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileNames()","Load a file",
                        "csv File (*.csv);;All Files (*)", options=options)[0]
            exit_load_file = False
            if self.current_file_name in self.files.keys():
                msg = QMessageBox()
                msg.setWindowTitle("Action not allowed")
                msg.setText("This file is already loaded")
                msg.exec_()

                exit_load_file = True

        except FileNotFoundError:
            msg = QMessageBox()
            msg.setWindowTitle("::FileNotFoundError::")
            msg.setText("!!!")
            msg.exec_()
            exit_load_file = True

        if not exit_load_file:
            self.update_comboBox_options()

    def clear_graph(self):
        self.graphicsView.clear()

    def plot(self):


        for n in range(len(self.comboBoxes)):
            #print(self.comboBoxes[n].currentText, self.comboBoxes[n].currentIndex())
            if self.checkBoxes[n].checkState():
                column = self.comboBoxes[n].currentText()
                #print(column)
                self.data = get_data(self.current_file_name, column)

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
                self.graphicsView.plot( y, pen=pen)

            else:
                print("checkbox not clicked")

    def delete_all_comboBox_items(self):
        for combo in self.comboBoxes:
            combo.clear()

    def update_comboBox_options(self):
        # delete all comboBox items
        self.delete_all_comboBox_items()


        # adding filename and columns to self.files dict
        #print(self.current_file_name)
        columns = get_columns(self.current_file_name)
        self.files[self.current_file_name] = columns

        # adding the file name to the files combobox
        for n, file_name in enumerate(self.files):
            if n == 0:
                self.comboBox_files.setItemText(n,file_name)
            elif self.comboBox_files.count() == len(self.files):
                pass
            else:
                self.comboBox_files.addItem(file_name)


        # print(self.files)
        # columns_num = len(columns)

        # adding all columns of all loaded files
        # self.files = {
        #      file_name: [column1,column2,...]}

        self.update_selected_file()

        for comboBox in self.comboBoxes:
            comboBox.addItems(self.files[self.current_file_name])


    def update_selected_file(self):
        self.current_file_name = self.comboBox_files.currentText()

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