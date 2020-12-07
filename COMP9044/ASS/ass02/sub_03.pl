#!/usr/bin/perl
#ZANNING WANG 	z5224151

if ($#ARGV eq 0){
	$file = shift (@ARGV);
	open my $in, '<', "$file" or die "can not open $file";
	@file_lines = <$in>;
	close $in;
}

%compare = ("-lt" => "<", "-le" => "<=", "-eq" => "=", "-gt" => ">", "-ge" => "=>");


sub funct_while {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)while(\s+)(.*)/){
		my $whitespace = $1;
		my $content = $3;
		
		#check -lt
		if ($content =~ m/test\s+(.*) (.*) (.*)/){
			#use dict to print signal"<=""
			my $signal = $compare{"$2"};
			my $var1 = $1;
			my $var2 = $3;
			print ("$whitespace");
			print ("while ($var1 $signal $var2) {\n");
		}
	}
}


foreach $line(@file_lines){

#print if there is a "echo" command
	if ($line =~ m/(\s*)while(\s+)(.*)/){
		funct_while($line);
	}
}