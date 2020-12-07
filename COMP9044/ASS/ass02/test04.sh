#!/bin/bash
#ZANNING WANG	z5224151
#This test00 mainly test subset 0 and subset 1 ,2


for pict in $@
do
	if test -e "$pict"
	then
		time_label=`ls -l "$pict"|awk '{print $6,$7,$8}'`
		convert -gravity south -pointsize 36 -draw "text 0,20  '$time_label'" $pict $pict

	else
		echo "Image not exist!"
		exit 1
	fi
done
