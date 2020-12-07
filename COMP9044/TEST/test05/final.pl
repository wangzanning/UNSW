#!/usr/bin/perl

$line = "1,2,3,4,5";
print("$line\n");
@lines = split(/,/ ,$line);
print("@lines\n");
$line2 = join(",",@lines);
print("$line2\n");