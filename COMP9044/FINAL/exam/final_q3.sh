#!/bin/dash

sort -k2|
cut -d'|' -f2|
uniq -c|
egrep "^\s*2"|
awk '{print$2}'|sort