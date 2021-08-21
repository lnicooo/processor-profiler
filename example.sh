#!/bin/sh

# Check Installation supports this example
checkinstall.exe -p install.pkg --nobanner || exit


CROSS=RISCV32


if [[ -z "$APPLICATION_LIST" ]]; then
    APPLICATION_LIST=($(ls baremetal))
fi

mkdir -p build
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

    harness/harness.${IMPERAS_ARCH}.exe --program build/app.${CROSS}.elf --appdisassembly ${application}.out $*

    #awk -f funcs.awk app.out | sort -nk2 -r > ${application}.out

    #rm app.out
    rm build/*.c build/*.elf

    echo -e "\e[1;32m ********************************* \e[0m"
    echo -e "\e[1;32m Done: ${application} \e[0m"
    echo -e "\e[1;32m ********************************* \e[0m"
done
