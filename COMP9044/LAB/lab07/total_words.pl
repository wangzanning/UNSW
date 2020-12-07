#!/usr/bin/perl
#z5224151	ZANNING WANG

use warnings;


while ($line = <STDIN>){
	#change non-alphabetic characters to " "
	$line =~ s/[^a-zA-Z]/ /g;
	#seperate words by " "
	@words = split(/\s+/, $line);
	
	foreach (@words){
		if (/^[a-zA-Z]+$/){
			$counter++;
		}
	}
}

print ("$counter words\n");