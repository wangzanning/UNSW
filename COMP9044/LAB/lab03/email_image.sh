#!/bin/bash

for pict in $@
do
	if test -e "$pict"
	then
		display "$pict" 2>/dev/null
		read -p "Address to e-mail this image to?" mail_address	
		read -p "Message to accompany image?" message
		echo "$message"|mutt -s "$pict" -e 'set copy=no' -a "$pict" -- "$mail_address"
		echo "$pict" sent to "$mail_address"
	else
		echo "Image not exist!"
		exit 1
	fi

done
