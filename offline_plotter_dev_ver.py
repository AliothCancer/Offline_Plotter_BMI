import pyqtgraph
import pyqtgraph as pg
from PyQt5.QtGui import QPen, QColor
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
import sys, time
from loaded_file_parsing import get_columns, get_data
import platform
import os, sys
#QtWidgets.QComboBox.activated

#QtWidgets.QComboBox.setItemText()

class OfflinePlotter(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        if getattr(sys, 'frozen', False):
            ui_file = os.path.join(sys._MEIPASS, "offline_plotter_bmi.ui")
        else:
            ui_file = "offline_plotter_bmi.ui"
        self.ui = uic.loadUi(ui_file, self)

        self.setWindowTitle("BMI Offline Plotter")


        # THREADS CONTAINER
        #https://www.youtube.com/watch?v=k5tIk7w50L4&t=4s
        self.thread={}

        self.comboBox_files.addItem("None")

        # SLIDER CONNECTION
        self.sliders = {
            self.scroll_velocity_slider: self.scroll_velocity_label,
            self.values_quantity_slider: self.values_quantity_label
        }
        for slider in self.sliders:
            slider.valueChanged.connect(self.update_sliders)


        # LABEL
        self.scroll_velocity_label.setText(str(self.scroll_velocity_slider.value()))
        self.values_quantity_label.setText(str(self.values_quantity_slider.value()))
        #QtWidgets.QLabel.setText()

        self.scrolling_slider.valueChanged.connect(self.update_scrolling)
        self.values_quantity_slider.valueChanged.connect(self.update_zoom)


        # BUTTON CONNECTION
        self.load_file_button.clicked.connect(self.load_file)
        self.plot_button.clicked.connect(self.plot)
        self.clear_graph_button.clicked.connect(self.clear_graph)
        self.play_button.clicked.connect(self.play_thread)
        self.pause_button.clicked.connect(self.pause_thread)

        # comboBox_files signal connection
        self.comboBox_files.currentIndexChanged.connect(self.update_comboBox_options)

        # show grid on ptqtgraph graph x,y
        self.graphicsView.showGrid(True,True)

        # self.files will contains file names as keys and lists of str column names as values
        # self.files = {
        #      file_name: [column1,column2,...]}
        # VARIABLES
        self.play_isRunning = False
        self.files = {}
        self.data = []
        self.current_file_name = ""
        self.graphs = []
        self.pens = []
        self.file_and_columns_plotted = {}
        self.pen_width = 3

        #self.x_scroll = []
        self.y = []
        self.init_value = 0

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
    def update_sliders(self):
        for slider in self.sliders:
            new_value = slider.value()
            self.sliders[slider].setText(str(new_value))


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
            self.current_file_name = repr(QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileNames()","Load a file",
                        "csv File (*.csv);;All Files (*)", options=options)[0]).strip("'")

            exit_load_file = False
            if self.current_file_name in self.files.keys():
                msg = QMessageBox()
                msg.setWindowTitle("Action not allowed")
                msg.setText("This file is already loaded")
                msg.exec_()

                exit_load_file = True

        except FileNotFoundError or KeyError:
            msg = QMessageBox()
            msg.setWindowTitle("::FileNotFoundError::")
            msg.setText("!!!")
            msg.exec_()
            exit_load_file = True

        if not exit_load_file:
            self.update_comboBox_options()

    def clear_graph(self):
        self.y = []
        self.graphicsView.clear()
        self.graphs = []
        self.pens = []
        self.init_value = 0
        self.file_and_columns_plotted.clear()
        self.signals_listWidget.clear()

    def plot(self):

        self.current_file_name = self.comboBox_files.currentText()
        print(self.current_file_name)

        if self.current_file_name not in self.file_and_columns_plotted.keys():
            self.file_and_columns_plotted[self.current_file_name] = []


        for n in range(len(self.comboBoxes)):

            if self.checkBoxes[n].checkState() and self.comboBoxes[n].count() != 0:
                self.y = []
                column = self.comboBoxes[n].currentText()
                if column not in self.file_and_columns_plotted[self.current_file_name]:
                    self.file_and_columns_plotted[self.current_file_name].append(column)
                #print(column)
                self.data = get_data(self.current_file_name, column)

                # adjusting sliders size based on data length

                max_length = len(self.data)
                self.scrolling_slider.setMaximum(max_length)
                self.scroll_velocity_slider.setMaximum(int(max_length*0.05))
                self.values_quantity_slider.setMaximum(int(max_length*0.8))
                    #QtWidgets.QSlider.setMaximum()

                for i in self.data:
                    self.y.append(i)
                #print(y)
                color = QColor(
                    self.colors[n][0],
                    self.colors[n][1],
                    self.colors[n][2],
                )
                self.pen_width = self.pen_width_slider.value()
                pen = pg.mkPen(color, width=self.pen_width)
                self.graphs.append(self.graphicsView.plot( self.y, pen=pen))
                self.pens.append(pen)

                self.graphicsView.setAutoVisible(y=1)
                self.graphicsView.setAutoVisible(x=1)
                self.graphicsView.enableAutoRange(axis='y', enable=True)
                self.graphicsView.enableAutoRange(axis='x', enable=True)

                self.signals_listWidget.clear()
                for file_name in self.file_and_columns_plotted:

                    plotted_columns = str(self.file_and_columns_plotted[file_name])

                    match platform.uname()[0]:
                        case "Linux" | "Darwin":
                            item = file_name.split("/")[-1] + ": " + plotted_columns
                        case "Windows":
                            item = file_name.split("\\")[-1] + ": " + plotted_columns

                    if file_name == self.comboBox_files.currentText():
                        self.signals_listWidget.addItem(item)

                    else:
                        self.signals_listWidget.addItem(item)

            else:
                try:
                    self.file_and_columns_plotted[self.current_file_name].remove(self.comboBoxes[n].currentText())
                except ValueError:
                    pass
                print("checkbox not clicked")

    def delete_all_comboBoxes_items(self):
        for combo in self.comboBoxes:
            combo.clear()

    def update_comboBox_options(self):
        # delete all comboBox items
        self.delete_all_comboBoxes_items()


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



        # adding all columns of loaded files
        # self.files = {
        #      file_name: [column1,column2,...]}
        self.update_selected_file()
        for n, comboBox in enumerate(self.comboBoxes):
            for k, item in enumerate(self.files[self.current_file_name]):
                if k == n:
                    comboBox.addItem(item)



        for comboBox in self.comboBoxes:
            for item in self.files[self.current_file_name]:
                if comboBox.currentText() != item:
                    comboBox.addItem(item)

    def update_selected_file(self):
        self.current_file_name = repr(self.comboBox_files.currentText()).strip("'")

    # AUTOMATIC GRAPH SCROLLER
    # THREAD FUNCTIONS
    def play_thread(self):
        self.play_isRunning = True
        self.thread[1] = ThreadClass(parent=None,index=1)
        self.thread[1].start()
        self.thread[1].any_signal.connect(self.my_function)
        self.play_button.setEnabled(False)


    def update_scrolling(self):
        #self.pause_thread()
        if self.play_isRunning:
            self.init_value = self.scrolling_slider.value() - self.values_quantity_slider.value()
        else:
            self.init_value = self.scrolling_slider.value() - self.values_quantity_slider.value()
            intervall_lenght = int(self.values_quantity_label.text())
            # QtWidgets.QLabel.text()

            end_value = self.init_value + intervall_lenght
            print(self.init_value)
            self.graphicsView.setXRange(self.init_value, end_value)
            self.scrolling_slider.setValue(int(self.init_value + self.values_quantity_slider.value()))
            self.pen_width = self.pen_width_slider.value()

            for n, graph in enumerate(self.graphs):
                self.graphicsView.plot(graph.yData, pen=self.pens[n])
        #self.play_thread()

    def update_zoom(self):
        #self.scrolling_slider.setMinimum(self.scrolling_slider.value())


        intervall_lenght = int(self.values_quantity_label.text())
        # QtWidgets.QLabel.text()

        end_value = self.init_value + intervall_lenght


        self.graphicsView.setXRange(self.init_value, end_value)
        self.scrolling_slider.setValue(int(self.init_value + self.values_quantity_slider.value()))
        self.pen_width = self.pen_width_slider.value()

        for n, graph in enumerate(self.graphs):
            self.graphicsView.plot(graph.yData, pen=self.pens[n])

    def play(self):
        self.graphicsView.clear()


        #self.update_xy()
        if self.graphs != []:
            #self.graph.setYRange(min(self.y), max(self.y))
            intervall_lenght = int(self.values_quantity_label.text())
            #QtWidgets.QLabel.text()


            end_value = self.init_value + intervall_lenght

            self.graphicsView.setXRange(self.init_value, end_value)
            self.init_value += int(self.scroll_velocity_label.text())*0.15
            self.scrolling_slider.setValue(int(self.init_value + self.values_quantity_slider.value()))
            self.pen_width = self.pen_width_slider.value()

            for n, graph in enumerate(self.graphs):
                self.graphicsView.plot(graph.yData, pen=self.pens[n])

                #pyqtgraph.PlotDataItem.
            if self.init_value + self.values_quantity_slider.value() >= self.scrolling_slider.maximum():
                self.pause_thread()
                self.init_value = 0




    def pause_thread(self):
        self.play_isRunning = False
        self.thread[1].stop()
        self.play_button.setEnabled(True)
    

# here you can add other thread        
    def my_function(self):
        index = self.sender().index
        if index==1: # play
            self.play()


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