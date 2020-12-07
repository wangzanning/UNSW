#!/usr/bin/perl -w

# 从命令行把文件读进来
$file_name = shift @ARGV;

open my $in, '<', "$file_name";
@file_lines = (<$in>);
close $in;

# 1.用索引的方式去遍历 $file_lines[0], $file_lines[1]
# $index = 0;
# while ($index <= $#file_lines){


#    $index++;
# }

sub assign_expression {
    my ($line) = @_;
    #               a=$1
    # $a = $ARGV[0]
    if ($line =~ /(.*)=\$(\d+)/){
        my $param = $2;
        $param--;
        print "\$$1 = \$ARGV[$param];\n";

    } elsif ($line =~ /(.*)=(.*)/){
        print "\$$1 = \"$2\";\n";
    }
}

sub echo_expression {
    my ($line) = @_;
    #               a=$1
    # $a = $ARGV[0]
    if ($line =~ /(\s*)echo\s*(.*)/){
        print "$1";
        print "print \"$2\\n\";\n";
    }
}

sub if_expression {
    my ($lines) = @_;
    #               a=$1
    # $a = $ARGV[0]
    while (@$lines){
        my $if_line = shift @$lines;
        if ($if_line =~ /if\s*test\s*(.*)\s*=\s*(.*)/){
            # print "$1";
            print "if (\'$1\' eq \'$2\') {\n";
            next;
        }elsif ($if_line =~ /(\s*)else/){
            print "} else {\n";
            next;
        }

        elsif ($if_line =~ /(\s*)fi/){
            print "}\n";
            last;
        }elsif ($if_line =~ /then/){
            next;
        }else {
            unshift @$lines, $if_line;
            check_each_line($lines);
        }
    }
}

sub for_expression {
    my ($lines) = @_;
    #               a=$1
    # $a = $ARGV[0]
    while (@$lines){
        my $for_line = shift @$lines;
        if ($for_line =~/\s*for (.*) in (.*)\n/){
            my @words =split(/ /, $2);
            print "foreach \$$1 (\"";
            print join("\",\"",@words);
            print "\"){\n";
            next;
        } elsif ($for_line =~ /(\s*)done/){
            print "}\n";
            last;
        }
        elsif ($for_line =~ /(\s*)do/){
            next;
        }
       else {
            unshift @$lines, $for_line;
            check_each_line($lines);
        }
    }
}

sub check_each_line {
    my ($lines) = @_;
    my $line = shift @$lines;
    #  a=hello
    if ($line =~ /if\s*(.*)/){
        unshift @$lines, $line;
        if_expression($lines);
    }elsif ($line =~ /for\s*(.*)/){
        unshift @$lines, $line;
        for_expression($lines);
    }
    elsif ($line =~ /(.*)=(.*)/){
        assign_expression($line);
    }elsif ($line =~ /echo\s*(.*)/){
        echo_expression($line);
    }
}

print "#!/usr/bin/perl -w\n";

# 2.采用shift的方式，print each line
while (@file_lines) {
    # check every line
    check_each_line(\@file_lines);
}


# 终点掌握：
# 1.perl语法
# 2.perl regex
#   不仅是匹配，还要替换
# 3.特别要提醒
# 3.特别要提醒
# 3.特别要提醒
# perl 没有办法debug，只能print
# 主程序：尽量不要动，自己写多个测试小程序，把多个小程序拼起来