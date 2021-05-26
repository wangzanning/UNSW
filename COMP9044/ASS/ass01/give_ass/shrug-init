#!/bin/dash
#z5224151	ZANNING WANG

#check the argument given
if test $# -eq 0
then
	#check .shrug exist or not
	if (! test -d ".shrug")
	then
		mkdir ".shrug"
		cd "./.shrug"

		mkdir "index"
		mkdir "version"
		mkdir "delete_files"

		echo "Initialized empty shrug repository in .shrug"
	else
		echo "shrug-init: error: .shrug already exists"
		exit 1
	fi
else
	echo "Incorrect Input!"
	exit 1
fi