#!/bin/dash
egrep '"name"' $1|
sed 's/.*name": "//'|
sed 's/", .*//'|sort|uniq
