#!/usr/bin/env python3

import sys
import os

from optparse import OptionParser
from collections import Counter

import re
import math

import matplotlib.pyplot as plt
import numpy as np

# -------------------------------- Options Parser ---------------------------------------- #
parser = OptionParser()

parser.add_option("--instructions",     action="store_true", dest="instructionsprofile",    help="table uahhuh")
parser.add_option("--instructionsplot", action="store_true", dest="plotinstructionsprofile",help="Plot uahhuh")
parser.add_option("--registers",        action="store_true", dest="registersprofile",       help="print registers")
parser.add_option("--rw",        action="store_true", dest="readswrites",       help="print registers")

parser.add_option("--disassemblyfile",  action="append", type="string", dest="disassembly")

parser.add_option("--classifier"  ,     action="store", type="string", dest="classifier")
parser.add_option("--outputfile",       action="store", type="string", dest="outputfile")
parser.add_option("--disassemblyfolder",action="store", type="string", dest="disassemblyfolder")
# parse arguments
(options, args) = parser.parse_args()

# classification
AUCD = [['and','or','xor','andi','ori','xori','sll','srl','sra','slli','srli','srai','add','sub','addi','mul','div','rem','neg','not','sltiu'],
['j','jr','jal','jalr','ret','ecall','mret','auipc'],
['slt','slti','sltu','seqz','snez','sltz','sgtz','srai','beq','bne','blt','bltu','bge','bgeu','bgt','bgtu','ble','bleu','beqz','bnez','bltz','blez','bgez','bgtz'],
['lw','lh','lhu','lb','lbu','sw','sh','sb','li','la','lui','mv','lhu']]

rv_registers = ["ra","sp","gp","tp","t0","t1","t2","s0","s1","a0","a1","a2","a3","a4","a5","a6","a7","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","t3","t4","t5","t6","pc"]

rv_loads = ['lw','lh','lhu','lb','lbu','li','la','lui','lhu']
rv_writes = ['sw','sh','sb']

classAUCD = ['Arithmetic','Unconditional','Conditional','Data']


def readFolder(folderName):
    files=[]
    for filename in os.listdir(folderName):
        if re.match(".*out", filename) is not None:
            files.append(folderName+"/"+filename)

    files.sort()
    return files

def makeSpider( categories, values, title):

    colors=['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

    #categories += categories[:1]

    N = max(max(values))
    N = int(math.ceil(N/10))*10

    y_labels = np.arange(0,N+10,10)
    y_labels_str = [str(y) for y in y_labels]

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)

    angles=np.append(angles,angles[:1])

    # Initialise the spider plot
    ax = plt.subplot(polar=True)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=10)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks(y_labels, y_labels_str, color="grey", size=7)
    plt.ylim(0,N)

    for index,value in enumerate(values):
    # Ind1

        value += value[:1]
        ax.plot(angles, value, color=colors[index], linewidth=2, linestyle='solid')
        ax.fill(angles, value, color=colors[index], alpha=0.4)

    # Add a title
    plt.title(title, size=11, color="Grey", y=1.1)

def instructionsProfile(disassemblyfile, instrClassifier):
    data=[]

    with open(disassemblyfile , 'r') as f:
        for line in f:
            data.append(line.split())

    instr=[x[1] for x in data]

    instr_hist=list(Counter(instr).items())

    classification=np.zeros(len(instrClassifier))

    #print(instr_hist)

    #print(sum([x[1] for x in instr_hist]))

    #a=False

    for instr in instr_hist:
        for index, instrclass in enumerate(instrClassifier):
            if(instr[0] in instrclass):
                classification[index]+=instr[1]
                #a=True
        #if(a == False):
        #    print(instr[0])
        #a=False

    #print(sum(classification))

    return classification

def registerProfile(disassemblyfile):
    data=[]

    with open(disassemblyfile , 'r') as f:
        reg_read=[]
        reg_write=[]
        for line in f:

            line=line.split()
            register=[]
            if(len(line)>2):
                register=re.findall("[tsa]\d[0-1]*|ra|[sgt][p]",line[2])
            if(len(register)>1):
                reg_write.append(register[0])
            if(len(register)>2):
                for x in register[1:]:
                    reg_read.append(x)

    writes=list(Counter(reg_write).items())

    writes=[str(x[0]) for x in writes]

    reads=list(Counter(reg_read).items())

    reads=[str(x[0]) for x in reads]

    return writes,reads

if options.instructionsprofile:

    applications = readFolder(options.disassemblyfolder)

    table = open("{0}.csv".format(options.outputfile),'w')

    if(options.classifier == "AUCD"):
        head=",".join(classAUCD)
        classificator = AUCD
    head+="\n"
    table.write(head)

    for application in applications:

        classification = instructionsProfile(application, classificator)

        classification = [(x/sum(classification))*100 for x in classification]

        classification = ",".join([str(x) for x in classification])

        applicationName = application.split('/')[1][:-4]

        applicationProfile = "{0},{1}\n".format(applicationName,classification)

        table.write(applicationProfile)

    sys.exit()

if options.readswrites:

    applications = readFolder(options.disassemblyfolder)
    table = open("{0}.csv".format(options.outputfile),'w')
    """
    if(options.classifier == "AUCD"):
        head=",".join(classAUCD)
        classificator = AUCD
    head+="\n"
    """
    head = "Application, Reads, Writes\n"

    table.write(head)


    for application in applications:

        data=[]
        read=0
        write=0

        with open(application , 'r') as f:
           for line in f:
               data.append(line.split())
        instr=[x[1] for x in data]
        instr_hist=list(Counter(instr).items())
        for instr in instr_hist:
            if(instr[0] in rv_loads):
                read+=instr[1]
            elif(instr[0] in rv_writes):
                write+=instr[1]
        #instr_sum = sum([x[1] for x in instr_hist])
        rw_sum = read+write

        reads  = str((read/rw_sum)*100)
        writes = str((write/rw_sum)*100)

        applicationName =  application.split('/')[1][:-4]

        applicationRW = "{0},{1},{2}\n".format(applicationName,reads,writes)
        table.write(applicationRW)
    sys.exit()

if options.plotinstructionsprofile:

    values=[]
    my_dpi=96
    plt.figure(figsize=(1000/my_dpi, 1000/my_dpi), dpi=my_dpi)

    if(options.classifier == "AUCD"):

        classificator = AUCD
        classifier = classAUCD

    for application in options.disassembly:

        classification = instructionsProfile(application, classificator)

        classification = [(x/sum(classification))*100 for x in classification]

        values.append(classification)

    makeSpider(classifier, values, "Hello")

    plt.show()

if options.registersprofile:

    applications = readFolder(options.disassemblyfolder)

    table = open("{0}.csv".format(options.outputfile),"w")

    head="Application, Nº Registers, Registers\n"

    table.write(head)

    for application in applications:
        writes,reads = registerProfile(application)
        applicationName =  application.split('/')[1][:-4]

        writes = set(writes)
        writes.update(set(reads))

        registers = writes.intersection(set(rv_registers))

        numregisters = len(registers)

        applicationProfile = "{0},{1},{2}\n".format(applicationName,numregisters,registers)
        print(applicationProfile)
        table.write(applicationProfile)
