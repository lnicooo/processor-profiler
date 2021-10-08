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

echo -e "\e[1;32m ********************************* \e[0m"
echo -e "\e[1;32m Running: ${application} \e[0m"
echo -e "\e[1;32m ********************************* \e[0m"

make -C test-app CROSS=${CROSS}

harness/harness.${IMPERAS_ARCH}.exe \
--program test-app/app.${CROSS}.elf \
--appdisassembly ${report}/$1/disassembly/${application}.disas \
--enabletools \
--callcommand "top/u1/cpu1/vapTools/functionprofile -dotfile ${report}/$1/${application}.dot -sampleinterval 1  -filename ${report}/$1/${application}.iprof"

#awk -f funcs.awk app.out | sort -nk2 -r > ${application}.out
python classification.py --functionprofile --iprof ${report}/$1/${application}.iprof --outputfile ${report}/$1/${application}_func

python classification.py --rw --disassemblyfolder ${report}/$1/disassembly --outputfile ${report}/$1/${application}_rw

python classification.py --instructions --classifier AUCD --disassemblyfolder  ${report}/$1/disassembly --outputfile ${report}/$1/${application}_instr

echo -e "\e[1;32m ********************************* \e[0m"
echo -e "\e[1;32m Done: ${application} \e[0m"
echo -e "\e[1;32m ********************************* \e[0m"



