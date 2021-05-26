#!/bin/dash
#z5224151	ZANNING WANG

#check dir ".shrug" exists or not firstly
if (! test -d ".shrug")
then
	echo "shrug-status: Directiry .shrug does not exists!"
	exit 1
fi

#check the first version exist or not
version=`head -n 1 "./.shrug/version"`
if (! test "$version")
then 
	echo "Directiry .shrug/version/0 does not exists!"
	exit 1

#test the argument input
if test "$#" -eq 0
then 
	:
else
	echo "Incorrect input!"
	exit 1

#create tmp_stdout to print
if (! test -f ./.tmp_stdout)
then touch .tmp_stdout
fi

#check the latest repo
counter=0
while true
do
	if test -d "./.shrug/version/$counter"
	then
		counter=$(($counter+1))
	else		
		break
	fi
done		

#build function check difference
different(){
	diff "$1" "$2" >/dev/null
	if (test "$?" -eq 0)
	then
		return 1
	else
		return " "
}

check_exist(){
 	#check the file exist in current
 	if test "$2" = "current"
 	then
 		if test -f "./$1"
 		then 
 			return 1
 		else
 			return " "
 	#check the file exist in index
 	elif test "$2" = "index"
 	then
 		if test -f "./.shrug/index/$1"
 		then
 			return 1
 		else
 			return " "
 	#check the file exist in repo
 	elif test "$2" = "repo"
 	then		
		#check the file from the latest repo
		if test -f "./.shrug/version/$counter"
		then
			return 1
		else 
			return " "
		fi
 	fi
 }
#different situations as below
#a - file changed, different changes staged for commit
#b - file changed, changes staged for commit
#c - file changed, changes not staged for commit
#d - file deleted
#e - deleted
#f - same as repo
#g - added to index
#h - untracked
#i - added to index, file changed
#j - added to index, file deleted

#check the status from the file in current
for file in `ls`
do
	#different file in diferent directory
	current_file=./$file
	index_file=./.shrug/index/$file
	repo_file=./.shrug/version/$counter/$file

	#file in current and index, not in repo
	if (test (check_exist "$file" current)) && (test (check_exist "$file" index)) && (! test (check_exist "$file" repo))
	then
		if (test (different current_file index_file))
		then
			#case g
			echo "$file - added to index" >>.tmp_stdout
		else
			#case i
			echo "$file - added to index, file changed" >>.tmp_stdout
		fi

	elif (test (check_exist "$file" current) && (! test (check_exist "$file" index)) && (! test (check_exist "$file" repo))
	then
		#case h
		echo "$file - untracked" >>.tmp_stdout

	#file exist in current, index and repo
	elif (test (check_exist "$file" current) && (test (check_exist "$file" index)) && (test (check_exist "$file" repo))
		#file all same in current, index and repo
		if (test (different current_file index_file)) && (test (different repo_file index_file)) && (test (different current_file repo_file))
		then
			#case f
			echo "$file - same as repo" >>.tmp_stdout
		#file in three folder all different 
		elif (! test (different current_file index_file)) && (! test (different current_file repo_file)) && (! test (different repo_file index_file))
		then
			#case a
			echo "$file - file changed, different changes staged for commit" >>.tmp_stdout
		#current same as index, different from version, index also different from repo
		elif (test (different current_file index_file)) && (! test (different current_file repo_file)) && (! test (different repo_file index_file))
			#case b
			echo "$file - file changed, changes staged for commit" >>.tmp_stdout
		#current different from index and repo; index same as repo
		elif (test (different current_file index_file)) && (! test (different current_file repo_file)) && (! test (different repo_file index_file))
			#case c
			echo "$file - file changed, changes not staged for commit" >>.tmp_stdout
		fi
	fi

done

#get the file deleted
cd ./.shrug/delete_files     		#folder index
delete_file=`ls`
cd ../.. 							#folder current

for file in `echo "$delete_file"|xargs echo`
do
	current_file=./$file
	index_file=./.shrug/index/$file
	repo_file=./.shrug/version/$counter/$file

	#exist in index and repo, delete from current 
	if (! test (check_exist "$file" current)) && (test (check_exist "$file" index)) && (test (check_exist "$file" repo))
	then
		#file in repo same as index
		if (test (different repo_file index_file))
		then 
			#case d
			echo "$file - file deleted" >>.tmp_stdout
	#exist in version only
	elif (! test (check_exist "$file" current)) && (! test (check_exist "$file" index)) && ( test (check_exist "$file" repo))
	then 
		#case e
		echo "$file - deleted" >>.tmp_stdout
	#exist in index only
	elif (! test (check_exist "$file" current)) && (test (check_exist "$file" index)) && (! test (check_exist "$file" repo))
	then
		#case j
		echo "$file - added to index, file deleted" >>.tmp_stdout
	fi
done	

#print the .tmp_stdout
cat .tmp_stdout|sort
rm .tmp_stdout



