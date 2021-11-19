#!/bin/sh

# Check Installation supports this example
checkinstall.exe -p install.pkg --nobanner || exit

CROSS=RISCV32


if [[ -z "$APPLICATION_LIST" ]]; then
    APPLICATION_LIST=($(ls baremetal))
fi

mkdir -p build
mkdir -p elf
mkdir -p reports
mkdir -p reports/$1
mkdir -p disassembly

cp application/Makefile build/.

make  -C module
make  -C harness


for application in ${APPLICATION_LIST[*]}
do
    echo -e "\e[1;32m ********************************* \e[0m"
    echo -e "\e[1;32m Running: ${application} \e[0m"
    echo -e "\e[1;32m ********************************* \e[0m"

    cp baremetal/${application}/app.c build/.

    make -C build CROSS=${CROSS}

    harness/harness.${IMPERAS_ARCH}.exe \
    --program build/app.${CROSS}.elf \
    --appdisassembly disassembly/${application}.disas \
    --enabletools \
    --callcommand "top/u1/cpu1/vapTools/functionprofile -dotfile reports/$1/${application}.dot -sampleinterval 1  -filename reports/$1/${application}.iprof"

    #awk -f funcs.awk app.out | sort -nk2 -r > ${application}.out
    python classification.py --functionprofile --iprof reports/${application}.iprof --outputfile reports/$1/${application}_func.csv

    #rm app.out
    cp build/*.elf elf/${application}.elf
    rm build/*.c build/*.elf

    echo -e "\e[1;32m ********************************* \e[0m"
    echo -e "\e[1;32m Done: ${application} \e[0m"
    echo -e "\e[1;32m ********************************* \e[0m"

done

python classification.py --rw --disassemblyfolder disassembly --outputfile report/$1/${application}_rw

python classification.py --instructions --classifier AUCD --disassemblyfolder  disassembly --outputfile report/$1/${application}_instr
