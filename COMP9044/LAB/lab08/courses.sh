#!/bin/sh
#ZANNING WANG    z5224151
#<td class="data"><a href="COMP9434.html">COMP9434</a></td>


#<td class="data"><a href="COMP9434.html">Robotic Software Architecture</a></td>
code="$1"
website="http://www.timetable.unsw.edu.au/current/$1KENS.html"
echo $(wget -q -O- $website) >temp2.txt


#get the content of webiste
output=`wget -q -O- $website|egrep "$code[0-9]{4}.html\">[\(In\-\)]*[a-zA-Z]+[ |\-|, |/|$]+"`
echo $output >temp2.txt

#remove the redundant files
sed 's/<td class="data"><a href="//g' temp2.txt >temp3.txt
sed 's/.html">/ /g' temp3.txt>temp4.txt
#\n does not work properly in sed, only in tr
output=`sed "s/<\/a><\/td>/|/g" temp4.txt`
echo $output|tr '|' '\n'|sed 's/^ //g'|sed -e '$d'|sort -u
#rmmove the temp files
rm temp2.txt temp3.txt temp4.txt

