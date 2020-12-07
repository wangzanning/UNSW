#!/usr//bin/perl
#z5224151	ZANNING WANG

use warnings;

if ($#ARGV == 2){

	open (F, '>', $ARGV[2]);
	for (my $i = $ARGV[0]; $i < $ARGV[1]+1; $i++) {
		print F ("$i\n");
	}
	close F;
}else{
	print ("Incorrect Input!\n");
}