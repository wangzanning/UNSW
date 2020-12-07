#!/usr/bin/perl
#ZANNING WANG z5224151

$file = shift(@ARGV);
open my $in, "<", "$file" or die "$0: can't open file\n";
@lines = <$in>;
my %counter = ();

while ($content = <$in>) {
	$counter{$content} = length($content);
}

foreach my $key (sort{ $counter{$a} <=> $counter{$b} or $a cmp $b } keys %counter) {
		print "$key";
}