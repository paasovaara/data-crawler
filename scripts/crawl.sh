#!/bin/bash
source=$1
echo "crawling all pdfs from $source"

wget -r -A pdf -np -N $source

