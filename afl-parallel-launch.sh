#!/bin/bash

#script to spin up x instances of AFL-fuzz on a false X11 session 

#setup x11 session
if [ $# -ne 4 ]; then
	echo "Usage: IN_DIR SYNC_DIR BINARY NUM_CORES"
	exit 1
fi
Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./10.log -config ./xorg.conf :99
export DISPLAY=:99

#launch sessions
COUNT=$4
IN_DIR=$1
OUT_DIR=$2
EXEC=$3

echo Launching $COUNT fuzzer instances
afl-fuzz -m 1000 -i $IN_DIR -o $OUT_DIR -M fuzzer_0 $EXEC @@ &

for ((i=1;i<=(COUNT-1);i++))
do 
afl-fuzz -m 1000 -i $IN_DIR -o $OUT_DIR -S fuzzer_$i $EXEC @@ &
done