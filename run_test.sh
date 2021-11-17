#!/usr/bin/env bash
set -euo pipefail

#!/bin/sh

# Check Installation supports this example
checkinstall.exe -p install.pkg --nobanner || exit

CROSS=RISCV32

application=test-app

report=report-test

mkdir -p ${report}
mkdir -p ${report}/$1
mkdir -p ${report}/$1/disassembly

disasfile=${report}/$1/${application}.disas
dumpfile=${report}/$1/${application}.dump
outfile=${report}/$1/${application}

echo -e "\e[1;32m ********************************* \e[0m"
echo -e "\e[1;32m Running: ${application} \e[0m"
echo -e "\e[1;32m ********************************* \e[0m"

make -C ${application} CROSS=${CROSS}

mv ${application}/*.dump ${dumpfile}

harness/harness.${IMPERAS_ARCH}.exe \
--program ${application}/app.${CROSS}.elf \
--appdisassembly ${disasfile} \
--enabletools \
--callcommand "top/u1/cpu1/vapTools/functionprofile -dotfile ${outfile}.dot -sampleinterval 1  -filename ${outfile}.iprof"

python classification.py --iprof --iproffile ${outfile}.iprof --outputfile ${outfile}_func

python classification.py --rw --disassemblyfile ${disasfile} --outputfile ${outfile}_rw

python classification.py --registers --disassemblyfile ${disasfile} --outputfile ${outfile}_reg

python classification.py --instructions --classifier AUCD --disassemblyfile ${disasfile} --outputfile ${outfile}_instr

python classification.py --disassemblyfunc --classifier AUCD --disassemblyfile ${disasfile} --dumpfile ${dumpfile} --outputfile ${outfile}_func_disas


echo -e "\e[1;32m ********************************* \e[0m"
echo -e "\e[1;32m Done: ${application} \e[0m"
echo -e "\e[1;32m ********************************* \e[0m"



