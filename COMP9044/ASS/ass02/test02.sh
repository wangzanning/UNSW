#!/bin/bash
#ZANNING WANG	z5224151
#This test00 mainly test subset 0 and subset 1 ,2


if test $# -eq 3
then
	touch $3
	counter=$1

	while test  $counter -le $2
	do	
		echo $counter >> $3
		counter=$(($counter+1))
	done

else
	echo "Incorrect Input!"

fi