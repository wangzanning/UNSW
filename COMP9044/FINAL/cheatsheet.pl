#!/usr/bin/perl

#文本正则：
($family_name, $given_name) = $string =~ /([^,]*), (\S+)/;

\d matches any digit, i.e. [0-9]
\D matches any non-digit, i.e. [^0-9]
\w matches any "word" char, i.e. [a-zA-Z_0-9]
\W matches any non "word" char, i.e. [^a-zA-Z_0-9]
\s matches any whitespace, i.e. [ \t\n\r\f]
\S matches any non-whitespace, i.e. [^ \t\n\r\f]

#匹配整个一行的数字，存入@中
my @numbers = $line =~ /(\d+\.?\d*)/g;

#四舍五入数字.nf
$number_round = sprintf "%.0f", $number;

#$转@
my @arr = split(/\s+/,$input);

#标准输入直接存入@
@lines = <STDIN>;

#array排序
my @sorted = sort (@arr);

#通过字典排序
@sorted_words = sort {$count{$a} <=> $count{$b}} @words;

#@转$
my $output = join(" ",@sorted);

#打开文件
open my $f, '<', $file or die "$0: can not open $file: $!";

#保存到array
@lines = <$f>;

#保存到变量中，逐行操作
while ($line = <$f>) {}

#遍历文件
foreach $file (glob("*.[ch]")) {
while (<>) {
    chomp;

#分割后保存到变量中
($sid,$mark) = split;

#获得排序后的key，保存到array
@words = keys %count;

#盾变量中的，进行分割
my ($id,$type,$number) = split /,/, $line;

#遍历排序后的key
foreach $word (sort keys %w) {}

#切割成单个字母
@hi = split //,"hello";

#合并变量中以空格分割的，成一个array
my @fields = split /\s+/, $line;

#写文件，print后无“，”
open my $out, '>', $file or die "Can not open $file: $!";
    foreach $line (@lines) {
        print $out $line 
    }
close $out;

#把b直接拼接到a后
$a .= $b

#读取输入存到变量中
my $html_source = join "", <>;

#标准化输出
printf "%s %4.1f %s\n", $a, $total{$sid}, $passfail;

#利用map进行映射，得出 1 4 9 16 25
@vec = map { $_ ** 2 } (1,2,3,4,5);
map {tr /aeiouAEIOU/AEIOUaeiou/} @lines;

#存入字典
$w{$word} = "deleted";
$count{$word}++





