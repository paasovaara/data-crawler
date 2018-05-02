#!/bin/bash
source .env/bin/activate

NAME=${1:-foo}
python ./importer/main.py process --name $NAME

