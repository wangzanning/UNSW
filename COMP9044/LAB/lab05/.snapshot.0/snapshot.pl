#!/usr/bin/perl
#z5224151	ZANNING WANG

use warnings;
use File::Copy;

#check the dict exists or not
$counter = 0;
	while (1){
		$backup_dir = ".snapshot.$counter";
		if (-d $backup_dir){
			$counter++;
		}else{
			last;
		}
	}

if ($#ARGV == 0 && $ARGV[0] eq "save"){

	#backup the file
	mkdir("$backup_dir") or die "can't create $backup_dir\n";
	foreach $file (glob "*"){
		if ($file !~ /^\.\/\./ && $file ne "snapshot.pl"){
			copy("$file", "$backup_dir")||warn "can't copy files:$!";
		}
	}
	print "Creating snapshot $counter\n";

}

if ($#ARGV == 1 && $ARGV[0] eq "load" && $ARGV[1] >= 0){

	#backup the file first
	mkdir("$backup_dir") or die "can't create $backup_dir\n";
	foreach $file (glob "*"){
		if ($file !~ /^\.\/\./ && $file ne "snapshot.pl"){
			copy("$file", "$backup_dir");
		}
	}
	print "Creating snapshot $counter\n";

	#restore the file back to the f
	$restore_dir = ".snapshot.$ARGV[1]";
	foreach $file (glob "./$restore_dir/*"){
		copy("$file", "./")||warn "can't copy files:$!";
	}
	print "Restoring snapshot $ARGV[1]\n";

}else{
	print "Incorrect Input!\n"
}
