#!/usr/bin/perl
while($word = <STDIN>){
	@lines = split(/ /,$word);
	print(@lines);

}