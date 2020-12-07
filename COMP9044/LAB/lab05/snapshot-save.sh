#!/bin/dash
#z5224151	ZANNING WANG

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

mkdir "$backup_dir"

for file in `ls`
do
	if [[ "$file" != "snapshot-save.sh" ]]&&[[ "$file" != "snapshot-load.sh" ]]
	then	
		cp "$file" "./$backup_dir/$file"
	fi
done

echo "Creating snapshot $counter"

#there is a bug I do not konw why
#it does not work if i write below
#for file in `"ls|egrep -v "snapshot-save.sh|snapshot-load.sh"`
#therefore i should add one more line to check the file name
