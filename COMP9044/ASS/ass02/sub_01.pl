#!/usr/bin/perl
#ZANNING WANG 	z5224151

if ($#ARGV eq 0){
	$file = shift (@ARGV);
	open my $in, '<', "$file" or die "can not open $file";
	@file_lines = <$in>;
	close $in;
}


#used to translate function "if"
sub funct_if {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)if\s+(.*)/){
		my $whitespace = $1;
		my $content = $2;		
		#only check test =
		if ($content =~ m/test\s+(.*) = (.*)/){
			print ("$whitespace");
			print ("if (\'$1\' eq \'$2\') {\n")
		#to be add more situations if needed
		}
	}
}

#used to translate function "elif"
sub funct_elif {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)\belif\b\s+(.*)/){
		my $whitespace = $1;
		my $content = $2;
		#only check test =
		if ($content =~ m/test\s+(.*) = (.*)/){
			print ("$whitespace    ");
			print ("} elsif (\'$1\' eq \'$2\') {\n")
		#to be add more situations if needed
		}
	}
}

#used to translate function "else"
sub funct_else {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)else$/) {
		print ("$1    ");
		print ("} else {\n");
	}
}

#used to translate function "fi"
sub funct_fi {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)fi$/) {
		print ("$1    }\n");
	}
}

foreach $line(@file_lines){

	#print if there is a "if" command
	if ($line =~ m/(\s*)\bif\b\s+(.*)/) {
		funct_if($line);
	}

	#print if there is a "elif" command
	if ($line =~ m/(\s*)\belif\b\s+(.*)/) {
		funct_elif($line);
	}

	#print if there is a "else" command
	if ($line =~ m/(\s*)\belse\b$/) {
		funct_else($line);
	}

	#print if there is a "else" command
	if ($line =~ m/(\s*)\bfi\b$/) {
		funct_fi($line);
	}










}