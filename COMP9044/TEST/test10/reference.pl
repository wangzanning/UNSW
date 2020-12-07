#!/usr/bin/perl

@lines = <STDIN>;
foreach $line(@lines){
	if ($line =~ /^#(\d+)/){
		$line_refer = $1 - 1;
		print("$lines[$line_refer]");

	}else{
		print("$line");
	}
}

