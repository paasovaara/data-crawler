# Data crawler

This project contains tools to crawl material for later endeavors, f.ex machine learning purposes etc.

## Scripts

folder /scripts contain shell scripts to crawl and format the material into text files.

## Importer

Python scripts to import the text files into SQLite database. Use scripts to setup and launch.

Init:

```
./init.sh
```

Running:

```
./run_import.sh
```

OR

```
./run_process.sh <filetoprocess>
```

## TODO
word stemming and lemmatization
https://www.analyticsvidhya.com/blog/2017/01/ultimate-guide-to-understand-implement-natural-language-processing-codes-in-python/

see
- snowball stemmer (should have finnish)
- python nltk
