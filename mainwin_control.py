#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QFileDialog, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
from enum import Enum
import mainwin


class CmdList(Enum):
    ADD = 'add'
    DELETE = 'delete'
    FIND = 'find'
    REPLACE = 'replace'
    DELETE_SPACE = 'deleteSpace'

class ObjectType(Enum):
    FILE_NAME = 'fileName'
    TEXT_CONTENT = 'textContent'

class FileFormat(Enum):
    ALL = 'all'
    C = '.c'
    H = '.h'
    TXT = '.txt'


class MainWinControl(QMainWindow, mainwin.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWinControl, self).__init__(parent)
        self.setupUi(self)
        self.initUi()
        self.screenCenter()
        self.fileThread = FileOperation()
        self.fileThread.finished.connect(self.fileThreadFinish)
        self.fileThread.outputInfo.connect(self.printExecInformation)

    def initUi(self):
        self.setWindowTitle('Code Modify')
        # self.setWindowIcon(QIcon('icons/logo.jpg'))
        self.textEditFindText.setFocus()
        self.lineEditDestPath.setText(os.getcwd())
        self.textEditModifyText.setAcceptRichText(False)
        self.textEditFindText.setAcceptRichText(False)

        self.pushButtonChoosePath.clicked.connect(self.chooseFilePath)
        self.pushButtonChoosePath.setToolTip('Choose a folder or file directory')
        self.pushButtonDeleteWhitespace.clicked.connect(self.deleteWhitespace)
        # (lambda :self.btnAddString(self.pushButtonDelete))
        self.pushButtonAdd.clicked.connect(self.btnAddString)
        self.pushButtonDelete.clicked.connect(self.btnDeleteString)
        self.pushButtonFind.clicked.connect(self.BtnFindString)
        self.pushButtonReplace.clicked.connect(self.BtnReplaceString)

        self.checkBoxMatchCase.setChecked(True)
        self.checkBoxRecursivelyScan.setChecked(True)
        self.checkBoxCFormat.setChecked(True)
        self.checkBoxHFormat.setChecked(True)

        self.radioButtonCustomFormat.toggled.connect(self.fileFormatControl)
        self.radioButtonCustomFormat.setChecked(True)
        self.radioButtonTextContent.toggled.connect(self.funcValidControl)
        self.radioButtonTextContent.setChecked(True)


    def enableAllButton(self):
        self.pushButtonAdd.setEnabled(True)
        self.pushButtonDelete.setEnabled(True)
        self.pushButtonDeleteWhitespace.setEnabled(True)
        self.pushButtonFind.setEnabled(True)
        self.pushButtonReplace.setEnabled(True)

    def disableAllButton(self):
        self.pushButtonAdd.setEnabled(False)
        self.pushButtonDelete.setEnabled(False)
        self.pushButtonDeleteWhitespace.setEnabled(False)
        self.pushButtonFind.setEnabled(False)
        self.pushButtonReplace.setEnabled(False)

    def screenCenter(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)

    def printExecInformation(self, string):
        self.textBrowser.append(string)

    def fileThreadFinish(self, str):
        self.printExecInformation(str + ' function is completed!')
        self.enableAllButton()

    def fileThreadStart(self, cmd):
        folderPath = self.lineEditDestPath.text()
        if folderPath == '':
            QMessageBox.warning(self, 'warning', "Please select a valid destination path!")
            return
        if self.checkBoxRecursivelyScan.isChecked():
            recursive = True
        else:
            recursive = False
        if self.checkBoxMatchCase.isChecked():
            matchCase = True
        else:
            matchCase = False
        # Check object type
        if self.radioButtonFileName.isChecked():
            objectType = ObjectType.FILE_NAME
        elif self.radioButtonTextContent.isChecked():
            objectType = ObjectType.TEXT_CONTENT
        # Check file format
        fileFormat = []
        if self.radioButtonAllFormat.isChecked():
            fileFormat.append(FileFormat.ALL)
        else:
            if self.checkBoxCFormat.isChecked():
                fileFormat.append(FileFormat.C)
            if self.checkBoxHFormat.isChecked():
                fileFormat.append(FileFormat.H)
            if self.checkBoxTxtFormat.isChecked():
                fileFormat.append(FileFormat.TXT)
        self.fileThread.setBasePara(folderPath, recursive, matchCase, objectType, fileFormat)

        tempStr = self.textEditFindText.toPlainText()
        if tempStr == '' and cmd != CmdList.DELETE_SPACE:
            QMessageBox.warning(self, 'warning', 'Please enter a valid string into the find textbox!')
            return
        findStr = tempStr.splitlines(True)
        # if findStr[-1][-1] == '\n':
        #     findStr.append('')

        tempStr = self.textEditModifyText.toPlainText()
        if tempStr == '' and (cmd == CmdList.ADD or cmd == CmdList.REPLACE):
            QMessageBox.warning(self, 'warning', 'Please enter a valid string into the modify textbox!')
            return
        modifyStr = tempStr.splitlines(True)
        # if modifyStr[-1][-1] == '\n':
        #     modifyStr.append('')

        self.fileThread.setOperaPara(cmd, findStr, modifyStr)
        self.textBrowser.setText('')
        self.printExecInformation('Start running program.')
        if not self.fileThread.isRunning():
            self.fileThread.start()
        self.fileThread.startThread()
        self.disableAllButton()

    def chooseFilePath(self):
        objectDirecoty = QFileDialog.getExistingDirectory(self, 'choose file or folder', '.')
        self.lineEditDestPath.setText(objectDirecoty)

    def deleteWhitespace(self):
        self.fileThreadStart(CmdList.DELETE_SPACE)

    def btnAddString(self):
        self.fileThreadStart(CmdList.ADD)

    def btnDeleteString(self):
        self.fileThreadStart(CmdList.DELETE)

    def BtnFindString(self):
        self.fileThreadStart(CmdList.FIND)

    def BtnReplaceString(self):
        self.fileThreadStart(CmdList.REPLACE)

    def funcValidControl(self):
        if self.radioButtonTextContent.isChecked():
            self.pushButtonAdd.setEnabled(True)
            self.pushButtonDelete.setEnabled(True)
            self.pushButtonDeleteWhitespace.setEnabled(True)
        else:
            self.pushButtonAdd.setEnabled(False)
            self.pushButtonDelete.setEnabled(False)
            self.pushButtonDeleteWhitespace.setEnabled(False)

    def fileFormatControl(self):
        if self.radioButtonCustomFormat.isChecked():
            self.checkBoxCFormat.setEnabled(True)
            self.checkBoxHFormat.setEnabled(True)
            self.checkBoxTxtFormat.setEnabled(True)
        else:
            self.checkBoxCFormat.setEnabled(False)
            self.checkBoxHFormat.setEnabled(False)
            self.checkBoxTxtFormat.setEnabled(False)


class FileOperation(QThread):
    finished = pyqtSignal(str)
    outputInfo = pyqtSignal(str)

    def __init__(self, parent=None):
        super(FileOperation, self).__init__(parent)
        self.running = True
        self.execute = False

    def __del__(self):
        self.running = False
        self.wait()

    def setBasePara(self, path, recursively, matchase, objecttype, fileformat):
        self.path = path
        self.recursively = recursively
        self.matchcase = matchase
        self.objecttype = objecttype
        self.fileformat = fileformat

    def setOperaPara(self, cmd, findstr=None, modifystr=None):
        self.cmd = cmd
        if findstr == None:
            findstr = []
        self.findstr = findstr
        if modifystr == None:
            modifystr = []
        self.modifystr = modifystr

    def startThread(self):
        self.execute = True

    def run(self):
        while self.running:
            if self.execute:
                if self.cmd == CmdList.ADD:
                    self.addFileString()
                elif self.cmd == CmdList.DELETE:
                    self.deleteFileString()
                elif self.cmd == CmdList.FIND:
                    if self.objecttype == ObjectType.FILE_NAME:
                        self.findFileName()
                    elif self.objecttype == ObjectType.TEXT_CONTENT:
                        self.findFileString()
                elif self.cmd == CmdList.REPLACE:
                    if self.objecttype == ObjectType.FILE_NAME:
                        self.replaceFileName()
                    elif self.objecttype == ObjectType.TEXT_CONTENT:
                        self.replaceFileString()
                elif self.cmd == CmdList.DELETE_SPACE:
                    self.deleteFileSpaceAndTabs()
                # Transmit signal
                self.finished.emit(self.cmd.value)
                self.execute = False
            else:
                self.wait(5)

    def printInformation(self, string):
        self.outputInfo.emit(string)

    def getFileList(self, path=None):
        if path == None:
            path = self.path
        fileList = []
        # os.walk(), return a triple
        for root, dirs, files in os.walk(path):
            for fileObj in files:
                # Determine the file suffix
                if self.fileformat[0] == FileFormat.ALL:
                    fileList.append(os.path.join(root, fileObj))
                else:
                    extension = os.path.splitext(fileObj)[-1]
                    extension = extension.lower()
                    for fileSuf in self.fileformat:
                        if extension == fileSuf.value:
                            fileList.append(os.path.join(root, fileObj))
            if not self.recursively:
                break
        return fileList

    def compareString(self, referStr, cmpStr):
        referLen = len(referStr)
        cmpLen = len(cmpStr)
        if referLen > cmpLen:
            return False

        cmpCount = 0
        cmpFlag = True
        while cmpCount < referLen:
            if self.matchcase:
                if referStr[cmpCount] != cmpStr[cmpCount]:
                    cmpFlag = False
            else:
                if referStr[cmpCount].upper() != cmpStr[cmpCount].upper():
                    cmpFlag = False
            if not cmpFlag:
                break
            cmpCount += 1
        return cmpFlag

    def findDataValid(self, dataStr, findStr):
        if self.matchcase:
            return dataStr.find(findStr)
        else:
            return dataStr.upper().find(findStr.upper())

    def findString(self, filePath, findString):
        try:
            file = open(filePath, 'r', encoding='iso-8859-1')
            allLines = file.readlines()
            strLen = len(allLines)
            # multi-line
            if len(findString) > 1:
                lineNum = 0
                while lineNum < strLen:
                    if self.compareString(findString, allLines[lineNum:]):
                        if allLines[lineNum][-1] == '\n':
                            printLine = allLines[lineNum][:-1]
                        else:
                            printLine = allLines[lineNum]
                        self.printInformation(filePath + '\t' + 'line {0}'.format(lineNum+1) + '\t' + printLine)
                    lineNum += 1
            # one line
            else:
                lineNumber = 1
                for lineData in allLines:
                    if self.findDataValid(lineData, findString[0]) >= 0:
                        if lineData[-1] == '\n':
                            printLine = lineData[:-1]
                        else:
                            printLine = lineData
                        self.printInformation(filePath + '\t' + 'line {0}'.format(lineNumber) + '\t' + printLine)
                    lineNumber += 1
        finally:
            if file:
                file.close()

    def findFileString(self, findString=None):
        if findString == None:
            findString = self.findstr
        # Get the file name list
        fileNameList = self.getFileList()
        # Recursion find
        for filePath in fileNameList:
            self.findString(filePath, findString)

    def replaceString(self, filePath, findString, replaceString):
        try:
            file = open(filePath, 'r+', encoding='iso-8859-1')
            allLines = file.readlines()
            file.seek(0)
            file.truncate()
            strLen = len(allLines)
            triggerFlag = 0
            # multi-line
            if len(findString) > 1:
                lineNum = 0
                while lineNum < strLen:
                    if self.compareString(findString, allLines[lineNum:]):
                        for newLine in replaceString:
                            file.write(newLine)
                        lineNum += len(findString)
                        triggerFlag = 1
                    else:
                        file.write(allLines[lineNum])
                        lineNum += 1
            # one line
            else:
                for lineData in allLines:
                    if self.findDataValid(lineData, findString[0]) >= 0:
                        if len(replaceString) > 1:
                            for newLine in replaceString:
                                file.write(newLine)
                        else:
                            newLine = lineData.replace(findString[0], replaceString[0])
                            file.write(newLine)
                        triggerFlag = 1
                    else:
                        file.write(lineData)
            if triggerFlag == 1:
                self.printInformation(filePath)
        finally:
            if file:
                file.close()

    def replaceFileString(self, findString=None, repString=None):
        if findString == None:
            findString = self.findstr
        if repString == None:
            repString = self.modifystr
        # Get the file name list
        fileNameList = self.getFileList()
        # Recursion find and replace
        for filePath in fileNameList:
            self.replaceString(filePath, findString, repString)

    def addString(self, filePath, findString, addString):
        try:
            file = open(filePath, 'r+', encoding='iso-8859-1')
            allLines = file.readlines()
            file.seek(0)
            file.truncate()
            strLen = len(allLines)
            triggerFlag = 0
            # multi-line
            if len(findString) > 1:
                lineNum = 0
                while lineNum < strLen:
                    if self.compareString(findString, allLines[lineNum:]):
                        for oldLine in findString:
                            file.write(oldLine)
                        for newLine in addString:
                            file.write(newLine)
                        lineNum += len(findString)
                        triggerFlag = 1
                    else:
                        file.write(allLines[lineNum])
                        lineNum += 1
            # one line
            else:
                for lineData in allLines:
                    file.write(lineData)
                    if self.findDataValid(lineData, findString[0]) >= 0:
                        for addLine in addString:
                            file.write(addLine)
                        triggerFlag = 1
            if triggerFlag == 1:
                self.printInformation(filePath)
        finally:
            if file:
                file.close()

    def addFileString(self, findString=None, addString=None):
        if findString == None:
            findString = self.findstr
        if addString == None:
            addString = self.modifystr
        # Get the file name list
        fileNameList = self.getFileList()
        # Recursion find and add
        for filePath in fileNameList:
            self.addString(filePath, findString, addString)

    def deleteString(self, filePath, findString):
        try:
            file = open(filePath, 'r+', encoding='iso-8859-1')
            allLines = file.readlines()
            file.seek(0)
            file.truncate()
            strLen = len(allLines)
            triggerFlag = 0
            # multi-line
            if len(findString) > 1:
                lineNum = 0
                while lineNum < strLen:
                    if self.compareString(findString, allLines[lineNum:]):
                        lineNum += len(findString)
                        triggerFlag = 1
                    else:
                        file.write(allLines[lineNum])
                        lineNum += 1
            # one line
            else:
                for lineData in allLines:
                    if self.findDataValid(lineData, findString[0]) >= 0:
                        triggerFlag = 1
                    else:
                        file.write(lineData)
            if triggerFlag == 1:
                self.printInformation(filePath)
        finally:
            if file:
                file.close()

    def deleteFileString(self, findString=None):
        if findString == None:
            findString = self.findstr
        # Get the file name list
        fileNameList = self.getFileList()
        # Recursion find and add
        for filePath in fileNameList:
            self.deleteString(filePath, findString)


    def deleteSpaceAndTabs(self, filePath):
        try:
            file = open(filePath, 'r+', encoding='iso-8859-1')
            allLines = file.readlines()
            file.seek(0)
            file.truncate()
            triggerFlag = 0
            # Replace all lines
            for line in allLines:
                newLine = line.rstrip() + '\n'
                file.write(newLine)
                if triggerFlag == 0 and newLine != line:
                    triggerFlag = 1
            if triggerFlag == 1:
                print(filePath)
        finally:
            if file:
                file.close()

    def deleteFileSpaceAndTabs(self):
        # Get the file name list
        fileNameList = self.getFileList()
        # Delete excess space and tabs
        for filePath in fileNameList:
            self.deleteSpaceAndTabs(filePath)


    def replaceName(self, filePath, findString, repString):
        path = os.path.split(filePath)
        dirName = path[0]
        fileName = path[1]
        result = fileName.find(findString)
        if result >= 0:
            newName = fileName.replace(findString, repString)
            extension = os.path.splitext(newName)
            if extension == '.c' or extension == '.h' or extension == '.txt':
                return
            else:
                os.rename(filePath, dirName + '\\' + newName)

    def replaceFileName(self, findString=None, repString=None):
        if findString == None:
            findString = self.findstr
        if repString == None:
            repString = self.modifystr
        # Get the file name list
        fileNameList = self.getFileList()
        # Recursion find and replace
        for filePath in fileNameList:
            self.replaceName(filePath, findString, repString)

    def findName(self, filePath, findString):
        path = os.path.split(filePath)
        dirName = path[0]
        fileName = path[1]
        findCount = 0
        for string in findString:
            result = fileName.find(string)
            if result >= 0:
                findCount += 1
        if findCount != 0:
            os.remove(filePath)

    def findFileName(self, findString=None):
        if findString == None:
            findString = self.findstr
        # Get the file name list
        fileNameList = self.getFileList()
        # Recursion find and add
        for filePath in fileNameList:
            self.findName(filePath, findString)



























if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWinControl()
    mainWin.show()
    sys.exit(app.exec_())
