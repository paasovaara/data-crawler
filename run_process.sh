#!/bin/bash
NAME=${1:-foo}
python ./importer/main.py process --name $NAME

