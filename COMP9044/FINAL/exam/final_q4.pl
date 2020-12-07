#!/usr/bin/perl


while ($line = <STDIN>){
	if ($line =~ m/(^[A-Z]{4}[0-9]{4})/){
		$course_name = $1;
		#print("$course_name\n");
	}
	if ($line =~ m/\|(\d+)\|\w/){
		$id = $1;
		#print("$id\n");
	}
	$dict1{$id}++;

}

foreach $id_stu(keys %dict1){
	if ($dict1{$id_stu} == 2){
		push @output,$id_stu;
	}
}

@sort_output = sort(@output);

foreach $a (@sort_output){
	print("$a\n");
}

