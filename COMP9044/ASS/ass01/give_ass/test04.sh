#!/bin/sh
#ZANNNING WANG	z5224151

#This test mainly for test subset 0
#this test only test shrug-commit
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
sh shrug-commit -m third
expected_output="nothing to commit"
my_output=`sh shrug-commit -m fourth`
if test "$expected_output" = "$my_output"
then
	echo -en "\e[32mshrug-commit passed\n"
else
	echo -en "\e[31mshrug-commit failed\n"
fi	

#test end
echo -en "\e[32mTESTS00 END\n"