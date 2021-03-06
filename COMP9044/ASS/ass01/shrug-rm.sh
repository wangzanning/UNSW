#!/bin/dash
#z5224151	ZANNING	WANG

#test the directory exist or not
if (! test -d ".shrug")
then
	echo "shrug-rm: Directiry .shrug does not exists!"
	exit 1
fi

#test the argument with "--cached" or "--force"

with_force="no"
with_cached="no"
for argument in "$@"
do
	#test "--force" in argument
	if test "$argument" = "--force"
	then
		with_force="yes"
		shift 
		continue
	fi
	#test "--cached" in argument
	if test "$argument" = "--cached"
	then
		with_cached="yes"
		shift
		continue
	fi
	#test the file name input
	filename=`echo "$argument"|egrep "^-+"`
	if test "$filename"
	then
		echo "Incorrect Input with '$filename'"
		exit 1
done

#rm the file from the index and the current
for file in "$@"
do
	#rm file without force and cached
	if (test "$with_cached" = "no") && (test "$with_force" = "no")
	then
		#test file exist in index and current
		if (test -f "./.shrug/index/$file") && (test -f "$file")
		then 
			diff "./.shrug/index/$file" "$file" >/dev/null
			#check the file content same or not 
			if (test "$?" -eq 0)
			then
				#backup delete_files
				cp -f "$file" "./.shrug/delete_files" 
				rm -f "./.shrug/index/$file" "$file"
				echo "rm '$file'"
			else
				echo "Error_1!"
				exit 1
			fi
		else
			echo "fatal: pathspec '$file' did not match any files"
			exit 1
		fi

	#rm file with cached and without force
	elif (test "$with_cached" = "yes") && (test "with_force" = "no")
	then
		#test exist in index
		if test -f "./.shrug/index/$file"
		then
			cp -f "./.shrug/index/$file" "./.shrug/delete_files" 
			rm "./.shrug/index/$file"
			echo "rm '$file'"
		else
			echo "fatal: pathspec '$file' did not match any files"
			exit 1
		fi

	#rm file without cached and with force 
	elif (test "$with_cached" = "no") && (test "with_force" = "yes")
	then
		#test exist in index or current
		if (test -f "./.shrug/index/$file") || (test -f "$file")
		then
			cp -f "./.shrug/index/$file" "./.shrug/delete_files"
			rm "./.shrug/index/$file" "$file" >/dev/null
			echo "rm '$file'"
		else
			echo "fatal: pathspec '$file' did not match any files"
			exit 1
		fi

	#rm file with cached and with force
	elif (test "$with_cached" = "yes") && (test "with_force" = "yes")
	then
		#test exist in index
		if test -f "./.shrug/index/$file"
		then 
			cp -f "./.shrug/index/$file" "./.shrug/delete_files" 
			rm "./.shrug/index/$file"
			echo "rm '$file'"
		else
			echo "fatal: pathspec '$file' did not match any files"
			exit 1
		fi

	fi
done

