#!/usr/bin/perl
#ZANNING WANG	z5224151

$time = `date`;
print ("# Makefile generated at $time\n");
print ("CC = gcc\n");
print ("CFLAGS = -Wall -g\n");

@out_name = ();
%dict = ();
%dict_h_h = ();

my @files_h = glob("*.h");
foreach my $file_h (@files_h){
	
	my $name_h = $file_h;
	open my $in , "<", "$file_h" or die "Not exist";
	my @lines_h = <$in>;
	my @list_h_h = ();
	my $file_h_h;
	foreach $line_h (@lines_h){
		
		if ($line_h =~ m/\"(.*\.h)\"/){
					
			$file_h_h = $1;
			#print ("$file_h_h\n");
			push @list_h_h, $file_h_h;		
		}
	}
	$h_h = join(" ", @list_h_h);
	$dict_h_h{$name_h} = $h_h;
	
}




my @files = glob("*.c");
foreach $file (@files){
	my @list_h;
	$file_c = $file;
	open my $in , "<", "$file" or die "Not exist";
	@lines = <$in>;

	$file =~ s/\.c/\.o/;
	$file_name_out = $file;
	#print ("$file\n");
	push @out_name, "$file_name_out";
	
	if ($file =~ m/main/){
		$file =~ s/\.o//;
		$file_main = $file;
		#print ("$file_main\n");
	}

	#creat command for each file 
	
	foreach $line (@lines){
		if ($line =~ m/\"(.*\.h)\"/){
			my $file_h;			
			$file_h = $1;
			push @list_h, $file_h;	
			#$more_h = $dict_h_h{$file_h};
			#print("11111$more_h\n");
			push @list_h, $dict_h_h{$file_h};
			if ($dict_h_h{$file_h}){
				$h_h_h = $dict_h_h{$file_h};
				push @list_h,$dict_h_h{$h_h_h};
			}

		}		
	}
	push @list_h, $file_c;
	$h = join(" ", @list_h);
	$dict{$file_name_out} = $h;
	#print ("234$h\n");
	
}


print("$file_main: @out_name\n");
print("	\$(CC) \$(CFLAGS) -o \$@ @out_name\n");
foreach $name (keys %dict){
	print("$name : $dict{$name}\n");
}

#print ("@out_name\n");





