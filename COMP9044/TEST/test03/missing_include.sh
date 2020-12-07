#!/bin/bash

for file in "$@"
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