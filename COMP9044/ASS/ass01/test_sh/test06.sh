#!/bin/sh
#ZANNNING WANG	z5224151

#This test mainly for test subset 0
#this test only test shrug-log
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

#test end
echo -en "\e[32mTESTS00 END\n"