#!/usr/bin/perl
#ZANNING WANG	z5224151

#use warnings;
use LWP::Simple;
$url = "http://www.timetable.unsw.edu.au/current/$ARGV[0]KENS.html";
$web_page = get($url) or die "Unable to get $url";

if (! $ARGV[0]){
	die "incorrect input\n";
}

@lines = split "\n", $web_page;
my %count;
my @uniq_lines = grep { ++$count{ $_ } < 2; } @lines;
my @sortted_lines = sort @uniq_lines;

#save in file temp.txt
#open my $myfile, ">","temp.txt" or die '1111111';
#print $myfile $web_page;

#open my $in, "<", "temp.txt" or die "$0: can't open file\n";

#print $web_page;
#<td class="data"><a href="COMP9434.html">COMP9434</a></td>
#<td class="data"><a href="COMP9434.html">Robotic Software Architecture</a></td>


$code = shift(@ARGV);

foreach $line (@sortted_lines){
	 if ($line =~ m/<td class=\"data\"><a href=\"$code\d{4}\.html\">.*<\/a><\/td>$/){
	 	#print ("$line\n");
		#remove unnecessery output
		if ($line !~ /<td class="data"><a href="($code\d{4})\.html">($code\d{4})<\/a><\/td>/){
		$line =~ s/<td class="data">//;
		$line =~ s/<\/a><\/td>//;
		$line =~ s/<a href="//;
		$line =~ s/.html">/ /;
		$line =~ s/^\s+//;
		print ("$line\n");
		}
		
	 }

}
