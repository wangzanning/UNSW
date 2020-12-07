#!/usr/bin/perl
#ZANNING WANG z5224151

use warnings;
$flag = 0;
@output = ();

foreach $argue(@ARGV){
	if ($argue =~/[aeiou]{3}/i){
		push @output, $argue;
		$flag = 1;
	}
}
if ($flag == 0){
	print (" \n");
}else{
	print "@output\n";
}

