#!/usr/bin/perl
#ZANNING WANG z5224151

use warnings;

my %content = ();
$file = shift(@ARGV);
$counter = 0;

open my $in, "<", "$file" or die "$0: can't open file\n";
while ($line = <$in>){
	
	$content{$counter} = $line;
	$counter++;
}

$check = $counter % 2;
if ($counter > 0){
	if ($check == 1){
		$print = ($counter +1)/2;
		print("$content{$print-1}");

	}else{
		$print = $counter/2;
		print("$content{($print-1)}");
		print("$content{$print}");
		}

}