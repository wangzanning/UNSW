#!/bin/bash
#z5224151	ZANNING WANG

if test $# -eq 3
then
	touch $3
	counter=$1

	while test $counter -le $2
	do	
		echo $counter >> $3
		counter=$(($counter+1))
	done

else
	echo "Incorrect Input!"

fi