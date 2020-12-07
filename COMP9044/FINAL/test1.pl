#!/usr/bin/perl


use warnings;

while (<>) {
	($word1,$word2) = split;
	print("$word2\n");
	print ("$word1\n");

	$word1 .= $word2;
	print("$word1\n");

}