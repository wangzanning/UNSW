#!/bin/dash

egrep "COMP[29]041" enrollments.txt |
cut -d"|" -f3|
cut -d"," -f2|
cut -d" " -f2|
sort|uniq -c|sort -nr|
head -1|awk '{print$2}'