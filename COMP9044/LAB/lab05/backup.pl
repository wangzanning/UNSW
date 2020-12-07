#!/usr/bin/perl
#z5224151	ZANNING WANG

use warnings;

foreach $file(@ARGV){
	$counter = 0;
	open my $in, "<", "$file" or die "$0: can't open $file\n";
	@lines = <$in>;


	while (1){
		$backup = ".$file.$counter";
		if (-e $backup) {
			$counter++;
		}else{
			open my $out, ">", "$backup" or die "$0 can't open $backup\n";
			print $out @lines;
			print "Backup of '$file' saved as '$backup'\n";
			close $out;
			last;
		}
	}


}



