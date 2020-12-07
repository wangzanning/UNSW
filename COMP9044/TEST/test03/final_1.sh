#!/bin/bash

for file in $@
do
	check_file=`egrep '^#include *"' $file|sed 's/" *$//;s/^.*"//'`
	#echo "$check_file"
	for file_h in $check_file
	do
		echo $file_h 23333
	done

done

