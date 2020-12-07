#!/usr/bin/perl
#ZANNING WANG z5224151

use warnings;
$repeat_times = shift(@ARGV);
my %content = ();
my $flag = 0;
while (my $input = <STDIN>){
	$content{$input}++;

	if ($content{$input} == $repeat_times){
		print "Snap: $input";
		$flag =1;

	}
	if ($flag == 1){
		last;
	}

}


