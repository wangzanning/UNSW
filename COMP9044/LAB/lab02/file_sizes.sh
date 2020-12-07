#!/bin/bash
list_small='Small files:'
list_medi='Medium-sized files:'
list_larg='Large files:'

for file in *
do 
	counter=`wc -l $file|awk '{print $1}'`
	
	if test $counter -lt 10
		then
			list_small+="$file "
	elif test $counter -lt 100
		then
			list_medi+="$file "
	else 
			list_larg+="$file "
	fi
done

echo $list_small
echo $list_medi
echo $list_larg
