# Data crawler

This project contains tools to crawl material for later endeavors, f.ex machine learning purposes etc. 
At the moment the idea is to enable crawling pdf data and import that as text data for nlp. 
Next step is to augment that with numeric data.

## Scripts

folder /scripts contain shell scripts to crawl and format the material into text files.

## Application

Python scripts to import and process the data. Text data is imported from .txt files and stored in a SQLite database. 
Use scripts to initialize and launch.

Init:

```
./init.sh
```

Running:

```
./run_import.sh <foldertoimport>
```

OR

```
./run_process.sh <filetoprocess>
```

## TODO
word stemming and lemmatization
https://www.analyticsvidhya.com/blog/2017/01/ultimate-guide-to-understand-implement-natural-language-processing-codes-in-python/
