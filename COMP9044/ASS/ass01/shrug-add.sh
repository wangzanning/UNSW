#!/bin/dash
#z5224151	ZANNING WANG

#check dir ".shrug" exists or not firstly
if (! test -d ".shrug")
then
	echo "shrug-add: Directiry .shrug does not exists!"
	exit 1
fi
#check the parameter start with "-"
for file in $@
do 
	parameter=`echo $file|egrep "^-+"`
	if test "$parameter"
	then
		echo "Incorrect Input with \"-\"!"
		exit 1 
	fi
done

#check the argument given exist or not
for file in $@
do
	if (! test -f "$file")
	then
		echo "Incorrect Input with '$file' not exists!"
		exit 1
	else
		#check the filename only contain alpha-numeric characters, plus '.', '-' and '_' characters.
		file_name=`echo $file|egrep -v "^[a-zA-Z0-9]+[.-_]*"`
		if test "$file_name"
		then 
			echo "Incorrect Input with '$file' name beyond [a-zA-Z0-9.-_]"
		fi
	fi
done

#copy the file into the index
for file in $@
do
	cp "$file" "./.shrug/index" 

done




























