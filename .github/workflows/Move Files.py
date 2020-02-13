"""
Owner: Extravar

It takes all the files under one folder (including files in subfolders) and moves them into one folder.
It also creates a log file of the file names and the location of the files that are moved.
# GUI in progress
"""
import os, sys, csv
import shutil
from datetime import datetime

def main():
    csvFileName = 'testLog.csv'
    logsDir = os.getcwd()
    destinationDir, sourceDir =  'D:\ImageTestEnvir\These nutz', 'D:\ImageTestEnvir\Move'
    if (not os.path.isdir("Logs")):
        os.mkdir("Logs")
    logsDir = os.path.join(logsDir, "Logs")
    os.chdir(logsDir)
    csvFileName, lenFileList = spider(csvFileName, sourceDir, logsDir)
    move(csvFileName, destinationDir, logsDir, lenFileList)


def move(csvFileName, destinationDir, logsDir, lenFileList):
    lineCount = 0
    rowList = read(csvFileName, logsDir)
    os.chdir(destinationDir)
    for row in rowList:
        fileName = row[1]
        if (lineCount != 0):
            fileName = checkFileName(fileName)
            if (row[1] != fileName):
                os.rename(row[1], fileName)
            shutil.move(row[2], destinationDir)
            printProgressBar(int(row[0]), lenFileList, "Moving files...")
        lineCount += 1


def write(csvFileName, logsDir, locDataset1, locDataset2):
    os.chdir(logsDir)
    date = datetime.now()
    csvFileName = csvFileName[0:csvFileName.rindex(".")]
    csvFileName = csvFileName+" ["+date.strftime("%d/%m/%Y, %H:%M:%S")+"].csv"
    for i in range(csvFileName.count("/")):
        csvFileName = csvFileName.replace("/", ".")
    for i in range(csvFileName.count(":")):
        csvFileName = csvFileName.replace(":", "!")
    with open(csvFileName, 'w', newline='', encoding="utf-8") as csvFile:
        fieldnames = ['ID', 'File Name', 'File Directory']
        theWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
        theWriter.writeheader()
        for id in range(0, len(locDataset1)):
            #if (locDataset1[id][-3:-1] != "in"):
            try:
                theWriter.writerow({fieldnames[0]: id+1, fieldnames[1]: locDataset1[id], fieldnames[2]: locDataset2[id]})
            except:
                continue
    csvFile.close()
    return csvFileName


def read(csvFileName, logsDir):
    rowList = []
    os.chdir(logsDir)
    with open(csvFileName, 'r', newline='', encoding="utf-8") as csvFile:
        theReader = csv.reader(csvFile)
        for row in theReader:
            rowList.append(row)
    csvFile.close()
    return rowList


def spider(csvFileName, sourceDir, logsDir):
    fileNamesList, fileNamesDir = [], []
    os.chdir(sourceDir)
    for dir_path, dir_names, file_names in os.walk(sourceDir):
        for f in (file_names):
            fileNamesList.append(f)
            fileNamesDir.append(os.path.join(dir_path, f))
    return write(csvFileName, logsDir, fileNamesList, fileNamesDir), len(fileNamesList)


def checkFileName(fileName):
    n = 0
    while (os.path.exists(fileName)):
        n += 1
        fileExt = fileName[fileName.rindex("."):len(fileName)]
        if (("(" and int and ")") in fileName):
            newFileName = fileName[0:fileName.rindex("(")]
        else:
            newFileName = fileName[0:fileName.rindex(".")]
        newFileName = newFileName+"({0})"+fileExt
        fileName = newFileName.format(n)
    return fileName


def printProgressBar(i,max,postText):
    n_bar = 20 #size of progress bar
    j= i/max
    sys.stdout.write('\r')
    if (i == 1):
        sys.stdout.write(f"   {postText}")
        sys.stdout.write('\n')
    sys.stdout.write(f" {int(round(100 * j+0.49))}% [{'=' * int(round(n_bar * j + 0.49)):{n_bar}s}]  {'Files moved: ' + str(i) + ' of ' + str(max)}")
    sys.stdout.flush()

if __name__ == '__main__':
    main()