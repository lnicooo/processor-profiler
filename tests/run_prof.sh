#!/bin/sh

# Check Installation supports this example
checkinstall.exe -p install.pkg --nobanner || exit

CROSS=RISCV32

cd baremetal

application=$1

mkdir -p build

cp ${application}/app.c build/.

cp Makefile build/.

echo -e "\e[1;32m ********************************* \e[0m"
echo -e "\e[1;32m Running: ${application} \e[0m"
echo -e "\e[1;32m ********************************* \e[0m"

make -C build

cd ..

harness.exe \
    --modulefile module/model.${IMPERAS_SHRSUF}\
    --program baremetal/build/app.${CROSS}.elf


echo -e "\e[1;32m ********************************* \e[0m"
echo -e "\e[1;32m Done: ${application} \e[0m"
echo -e "\e[1;32m ********************************* \e[0m"

rm baremetal/build/*.elf
