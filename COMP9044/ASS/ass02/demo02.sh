#!/bin/bash
#ZANNING WANG	z5224151
#This demo mainly show the translation in subset 0, 1 and 2
#This demo need two names as arguements to run.

name1=$1
name2=$2

ls
for py_file in *.pl
do
	if test $py_file = HD.pl
	then 
		echo God, there is a assignment got HD \!
		if test $name1 = Rick
		then
			echo Of course not, Rick never do any homework \!
		elif test $name2 = Morty
		then
			echo Do not kidding, Do u think morty can get HD \?
		else
			echo Sorry, it is mine.
		fi
done
