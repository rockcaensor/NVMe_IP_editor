import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from gui import Ui_NVMe_IP_tool
from OpSysFunctions import PathMaker
from FileFunctions import *
from locations import *
import os
import datetime

class MainApp(QMainWindow, Ui_NVMe_IP_tool):
    def __init__ (self):
        super().__init__() 
        self.NVMe_list_main = []
        self.tabs_number_main = 0
        self.directory = ""
        self.UIRender(self.tabs_number_main)
        self.ListChangeIdx = 0
        self.OpenFolderProcess = 0 

    def UIRender(self, number):
        self.ui = Ui_NVMe_IP_tool()
        self.ui.tabs_number = number    
        self.ui.setupUi(self)
        self.ui.retranslateUi(self)
        self.ui.OpenProjectButton.clicked.connect(self.browse_folder)
        self.ui.ShowSettingsButton.clicked.connect(self.ShowSettings)
        
        for i in range (self.ui.tabs_number):           
            self.ui.BlockLocationComboBox[i].currentTextChanged.connect(self.GTListChange)          
            self.ui.ApplyButton[i].clicked.connect(self.ApplySettings)
            
        self.show()

    def ShowSettings(self):
        TabIndex = self.ui.tabWidget.currentIndex()
        ValuesList = []
        LogText_0 = ""

        for i in range(len(self.NVMe_list_main)):
            ValuesList.append(GetValues(self.NVMe_list_main[i][1]))

        for i in range(len(self.NVMe_list_main)):
            LogText_0 = self.GetCurrentTime() + "  " + self.NVMe_list_main[i][0] + " - PCIe Block Location: " + \
                ValuesList[i][0] + ", GT Selection: " + ValuesList[i][1]
            self.ui.LogWindow.addItem(LogText_0)      
        
        

    def ApplySettings(self):
        TabIndex = self.ui.tabWidget.currentIndex()
        FileName = self.NVMe_list_main[TabIndex][1]
        BlockLocationValue = self.ui.BlockLocationComboBox[TabIndex].currentText()
        QuadValue = self.ui.GTSelectionComboBox[TabIndex].currentText()
        Set_pcie_blk_locn(FileName, BlockLocationValue)  #filename, value
        Set_quad(FileName, QuadValue)
        
        SetText = '  Set block location "' + str(BlockLocationValue) + '" and' \
            +  ' GT Selection "' + str(QuadValue) + '" for ' + str(self.NVMe_list_main[TabIndex][0]) + " core"

        LogText_0 = self.GetCurrentTime() + SetText    #   Text string for console
        self.ui.LogWindow.addItem(LogText_0)   #   Console write



    def GTListChange(self):
        if (self.OpenFolderProcess != 1):
            TabIndex = self.ui.tabWidget.currentIndex()
            self.ui.GTSelectionComboBox[TabIndex].clear()
            self.ui.GTSelectionComboBox[TabIndex].addItems(GTQuad[self.ui.BlockLocationComboBox[TabIndex].currentText()])
        else:
            for i in range(self.ui.tabs_number):
                self.ui.GTSelectionComboBox[i].clear()
                self.ui.GTSelectionComboBox[i].addItems(GTQuad[self.ui.BlockLocationComboBox[i].currentText()])
        


    def browse_folder(self):
        self.ui.ProjectWindow.clear()
        self.directory = ""
        self.directory = QFileDialog.getExistingDirectory(self, "Выберите папку")

        if self.directory:
            try:
                self.NVMe_list_main = PathMaker(self.directory)
            except NotADirectoryError:
                self.ui.LogWindow.addItem(\
                    "ERROR: There are no Vivado project in this folder or output product was not generated")
                exit
            else:    
            
                self.IP_count = len(self.NVMe_list_main)  
                self.ui.tabs_number = self.IP_count

                for i in range (len(self.NVMe_list_main)):               
                    self.ui.NVMe_name.append(self.NVMe_list_main[i][0])
                
                self.UIRender(self.ui.tabs_number)

                ValuesList = []    

                self.OpenFolderProcess = 1
                
                for i in range(len(self.NVMe_list_main)):
                    ValuesList.append(GetValues(self.NVMe_list_main[i][1]))
                    self.ui.BlockLocationComboBox[i].setCurrentText(ValuesList[i][0])
                    
                for i in range(len(self.NVMe_list_main)):
                    self.ui.GTSelectionComboBox[i].setCurrentText(ValuesList[i][1])  
                  
                self.OpenFolderProcess = 0    

                self.ui.ProjectWindow.addItem(self.directory)

                coresText = ""
                if self.IP_count == 1:
                    coresText = " IP core)"
                else:
                    coresText = " IP cores)"     

                LogText_1 = "(Finding " + str(self.IP_count) + coresText
                LogText_0 = self.GetCurrentTime() + "  Open project:  " + self.directory + (" "*8) + LogText_1
                
                self.ui.LogWindow.addItem(LogText_0)
               # self.ui.LogWindow.addItem(LogText_1)

    def GetCurrentTime(self):
        Time = str(datetime.datetime.now())[11:19]
        return Time            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec_())
