#!/usr/bin/perl
#z5224151	ZANNING WANG

use warnings;

$search_word = shift(@ARGV);
$search_word =~ s/A-Z/a-z/g;
$counter = 0;

while ($line = <STDIN>){
	$line =~ tr/A-Z/a-z/;
	$line =~ s/[^a-z]/ /g;
	@words = split(/\s+/, $line);

	foreach (@words){
		if ($_ eq $search_word){
			$counter++;
		}
	}
}

print("$search_word occurred $counter times\n")

