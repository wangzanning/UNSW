#!/bin/bash
#ZANNING WANG	z5224151
#This demo mainly show the translation in subset 0, 1, and 2

for language in python perl C java
do
	echo I like $language
	echo Good Good Study, Day Day up!
done

for number in 1 2 3
do 
	if test $number = 1
	then 
		echo The number is one!
	elif test $number = 2
	then
		echo Of course the number is two.
	else
		echo Only three left.
done
exit 1



