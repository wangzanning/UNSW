#!/usr/bin/perl
#z5224151	ZANNING WANG

use warnings;

#get the word searched
$search_word = shift(@ARGV);
$search_word =~ tr/A-Z/a-z/;

#check file one by one
foreach $file (glob "lyrics/*.txt") {
	$total_word = 0;
	$counter = 0;
	
	#open the file to $in
	open my $in, "<", "$file" or die "$0: can't open file\n";
	
	while ($line = <$in>){
		#remove non-alphabetic characters seperate by " "
		$line =~ tr/A-Z/a-z/;
		$line =~ s/[^a-z]/ /g;
		@words = split(/\s+/, $line);

		#get the number of search_word
		foreach (@words){
			if ($_ eq $search_word){
				$counter++;
			}
		}

		#get the number of total word in this file
		foreach (@words){
			if (/^[a-zA-Z]+$/){
				$total_word++;
			}
		}
	}

	$frequency = log(($counter + 1)/$total_word);
	#get the right format of filename
	$file =~ s/lyrics\///g;
	$file =~ tr/_/ /;
	$file =~ s/.txt//g;
	#get the right format of counter,total_word, frequency.
	$counter = sprintf "%d", $counter;
	$total_word = sprintf "%6d", $total_word;
	$frequency = sprintf "%8.4f", $frequency;
	print("log (($counter+1)/$total_word) = $frequency $file\n");	
}


















