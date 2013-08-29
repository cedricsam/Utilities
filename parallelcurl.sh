#!/bin/bash

if [ $# -lt 1 ]
then
    exit
fi

url=`echo $1 | cut -d, -f1`
out=`echo $1 | cut -d, -f2`
F="${out}.html"

curl -s "${url}" -o "${F}"
