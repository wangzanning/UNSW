#!/usr/bin/perl

%count = ();
@output = ();
foreach $arg(@ARGV){
	$count{$arg}++;
	if ($count{$arg} == 1) {
		push @output, $arg;
	}
}

print("@output\n");