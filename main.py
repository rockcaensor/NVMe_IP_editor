import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import gui
import os

class MainApp(QMainWindow, gui.Ui_NVMe_IP_tool):
    def __init__ (self):
        super().__init__()
        self.setupUi(self)


    def UIRender(self):
        return 0         
   

app = QApplication(sys.argv)
window = MainApp()
window.show()
app.exec_()
    
 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec_())