#!/usr/bin/perl

@output = ();
while($line = <STDIN>){
	if ($line =~ /\d+/){
		
		my @numbers = $line =~ /(\d+\.?\d*)/g;
		#print("@numbers\n");
		foreach $number(@numbers){
			$number_round = sprintf "%.0f", $number;
			#print("$number_round\n");
			$line =~ s/\Q$number\E/$number_round/;
		}
	}

	push @output,$line;
}
print("@output\n");