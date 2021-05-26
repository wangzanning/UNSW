#!/bin/dash
#z5224151	ZANNING WANG

#test the directory exist or not
if (! test -d ".shrug")
then
	echo "shrug-log: Directiry .shrug does not exists!"
	exit 1
fi

#check the number of argument
if (! test "$#" -eq 0)
then
	echo "Incorrect Input with too many arguments"
	exit 1
fi

#get the commit for each version
cd ./.shrug/version 				#folder version

for dire in `ls`
do
	if test -d "$dire"
	then
		cd ./"$dire"   				#folder 0 1 2 3...
		
		log=`cat "commit_log.txt"`
		echo "$dire $log"
		cd .. 						#back to folder version

	fi
done






