#!/usr/bin/per
#ZANNING WANG	z5224151

use warnings;

d_flag = False;
foreach $argue(@ARGV){
	if ($argue eq "-d"){
		d_flag = True;
	}
}

#with "-d"
if (d_flag = "True"){
	shift @ARGV;

	foreach $file_song(@ARGV){




		foreach $file_lyrics(glob "lyrics/*.txt"){

			open my $in, "<", "$file_song" or die "can not open $file_song";
			while ($line = <$in>){
				$line =~ tr/A-Z/a-z/;
				$line =~ s/[^a-z]/ /g;
				@words = split(/\s+/, $line);
			}
			
			foreach $word(@words){


			}


		}


	}






#without "-d"
}else{





}
