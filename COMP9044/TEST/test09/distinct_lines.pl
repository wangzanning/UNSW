#!/usr/bin/perl
#ZANNING WANG	z5224151

$number = shift(@ARGV);
$counter = 0;
$counter_total = 0;

while($line = <STDIN>){
	$line = lc($line);
	$line =~ s/\s+/ /g;
	$line =~ s/^\s+//g;
	$line =~ s/\s+$//g;
	$counter_total++;
	
	if( ! grep /^$line$/, @list ){
		push @list, $line;
    	$counter++;
	}

		
	if ($counter eq $number){
		print("$number distinct lines seen after $counter_total lines read.\n");
		exit 1
	}

}
print ("End of input reached after $counter_total lines read - $number different lines not seen.\n");