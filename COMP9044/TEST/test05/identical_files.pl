#!/usr/bin/perl
#z5224151	ZANNING WANG

if ($#ARGV == -1){
	die "Usage:$0 <files>\n";
	exit 1;
}

sub get_content{
	my $files = "@_";
	open my $input, "<", "$files" or die "$0: can not open $files: $!\n";
	my @line = <$input>;
	$output = join("",@line);
	close $input;
	return $output;

}

$first = get_content($ARGV[0]);
shift (@ARGV);

foreach $files (@ARGV){
	if (get_content($files) eq "$first"){
		$first = get_content("$files");
	}else{
		print "$files is not identical\n";
		exit 0;
	}
}

print "All files are identical\n";