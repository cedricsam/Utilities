#!/bin/bash

if [ $# -lt 1 ]
then
    echo "Missing table name"
    exit
fi

ACCESS_TOKEN=`cat ${HOME}/google.fusiontables.token | grep access_token | cut -d\" -f4`
TOKEN_TYPE=`cat ${HOME}/google.fusiontables.token | grep token_type | cut -d\" -f4`
AUTH_TOKEN="${TOKEN_TYPE} ${ACCESS_TOKEN}"

TABLEDATA=`${HOME}/bin/fttables.py $1`

#echo $TABLEDATA
curl "https://www.googleapis.com/fusiontables/v1/tables" -H "Authorization: ${AUTH_TOKEN}" -H "Content-Type: application/json" -d "${TABLEDATA}"
