"""
Owner: Extravar

It takes all the files under one folder (including files in subfolders) and moves them into one folder.
It also creates a log file of the file names and the location of the files that are moved.
# GUI in progress
"""
import os, sys, csv
import shutil
from datetime import datetime
from pathlib import Path

def main():
    csvFileName = 'testLog.csv'
    logsDir = os.getcwd()
    destinationDir, sourceDir = r'E:\Files\Not Porn\Organized', r'E:\Files\Not Porn\Organized'
    if (not os.path.isdir("Logs")):
        os.mkdir("Logs")
    logsDir = os.path.join(logsDir, "Logs")
    os.chdir(logsDir)
    csvFileName, lenFileList = spider(csvFileName, sourceDir, logsDir)
    move(csvFileName, destinationDir, logsDir, lenFileList)
    organize_junk(destinationDir, lenFileList)


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
            try:
                shutil.move(row[2], destinationDir)
            except:
                None
            printProgressBarMove(int(row[0]), lenFileList, "Moving files...")
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
            theWriter.writerow({fieldnames[0]: id+1, fieldnames[1]: locDataset1[id], fieldnames[2]: locDataset2[id]})
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
    n = 0
    os.chdir(sourceDir)
    for dir_path, dir_names, file_names in os.walk(sourceDir):
        for f in (file_names):
            n += 1
            fileNamesList.append(f)
            fileNamesDir.append(os.path.join(dir_path, f))
            printProgressBarCrawl(n, "Crawling files...")
    return write(csvFileName, logsDir, fileNamesList, fileNamesDir), len(fileNamesList)


def checkFileName(fileName):
    n = 0
    while (os.path.exists(fileName)):
        n += 1
        fileExt = fileName[fileName.rindex("."):len(fileName)]
        try:
            if (((").") in fileName) and (("(") in fileName)):
                newFileName = fileName[0:fileName.rindex("(")]
            else:
                newFileName = fileName[0:fileName.rindex(".")]
        except:
            print(fileName)
        newFileName = newFileName+"({0})"+fileExt
        fileName = newFileName.format(n)
    return fileName


def printProgressBarCrawl(i, postText):
    sys.stdout.write('\r')
    if (i == 1):
        sys.stdout.write(f"   {postText}")
        sys.stdout.write('\n')
    sys.stdout.write(f" {'Files crawled: ' + str(i)}")
    sys.stdout.flush()

def printProgressBarMove(i,max,postText):
    n_bar = 20 #size of progress bar
    j= i/max
    sys.stdout.write('\r')
    if (i == 1):
        sys.stdout.write('\n')
        sys.stdout.write(f"   {postText}")
        sys.stdout.write('\n')
    sys.stdout.write(f" {int(round(100 * j+0.49))}% [{'=' * int(round(n_bar * j + 0.49)):{n_bar}s}]  {'Files moved: ' + str(i) + ' of ' + str(max)}")
    sys.stdout.flush()

def printProgressBarSort(i,max,postText):
    n_bar = 20 #size of progress bar
    try:
        j= i/max
    except:
        print("ERROR: No files to sort\n Exiting now...")
        exit()
    sys.stdout.write('\r')
    if (i == 1):
        sys.stdout.write('\n')
        sys.stdout.write(f"   {postText}")
        sys.stdout.write('\n')
    sys.stdout.write(f" {int(round(100 * j+0.49))}% [{'=' * int(round(n_bar * j + 0.49)):{n_bar}s}]  {'Files sorted: ' + str(i) + ' of ' + str(max)}")
    sys.stdout.flush()


def organize_junk(mainWorkingDir, lenFileList):
    # Some of the code in this function is from:
    # https://www.geeksforgeeks.org/junk-file-organizer-python/
    os.chdir(mainWorkingDir)
    n = 0
    for entry in os.scandir():
        if entry.is_dir():
            continue
        n += 1
        printProgressBarSort(n, lenFileList, "Sorting Files...")
        file_path = Path(entry)
        file_format = file_path.suffix.lower()
        if file_format in FILE_FORMATS:
            directory_path = Path(FILE_FORMATS[file_format])
            directory_path.mkdir(exist_ok=True)
            file_path.rename(directory_path.joinpath(file_path))
        else:
            directory_path = Path("OTHER")
            directory_path.mkdir(exist_ok=True)
            file_path.rename(directory_path.joinpath(file_path))

DIRECTORIES = {
    "HTML": [".html5", ".html", ".htm", ".xhtml", ".webp", ".opdownload"],
    "IMAGES": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg",
               ".heif", ".psd"],
    "VIDEOS": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".vob", ".mng",
               ".qt", ".mpg", ".mpeg", ".3gp"],
    "WEBM": [".webm"],
    "DOCUMENTS": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods",
                  ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
                  ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt",
                  "pptx"],
    "ARCHIVES": [".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z",
                 ".dmg", ".rar", ".xar", ".zip"],
    "AUDIO": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3",
              ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"],
    "PLAINTEXT": [".txt", ".in", ".out"],
    "PDF": [".pdf"],
    "CODE": [".py", ".php"],
    "XML": [".xml"],
    "EXE": [".exe"],
    "SHELL": [".sh"],
}

FILE_FORMATS = {file_format: directory
                for directory, file_formats in DIRECTORIES.items()
                for file_format in file_formats}

if __name__ == '__main__':
    main()