#!/bin/bash
folder=$1
if [ $# -eq 2 ] && [ $2 == "clean" ]; then 
  echo "cleaning all txt files from folder $folder"
  read -p "Press any key to continue..."
  find $folder -name '*.txt' -print0 | xargs -0 rm
fi

find $folder -name '*.pdf' -exec pdftotext {} \;
find $folder -name '*.txt'
