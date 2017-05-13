gcc shellcode.S -c -o shellcode.o -m32 -g -std=c99 -Wall -Werror -D_GNU_SOURCE -fno-stack-protector
objcopy -S -O binary -j .text shellcode.o shellcode.bin
