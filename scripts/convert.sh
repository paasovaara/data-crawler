#!/bin/bash
input=$1
output=$2
temp=$output.temp

#convert pdf to txt
gs -sDEVICE=txtwrite -o $temp $input  
#trim whitespaces
tr -s " " < $temp > $output

rm $temp

