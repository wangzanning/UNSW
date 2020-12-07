#!/usr/bin/perl
#ZANNING WANG z5224151
use warnings;

@output = ();
push @output, $ARGV[0];
shift;
foreach $word(@ARGV){
	$counter = 0;
	foreach $check(@output){
		if ($check eq $word){
			$counter++;
		}
	}
	if ($counter == 0){
		push @output, $word;
	}	

}

print "@output\n";

