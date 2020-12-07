#!/bin/bash
#ZANNING WANG	z5224151

if (test "$#" != 2)
then 
	echo "Error!"
	exit 1
fi

dir1=$1
dir2=$2

ls "$dir1"|sort|
while read file1
do	

	ls "$dir2"|sort|
	while read file2
	do
		
		if (test "$file1" = "$file2")
		then

			diff "$dir1/$file1" "$dir2/$file2">/dev/null
			if (test "$?" -eq 0)
			then
				echo "$file1"
			fi
		fi

	done
done


