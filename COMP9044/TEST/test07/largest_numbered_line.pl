#!/usr/bin/perl
#ZANNING WANG z5224151

use warnings;

my %content = ();
#$counter = 0;
$flag= 0;

while ($line = <STDIN>){
	$file_unchanged = $line;
	$line =~ s/[^0-9]/ /g;
	$line =~ s/\s+/ /g;
	$line =~ s/^\s+//g;
	$line =~ s/\s+$//g;
	my @list = split(/\s+/,$line);
	
	if ($line){
		$largest = (sort {$b <=> $a} @list)[0];
		push @largest_list, $largest;
		$content{$largest} = $file_unchanged;
		$flag =1;
	}
}
if ($flag == 1){
	$largest_num = (sort {$b <=> $a} @largest_list)[0];
	print "$content{$largest_num}";
}

