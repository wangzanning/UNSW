#!/bin/sh
#ZANNNING WANG	z5224151

#This test mainly for test subset 0
#this test only test shrug-show
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
echo line1 >a
sh shrug-add a
sh shrug-commit -m first


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

#test end
echo -en "\e[32mTESTS00 END\n"