# Installation from release
Download the archive in the release section for your OS, available platforms:
- Linux_x86_64
- Windows amd64

Once you downloaded the archive, extract it and launch main.exe on windows or the binary main on linux.

Note: The images in the archive must be in the same folder to make the program load the pause and play button image.


# Preview
![alt text](https://github.com/AliothCancer/Offline_Plotter_BMI/blob/main/preview/offline_plotter_1)
![alt text](https://github.com/AliothCancer/Offline_Plotter_BMI/blob/main/preview/offline_plotter_2)



# Generic Installation

Go to the folder you want to install the program, open a terminal within that folder and copy paste this:
      
      git clone https://github.com/AliothCancer/Offline_Plotter_BMI.git
      cd Offline_Plotter_BMI
      pip install -r requirements.txt
      python application/main.py
N.B Use python3 instead of python if python is not recognized as a command, the same for pip, use pip3 if that's the case

--------------- --------

# Package         Version

--------------- --------
- numpy           1.22.4
- pandas          1.4.2
- pip             22.1.2
- PyQt5           5.15.6
- PyQt5-Qt5       5.15.2
- PyQt5-sip       12.10.1
- PyQt5-stubs     5.15.6.0
- pyqtgraph       0.12.4
- python-dateutil 2.8.2
- pytz            2022.1
- setuptools      60.2.0
- six             1.16.0
- wheel           0.37.1
