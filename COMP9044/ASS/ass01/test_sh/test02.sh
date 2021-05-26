#!/bin/sh
#ZANNNING WANG	z5224151

#This test mainly for test subset 0
#this test only test shrug-add
#Attention others who may try this autotest need to change  
#the path according to their own design of repo
#some of error messages may vary from different designs

index_path="./.shrug/index"
repo_path="./.shrug/version"
#clean the exists .shrug
rm -rf .shrug >/dev/null

#the meaning of color show belows
#[33m----color yellow----show warnings
#[32m----color Green-----all good
#[31m----color Red-------something wrong
#[30m----color Black-----stdout
#test beigin
echo -en "\e[32mTESTS00 BEGIN\n"

#initial the ".shrug"
sh shrug-init

#test shrug-add 
#if the file not exists
expected_output="Incorrect Input with 'not_exist_file' not exists!"
my_output=`sh shrug-add not_exist_file`
if test "$expected_output" = "$my_output"
then 
	echo -en "\e[32mshrug-add passed(check error)\n"
else
	echo -en "\e[31mshrug-add failed(check error)\n"
fi

#test shrug-add
#the input argument with "-"
expected_output="Incorrect Input with \"-\""
my_output=`sh shrug-add -a`
if test "$expected_output" = "$my_output"
then
	echo -en "\e[32mshrug-add passed(check error)\n"
else
	echo -en "\e[31mshrug-add failed(check error)\n"
fi

#test shrug-add
#the inout argument with illegal filename
expected_output="Incorrect Input with '/a' name beyond [a-zA-Z0-9.-_]"
my_output=`sh shrug-add /a`
if test "$expected_output" = "$my_output"
then
	echo -en "\e[32mshrug-add passed(check error)\n"
else
	echo -en "\e[31mshrug-add failed(check error)\n"
fi


#test end
echo -en "\e[32mTESTS00 END\n"