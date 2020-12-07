#!/usr/bin/perl
#z5224151	ZANNING WANG

use warnings;

while ($input = <STDIN>) {
	my @arr = split(/\s+/,$input);
	my @sorted = sort (@arr);
	my $output = join(" ",@sorted);

	print "$output\n";


}