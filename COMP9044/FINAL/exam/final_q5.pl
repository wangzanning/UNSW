#!/usr/bin/perl

@output=();
while($line = <STDIN>){
	if ($line =~ /\d+/){
		my @numbers = $line =~ /(\d+)/g;
		print("@numbers\n");
	}
	
	$counter = @numbers - 1;
	$first = $numbers[0];
	$last = $#numbers;
	#print("$first\n");
	#print("$last\n");

	$line =~ s/\Q$first\E/$last/;
	$line =~ s/\Q$last\E/$first/;
	print("$line\n");
}



