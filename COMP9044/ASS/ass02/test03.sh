#!/bin/bash
#ZANNING WANG	z5224151
#This test00 mainly test subset 0 and subset 1 ,2


counter=0
while true
do
	backup_dir=".snapshot.$counter"
	if test -d "$backup_dir"
	then 
		counter=$[$counter+1]	
	else
		break
	fi
done
