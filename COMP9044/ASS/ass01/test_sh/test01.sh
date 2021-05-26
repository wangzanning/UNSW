#!/bin/sh
#ZANNNING WANG	z5224151

#This test mainly for test subset 0
#this test only test shrug-init
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

#test end
echo -en "\e[32mTESTS00 END\n"