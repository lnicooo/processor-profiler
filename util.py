#!/usr/bin/env python3
import os
import re

def readFolder(folder, extension):
    files=[]
    for filename in os.listdir(folder):
        if re.match(extension, filename) is not None:
            files.append(folderName+"/"+filename)

    files.sort()
    return files

def openFile(myfile):
    data =[]

    with open(myfile , 'r') as f:
        for line in f:
            data.append(line.split())

    return data
