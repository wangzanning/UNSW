#!/bin/bash
#ZANNING WANG	z5224151

filename=$1;
cat $filename|while read line
do
	echo $line|tr -d "[]"|cut -d":" -f2|cut -d"," -f1|tr -d '"'|
	tr -d "\n"|sed 's/^[ ]*//g'>>temp.txt
done

cat temp.txt|sort|uniq
rm temp.txt
