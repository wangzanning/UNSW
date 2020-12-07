#!/bin/bash
#z5224151	ZANNING WANG

for file in $@
do
	counter=0
	while true
	do
		backup=".$file.$counter"
		if test -e $backup
		then 
			counter=$[$counter+1]	
			#same as: counter=`expr$counter+1`
		else
			cp "$file" "$backup"
			echo "Backup of '$file' saved as '$backup'"
			break
		fi
	done

done