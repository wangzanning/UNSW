#!/usr/bin/perl
#ZANNING WANG	z5224151

if ($#ARGV != 1){
	die "Usage: $0 <directory1> <directory2>\n";
}

sub get_content {
	my $files = "@_";
	open my $input, "<", "$files" or die "$0: can not open $files: $!\n";
	my @line = <$input>;
	$output = join("",@line);
	close $input;
	return $output;
}

sub check_identical{
	my ($file1, $file2) = @_;

	$file1_content = get_content("$ARGV[0]/$file1");
	$file2_content = get_content("$ARGV[1]/$file2");

	if ($file1_content eq $file2_content) {
		return 1;
	}else{
		return "";
	}
}

for $file1 (sort glob "$ARGV[0]/*"){
	$file1=~s/.*\///;

	for $file2 (sort glob "$ARGV[1]/*"){
		$file2=~s/.*\///;

		if ($file1 eq $file2){

			if (check_identical($file1,$file2)){
				print("$file1\n");
			}
		}

	}

}
