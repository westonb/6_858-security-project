cd ../../../pcb
make clean
make CFLAGS="-g -O2 -Wall -Wdeclaration-after-statement -fno-stack-protector -U _FORTIFY_SOURCE -z execstack -no-pie"
execstack -s ./pcb