#!/bin/dash
#z5224151	ZANNING WANG

sh snapshot-save.sh
cd ".snapshot.$1"
for file in `ls`
do
	if test -f "$file"
	then
		cp "$file" "../"

	else
		echo "Only copy files!"
	fi

done 
echo "Restoring snapshot $1"