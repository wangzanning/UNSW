#!/bin/dash
#z5224151	ZANNING WANG

#test the directory exist or not
if (! test -d ".shrug")
then
	echo "shrug-show: Directiry .shrug does not exists!"
	exit 1
fi

#check the arguments given and argument with ":"
argument=`echo $1|egrep ":"`
if (test "$#" -eq 1) && (test $argument)
then
	version=`echo "$1"|cut -d":" -f1`
	show_file=`echo "$1"|cut -d":" -f2`

#print the file from the folder index if the version not given
	if (! test "$version")
	then
		cd ./.shrug/index
		if test -f "$show_file"
		then
			cat "$show_file"
		else
			echo "file $show_file not exists"
			exit 1
		fi

	#print the file from folder version if the version given
	else 
		#check the version exists or not 
		if test -d "./.shrug/version/$version"
		then
			cd ./.shrug/version/"$version"         	#folder version
			#test show_file exists or not 
			if test -f "$show_file"
			then
				cat "$show_file"
			else
				echo "file $show_file not exists"
				exit 1
			fi
		fi
	fi
	

else
	echo "Incorrect Input with too many (or less) arguments"
	exit 1
fi





