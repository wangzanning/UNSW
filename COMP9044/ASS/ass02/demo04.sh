#!/bin/bash
#ZANNING WANG	z5224151
#This demo mainly show the translation in subset 0, 1 ,2 ,3 and 4.
#This demo need two number as arguements to run.

compare_number() {
	local a b
	a=$1
	b=$2
	if test $a -lt $b
	then 
		return 1
	else
		return 0
	fi
}

result=compare_number(a, b)
if test $result -eq 1
	echo Yes
else
	echo no