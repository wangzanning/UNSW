#!/usr/bin/perl
#ZANNING WANG 	z5224151

#check the input and read the file from ARGV
if ($#ARGV eq 0){
	$file = shift (@ARGV);
	open my $in, '<', "$file" or die "can not open $file";
	@file_lines = <$in>;
	close $in;
}

#subset 0
#used to translate function "echo"
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

#used to translate function "ls"
sub funct_ls {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)ls\s*(-l)?\s+(.*)/){
		print ("$1");
		my $ls = $2;
		my $out = $3;
		#print if there is "-l";
		if ($argu =~ m/^ls$/){
			print ("system \"ls\";\n");
		}
		elsif ($argu =~ m/-l/){
			print ("system \"ls $ls $out\";\n");
		}
		#print if there is no "-l";
		else{
			print ("system \"ls $ls$out\";\n");
		}
	}
}

#used to translate "=", when there is a variables allocated
sub funct_allocate{
	my ($argu) = @_;
	if ($argu =~ m/(\s*)(\b\w+\b)=(\b\w+\b)/){
		print ("$1");
		print ("\$$2 = \'$3\';\n");
	}
}

#used to translate function "pwd"
sub funct_pwd {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)pwd$/){
		print ("$1system \"pwd\";\n");
	}
}

#used to translate function "id"
sub funct_id {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)id$/){
		print ("$1system \"id\";\n");
	}
}

#used to translate function "date"
sub funct_date {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)date$/){
		print ("$1system \"date\";\n");
	}
}

#subset 1

#used to translate function "cd"
sub funct_cd {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)cd\s+(.*)/) {
		print ("$1chdir \'$2\';\n");
	}
	
}

#used to translate function "read"
sub funct_read {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)read\s+(.*)/){
		print ("$1\$$2 = <STDIN>;\n");
		print ("chomp \$$2;\n");
	}
}

#used to translate loop "for"
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
			#check the digits, add output without ""
			if ($word =~ m/\d+/){
				push @output, "$word";
			#check the word add output with ""
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

#used to translate loop "done"
sub funct_done {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)done$/){
		print ("$1}\n");
	}
	
}

#used to translate function "exit"
sub funct_exit {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)exit\s+(.*)/){
		print ("$1exit $2;\n");
	}	
}

#subset 2

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

#used to translate function " "
sub funct_ {
	
}

#used to translate function " "
sub funct_ {
	
}

#used to translate function " "
sub funct_ {
	
}

#used to translate function " "
sub funct_ {
	
}

#used to translate function " "
sub funct_ {
	
}
#do then do nothing 



#start to translate sh line by line
foreach $line(@file_lines){

	#subset 0
	#print necessart command;
	if ($line =~ m/\#\!\/bin\/dash/){
		print ("#!/usr/bin/perl -w\n");
	}

	#print if there is "=" to allocate variables
	elsif ($line =~ m/(\s*)(\b\w+\b)=(\b\w+\b)\s*/) {
		funct_allocate($line);
	}

	#print if there is a "echo" command;
	elsif ($line =~ m/(.*)echo\s+(.*)/){
		funct_echo($line);
	}

	#print if there is a "ls" command
	elsif ($line =~ m/(\s*)ls\s*(.*)/){
		funct_ls($line);
	}

	#print if there is a "pwd" command
	elsif ($line =~ m/(\s*)pwd$/){
		funct_pwd($line);
	}

	#print if there is a "id" command
	elsif ($line =~ m/(\s*)id$/){
		funct_id($line);
	}

	#print if there is a "date" command
	elsif ($line =~ m/(\s*)date$/){
		funct_date($line);
	}

	#print if there is a "cd" command
	elsif ($line =~ m/(\s*)cd\s+(.*)/) {
		funct_cd($line);		
	}

	#subset 1

	#print if there is a "for" loop
	if ($line =~ m/(\s*)for\s+(.*)\s+in\s+(.*)/){
		funct_for($line);
	}

	#print if there is a "read" command
	elsif ($line =~ m/(\s*)read\s+(.*)/){
		funct_read($line);
	}

	#print if there is a "done" loop
	elsif ($line =~ m/(\s*)done$/) {
		funct_done($line);
	}


	#print if there is a "exit" command
	elsif ($line =~ m/(\s*)exit\s+(.*)/) {
		funct_exit($line);
	}

	#subset 2

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


	#print if there is a " " command
	if ($line =~ m//) {
		funct_($line)
	}

	#print if there is a " " command
	if ($line =~ m//) {
		funct_($line)
	}

	#print if there is a " " command
	if ($line =~ m//) {
		funct_($line)
	}















}



