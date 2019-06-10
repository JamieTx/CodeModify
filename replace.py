#!/usr/bin/python3

import os
import sys

# global variable
rootDirectory = ''

class FileFind:
    pass

def getFileList(dirPath):
    fileList = []
    # os.walk(), return a triple
    for root, dirs, files in os.walk(dirPath):
        for fileObj in files:
            # Determine if the file suffix is .c or .h
            extension = os.path.splitext(fileObj)[-1]
            extension = extension.lower()
            if extension == '.c' or extension == '.h' or extension == '.txt':
                fileList.append(os.path.join(root, fileObj))
    return fileList

def printPathList(filePathName):
    for filePath in filePathName:
        print(filePath)

def findSpecifyString(filePath, findString):
    try:
        file = open(filePath, 'r', encoding='iso-8859-1')
        allLines = file.readlines()
        file.seek(0)
        # Search all lines
        lineNumber = 1
        for line in allLines:
            result = line.find(findString)
            if result >= 0:
                if line.find('\n') > 0:
                    print(filePath + '\t\t' + 'line {0}'.format(lineNumber) + '\t\t' + line, end='')
                else:
                    print(filePath + '\t\t' + 'line {0}'.format(lineNumber) + '\t\t' + line)
            lineNumber += 1
    finally:
        if file:
            file.close()

def replaceSpecifyString(filePath, findString, replaceString):
    try:
        file = open(filePath, 'r+', encoding='iso-8859-1')
        allLines = file.readlines()
        file.seek(0)
        file.truncate()
        triggerFlag = 0
        # Replace all lines
        for line in allLines:
            newLine = line.replace(findString, replaceString)
            file.write(newLine)
            if triggerFlag == 0 and newLine != line:
                triggerFlag = 1
        if triggerFlag == 1:
            print(filePath)
    finally:
        if file:
            file.close()

def addPathSubFunc(filePath):
    try:
        file = open(filePath, 'r+', encoding='iso-8859-1')
        allLines = file.readlines()
        file.seek(0)
        file.truncate()
        # Replace all lines
        for line in allLines:
            triggerFlag = 0
            result1 = line.find('main.c')
            result2 = line.find('ddl_config.h')
            if result1 >= 0:
                index = filePath.find('example')
                pathStr = filePath[index:]
                pathStr = pathStr[8:]
                newLine = line.replace('main.c', pathStr)
                newLine = newLine.replace('\\', '/')
                file.write(newLine)
                triggerFlag = 1
            elif result2 >= 0:
                index = filePath.find('example')
                pathStr = filePath[index:]
                pathStr = pathStr[8:]
                newLine = line.replace('ddl_config.h', pathStr)
                newLine = newLine.replace('\\', '/')
                file.write(newLine)
                triggerFlag = 1

            if triggerFlag == 0:
                file.write(line)
    finally:
        if file:
            file.close()

def addSpecifyString(filePath, findString, addString):
    try:
        file = open(filePath, 'r+', encoding='iso-8859-1')
        allLines = file.readlines()
        file.seek(0)
        file.truncate()
        triggerFlag = 0
        # Replace all lines
        for line in allLines:
            file.write(line)
            result = line.find(findString)
            if result >= 0:
                for addLine in addString:
                    file.write(addLine + '\n')
                if triggerFlag == 0:
                    triggerFlag = 1
        if triggerFlag == 1:
            print(filePath)
    finally:
        if file:
            file.close()

def deleteSpecifyString(filePath, findString):
    try:
        file = open(filePath, 'r+', encoding='iso-8859-1')
        allLines = file.readlines()
        file.seek(0)
        file.truncate()
        triggerFlag = 0
        # Replace all lines
        for line in allLines:
            findCount = 0
            for string in findString:
                result = line.find(string)
                if result >= 0:
                    findCount += 1
            if findCount == 0:
                file.write(line)
            else:
                if triggerFlag == 0:
                    triggerFlag = 1
        if triggerFlag == 1:
            print(filePath)
    finally:
        if file:
            file.close()

def deleteExcessSpaceAndTabs(filePath):
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

def replaceNameFunc(filePath, findString, repString):
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

def deleteFileFunc(filePath, findString):
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

def findFileString(findString):
    global rootDirectory

    if findString == '\\t':
        findString = '\t'
    # Get the file name list
    fileNameList = getFileList(rootDirectory)
    # Recursion find
    for filePath in fileNameList:
        findSpecifyString(filePath, findString)

def replaceFileString(findString, repString=''):
    global rootDirectory

    if findString == '\\t':
        findString = '\t'
    # Get the file name list
    fileNameList = getFileList(rootDirectory)
    # Recursion find and replace
    for filePath in fileNameList:
        replaceSpecifyString(filePath, findString, repString)

def addFileString(findString, add_string):
    global rootDirectory

    if findString == '\\t':
        findString = '\t'
    # Get the file name list
    fileNameList = getFileList(rootDirectory)
    # Recursion find and add
    for filePath in fileNameList:
        addSpecifyString(filePath, findString, add_string)

def deleteFileString(findString):
    global rootDirectory

    if findString == '\\t':
        findString = '\t'
    # Get the file name list
    fileNameList = getFileList(rootDirectory)
    # Recursion find and add
    for filePath in fileNameList:
        deleteSpecifyString(filePath, findString)

def specifyFilePath(filePath):
    global rootDirectory

    rootDirectory = filePath
    print('Current directory: {}'.format(rootDirectory))

def deleteSpaceAndTabs():
    global rootDirectory

    # Get the file name list
    fileNameList = getFileList(rootDirectory)
    # Delete excess space and tabs
    for filePath in fileNameList:
        deleteExcessSpaceAndTabs(filePath)

def addPathInfomation():
    global rootDirectory

    # Get the file name list
    fileNameList = getFileList(rootDirectory)
    # Recursion find and replace
    for filePath in fileNameList:
        addPathSubFunc(filePath)

def replaceFileName(findString, repString=''):
    global rootDirectory

    if findString == '\\t':
        findString = '\t'
    # Get the file name list
    fileNameList = getFileList(rootDirectory)
    # Recursion find and replace
    for filePath in fileNameList:
        replaceNameFunc(filePath, findString, repString)

def deleteFile(findString):
    global rootDirectory

    if findString == '\\t':
        findString = '\t'
    # Get the file name list
    fileNameList = getFileList(rootDirectory)
    # Recursion find and add
    for filePath in fileNameList:
        deleteFileFunc(filePath, findString)

def consoleUi():
    global rootDirectory
    rootDirectory = os.getcwd()

    while True:
        print('\n####               Script tool V0.2               ####')
        print('#### Get help by entering only command characters ####')
        print('1. Finds the specified string in all files')
        print('2. Replaces the specified string found in all files')
        print('3. Adds string line after finding the specified string in all files')
        print('4. Deletes lines in all files that contain the specified string')
        print('5. Specify the script root directory')
        print('6. Deletes excess whitespace and tabs at the end of a line')
        print('7. Replaces all specified file names')
        print('8. Deletes all specified file names')
#        print('7  Add path information before @file name')
        print('0: Exit')

        enterString = input('\nEnter command and parameters:\n')
        if len(enterString) == 0:
            print('Invalid inputs')
            continue

        cmdString = enterString.split(maxsplit=1)
        if len(cmdString) > 1:
            paraString = cmdString[1].split(sep='$')
        else:
            paraString = ''

        if cmdString[0] == '1':
            if len(cmdString) == 2:
                findFileString(cmdString[1])
            else:
                print('\nReference command: 1 string')
        elif cmdString[0] == '2':
            if len(paraString) == 2:
                replaceFileString(paraString[0], paraString[1])
            elif len(paraString) == 1:
                replaceFileString(paraString[0])
            else:
                print('\nReference command: 2 old_string$new_string')
        elif cmdString[0] == '3':
            if len(paraString) >= 2:
                addFileString(paraString[0], paraString[1:])
            else:
                print('\nReference command: 3 string$line$line$...')
        elif cmdString[0] == '4':
            if len(paraString) >= 1:
                deleteFileString(paraString)
            else:
                print('\nReference command: 4 string$string$...')
        elif cmdString[0] == '5':
            if len(cmdString) == 2:
                specifyFilePath(cmdString[1])
            else:
                print('\nReference command: 5 string')
        elif cmdString[0] == '6':
            deleteSpaceAndTabs()
        elif cmdString[0] == '7':
            if len(paraString) == 2:
                replaceFileName(paraString[0], paraString[1])
            elif len(paraString) == 1:
                replaceFileName(paraString[0])
            else:
                print('\nReference command: 7 old_string$new_string')
        elif cmdString[0] == '8':
            if len(paraString) >= 1:
                deleteFile(paraString)
            else:
                print('\nReference command: 8 string$string$...')
        elif cmdString[0] == '0':
            break
        else:
            print('Invalid commands')
    else:
        print('Exit script')

def timeTest():
    pass

if __name__ == '__main__':
    consoleUi()
