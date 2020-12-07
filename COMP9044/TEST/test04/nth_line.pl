#!/usr/bin/perl
#z5224151	ZANNING WANG

use warnings;

if ($#ARGV == 1){
	$lineprint = shift @ARGV;
	open my $in, "<", "$ARGV[0]" or die "$0: can't open file\n";
	@lines = <$in>;
	$counter = @lines;
	
	if ($counter <= $lineprint-1) {
		print ("\n");
	}else{
		print $lines[$lineprint-1];
	}
	close $in;

} else{
	print ("Incorrect Input\n");
}
