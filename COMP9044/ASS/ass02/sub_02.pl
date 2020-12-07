#!/usr/bin/perl
#ZANNING WANG 	z5224151

if ($#ARGV eq 0){
	$file = shift (@ARGV);
	open my $in, '<', "$file" or die "can not open $file";
	@file_lines = <$in>;
	close $in;
}


sub funct_echo {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)echo\s*\'*(.*)\'*$/){
		my $whitespace = $1;
		my $content = $2;
		$content =~ s/\'$//g;
		$content =~ s/\"/\\\"/g;
		if ($content =~ m/(\$)(\d)/){
			my $value = "$1$2";
			my $number = "$2" -1;
			#/\Q$a\E/   use \Q  \E to add variables;
			$content =~ s/\Q$value\E/\$ARGV[\Q$number\E]/g;
		}

		print ("$whitespace");
		print ("print \"$content\\n\";\n");
	}
}


foreach $line(@file_lines){

#print if there is a "echo" command
	if ($line =~ m/(.*)echo\s+(.*)/){
		funct_echo($line);
	}
}