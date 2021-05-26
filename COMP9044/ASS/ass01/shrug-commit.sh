#!/bin/dash
#z5224151	ZANNING WANG

#test the directory exist or not
if (! test -d ".shrug")
then
	echo "shrug-commit: Directiry .shrug does not exists!"
	exit 1
fi

#test the number of parameter
if test "$#" -eq 2
then 
	argument=`echo "$2"|egrep "^-+"`
	if (test "$1" = "-m") && (! test "$argument")
	then
		:
	else
		echo "Incorrect Input without \"-a\" option"
		exit 1
	fi
		#test the input with "-a"
elif test "$#" -eq 3
then
	argument=`echo "$3"|egrep "^-+"`
	if (test "$1" = "-a") && (test "$2" = "-m") && (! test "$argument")
	then
		:
	else
		echo "Incorrect Input with \"-a\" option"
		exit 1
	fi
		
else
	echo "Incorrect Input with too many (or less) argument!"
	exit 1
fi

cd ./.shrug/version      	#folder version
#check the exist commit in folder version
counter=0
while true
do
	if test -d "$counter"
	then
		counter=$(($counter+1))
	else

		mkdir "$counter"
		cd ./"$counter"
		echo "$2" > commit_log.txt
		cd ../../..		#back to the folder current			
		break
	fi
done
#bckup the file from the index to the right commit-version without "-a" option
if test "$#" -eq 2
then
	cd ./.shrug/index
	for file in `ls`
	do	
		backupfile=`echo "$file"|egrep -v "shrug-*"`
		if test "$backupfile"
		then 
			dir="../version/$counter"

			cp "$file" "$dir"
		fi
	done
	cd ../..		   #back to the folder current
	#check the files same as previous version
	cd ./.shrug/index
	check_file=`ls`
	cd ../..		   #back to folder current

	#bulid_flag to test same
	not_same_flag="same"
	if (test $counter -gt 0)
	then
		for file in $check_file
		do
			#check the exist of file in old version
			if test -f "./.shrug/version/$((counter-1))/$file"
			then	
				#test the file in index same as previos repo
				diff "./.shrug/index/$file" "./.shrug/version/$((counter-1))/$file" >/dev/null
				if (test "$?" -eq 0)
				then
					:
				else
					not_same_flag="different"
					break
				fi
			else
				not_same_flag="different"
			fi
		done
	else
		#change the flag when the first commit create
		not_same_flag="different"
	fi
	#if there is no changes, delete the backup in repo
	if (test "$not_same_flag" = "different")
	then
		echo "Committed as commit $counter"
	else
		rm -rf ./.shrug/version/$counter
		echo "nothing to commit"
	fi
fi

#backup the file to the right commit-version with "-a" option
if test "$#" -eq 3
then
	cd ./.shrug/index      		#folder index
	backupfile=`ls|egrep -v "shrug-*"`
	cd ../..       				#folder current
	#check the file content from their current dirctory
	for file in `echo "$backupfile"|xargs echo`		#current
	do
		if test -f "file"
		then
			cp -f "$file" "./.shrug/index"
		fi	
	done
#backup the file from the index to version
	cd ./.shrug/index
	for file in `ls`
	do
		backupfile=`echo "$file"|egrep -v "shrug-*"`
		if test "$backupfile"
		then 
			dir="../version/$counter"

			cp "$file" "$dir"
		fi
	done

	echo "Committed as commit $counter"
fi

