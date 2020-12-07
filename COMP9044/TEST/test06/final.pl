#!/usr/bin/perl
#ZANNING WANG z5224151

use warnings;
$repeat_times = shift(@ARGV);
#my %content = ();
while (my $input = <STDIN>){
	$input = lc($input);
	$content{$input}++;

	if ($content{$input} == $repeat_times){
		print "Snap: $input";
		last

	}

}


