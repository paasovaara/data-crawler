#!/bin/bash
source .env/bin/activate
FOLDER=${1:-.}

python ./application/main.py import --root $FOLDER

