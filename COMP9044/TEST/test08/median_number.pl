#!/usr/bin/perl
#ZANNING WANG	z5224151

use warnings;

my @sort_argv = sort{$b<=>$a}(@ARGV);

my $counter = @sort_argv;

my $print_line = ($counter + 1)/2;

print("$sort_argv[$print_line]\n");

#print ("$counter\n");
