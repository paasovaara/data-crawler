#!/bin/bash
source .env/bin/activate

NAME=${1:-foo}
python ./application/main.py process --name $NAME

