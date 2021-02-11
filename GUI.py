import numpy as np
import PyQt5
from PyQt5 import QtCore,QtGui
import sys
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QGridLayout, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QPushButton, QApplication,QGridLayout,QGroupBox,QLineEdit
from PyQt5.QtWidgets import QGridLayout, QCheckBox, QTextEdit, QTextBrowser,QComboBox
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Have a good clearing'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 800
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table_widget = HAGC(self)
        self.setCentralWidget(self.table_widget)
        self.show()


class HAGC(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.mainLayout=QGridLayout()
        '''self.LogInLayout=QHBoxLayout()
        self.Label=QLabel('userName:')
        self.LogInLayout.addWidget(self.Label)'''
        self.Tablayout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.resize(500, 500)
        self.createGPLEAnalysisTab()
        self.createSIWTab()
        self.tabs.addTab(self.tab_GPLE, "GPLE Analysis")
        self.tabs.addTab(self.tab_SIW, "SIW")
        self.Tablayout.addWidget(self.tabs)
        self.setLayout(self.Tablayout)
        #self.mainLayout.addWidget(self.LogInLayout,0,0,1,2)
        #self.mainLayout.addWidget(self.Tablayout)
        #self.setLayout(self.mainLayout)

    def createGPLEAnalysisTab(self):
        self.tab_GPLE = QWidget()
        self.tab_GPLE.layout = QGridLayout(self)
        self.RunButton = QPushButton("Run")
        self.createCustomisedFilterConditionBox()
        self.createMRiskQueryBox()
        self.createMainClearingInfoBox()
        self.createDropfileDownloadingBox()
        self.createRunComparisonBox()
        self.createRunScalpelBox()
        self.createRunMedusaBox()
        self.createRunGPLEStraBox()
        self.createGenerateFinalReportBox()
        self.RunButton.clicked.connect(self.Run)
    
        self.tab_GPLE.layout.addWidget(self.RunButton,0,0)
        self.tab_GPLE.layout.addWidget(self.FilterConditionBox,0,1,1,3)
        self.tab_GPLE.layout.addWidget(self.MainClearingInfoBox,1,0,1,3)
        self.tab_GPLE.layout.addWidget(self.MRiskQueryBox,2,0)
        self.tab_GPLE.layout.addWidget(self.DropfileDownloadingBox,2,1)
        self.tab_GPLE.layout.addWidget(self.RunComparisonBox,2,2)
        self.tab_GPLE.layout.addWidget(self.RunScalpelBox,3,0)
        self.tab_GPLE.layout.addWidget(self.RunMedusaBox,3,1)
        self.tab_GPLE.layout.addWidget(self.RunGPLEStraBox,3,2)
        self.tab_GPLE.layout.addWidget(self.GenerateFinalReportBox,4,0)
        
        self.RuningInfo = QTextBrowser()
        self.RuningInfo.setObjectName('Runing Info')
        self.tab_GPLE.layout.addWidget(self.RuningInfo,4,1)
        self.tab_GPLE.setLayout(self.tab_GPLE.layout)
    def createCustomisedFilterConditionBox(self):
        columns=['None','TRADE_ID','2','3']
        self.FilterConditionBox=QGroupBox("Customized Filter Condition")
        self.FilterConditionBox.setCheckable(True)
        self.FilterConditionBox.setChecked(False)
        self.FilterConditionComboBox1=QComboBox()
        self.FilterConditionComboBox1.addItems(columns)
        self.FilterConditionLine1=QTextEdit()
        self.FilterConditionComboBox2=QComboBox()
        self.FilterConditionComboBox2.addItems(columns)
        self.FilterConditionLine2=QTextEdit()
        self.FilterConditionComboBox1.setFixedWidth(150)
        self.FilterConditionComboBox2.setFixedWidth(150)
        self.FilterConditionLine1.setFixedHeight(20)
        self.FilterConditionLine2.setFixedHeight(20)
        layout=QGridLayout()
        layout.addWidget(self.FilterConditionComboBox1,0,0)
        layout.addWidget(self.FilterConditionLine1,0,1)
        layout.addWidget(self.FilterConditionComboBox2,1,0)
        layout.addWidget(self.FilterConditionLine2,1,1)
    
        self.FilterConditionBox.setLayout(layout)
    def createMainClearingInfoBox(self):
        self.MainClearingInfoBox=QGroupBox("Main Infomation")
        pathLabel=QLabel()
        pathLabel.setText('mainPath:')
        self.mainPathLine=QLineEdit()
        #pathLabel.setBuddy(mainPathLine)
        protoTypeDirLabel=QLabel()
        protoTypeDirLabel.setText('prototype Folder')
        self.protoTypeDirLine=QLineEdit()
        self.protoTypeDirLine.setText('C:/good morning')
        

        startDateLabel=QLabel()
        startDateLabel.setText('startDate: (format:2020-12-01)')
        self.startDateLine=QLineEdit()
        endDateLabel=QLabel()
        endDateLabel.setText('endDate: (format:2020-12-01)')
        self.endDateLine=QLineEdit()
        layout=QGridLayout()
    
        layout.addWidget(pathLabel,0,0)
        layout.addWidget(self.mainPathLine,0,1)
        layout.addWidget(protoTypeDirLabel)
        layout.addWidget(self.protoTypeDirLine)
        layout.addWidget(startDateLabel)
        layout.addWidget(self.startDateLine)
        layout.addWidget(endDateLabel)
        layout.addWidget(self.endDateLine)

        self.MainClearingInfoBox.setLayout(layout)
    def createMRiskQueryBox(self):
        self.MRiskQueryBox=QGroupBox("MRisk Query")
        self.MRiskQueryBox.setCheckable(True)
        self.MRiskQueryBox.setChecked(True)
        nameLabel = QLabel()
        nameLabel.setText('UserName:')
        #nameLabel.move(20,20)
        self.UserNameLine=QLineEdit()
        passwordLabel = QLabel()
        passwordLabel.setText('PassWord:')
        #nameLabel.move(20,20)
        self.PasswordLine=QLineEdit()


        layout=QGridLayout()
        layout.addWidget(nameLabel)
        layout.addWidget(self.UserNameLine)
        layout.addWidget(passwordLabel)
        layout.addWidget(self.PasswordLine)
        self.MRiskQueryBox.setLayout(layout)
    def createDropfileDownloadingBox(self):
        self.DropfileDownloadingBox=QGroupBox("Dropfile Downloading")
        self.DropfileDownloadingBox.setCheckable(True)
        self.DropfileDownloadingBox.setChecked(True)
    def createRunComparisonBox(self):
        self.RunComparisonBox=QGroupBox("Run Comparison")
        self.RunComparisonBox.setCheckable(True)
        self.RunComparisonBox.setChecked(True)
    def createRunScalpelBox(self):
        self.RunScalpelBox=QGroupBox("Run Scalpel")
        self.RunScalpelBox.setCheckable(True)
        self.RunScalpelBox.setChecked(True)
        self.Scalpel_InitialAnalysisBox=self.createInitialAnalysisCheckBox()
        self.Scalpel_OneOffSummaryBox=self.createOneOffSummaryCheckBox()
        self.Scalpel_CheckApprovalTypeBox=self.createCheckApprovalTypeCheckBox()
        self.Scalpel_CheckConditionBox=self.createCheckConditionCheckBox()
        self.Scalpel_CheckDefaultControlBox=self.createCheckDefaultControlCheckBox()
        self.Scalpel_GenerateReportBox=self.createGenerateReportCheckBox()

        layout=QGridLayout()
        layout.addWidget(self.Scalpel_InitialAnalysisBox)
        layout.addWidget(self.Scalpel_OneOffSummaryBox)
        layout.addWidget(self.Scalpel_CheckApprovalTypeBox)
        layout.addWidget(self.Scalpel_CheckConditionBox)
        layout.addWidget(self.Scalpel_CheckDefaultControlBox)
        layout.addWidget(self.Scalpel_GenerateReportBox)
        self.RunScalpelBox.setLayout(layout)
    def createRunMedusaBox(self):
        self.RunMedusaBox=QGroupBox("Run Medusa")
        self.RunMedusaBox.setCheckable(True)
        self.RunMedusaBox.setChecked(True)
        self.Medusa_InitialAnalysisBox=self.createInitialAnalysisCheckBox()
        self.Medusa_OneOffSummaryBox=self.createOneOffSummaryCheckBox(setCheck=False)
        self.Medusa_CheckApprovalTypeBox=self.createCheckApprovalTypeCheckBox()
        self.Medusa_GenerateReportBox=self.createGenerateReportCheckBox()

        layout=QGridLayout()
        layout.addWidget(self.Medusa_InitialAnalysisBox)
        layout.addWidget(self.Medusa_OneOffSummaryBox)
        layout.addWidget(self.Medusa_CheckApprovalTypeBox)
        layout.addWidget(self.Medusa_GenerateReportBox)
        self.RunMedusaBox.setLayout(layout)   
    def createRunGPLEStraBox(self):
        self.RunGPLEStraBox=QGroupBox("Run GPLE Strategy")
        self.RunGPLEStraBox.setCheckable(True)
        self.RunGPLEStraBox.setChecked(True)
        self.GPLEStra_InitialAnalysisBox=self.createInitialAnalysisCheckBox()
        self.GPLEStra_OneOffSummaryBox=self.createOneOffSummaryCheckBox(setCheck=False)
        self.GPLEStra_CheckApprovalTypeBox=self.createCheckApprovalTypeCheckBox()
        self.GPLEStra_GenerateReportBox=self.createGenerateReportCheckBox()

        layout=QGridLayout()
        layout.addWidget(self.GPLEStra_InitialAnalysisBox)
        layout.addWidget(self.GPLEStra_OneOffSummaryBox)
        layout.addWidget(self.GPLEStra_CheckApprovalTypeBox)
        layout.addWidget(self.GPLEStra_GenerateReportBox)
        self.RunGPLEStraBox.setLayout(layout)  
    def createGenerateFinalReportBox(self):
        self.GenerateFinalReportBox=QGroupBox("Generate Final Report")
        self.GenerateFinalReportBox.setCheckable(True)
        self.GenerateFinalReportBox.setChecked(True)
    def createInitialAnalysisCheckBox(self):
        InitialAnalysisCheckBox=QCheckBox("Initial Analysis")     
        InitialAnalysisCheckBox.setChecked(True)
        return InitialAnalysisCheckBox
    def createOneOffSummaryCheckBox(self,setCheck=True):
        OneOffSummaryCheckBox=QCheckBox("OneOff Trade Summary")     
        OneOffSummaryCheckBox.setChecked(setCheck)
        return OneOffSummaryCheckBox
    def createCheckApprovalTypeCheckBox(self):
        CheckApprovalTypeBox=QCheckBox("Check Approval Type")     
        CheckApprovalTypeBox.setChecked(True)
        return CheckApprovalTypeBox
    def createCheckConditionCheckBox(self):
        CheckConditionBox=QCheckBox("Check Condition")     
        CheckConditionBox.setChecked(True)
        return CheckConditionBox
    def createCheckDefaultControlCheckBox(self):
        CheckDefaultControlBox=QCheckBox("Check Default Control")     
        CheckDefaultControlBox.setChecked(True)
        return CheckDefaultControlBox
    def createGenerateReportCheckBox(self):
        GenerateReportBox=QCheckBox("Generate report")     
        GenerateReportBox.setChecked(True)
        return GenerateReportBox
    def Run(self):
        self.RuningInfo.append('....................Start.....................')
        mainPath=self.mainPathLine.text()
        print('set mainPath',mainPath) 
        protoTypeDir=self.protoTypeDirLine.text()
        print('set prototype folder',protoTypeDir)
        startDate=self.startDateLine.text()
        print('set start date',startDate)
        endDate=self.endDateLine.text()
        print('set end date',endDate)
        if self.MRiskQueryBox.isChecked():
            self.RuningInfo.append('Run Mrisk Query...')
            print('Run Mrisk Query...')
            userName=self.UserNameLine.text()
            passWord=self.PasswordLine.text()
            print('user name', userName, 'password',passWord)
        if self.DropfileDownloadingBox.isChecked():
            self.RuningInfo.append('Run Dropfile Downloading...')
            print('Run Dropfile Downlaoding...')
        if self.RunComparisonBox.isChecked():
            print('Run Comparison...')
            self.RuningInfo.append('Run Comparison...')
        if self.RunScalpelBox.isChecked():
            print('Run Scalpel...')
            self.RuningInfo.append('Run Scalpel...')
            if self.Scalpel_InitialAnalysisBox.isChecked():
                RunInitialAnalysis=True
                print('Run Initial Analysis')
            else:
                RunInitialAnalysis=False
            if self.Scalpel_OneOffSummaryBox.isChecked():
                RunOneOffSummary=True
                print('Run Oneoff summary')
            else:
                RunOneOffSummary=False
            if self.Scalpel_CheckApprovalTypeBox.isChecked():
                RunCheckApprovalType=True
                print('Check Approval Type')
            else:
                RunCheckApprovalType=False
            if self.Scalpel_CheckConditionBox.isChecked():
                RunCheckCondition=True
                print('Check Approval Type')
            else:
                RunCheckCondition=False
            if self.Scalpel_CheckDefaultControlBox.isChecked():
                RunCheckDefaultControl=True
                print('Check Default Control')
            else:
                RunCheckDefaultControl=False
            if self.Scalpel_GenerateReportBox.isChecked():
                RunGenerageReport=True
                print('generate report for scalpel')
            else:
                RunGenerageReport=False
        self.RuningInfo.append('....................Finish.....................')
    def createSIWTab(self):
        self.tab_SIW = QWidget()
        self.tab_SIW.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("No Run")
        self.tab_SIW.layout.addWidget(self.pushButton1)
        self.tab_SIW.setLayout(self.tab_SIW.layout)
class MyStream(QtCore.QObject):
    message = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(MyStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message))

if __name__ == '__main__':
    app = QApplication (sys.argv)
    ex = App()
    '''myStream = MyStream()
    myStream.message.connect(ex.table_widget.on_myStream_message)'''
    sys.exit(app.exec_())

 
