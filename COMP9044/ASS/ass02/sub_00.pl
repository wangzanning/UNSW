#!/usr/bin/perl
#ZANNING WANG 	z5224151

if ($#ARGV eq 0){
	$file = shift (@ARGV);
	open my $in, '<', "$file" or die "can not open $file";
	@file_lines = <$in>;
	close $in;
}


sub funct_for {
	my ($argu) = @_;
	#check input
	if ($argu =~ m/(\s*)for\s+(.*)\s+in\s+(.*)/) {	
		my $n = $2;
		my @input = split(/ /,$3);
		my @output = ();
		my $flag = 1;
		#check the word is "digits" or "*.c" or "character"
		foreach $word (@input){
			if ($word =~ m/(\*.c)$/) {
				print ("foreach \$$n (glob(\"$1\")) {\n");
				$flag = 0;
				last;
			}
			if ($word =~ m/\d+/){
				push @output, "$word";

			}else{
				push @output, "\'$word\'";
			}
		}
		if ($flag eq 1){
			my $out = join(", ",@output);
			print ("foreach \$$n ($out) {\n");
		}
	}
}


foreach $line(@file_lines){

#print if there is a "for" command
	if ($line =~ m/(\s*)for\s+(.*)\s+in\s+(.*)/){
		funct_for($line);
	}
}