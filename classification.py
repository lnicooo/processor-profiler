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
parser.add_option("--dumpfile",         action="store",  type="string", dest="dumpfile")

parser.add_option("--classifier"  ,     action="store", type="string", dest="classifier")
parser.add_option("--outputfile",       action="store", type="string", dest="outputfile")
parser.add_option("--disassemblyfolder",action="store", type="string", dest="disassemblyfolder")
parser.add_option("--iproffile",        action="store", type="string", dest="iproffile")

# parse arguments
(options, args) = parser.parse_args()

classAUCD = ['Arithmetic','Unconditional','Conditional','Data']

if options.instructionsprofile:

    if(options.disassemblyfolder != None):
        applications = readFolder(options.disassemblyfolder, 'disas')
    else:
        applications = options.disassemblyfile

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

    if(options.disassemblyfolder != None):
        applications = readFolder(options.disassemblyfolder, 'disas')
    else:
        applications = options.disassemblyfile

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

    if(options.disassemblyfolder != None):
        applications = readFolder(options.disassemblyfolder, "disas")
    else:
        applications = options.disassemblyfile

    table = open("{0}.csv".format(options.outputfile),"w")

    head="Application, Nº Registers, Registers\n"

    table.write(head)

    for application in applications:

        applicationName =  application.split('/')[1][:-4]

        disas_f = openFile(application)

        reg = Register(disas_f, 'riscv')

        registers = reg.list()

        numregisters = reg.reg_num

        applicationProfile = "{0},{1},{2}\n".format(applicationName,numregisters,registers)

        table.write(applicationProfile)

if options.iprof:

    df = pd.DataFrame()

    iprof_f = openFile(options.iproffile)

    df = Function().iprof(iprof_f)

    options.outputfile = options.outputfile+".csv"

    df.to_csv(options.outputfile)

if options.disassemblyfunction:

    reads=0
    writes=0

    disas=[]
    dump=[]

    disas_func={}

    df_iprof = pd.DataFrame()

    table = open("{0}.csv".format(options.outputfile),'w')

    if(options.classifier == "AUCD"):
        head=",".join(classAUCD)

    head="Function,Instructions,Reads,Writes,Registers,Reads %,Writes %,NºRegisters,"+head+",Instr_Reads %,Instr_Writes %,Usage%\n"

    table.write(head)

    #Open disasembly file
    disas = openFile(options.disassemblyfile[0])

    exe_instr = len(disas)

    #Open dump file
    dump = openFile(options.dumpfile)

    #Open iprof file
    #iprof = openFile(options.iproffile)

    #Clean empty linea
    dump = list(filter(None,dump))
    #Delete first 2 lines
    dump = dump[2:]

    disas_func = Function().disassembly(dump, disas)
    #df_iprof = Function().iprof(iprof)

    for func in disas_func:
        funcprofile=[]
        funcprofile.append(func)

        instr_func = len(disas_func[func])

        funcprofile.append(str(instr_func))

        reg = Register(disas_func[func], 'riscv')

        reads,writes = reg.readwrite()

        reads = " ".join(reads)
        funcprofile.append(reads)
        writes = " ".join(writes)
        funcprofile.append(writes)

        registers = reg.list()

        registers = " ".join(registers)

        funcprofile.append(registers)

        funcprofile.append(str(reg.reads_perc))
        funcprofile.append(str(reg.writes_perc))

        numregister = reg.reg_num

        funcprofile.append(str(numregister))

        disas = Instruction(disas_func[func], 'riscv')

        classifier = disas.arch_AUCD

        classification = disas.profile(classifier)

        classification = ",".join([str(x) for x in classification])

        funcprofile.append(classification)

        instr_r,instr_w = disas.readwrite()

        funcprofile.append(str(instr_r))

        funcprofile.append(str(instr_w))

        exe_perc = (instr_func/exe_instr)*100

        funcprofile.append(str(exe_perc))

        funcprofile = ",".join(funcprofile)

        funcprofile += "\n"

        table.write(funcprofile)

if options.plotinstructionsprofile:

    values=[]
    my_dpi=96
    plt.figure(figsize=(1000/my_dpi, 1000/my_dpi), dpi=my_dpi)

    if(options.classifier == "AUCD"):

        classificator = "AUCD"
        classifier = classAUCD
    application = options.disassemblyfile[0]
    #for application in options.disassemblyfile:

    #instr = Instruction(application,'riscv')

    #classifier = Instruction.classAUCD

    #classification = instr.profile(classifier)
    #classification = instructionsProfile(application, classificator)

    disas_f = openFile(application)
    disas = Instruction(disas_f,'riscv')
    classifier = disas.arch_AUCD
    classification = disas.profile(disas.arch_AUCD)
    print(classification)
    #classification = [(x/sum(classification))*100 for x in classification]
    #print(classification)
    values.append(classification)

    makeSpider(classifier, values, "Hello")

    plt.show()
