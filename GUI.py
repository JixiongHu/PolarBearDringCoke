import numpy as np
import PyQt5
import os
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QGridLayout, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QPushButton, QApplication, QGridLayout, QGroupBox, QLineEdit
from PyQt5.QtWidgets import QGridLayout, QCheckBox, QTextEdit, QTextBrowser, QComboBox, QTableView, QMessageBox, QStyle
from PyQt5.QtCore import QAbstractTableModel, Qt, QSize
import json
import webbrowser

try:
    with open("Config.json", 'r') as f:
        Config = json.load(f)
except:
    with open("Config_default.json", 'r') as f:
        Config = json.load(f)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Have a good clearing'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 1000
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.Tablayout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.resize(1000, 1000)
        self.tab_GPLE = GPLEAnalysis(self)
        self.tab_SIW = SIW(self)
        self.tabs.addTab(self.tab_GPLE, "GPLE Analysis")
        self.tabs.addTab(self.tab_SIW, "SIW")
        self.Tablayout.addWidget(self.tabs)
        #self.setLayout(self.Tablayout)
        self.table_widget = QWidget()
        self.table_widget.setLayout(self.Tablayout)
        self.setCentralWidget(self.table_widget)
        self.show()


class GPLEAnalysis(QWidget):
    def __init__(self, parent):
        super(GPLEAnalysis, self).__init__(parent)
        self.createGPLEAnalysisTab()
        self.setLayout(self.tab_GPLE.layout)
        self.setDefaultInfo()
        self.Size = self.sizeHint()
        #print(self.sizeHint())
        #self.miniSize=self.sizeHint()

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
        self.createExtraWindowButton = QPushButton()
        self.createExtraWindowButton.setFixedSize(25, 600)
        style = self.style()
        icon = style.standardIcon(style.SP_MediaPlay)
        self.createExtraWindowButton.setIcon(icon)

        self.createExtraWindowButton_clicked = -1
        self.extraWindowCreated = 0
        self.createExtraWindowButton.clicked.connect(self.addRemoveExtraWindow)

        self.RunButton.clicked.connect(self.Run)

        self.tab_GPLE.layout.addWidget(self.RunButton, 0, 0, 1, 1)
        self.tab_GPLE.layout.addWidget(self.MainClearingInfoBox, 0, 1, 1, 5)
        self.tab_GPLE.layout.addWidget(self.MRiskQueryBox, 1, 0, 2, 2)
        self.tab_GPLE.layout.addWidget(self.FilterConditionBox, 1, 2, 2, 3)

        self.tab_GPLE.layout.addWidget(self.DropfileDownloadingBox, 1, 5, 1, 1)
        self.tab_GPLE.layout.addWidget(self.RunComparisonBox, 2, 5, 1, 1)
        self.tab_GPLE.layout.addWidget(self.RunScalpelBox, 3, 0, 1, 2)
        self.tab_GPLE.layout.addWidget(self.RunMedusaBox, 3, 2, 1, 2)
        self.tab_GPLE.layout.addWidget(self.RunGPLEStraBox, 3, 4, 1, 2)
        self.tab_GPLE.layout.addWidget(self.GenerateFinalReportBox, 4, 0, 1, 1)
        self.tab_GPLE.layout.addWidget(
            self.createExtraWindowButton, 0, 6, 5, 6)

        self.RuningInfo = QTextBrowser()
        self.RuningInfo.setObjectName('Running Info')
        self.tab_GPLE.layout.addWidget(self.RuningInfo, 4, 1, 1, 5)

        #self.tab_GPLE.setLayout(self.tab_GPLE.layout)

    def addRemoveExtraWindow(self):
        if self.createExtraWindowButton_clicked == 1:
            self.RunExtraComparisonBox.hide()
            self.resize(self.Size)
        if self.createExtraWindowButton_clicked == -1:
            if self.extraWindowCreated == 1:
                self.RunExtraComparisonBox.show()
            else:
                self.createRunExtraComparison()
                self.tab_GPLE.layout.addWidget(
                    self.RunExtraComparisonBox, 0, 7, 4, 8)
                self.extraWindowCreated = 1
        self.createExtraWindowButton_clicked *= -1

    def createCustomisedFilterConditionBox(self):
        self.columnsCondition = [
            'None', 'TRADE_ID', 'PRODUCT_NAME', 'MODEL_NAME']
        self.FilterConditionBox = QGroupBox("Customized Filter Condition")
        self.Conditions = {}
        self.FilterConditionBox.setCheckable(True)
        self.FilterConditionBox.setChecked(False)
        self.FilterConditionComboBox1 = QComboBox()
        self.FilterConditionComboBox1.setObjectName('FilterCondition')

        self.FilterConditionComboBox1.addItems(self.columnsCondition)
        self.FilterConditionLine1 = QLineEdit()
        self.FilterConditionLine1.setObjectName('FilterValue')
        self.FilterConditionComboBox1.setFixedWidth(150)
        self.FilterConditionLine1.setFixedHeight(20)
        self.AddFilterConditionButton = QPushButton('+')
        self.AddFilterConditionButton.clicked.connect(self.addFilterCondition)
        self.AddFilterConditionButton.setFixedSize(30, 30)
        self.layout_filterCondition = QGridLayout()
        self.layout_filterCondition.addWidget(
            self.FilterConditionComboBox1, 0, 0)
        self.layout_filterCondition.addWidget(self.FilterConditionLine1, 0, 1)
        self.layout_filterCondition.addWidget(
            self.AddFilterConditionButton, 0, 2)
        self.ConditionsCount = 1
        self.FilterConditionBox.setLayout(self.layout_filterCondition)

    def addFilterCondition(self):
        FilterConditionComboBox = QComboBox()
        FilterConditionComboBox.addItems(self.columnsCondition)
        FilterConditionLine = QLineEdit()
        FilterConditionComboBox.setFixedWidth(150)
        FilterConditionLine.setFixedHeight(20)
        FilterConditionLine.setObjectName('FilterValue')
        FilterConditionComboBox.setObjectName('FilterCondition')
        self.layout_filterCondition.addWidget(
            FilterConditionComboBox, self.ConditionsCount, 0)
        self.layout_filterCondition.addWidget(
            FilterConditionLine, self.ConditionsCount, 1)
        self.ConditionsCount += 1

    def createMainClearingInfoBox(self):
        self.MainClearingInfoBox = QGroupBox("Main Infomation")
        pathLabel = QLabel()
        pathLabel.setText('mainPath:')
        self.mainPathLine = QLineEdit()
        self.toolButtonOpenDialog_mainpath = self._create_file_dialog_button(
            self.mainPathLine)

        protoTypeDirLabel = QLabel()
        protoTypeDirLabel.setText('prototype Folder:')
        self.protoTypeDirLine = QLineEdit()
        self.toolButtonOpenDialog_protoType = self._create_file_dialog_button(
            self.protoTypeDirLine)

        startDateLabel = QLabel()
        startDateLabel.setText('startDate: (e.g.2020-12-01)')
        self.startDateLine = QLineEdit()
        self.startDateLine.setFixedWidth(120)
        endDateLabel = QLabel()
        endDateLabel.setText('endDate: (e.g.2020-12-01)')
        self.endDateLine = QLineEdit()
        self.endDateLine.setFixedWidth(120)

        layout = QGridLayout()
        layout.addWidget(pathLabel, 0, 0, 1, 1)
        layout.addWidget(self.mainPathLine, 0, 1, 1, 4)
        layout.addWidget(self.toolButtonOpenDialog_mainpath, 0,
                         4, 1, 3, alignment=QtCore.Qt.AlignRight)
        layout.addWidget(protoTypeDirLabel, 1, 0, 1, 1)
        layout.addWidget(self.protoTypeDirLine, 1, 1, 1, 4)
        layout.addWidget(self.toolButtonOpenDialog_protoType,
                         1, 4, 1, 3, alignment=QtCore.Qt.AlignRight)

        layout.addWidget(startDateLabel, 2, 0)
        layout.addWidget(self.startDateLine, 2, 1)
        layout.addWidget(endDateLabel, 2, 2)
        layout.addWidget(self.endDateLine, 2, 3)

        self.MainClearingInfoBox.setLayout(layout)

    def createMRiskQueryBox(self):
        self.MRiskQueryBox = QGroupBox("MRisk Query")
        self.MRiskQueryBox.setCheckable(True)
        self.MRiskQueryBox.setChecked(True)
        nameLabel = QLabel()
        nameLabel.setText('UserName:')

        self.UserNameLine = QLineEdit()

        passwordLabel = QLabel()
        passwordLabel.setText('PassWord:')
        self.PasswordLine = QLineEdit()

        self.customisedSQL = QGroupBox("customised SQL")
        self.customisedSQL.setCheckable(True)
        self.customisedSQL.setChecked(False)
        self.customisedSQLPathLabel = QLabel()
        self.customisedSQLPathLabel.setText('Path:')
        self.customisedSQLPathLine = QLineEdit()
        self.customisedSQLPathLine.setFixedWidth(170)
        self.toolButtonOpenDialog_sql = self._create_file_dialog_button(
            self.customisedSQLPathLine, ChooseFile=True)
        layout_sql = QGridLayout()
        layout_sql.addWidget(self.customisedSQLPathLabel, 0, 0, 1, 1)
        layout_sql.addWidget(self.customisedSQLPathLine, 0, 1, 1, 3)
        layout_sql.addWidget(self.toolButtonOpenDialog_sql,
                             0, 4, 1, 4, alignment=QtCore.Qt.AlignRight)
        self.customisedSQL.setLayout(layout_sql)
        layout = QGridLayout()
        layout.addWidget(nameLabel, 0, 0, 1, 1)
        layout.addWidget(self.UserNameLine, 0, 1, 1, 2)
        layout.addWidget(passwordLabel, 1, 0, 1, 1)
        layout.addWidget(self.PasswordLine, 1, 1, 1, 2)
        layout.addWidget(self.customisedSQL, 2, 0, 1, 3)
        #layout.addWidget(self.customisedSQL)
        self.MRiskQueryBox.setLayout(layout)

    def createDropfileDownloadingBox(self):
        self.DropfileDownloadingBox = QGroupBox("Dropfile Downloading")
        self.DropfileDownloadingBox.setCheckable(True)
        self.DropfileDownloadingBox.setChecked(True)
        DropfileDownloadingInfoButton = self._create_info_button(
            'Input: TIC.txt file under main path \nOutput: dropfiles w.r.t TIC in "scalpel dropfiles" folder under main path\n')
        DropfileDownloadingInfoButton.setParent(self.DropfileDownloadingBox)
        DropfileDownloadingInfoButton.move(150, 0)

        '''self.Download_layout = QVBoxLayout()
        self.Download_layout.addWidget(
            DropfileDownloadingInfoButton, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.DropfileDownloadingBox.setLayout(self.Download_layout)'''

    def createRunComparisonBox(self):
        self.RunComparisonBox = QGroupBox("Run Comparison")
        self.RunComparisonBox.setCheckable(True)
        self.RunComparisonBox.setChecked(True)
        ComparisonInfoButton = self._create_info_button(
            'Input: prototype folder && dropfiles folder \nOutput: comparison results\n')
        ComparisonInfoButton.setParent(self.RunComparisonBox)
        ComparisonInfoButton.move(150, 0)

        #layout = QVBoxLayout()
        #layout.addWidget(ComparisonInfoButton, alignment=QtCore.Qt.AlignTop)
        #self.RunComparisonBox.setLayout(layout)

    def createRunScalpelBox(self):
        self.RunScalpelBox = QGroupBox("Run Scalpel")
        self.RunScalpelBox.setCheckable(True)
        self.RunScalpelBox.setChecked(True)
        self.Scalpel_InitialAnalysisBox = self.createInitialAnalysisCheckBox()
        self.Scalpel_OneOffSummaryBox = self.createOneOffSummaryCheckBox()
        self.Scalpel_CheckApprovalTypeBox = self.createCheckApprovalTypeCheckBox()
        self.Scalpel_CheckConditionBox = self.createCheckConditionCheckBox()
        self.Scalpel_CheckDefaultControlBox = self.createCheckDefaultControlCheckBox()
        self.Scalpel_GenerateReportBox = self.createGenerateReportCheckBox()

        layout = QGridLayout()
        layout.addWidget(self.Scalpel_InitialAnalysisBox)
        layout.addWidget(self.Scalpel_OneOffSummaryBox)
        layout.addWidget(self.Scalpel_CheckApprovalTypeBox)
        layout.addWidget(self.Scalpel_CheckConditionBox)
        layout.addWidget(self.Scalpel_CheckDefaultControlBox)
        layout.addWidget(self.Scalpel_GenerateReportBox)
        self.RunScalpelBox.setLayout(layout)

    def createRunMedusaBox(self):
        self.RunMedusaBox = QGroupBox("Run Medusa")
        self.RunMedusaBox.setCheckable(True)
        self.RunMedusaBox.setChecked(True)
        self.Medusa_InitialAnalysisBox = self.createInitialAnalysisCheckBox()
        self.Medusa_OneOffSummaryBox = self.createOneOffSummaryCheckBox(
            setCheck=False)
        self.Medusa_CheckApprovalTypeBox = self.createCheckApprovalTypeCheckBox()
        self.Medusa_GenerateReportBox = self.createGenerateReportCheckBox()

        layout = QGridLayout()
        layout.addWidget(self.Medusa_InitialAnalysisBox)
        layout.addWidget(self.Medusa_OneOffSummaryBox)
        layout.addWidget(self.Medusa_CheckApprovalTypeBox)
        layout.addWidget(self.Medusa_GenerateReportBox)
        self.RunMedusaBox.setLayout(layout)

    def createRunGPLEStraBox(self):
        self.RunGPLEStraBox = QGroupBox("Run GPLE Strategy")
        self.RunGPLEStraBox.setCheckable(True)
        self.RunGPLEStraBox.setChecked(True)
        self.GPLEStra_InitialAnalysisBox = self.createInitialAnalysisCheckBox()
        self.GPLEStra_OneOffSummaryBox = self.createOneOffSummaryCheckBox(
            setCheck=False)
        self.GPLEStra_CheckApprovalTypeBox = self.createCheckApprovalTypeCheckBox()
        self.GPLEStra_GenerateReportBox = self.createGenerateReportCheckBox()

        layout = QGridLayout()
        layout.addWidget(self.GPLEStra_InitialAnalysisBox)
        layout.addWidget(self.GPLEStra_OneOffSummaryBox)
        layout.addWidget(self.GPLEStra_CheckApprovalTypeBox)
        layout.addWidget(self.GPLEStra_GenerateReportBox)
        self.RunGPLEStraBox.setLayout(layout)

    def createGenerateFinalReportBox(self):
        self.GenerateFinalReportBox = QGroupBox("Generate Final Report")
        self.GenerateFinalReportBox.setCheckable(True)
        self.GenerateFinalReportBox.setChecked(True)

    def createInitialAnalysisCheckBox(self):
        InitialAnalysisCheckBox = QCheckBox("Initial Analysis")
        InitialAnalysisCheckBox.setChecked(True)
        return InitialAnalysisCheckBox

    def createOneOffSummaryCheckBox(self, setCheck=True):
        OneOffSummaryCheckBox = QCheckBox("OneOff Trade Summary")
        OneOffSummaryCheckBox.setChecked(setCheck)
        return OneOffSummaryCheckBox

    def createCheckApprovalTypeCheckBox(self):
        CheckApprovalTypeBox = QCheckBox("Check Approval Type")
        CheckApprovalTypeBox.setChecked(True)
        return CheckApprovalTypeBox

    def createCheckConditionCheckBox(self):
        CheckConditionBox = QCheckBox("Check Condition")
        CheckConditionBox.setChecked(True)
        return CheckConditionBox

    def createCheckDefaultControlCheckBox(self):
        CheckDefaultControlBox = QCheckBox("Check Default Control")
        CheckDefaultControlBox.setChecked(True)
        return CheckDefaultControlBox

    def createGenerateReportCheckBox(self):
        GenerateReportBox = QCheckBox("Generate report")
        GenerateReportBox.setChecked(True)
        return GenerateReportBox

    def createRunExtraComparison(self):
        self.RunExtraComparisonBox = QGroupBox("Run Extra Comparison")
        self.RunExtraComparisonBox.setCheckable(True)
        self.RunExtraComparisonBox.setChecked(True)

        self.TicLabel = QLabel()
        self.TicLabel.setText('TICS')
        self.TicText = QTextEdit()

        self.PrototypeLabel_1 = QLabel()
        self.PrototypeLabel_1.setText('Prototype Folder: ')
        self.protoTypeDirLine_1 = QLineEdit()
        self.protoTypeDirFileDiaglog = self._create_file_dialog_button(
            self.protoTypeDirLine_1)

        self.prototypeButton = QPushButton('Create Folder')
        self.prototypeButton.clicked.connect(self.createPrototypeFolder)
        self.RunExtraComparisonButton = QPushButton('Run Extra Comparison')
        self.RunExtraComparisonButton.clicked.connect(self.RunExtraComparison)
        self.ReplaceInitialResults = QPushButton("Replace Initial Report")
        self.GenerateClearingReport = QPushButton("Generate Clearing Report")
        layout_Comparison = QGridLayout()
        layout_Comparison.addWidget(self.TicLabel, 0, 0, 1, 2)
        layout_Comparison.addWidget(self.TicText, 1, 0, 1, 2)
        layout_Comparison.addWidget(self.PrototypeLabel_1, 2, 0, 1, 1)
        layout_Comparison.addWidget(self.prototypeButton, 2, 1, 1, 2)
        layout_Comparison.addWidget(self.protoTypeDirLine_1, 3, 0, 1, 2)
        layout_Comparison.addWidget(
            self.protoTypeDirFileDiaglog, 3, 2, 1, 1)
        layout_Comparison.addWidget(self.RunExtraComparisonButton, 4, 0, 1, 2)
        layout_Comparison.addWidget(self.ReplaceInitialResults, 5, 0, 1, 2)
        layout_Comparison.addWidget(self.GenerateClearingReport, 6, 0, 1, 2)

        self.RunExtraComparisonBox.setLayout(layout_Comparison)

    def createPrototypeFolder(self):
        mainPath = self.mainPathLine.text()
        prototypepath = os.path.join(mainPath, 'ExtraComparison', 'prototype')
        self.RuningInfo.append('Create folder:')
        self.RuningInfo.append(prototypepath)
        if os.path.exists(prototypepath):
            self._create_message_box('Path exist')
        else:
            os.makedirs(prototypepath)
        #webbrowser.open(prototypepath)

        self.protoTypeDirLine_1.setText(prototypepath)

    def setDefaultInfo(self):
        self.UserNameLine.setText(Config["UserName"])
        self.PasswordLine.setText(Config["PassWord"])
        self.protoTypeDirLine.setText(Config["PrototypePath"])
        self.mainPathLine.setText(Config["MainPath"])

    def RunExtraComparison(self):
        #read and save TIC
        self.RuningInfo.append('read TIC')
        mainPath = self.mainPathLine.text()
        TicText = self.TicText.toPlainText()
        try:
            with open(os.path.join(mainPath, 'ExtraComparison', 'TIC.txt'), 'w') as f:
                f.write(TicText)
            self.RuningInfo.append(os.path.join(
                mainPath, 'ExtraComparison', 'TIC.txt'))
        except Exception as e:
            self._create_message_box(str(e), 'Error')
            self.RuningInfo.append('save TIC failed')
            return 0

    def Run(self):
        self.RuningInfo.append(
            '....................Start.....................')
        mainPath = self.mainPathLine.text()
        print('set mainPath', mainPath)
        self.RuningInfo.append('set mainPath: ' + mainPath)
        protoTypeDir = self.protoTypeDirLine.text()
        self.RuningInfo.append('set prototype folder: '+protoTypeDir)
        startDate = self.startDateLine.text()
        self.RuningInfo.append('set start date: ' + startDate)
        endDate = self.endDateLine.text()
        self.RuningInfo.append('set end date: ' + endDate)
        if self.MRiskQueryBox.isChecked():
            self.RuningInfo.append('Run Mrisk Query...')
            print('Run Mrisk Query...')
            userName = self.UserNameLine.text()
            passWord = self.PasswordLine.text()
            print('user name', userName, 'password', passWord)
        if self.FilterConditionBox.isChecked():
            _ValidValue = 0
            for i in range(self.layout_filterCondition.count()):
                item = self.layout_filterCondition.itemAt(i).widget()

                if item.objectName() == 'FilterCondition' and item.currentText() != 'None':
                    self.RuningInfo.append(
                        '    Condition: '+item.currentText())
                    _ValidValue = 1
                if item.objectName() == 'FilterValue' and _ValidValue == 1:
                    self.RuningInfo.append('    Value: '+item.text())
                    _ValidValue = 0
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
                RunInitialAnalysis = True
                print('Run Initial Analysis')
            else:
                RunInitialAnalysis = False
            if self.Scalpel_OneOffSummaryBox.isChecked():
                RunOneOffSummary = True
                print('Run Oneoff summary')
            else:
                RunOneOffSummary = False
            if self.Scalpel_CheckApprovalTypeBox.isChecked():
                RunCheckApprovalType = True
                print('Check Approval Type')
            else:
                RunCheckApprovalType = False
            if self.Scalpel_CheckConditionBox.isChecked():
                RunCheckCondition = True
                print('Check Approval Type')
            else:
                RunCheckCondition = False
            if self.Scalpel_CheckDefaultControlBox.isChecked():
                RunCheckDefaultControl = True
                print('Check Default Control')
            else:
                RunCheckDefaultControl = False
            if self.Scalpel_GenerateReportBox.isChecked():
                RunGenerageReport = True
                print('generate report for scalpel')
            else:
                RunGenerageReport = False
        self.RuningInfo.append(
            '....................Finish.....................')

    def _open_file_dialog(self, line, ChooseFile=False):
    
        fileDialog = QtWidgets.QFileDialog
        if ChooseFile == False:
            text0=line.text()
            result = str(fileDialog.getExistingDirectory())
            if result=='': ## didn't choose any folder and doesn't replace the original text
                result=text0
            line.setText('{}'.format(result))
        else:
            result = str(fileDialog.getOpenFileName())
            line.setText(result.split('\'')[1])

        return result

    def _create_file_dialog_button(self, PathLine, ChooseFile=False):
    
        toolButtonOpenDialog = QtWidgets.QToolButton()
        toolButtonOpenDialog.setText('...')
        toolButtonOpenDialog.clicked.connect(
            lambda: self._open_file_dialog(PathLine, ChooseFile))
        toolButtonOpenDialog.setFixedSize(20, 20)
        return toolButtonOpenDialog

    def _create_info_button(self, InfoText):
        InfoButton = QPushButton()
        InfoButton.setFixedSize(28, 20)
        InfoButton.setIcon(self.style().standardIcon(
            self.style().SP_FileDialogInfoView))
        InfoButton.setIconSize(QSize(15, 15))
        #DropfileDownloadingInfo.clicked.connect(lambda: self.RuningInfo.append('Clicked'))
        #self.DropfileDownloadingInfo=QTextBrowser()
        #self.DropfileDownloadingInfo.setText('information')
        InfoButton.clicked.connect(
            lambda: self.RuningInfo.append(InfoText))
        return InfoButton

    def _create_message_box(self, text, title=""):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.exec()


class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class SIW(QWidget):
    def __init__(self, parent):
        super(SIW, self).__init__(parent)
        self.createSIWTab()
        self.setLayout(self.tab_SIW.layout)

    def createSIWTab(self):
        self.tab_SIW = QWidget()
        self.tab_SIW.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("No Run")
        self.TableReview = QTableView()
        df = pd.DataFrame({'a': [1, 2, 3], 'b': [1, 2, 3], 'c': [1, 2, 3]})
        model = pandasModel(df)
        self.TableReview.setModel(model)
        self.pushButton1.clicked.connect(lambda: self.TableReview.show())
        self.tab_SIW.layout.addWidget(self.pushButton1)

        #self.tab_SIW.layout.addWidget(self.TableReview)


class MyStream(QtCore.QObject):

    message = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(MyStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message))


if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = App()

    '''myStream = MyStream()
    myStream.message.connect(ex.table_widget.on_myStream_message)'''
    sys.exit(app.exec_())
