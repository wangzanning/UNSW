#!/bin/bash

for file in *.jpg
do
	filename=${file%.*}
	if test -e "$filename".png
	then
		echo "$filename".png already exists >&2
		exit 1
	else
		convert "$file" "$filename".png
		rm "$file"
		
	fi
done