#!/bin/sh

#打印第二列
awk '{print$2}'

#去掉文件名后缀
file_name=${file%.*}

#cut
cut -d’|’ -f1-3 data
cut -f1,4 data

#paste
cut -f1 data > data1
cut -f2 data > data2
cut -f3 data > data3
paste data1 data2 data3 > newdata

#sort
-r sort in descending order (reverse sort)
-n sort numerically rather than lexicographically
-d dictionary order: ignore non-letters and non-digits
-kn sort on column n    #对第几列排序
sort -nr -k3 data

#uniq
-c also print number of times each line is duplicated
-d only print (one copy of) duplicated lines
-u only print lines that occur uniquely (once only)

#xargs
for h in `echo "$h_file"|xargs echo`      
h_file 中包含一行参数，以空格间隔
（-d '字符'设置分割参数)（-n ‘数字’设置一次传入几个）逐个传递给所需for循环中

#sed
sed -n '1,1p'
sed -n -e ’1,10p’ < file

#find
find /home/jas/web -name ’*.html’ -print

• Horizontal slicing - select subset of lines:
cat, head, tail, *grep, sed, uniq
• Vertical slicing - select subset of columns: cut, sed
• Substitution: tr, sed
• Aggregation, simple statistics: wc, uniq
• Assembly - combining data sources: paste, join
• Reordering: sort
• Viewing (always end of pipeline): more, less
• File system filter: find
• Programmable filters: sed, (and perl)

#regexpr
egrep -i '<(p|br)( [^>]*)*>' /tmp/index.html
[1-9][0-9]*\.[0-9]+
egrep -v .
egrep '^$'
egrep '\b129\.94\.172\.([1-9]|1[0-9]|2[0-5])\b' ips.txt

#i++操作
i=`expr $i + $increment`
a=$(($a+1))

#循环
for (( i = first; i <= last; i += increment ))

#
if egrep -iw '</?blink>' $file >/dev/null

#重命名操作
mv "$file" "$file.bad"

#匹配后替换
egrep '^#include' "$file" | sed 's/[">][^">]*$//' 

#切割后进行转化
cut -d':' -f1,2 /etc/passwd | tr ':' '\t'

#删除尾缀
f1=`echo $f | sed -e 's/\.gz//'`

#多次替换，保存到临时文件，再重命名
sed 's/COMP2041/COMP2042/g;s/COMP9044/COMP9042/g' $file >$temporary_file && mv $temporary_file $file

#筛选输入文件，格式为f
for file in `find "$@" -type f`

#利用find查找
find . -name "*.jpg"
find . -regex "\./*[0-9]+\.png" 
find . -type f
find . -type f -size +100M 

#利用 -a 并列多个条件
if test $current_hour -ge 9 -a $current_hour -lt 17 

#筛选uniq -c后不是1的行
grep -v '^ *1 ' removes such lines, leaving only IDs that occur multiple times

#传入read line
wget -q -O- 'https://en.wikipedia.org/wiki/Triple_J_Hottest_100?action=raw'|
while read line



