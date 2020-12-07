#!/usr/bin/perl


$species = $ARGV[0];
$filename = $ARGV[1];
%dict=();
$total = 0;
open my $in ,"<", "$filename" or die;
while ($line = <$in>) {
	if ($line =~ m/\Q$species\E/){
		if ($line =~ m/"how_many": (\d+)/){
			$count = $1;
		}
		if ($line =~ m/"species": "(.*)"/){
			$name = $1;
		}
		$total = $total + $count;


	}

}
print("$total\n");