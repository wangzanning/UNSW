#!/bin/dash

max=$1
min=$1

list1=$@
echo $list1 >temp.txt

for number in $@
do
	if test $number -gt $max
	then 
		max=$number
	fi

	if test $number -lt $min
	then 
		min=$number
	fi
done

min=$(($min+1))
while (test $min -lt $max)
do
	if ! (egrep "$min" temp.txt) > /dev/null
	then
		echo "$min" 
		exit 1

	
	fi	
	min=$(($min+1))

done
