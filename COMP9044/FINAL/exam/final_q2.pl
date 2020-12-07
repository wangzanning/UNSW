#!/usr/bin/perl


while ($line = <STDIN>){
	if ($line =~ m/\|(\d+)\|\w/){
		$number = $1;
		#print("$number\n");
	}
	if ($line =~ m/(\|.+, .*\s+\|)/){
		$name = $1;
		$name =~ s/\|\d+\|//;
		$name =~ s/\s+\|//;
		$name =~ s/.*, //;
		$name =~ s/\s.+//;
		$name =~ s/\d+//;
		#print("$name\n");
	}
 
	#print("$number\n");
	$dict{$number} = $name;
}

foreach $a (sort keys %dict){
	$output = $dict{$a};
 	push @names, $output;
}
@name_sort = sort(@names);
foreach $out(@name_sort){
	print("$out\n");
}



# @lines = <STDIN>;
#print("@lines\n");