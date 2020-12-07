#!/bin/bash
#ZANNING WANG	z5224151
#This demo mainly show the translation in subset 0, 1 and 2
#this demo need one language as a arguement to run.

language_1=PHP
language_2=JAVA
language_3=Python
language_4=Perl

if test $language_1 = "the best language in the world"
then
	echo Definitely, PHP is the best language!
else
	echo I do not think so!
	exit 1
fi

echo what is your favorite language for cs
if test $1
then 
	echo Ummmmm, I think is $1.
	if test $1 = $language_2
	then
		echo Yeah, JAVA is awesome!
	elif test $1 = $language_3
	then 
		echo I like pyhton, too.
	else
		echo This homework was written in Perl.
	fi
else
	echo I do not want to tell you, bro.
fi




