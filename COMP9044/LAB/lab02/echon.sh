#!/bin/bash
if test $# -ne 2
then 
	echo "Usage: $0 <number of lines> <string>"
	exit 1
elif ! test $1 -gt '0' && test $# = 2 
then
	echo "$0: argument 1 must be a non-negative integer"
        exit 1
else
	yes $2|head -n $1

fi
