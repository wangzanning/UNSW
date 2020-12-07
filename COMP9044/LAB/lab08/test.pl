#!/usr/bin/perl -w

$code = $ARGV[0];

# open url
$url = "http://www.timetable.unsw.edu.au/current/".$code."KENS.html";
open F, "wget -q -O- $url|" or die;
while ($line = <F>) {
	
	if ($line =~ /<td class="data"><a href="($code[0-9]{4}).html">$code[0-9]{4}<\/a><\/td>/) {
		print $line =~ /<td class="data"><a href="($code[0-9]{4}).html">$code[0-9]{4}<\/a><\/td>/;
		print "\n";
	}
	
}
