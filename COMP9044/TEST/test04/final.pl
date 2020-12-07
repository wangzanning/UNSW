#!/usr/bin/perl

$first = $ARGV[0];
$end = $ARGV[1];
$file_name = $ARGV[2];

open $out ,'>', $file_name or die;
while ($first <= $end) {
	print $out ("$first\n");
	$first++; 
}
close $out;

open $in ,"<", $file_name or die

@lines = <$in>;
$counter = @lines;


foreach $line(@lines)


