#!/bin/bash
baseDir=$1
cd $baseDir
for dir in */ 
do
  base=$(basename "$dir")
  tar -czf "${base}.tar.gz" "$dir"
done

