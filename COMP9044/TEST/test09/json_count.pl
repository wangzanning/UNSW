#!/usr/bin/perl
#ZANNING WANG	z5224151
#use warnings;

$species = $ARGV[0];
$filename = $ARGV[1];
%dict=();

open my $in ,"<", "$filename" or die;
while ($line = <$in> ) {
	$line =~ s/\s+//;
	$line =~ s/,//;
	print("$line\n");




}




while ($line = <$in> ) {
	$line =~ s/\s+//;
	if ($line =~ m/"how_many": (\d+)/){
		$count = $1;
	}
	if ($line =~ m/"species": "(.*)"/){
		$name = $1;
	}
	if ($dict{$name}){	
		$total = $dict{$name};
		$total = $total + $count;
		$dict{$name} = $total;
		#print("$name\n");

	}else{
		$dict{$name} = $count;
		#print("$name\n");

	}
	#print ("$name\n");
	#print ("$line\n");
}
$output = $dict{$species};
$output = $output/3;

print("$output\n");