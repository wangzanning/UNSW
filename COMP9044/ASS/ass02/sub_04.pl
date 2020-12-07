#!/usr/bin/perl
#ZANNING WANG   z5224151

if ($#ARGV eq 0){
    $file = shift (@ARGV);
    open my $in, '<', "$file" or die "can not open $file";
    @file_lines = <$in>;
    close $in;
}

%compare = ("-lt" => "<", "-le" => "<=", "-eq" => "==", "-gt" => ">", "-ge" => "=>");

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


#used to translate function "&&"
sub funct_andand {
    my ($argu) = @_;
    if ($argu =~ m/(\s*)(.*)\s+&&\s+(.*)/) {
        my $whitespace = $1;
        my $first = $2;
        my $second = $3;
        print("$whitespace");
        print ("\$n % \$i == 0 and return 1;\n");
        
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


foreach $line(@file_lines){

    #print if there is a "&&" command
    if ($line =~ m/(\s+)&&(\s+)/){
        funct_andand($line);
    }

    #print if there is a "||" command
    if ($line =~ m/(\s+)\|\|(\s+)/){
        funct_oror($line);
    }


}
























