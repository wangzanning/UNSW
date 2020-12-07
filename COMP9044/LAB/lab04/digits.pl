#!/usr/bin/perl
#z5224151	ZANNING WANG
use warnings;

while ($input = <STDIN>) {
	$input =~ tr/012346789/<<<<<>>>>/;
	print "$input";
	}


