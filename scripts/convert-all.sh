#!/bin/bash
folder=$1
cmd=pdftotext
#find $folder -name '*.pdf' | xargs -0 pdftotext
find $folder -name '*.pdf' -exec pdftotext {} \;
find $folder -name '*.txt'
