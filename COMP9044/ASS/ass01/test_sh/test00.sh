#!/bin/sh
#ZANNNING WANG	z5224151

#This test mainly for test subset 0
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

#test shrug-init
expected_output="Initialized empty shrug repository in .shrug"
my_output=`sh shrug-init`

if (test "$expected_output" = "$my_output") && (test -d ".shrug")
then
	echo -en "\e[32mshrug-init passed\n"
else
	echo -en "\e[31mshrug-init failed\n"
fi

#test execute shrug-init again
expected_output="shrug-init: error: .shrug already exists"
my_output=`sh shrug-init`

if test "$expected_output" = "$my_output"
then
	echo -en "\e[32mshrug-init passed(check error)\n"
else
	echo -en "\e[31mshrug-init failed(check error)\n"
fi	

#test shrug-add
#create a b, only add a
touch a b
echo line1a >>a
echo line1b >>b
sh shrug-add a

if (test -f "$index_path/a")
then 
	echo -en "\e[32mshrug-add passed\n"
else
	echo -en "\e[31mshrug-add failed\n"
fi

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

#test shrug-commit
expected_output="Committed as commit 0"
my_output=`sh shrug_commit -m first`
if (test "$expected_output" = "$my_output") && (test -d "./.shrug/version/0")
then
	echo -en "\e[32mshrug-commit passed\n"
else
	echo -en "\e[31mshrug-commit failed\n"
fi

#test shrug-commit
#too many arguments given
expected_output="Incorrect Input with too many (or less) argument!"
my_output=`sh shrug-commit -m first second third`
if test "$expected_output" = "$my_output"
then
	echo -en "\e[32mshrug-commit passed(check error)\n"
else
	echo -en "\e[31mshrug-commit failed(check error)\n"
fi

sh shrug-add b
#test shrug-commit
#input argument without "-m"
expected_output="Incorrect Input without \"-a\" option"
my_output=`sh shrug-commit m second`
if test "$expected_output" = "$my_output"
then
	echo -en "\e[32mshrug-commit passed(check error)\n"
else
	echo -en "\e[31mshrug-commit failed(check error)\n"
fi	

#test shrug-commit
#test if there isn't any changes
sh shrug-commit -m second
touch b
sh shrug-add b

expected_output="nothing to commit"
my_output=`sh shrug-commit -m third`
if test "$expected_output" = "$my_output"
then
	echo -en "\e[32mshrug-commit passed\n"
else
	echo -en "\e[31mshrug-commit failed\n"
fi	

#test shrug-log
rm -rf ./.shrug
sh shrug-init
sh shrug-add a
sh shrug-commit -m 'first'
expected_output="0 first"
my_output=`sh shrug-log`
if test "$expected_output" = "$my_output"
then
	echo -en "\e[32mshrug-log passed\n"
else
	echo -en "\e[31mshrug-log failed\n"
fi	

#test shrug-log
#too many argument input

expected_output="Incorrect Input with too many arguments"
my_output=`sh shrug-log`
if test "$expected_output" = "$my_output"
then
	echo -en "\e[32mshrug-log passed(check error)\n"
else
	echo -en "\e[31mshrug-log failed(check error)\n"
fi	

#test shrug-show
expected_output="line1a"
my_output=`sh shrug-show 0:a`
if test "$expected_output" = "$my_output"
then
	echo -en "\e[32mshrug-show passed\n"
else
	echo -en "\e[31mshrug-show failed\n"
fi

#test shrug-show
#file not exist
expected_output="shrug-show: error: 'not_exist' not found in index"
my_output=`sh shrug-show 0:not_exist`
if test "$expected_output" = "$my_output"
then
	echo -en "\e[32mshrug-show passed(check error)\n"
else
	echo -en "\e[31mshrug-show failed(check error)\n"
fi

#test shrug-show
#version not found
expected_output="shrug-show: error: unknown commit '4'"
my_output=`sh shrug-show 4:a`
if test "$expected_output" = "$my_output"
then
	echo -en "\e[32mshrug-show passed(check error)\n"
else
	echo -en "\e[31mshrug-show failed(check error)\n"
fi

#test shrug-show
#use ";" instead of ":"
expected_output="Incorrect Input with too many (or less) arguments"
my_output=`sh shrug-show 0;a`
if test "$expected_output" = "$my_output"
then
	echo -en "\e[32mshrug-show passed(check error)\n"
else
	echo -en "\e[31mshrug-show failed(check error)\n"
fi

#test shrug-show
#no input argument
expected_output="Incorrect Input with too many (or less) arguments"
my_output=`sh shrug-show`
if test "$expected_output" = "$my_output"
then
	echo -en "\e[32mshrug-show passed(check error)\n"
else
	echo -en "\e[31mshrug-show failed(check error)\n"
fi

#test end
echo -en "\e[32mTESTS00 END\n"
