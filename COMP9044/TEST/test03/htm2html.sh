#!/bin/bash

for file in *.htm
do
	file_name=${file%.*}
	if test -e "$file_name".html
	then	
			echo "$file_name".html exists
			exit 1
	else
		mv "$file" "$file_name".html
		
	fi

done