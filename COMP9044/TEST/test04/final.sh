#!/bin/dash

start=$1
end=$2
file_name=$3
touch $file_name

while test $start -le $end
do

	echo $start >> "$file_name"
	start=$((start+1))


done
