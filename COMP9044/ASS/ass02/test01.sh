#!/bin/bash
#ZANNING WANG	z5224151
#This test00 mainly test subset 0 and subset 1 ,2


for file in $@
do
	h_file=`egrep '".+.h"' "$file"|cut -d'"' -f2|xargs`
	

	for h in `echo "$h_file"|xargs echo`
	do
		if [ ! -e "$h" ]
		then
			echo "$h" included into "$file" does not exist
		fi

	done

done