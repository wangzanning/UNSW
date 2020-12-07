#!/bin/bash
egrep "COMP[29]041" enrollments.txt|cut -d'|' -f3|cut -d',' -f2|awk '{print $1}'|sort -r|uniq -c|sort -r|sed -n '1,1p'|awk '{print$2}'