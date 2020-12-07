#!/usr/bin/perl
#z5224151	ZANNING WANG
use warnings;

$lineprint = 10;

#print from STDIN
if ($#ARGV == -1){
	@in = <STDIN>;
	$counter = @in;
	if ($counter <= $lineprint){
		print @in;
	}else{
		print @in[$counter-$lineprint..$counter-1];
	}
}

#get the parameter line to be print
if ($#ARGV > -1 && $ARGV[0] =~ /-[0-9]+/){
	$lineprint = shift @ARGV;
	#remove -
	$lineprint =~ s/-//;
}

if ($#ARGV > -1){
	#open the file one by one 
	foreach $file (@ARGV){
		open my $in, "<", "$file" or die "$0: can't open $file\n";
		#get the number of line for each file'in'
		@lines = <$in>;
		$counter = @lines;
		
		#more than one file to print
		if (@ARGV > 1){
				print "==> $file <==\n";
			}
		#use counter print last lines
		if ($counter <= $lineprint){
			print @lines;
		}else{
			print @lines[$counter-$lineprint..$counter-1];
		}
	}	
}


