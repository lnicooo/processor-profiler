#!/usr/bin/env python3

import sys
import os

from optparse import OptionParser
from util import *
from profiler import *
from plot import *


# -------------------------------- Options Parser ---------------------------------------- #
parser = OptionParser()

parser.add_option("--instructions",     action="store_true", dest="instructionsprofile",    help="table uahhuh")
parser.add_option("--instructionsplot", action="store_true", dest="plotinstructionsprofile",help="Plot uahhuh")
parser.add_option("--registers",        action="store_true", dest="registersprofile",       help="print registers")
parser.add_option("--rw",               action="store_true", dest="readswrites",            help="print registers")
parser.add_option("--disassemblyfunc",  action="store_true", dest="disassemblyfunction",    help="Generate csv from iprof")
parser.add_option("--iprof",            action="store_true", dest="iprof",                  help="List executing function")


parser.add_option("--disassemblyfile",  action="append", type="string", dest="disassemblyfile")
parser.add_option("--dumpfile",         action="store", type="string", dest="dumpfile")

parser.add_option("--classifier"  ,     action="store", type="string", dest="classifier")
parser.add_option("--outputfile",       action="store", type="string", dest="outputfile")
parser.add_option("--disassemblyfolder",action="store", type="string", dest="disassemblyfolder")
parser.add_option("--iproffile",        action="store", type="string", dest="iproffile")

# parse arguments
(options, args) = parser.parse_args()

classAUCD = ['Arithmetic','Unconditional','Conditional','Data']

if options.instructionsprofile:

    applications = readFolder(options.disassemblyfolder, "disas")

    table = open("{0}.csv".format(options.outputfile),'w')

    if(options.classifier == "AUCD"):
        head=",".join(classAUCD)

    head+="\n"
    table.write(head)

    for application in applications:

        disas_f = openFile(application)

        disas = Instruction(disas_f, 'riscv')

        classifier = disas.arch_AUCD

        classification = disas.profile(classifier)

        classification = ",".join([str(x) for x in classification])

        applicationName = application.split('/')[1][:-4]

        applicationProfile = "{0},{1}\n".format(applicationName,classification)

        table.write(applicationProfile)

    sys.exit()

if options.readswrites:

    applications = readFolder(options.disassemblyfolder, 'out')
    table = open("{0}.csv".format(options.outputfile),'w')

    head = "Application, Reads, Writes\n"

    table.write(head)

    for application in applications:

        reads  = 0
        writes = 0

        disas_f = openFile(application)

        instr = Instruction(disas_f, 'riscv')

        reads, writes = instr.readwrite()

        applicationName = application.split('/')[1][:-4]

        applicationRW = "{0},{1},{2}\n".format(applicationName,reads,writes)
        table.write(applicationRW)

    sys.exit()

if options.registersprofile:

    applications = readFolder(options.disassemblyfolder, "out")

    table = open("{0}.csv".format(options.outputfile),"w")

    head="Application, Nº Registers, Registers\n"

    table.write(head)

    for application in applications:

        applicationName =  application.split('/')[1][:-4]

        reg = Register(application, 'riscv')

        registers = reg.list()

        numregisters = reg.reg_num

        applicationProfile = "{0},{1},{2}\n".format(applicationName,numregisters,registers)

        table.write(applicationProfile)

if options.iprof:

    df = pd.DataFrame()

    df = Function.iprof(options.iproffile)

    df.to_csv(options.outputfile)

if options.disassemblyfunction:

    reads=0
    writes=0

    disas=[]
    dump=[]

    disas_func={}

    #Open disasembly file
    disas = openFile(options.disassemblyfile[0])

    #Open dump file
    dump = openFile(options.dumpfile)

    #Clean empty linea
    dump = list(filter(None,dump))
    #Delete first 2 lines
    dump = dump[2:]

    disas_func = Function().disassembly(dump, disas)

    for func in disas_func:

        reg = Register(disas_func[func], 'riscv')

        reads,writes = reg.readwrite()

        registers = reg.list()

        registers = "".join(registers)

        numregister = reg.reg_num

        disas = Instruction(disas_func[func], 'riscv')

        classifier = disas.arch_AUCD

        classification = disas.profile(classifier)

        classification = " ".join([str(x) for x in classification])

        print("Function: "+str(func))
        print("Registers: "+str(registers))
        print("Number of registers: "+str(numregister))
        print("Profile: "+str(classification))


if options.plotinstructionsprofile:

    values=[]
    my_dpi=96
    plt.figure(figsize=(1000/my_dpi, 1000/my_dpi), dpi=my_dpi)

    if(options.classifier == "AUCD"):

        classificator = AUCD
        classifier = classAUCD

    for application in options.disassemblyfile:

        instr = Instruction(application,'riscv')

        classifier = Instruction.classAUCD

        classification = instr.profile(classifier)

        classification = instructionsProfile(application, classificator)

        classification = [(x/sum(classification))*100 for x in classification]

        values.append(classification)

    makeSpider(classifier, values, "Hello")

    plt.show()
