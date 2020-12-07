#!/usr/bin/perl
#z5224151	ZANNING WANG

use warnings;

open my $input, "<", $ARGV[0] or die "open failed $!";
@lines = <$input>;

foreach $input (@lines){
	$input =~ tr/0123456789/##########/;
}

open my $output, ">", $ARGV[0] or die "open failed $!";
print $output @lines;

close "$input";
close "$output";