#!/bin/bash
#ZANNING WANG	z5224151
#This demo mainly show the translation in subset 0, 1 ,2 and 3.
#This demo need two number as arguements to run, first number need to no more than 100.

first_number=$1
second_number=$2

if test $first_number -lt $second_number
then 
	echo "first number is larger"
elif test $first_number -gt $second_number
then
	echo 'second number is larger'
else
	echo "they are equal"
fi

while test $first -lt 100
do
	echo $first
	first_number=$((second_number + 1))
done