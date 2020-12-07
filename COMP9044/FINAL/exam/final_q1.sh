#!/bin/dash

sort -k2|
cut -d'|' -f2-3|
uniq|cut -d'|' -f2|
cut -d',' -f2|
sed 's/^ //'|
cut -d' ' -f1


 
