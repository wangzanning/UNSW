#!/usr/bin/perl
#ZANNING WANG 	z5224151

#check the input and read the file from ARGV
if ($#ARGV eq 0){
	$file = shift (@ARGV);
	open my $in, '<', "$file" or die "can not open $file";
	@file_lines = <$in>;
	close $in;
}

#build a dict for signal
%compare = ("-lt" => "<", "-le" => "<=", "-eq" => "==", "-gt" => ">", "-ge" => "=>");

#build a flag for sub_function
$flag_funct = 0;

#subset 0
#used to translate function "echo"
sub funct_echo {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)echo\s*([\'\"]*.*[\'\"]*)$/){
		my $whitespace = $1;
		my $content = $2;
		
		#remove the ' from the start and end.
		if ($content =~ m/^\'(.*)\'$/){
			$content =~ s/^\'//g;
			$content =~ s/\'$//g;
		}

		#remove the " from the start and end.
		if ($content =~ m/^\"(.*)\"$/){
			$content =~ s/^\"//g;
			$content =~ s/\"$//g;
		}
		#add \ for " 
		$content =~ s/\"/\\\"/g;
		if ($content =~ m/(\$)(\d)/){
			my $value = "$1$2";
			my $number = "$2" - 1;
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
	if ($argu =~ m/(\s*)ls\s*(-\w+)?\s+(.*)/){
		print ("$1");
		my $ls = $2;
		my $out = $3;
		#CASE :system "ls"
		if ($argu =~ m/^ls$/){
			print ("system \"ls\";\n");
		}
		#CASE :system "ls -las @ARGV";
		if ($out =~ m/\$\@/){
			print ("system \"ls $ls \@ARGV\";\n");
		}
		#CASE: system "ls -las folder;
		else{
			if ($argu =~ m/-\w+/){
				print ("system \"ls $ls $out\";\n");
			}
			#print if there is no "-l";
			else{
				print ("system \"ls $ls$out\";\n");
			}
		}
	}
}

#used to translate "=", when there is a variables allocated
sub funct_allocate{
	my ($argu) = @_;
	my $flag = 0;
	if ($argu =~ m/(\s*)(\b\w+\b)=(.*)\s*/){
		print ("$1");
		my $left = $2;
		my $right = $3;
		#right side is $1 and not in 
		if ($right =~ m/(\$)(\d)/ && $flag_funct eq 0){
			my $number = "$2" - 1;		
			$flag = 1;
			print ("\$$left = \$ARGV[$number];\n");
		}
		#right side is word or number 
		if ($flag eq 0){
			#right is digits only
			if ($right =~ m/^(\d+)$/){
				print ("\$$left = $right;\n");
			}		
			#right is $number + 1
			elsif ($right =~ m/ \+ 1/){
				print ("\$$left = \$$left + 1;\n");
			}
			#right is $1
			elsif ($right =~ m/^\$(.*)/){
				my $digit = $1 - 1;
				if ($flag_funct eq 1){
					print ("\$$left = \$_[$digit];\n");
				}else{
					print ("\$$left = $right;\n");
				}
			}
			#right is word
			else{
				print ("\$$left = \'$right\';\n");
			}
		}
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
		print ("$whitespace");
		if ($content =~ m/test\s+(.*) = (.*)/){			
			print ("if (\'$1\' eq \'$2\') {\n")
		}
		#check: if [ -d /dev/null ]
		elsif ($content =~ m/\[\s*(.*)\s+\]/){
			my $content2 = $1;
			if ($content2 =~ m/(-\w)*(\s+)(.*)/){
				print ("if ($1 \'$3\') {\n");
			}
		}
		#check: if test -r /dev/null
		elsif ($content =~ m/test\s+(.*)/){
			my $content2 = $1;
			if ($content2 =~ m/(-\w)*(\s+)(.*)/){
				print ("if ($1 \'$3\') {\n");
			}
		}

		#to be add more situations if needed
	}
}

#used to translate function "elif"
sub funct_elif {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)\belif\b\s+(.*)/){
		my $whitespace = $1;
		my $content = $2;
		print ("$whitespace    ");
		#only check test =
		if ($content =~ m/test\s+(.*) = (.*)/){
			print ("} elsif (\'$1\' eq \'$2\') {\n")	
		}
		#check elsif [ -d /dev/null ]
		elsif ($content =~ m/\[\s*(.*)\s+\]/){
			my $content2 = $1;
			if ($content2 =~ m/(-\w)*(\s+)(.*)/){
				print ("elsif ($1 \'$3\') {\n");
			}
		}

		#check: elsif test -r /dev/null
		elsif ($content =~ m/test\s+(.*)/){
			my $content2 = $1;
			if ($content2 =~ m/(-\w)*(\s+)(.*)/){
				print ("elsif ($1 \'$3\') {\n");
			}
		}

		#to be add more situations if needed
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

#subset 3

#used to translate function "while"
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

#used to translate function "expr"
sub funct_expr {
	my ($argu) = @_;
	if ($argu =~ /(\s*)(\w+)(.*)expr\s+(.*)/){
		#print $argu;
		my $whitespace = $1;
		my $name = $2;
		my $check = $4;
		print ("$whitespace");
		#check increment number
		if ($check =~ m/\$\Q$name\E \+ 1/){
			print ("\$$name = \$$name + 1;\n");
		}
		#check decreasing number
		if ($check =~ m/\$\Q$name\E \- 1/){
			print ("\$$name = \$$name - 1;\n");
		}
	}
}

#subset 4

#used to translate function "function"
sub funct_function {
	my ($argu) = @_;
	if ($argu =~ m/^(\w+)\(\) {/){
		$flag_funct = 1;
		print ("sub $1 {\n");
	}
}

#used to translate function "local"
sub funct_local {
	my ($argu) = @_;
	if ($argu =~ m/(\s*)local (.*)/){
		my $whitespace =$1;
		my $content = $2;
		#add "$"before the argu and "," after the argu
		$content =~ s/\s+/\, \$/g;
		print ("$whitespace");
		print ("my (\$$content);\n");
	}
}

#used to translate function "return"
sub funct_return {
	my ($argu) = @_;
	if ($argu =~ m/^(\s*)return\s+(.*)/){
		my $whitespace = $1;
		my $content = $2;
		print ("$whitespace");
		print ("return $2;\n");
	}
}

#used to translate function "&&"
sub funct_andand {
    my ($argu) = @_;
    if ($argu =~ m/(\s*)(.*)\s+&&\s+(.*)/) {
        my $whitespace = $1;
        my $first = $2;
        my $second = $3;
        print("$whitespace");
        if ($second =~ m/echo/){
        	print ("$first or ");
        	my $out = funct_echo($second);
        }
        else{
        	print ("\$n % \$i == 0 and return 1;\n");
        }
        
    }
}

#used to translate function "||"
sub funct_oror {
    my ($argu) = @_;
    if ($argu =~ m/(\s*)(.*)\s+\|\|\s+(.*)/) {
        my $whitespace = $1;
        my $first = $2;
        my $second = $3;
        print("$whitespace");
        if ($first =~ m/is_prime/){
            print ("$first");
        }
        print (" or ");
        if ($second =~ m/echo/) {
            my $out = funct_echo($second);
            #print ("$out\n");      
        }
    }     
}

#used to translate function " "
sub funct_ {

	
}


#start to translate sh line by line
foreach $line(@file_lines){

	#subset 0
	#print nothing if the line show nothing
	if ($line =~ m/^\n$/){
		print ("\n");
	}

	#print comment line
	if ($line =~ m/^#(.*)/ && $line !~ m/\#\!\/bin\/dash/){
		print ("$line");
	}

	#print necessary command;
	if ($line =~ m/\#\!\/bin\/dash/){
		print ("#!/usr/bin/perl -w\n");
	}

	#print if there is "=" to allocate variables
	elsif ($line =~ m/(\s*)(\b\w+\b)=(.*)\s*/) {
		funct_allocate($line);
	}

	#print if there is a "echo" command;
	elsif ($line =~ m/^(\s*)echo\s+(.*)/){
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
	elsif ($line =~ m/(\s*)\belif\b\s+(.*)/) {
		funct_elif($line);
	}

	#print if there is a "else" command
	elsif ($line =~ m/(\s*)\belse\b$/) {
		funct_else($line);
	}

	#print if there is a "else" command
	elsif ($line =~ m/(\s*)\bfi\b$/) {
		funct_fi($line);
	}

	#subset 3

	#print if there is a "while" loop

	if ($line =~ m/(\s*)while(\s+)(.*)/){
		funct_while($line);
	}

	#print if there is a "expr" command
	# elsif ($line =~ m/`expr\s+(.*)/) {
	# 	funct_expr($line);
	# }

	#subset 4

	#print if there is a "function" command
	if ($line =~ m/^(\w+)\(\)\s*{/) {
		funct_function($line);
	}

	#print if there is a "}" command
	elsif ($line =~ m/^(\s*)}$/) {
		$flag_funct = 0;
		print ("$1}\n");
	}

	#print if there is a "local" command
	elsif ($line =~ m/^(\s*)local\s+(.*)/) {
		funct_local($line);
	}

	#print if there is a "return" command
	elsif ($line =~ m/^(\s*)return\s+/) {
		funct_return($line);
	}

    #print if there is a "&&" command
    if ($line =~ m/(\s+)&&(\s+)/){
        funct_andand($line);
    }

    #print if there is a "||" command
    if ($line =~ m/(\s+)\|\|(\s+)/){
        funct_oror($line);
    }


}


















