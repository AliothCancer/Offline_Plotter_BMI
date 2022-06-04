

from PyQt5 import QtCore, QtWidgets, QtGui
from pyqtgraph import PlotWidget
from PyQt5 import uic
import sys, time, math
 
class OfflinePlotter(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi("offline_plotter.ui",self)
 
        # THREADS CONTAINER
        self.thread={}


        # GRAPH DATA AND PARAMS
        self.resolution = 100
        interval = 100
        #self.x = [i/self.resolution for i in range(1,int(interval*self.resolution))]
        self.x = [i for i in range(1,interval)]

        self.y = [math.sin(i) for i in self.x]
        self.offset_step = 10

        # PLOTTING COMMAND
        self.graphicsView.plot(self.x,self.y)

        # threaded function button
        self.play_button.clicked.connect(self.play_thread)
        self.pause_button.clicked.connect(self.pause_thread)


        # normal function button
        self.forward_button.clicked.connect(self.draw_next)
        self.back_button.clicked.connect(self.draw_previous)
    


    # NORMAL FUNCTIONS
    def draw_next(self):

        print(f"x:{self.x}\ny:{self.y}")
        self.graphicsView.clear()
        self.update_xy()
        self.graphicsView.plot(self.x,self.y)

        

    def draw_previous(self):

        print(f"x:{self.x}\ny:{self.y}")
        self.graphicsView.clear()
        self.downdate_xy()
        self.graphicsView.plot(self.x,self.y)
        
    def update_xy(self):

        self.xy_counter=self.x[-1]

        # append new x and y element adjusted by self.offset_step
        self.x.append(int(self.xy_counter + self.offset_step / self.resolution))
        self.y.append(math.sin(self.x[-1]))
        self.xy_counter+= 1

        # add self.offset_step to all values in the self.x list
        self.x = [i+self.offset_step for i in self.x.copy()]

        # update self.y
        self.y = [math.sin(i) for i in self.x]

        # pop first element of x and y
        self.x.pop(0)       
        self.y.pop(0) 


    def downdate_xy(self):

        self.xy_rev_counter=self.x[0]

        # append first x and y element adjusted by self.offset_step
        self.x.insert(0,self.xy_rev_counter-self.offset_step/self.resolution)
        self.y.insert(0,math.sin(self.x[0]))

        # decide how much every new element should increase
        self.xy_rev_counter-= 1

        # update all values in the self.x list
        self.x = [i-self.offset_step for i in self.x.copy()]

         # update self.y
        self.y = [math.sin(i) for i in self.x]

        # pop latest element of x and y
        self.x.pop(-1)       
        self.y.pop(-1) 


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