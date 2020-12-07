#!/usr/bin/perl
#z5224151	ZANNING WANG

if ($#ARGV != 1)
	{
		print "Usage: $0 <number of lines> <string>\n";

	}else{
		if ($ARGV[0] > 0){		
			print(($ARGV[1]."\n") x $ARGV[0]);
		}elsif($ARGV[0] =~ /0/){
			print();
		}
			#use x to print n times input
		else{
			print "$0: argument 1 must be a non-negative integer\n";
		}
	}
	
