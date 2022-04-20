#!/usr/bin/env python3
#
#
import re

import pandas as pd
import numpy  as np

from collections import Counter

class Instruction():
    def __init__(self, data, arch):
        self.data  = data
        self.instr = [x[2] for x in data]
        
        if(arch == 'riscv'):
            self.__arch_loads   = ['lw','lh','lhu','lb','lbu','li','la','lui','lhu']
            self.__arch_writes  = ['sw','sh','sb']
            self.classAUCD      = ['Arithmetic','Unconditional','Conditional','Data']
            self.arch_AUCD      = [['and','or','xor','andi','ori','xori','sll','srl','sra','slli','srli','srai','add','sub','addi','mul','div','rem','neg','not','sltiu'],
                                     ['j','jr','jal','jalr','ret','ecall','mret','auipc'],
                                     ['slt','slti','sltu','seqz','snez','sltz','sgtz','srai','beq','bne','blt','bltu','bge','bgeu','bgt','bgtu','ble','bleu','beqz','bnez','bltz','blez','bgez','bgtz'],
                                     ['lw','lh','lhu','lb','lbu','sw','sh','sb','li','la','lui','mv','lhu']]

    def profile(self, instrClassifier):

        instr_hist=list(Counter(self.instr).items())

        classification=np.zeros(len(instrClassifier))

        for instr in instr_hist:
            for index, instrclass in enumerate(instrClassifier):
                if(instr[0] in instrclass):
                    classification[index]+=instr[1]
                    break

        classification = [(x/sum(classification))*100 for x in classification]

        return classification

    def disassembly(self, instrClassifier):

        classification = {}

        for instrclass in self.classAUCD:
            classification[instrclass] = []

        for instr in self.data:
            for index, instrclass in enumerate(instrClassifier):
                if(instr[2] in instrclass):
                    instrclass = self.classAUCD[index]
                    classification[instrclass].append(instr)
                    break

        return classification
    
    def readwrite(self):

        #returns percentage of reads and writes by executed data instructions
        #
        read=0
        write=0
        reads=0
        writes=0

        instr_hist=list(Counter(self.instr).items())

        for instr in instr_hist:
            if(instr[0] in self.__arch_loads):
                read+=instr[1]

            elif(instr[0] in self.__arch_writes):
                write+=instr[1]

        #instr_sum = sum([x[1] for x in instr_hist])
        rw_sum = read+write

        if(read>0):
            reads  = str((read/rw_sum)*100)
        if(write>0):
            writes = str((write/rw_sum)*100)

        return reads, writes

class Register():

    def __init__(self, data, arch):
        self.registers = [x[3] for x in data if len(x)>3]

        self.data = data
        self.writes_usage = 0
        self.reads_usage  = 0
        self.reg_usage    = 0
        self.reg_num      = 0
        self.reads_perc   = 0
        self.writes_perc  = 0

        if(arch == 'riscv'):
            self.arch_registers = ["ra","sp","gp","tp","t0","t1","t2","s0","s1","a0","a1","a2","a3","a4","a5","a6","a7","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","t3","t4","t5","t6","pc"]
            self.arch_read_instr = ['beq','bne','beqz','bnez','blt','bltu','bge','bgeu','sw','sh','sb']

            self.arch = arch
    def __maximum(self,max_value,w_table):
        #find the biggest value from table
        y=w_table[0]
        for j in w_table:
            if(j>=max_value):
                break
            y=j
        return y

    def vulnerability(self):
        #create empty table
        rvf_table={}
        rvf={}
        for reg in self.arch_registers:
            rvf_table[reg]=([],[])
            rvf[reg]=0

        for x in range(len(self.data)):
            curr_line = self.data[x]
            #print(str(x)+" "+str(j))
            if(len(curr_line)>3):
                regs = curr_line[3]
                instr = curr_line[2]
                regs_found = re.findall("s10|s11|re|t[0-2]|a[0-7]|s[0-9]|[sgt][p]", regs)
                if(instr in self.arch_read_instr):
                    #consider all regsiter as read
                    for reg in regs_found:
                        rvf_table[reg][0].append(x)
                else:
                    if(len(regs_found)>=1):
                        #write
                        rvf_table[regs_found[0]][1].append(x)
                    if(len(regs_found)>=2):
                        #read
                        for reg in regs_found[1:]:
                            rvf_table[reg][0].append(x)

        #finds the times register was vulnerable
        for reg in self.arch_registers:
            print(reg)
            writes=rvf_table[reg][1].copy()
            reads=rvf_table[reg][0].copy()
            regs_vuln={}
            if(len(writes)>0):

                for read_x in reads:
                    max_value=self.__maximum(read_x,writes)

                    if(max_value!=writes[0]):
                        #breaks the array for unused values
                        writes=writes[writes.index(max_value):]

                    regs_vuln[max_value]=read_x

            #calculate how many instructions that the register was vulnerable
            for x in regs_vuln:
                rvf[reg]+=regs_vuln[x]-x
            print(rvf[reg])

        return rvf


    def readwrite(self):

        reads=0
        writes=0

        reg_read=[]
        reg_write=[]
        for reg in self.registers:

            regs_found=[]
            #filter RISC-V registers
            regs_found=re.findall("s10|s11|ra|[tsa]\d|[sgt][p]", reg)

            #append fist register to read list
            if(len(regs_found)>=1):
                reg_write.append(regs_found[0])

            #append the rest to the write list
            if(len(regs_found)>=2):
                reg_read.extend(regs_found[1:])

        num_regs = len(reg_write)

        writes=list(Counter(reg_write).items())

        self.writes_usage = [(x[1]/num_regs)*100 for x in writes]

        writes=[str(x[0]) for x in writes]

        writes_tot = sum(Counter(reg_write).values())
        if(writes_tot>0):
            self.writes_perc = (writes_tot/num_regs)*100

        reads=list(Counter(reg_read).items())

        num_regs = len(reg_read)

        self.reads_usage = [(x[1]/num_regs)*100 for x in reads]

        reads=[str(x[0]) for x in reads]

        reads_tot = sum(Counter(reg_read).values())

        num_regs = writes_tot + reads_tot

        if(writes_tot>0):
            self.writes_perc = (writes_tot/num_regs)*100
        if(reads_tot>0):
            self.reads_perc = (reads_tot/num_regs)*100
            
        return reads,writes

    def list(self):

        regs_hist=[]

        #returns a list of the most used registers
        for reg in self.registers:
            regs_found=[]

            #filter RISC-V registers
            regs_found=re.findall("s10|s11|re|t[0-2]|a[0-7]|s[0-9]|[sgt][p]", reg)

            if(len(regs_found)>=1):
                regs_hist.extend(regs_found)

        regs_hist=list(Counter(regs_hist).items())

        self.reg_usage = regs_hist

        regs_hist=sorted(regs_hist,key=lambda x:x[1],reverse=True)

        num_reg = sum([x[1] for x in regs_hist])

        self.reg_num = len(regs_hist)

        #self.reg_usage = [(x[1]/num_reg)*100 for x in regs_hist]

        regs_class = (['a0','a1','a2','a3','a4','a5','a6','a7'],['s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11'],['t0','t1','t2','t3','t4','t5','t6'],['ra','sp','s0','gp','tp','pc'])

        x=[]

        for regs_c in regs_class:
            b=[]
            for i in regs_hist:
                if(i[0] in regs_c):
                    b.append(i[1])

            x.append(sum(b))

        #self.reg_usage = [str((l/sum(x))*100) for l in x]

        #self.reg_usage = regs_hist

        regs_hist=[str(x[0]) for x in regs_hist]

        return regs_hist

class Function():

    def disassembly(self,dump,disas):
        #return a tuple with disassembled code with function assigment
        func_addr={}
        func=""
        disas_func={}
        carac_func={}

        for line in dump:
            if(len(line)==2):
                func = line[1]
                func_addr[func]=[]
            else:
                func_addr[func].append(line[0][:-1])

        #print(func_addr['<mac>:'])

        for i,line in enumerate(disas):
            addr = hex(int(line[0]))[2:]
            for func in func_addr:

                func_name = func[1:-2]
                if(func_name not in disas_func):
                    func_pop = func_name
                    disas_func[func_name]=[]

                if(addr in func_addr[func]):
                    #line.append(i)

                    disas_func[func_name].append(line)
                    break

        empty_keys = [func for func in disas_func if disas_func[func]==[]]

        for key in empty_keys:
            disas_func.pop(key)

        return disas_func

    def iprof(self, iprof):
        #returns a dataframe
        df = pd.DataFrame(columns=['func','id','samp','perc','in','out'])

        a=re.compile('^(?:FP:)(\d*) (\w*) (?:[^ ]*) (\d*) (\d*)$')
        b=re.compile('^(?:FPC:)(\d*), (\d*), (\d*)$')


        for line in iprof:

            line = " ".join(line)

            m_a=a.match(line)
            m_b=b.match(line)

            if(m_a):
                x={'func':m_a.group(2), 'id':m_a.group(3),'samp':int(m_a.group(4)),'in':0}
                df=df.append(x,ignore_index=True)

            elif(m_b):
                #print(m_b.group(3))
                df.loc[df['id'] == m_b.group(3),['in']]+=int(m_b.group(1))

                df['out']  = df['in'] - df['samp']
                df['perc'] = (df['samp']/df['samp'].sum())*100
                df = df.sort_values(by=['perc'],ascending=False)

        #df.to_csv(options.outputfile)

        return df
