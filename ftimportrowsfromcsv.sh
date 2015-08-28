#!/bin/bash

if [ $# -lt 2 ]
then
    echo "ftimportrowsfromcsv.sh [csv file] [ft table id] "
    exit
fi
CSVFILE=$1
TABLEID=$2
START=0

ACCESS_TOKEN=`grep access_token ${HOME}/google.fusiontables.token | cut -d\" -f4`
TOKEN_TYPE=`grep token_type ${HOME}/google.fusiontables.token | cut -d\" -f4`
AUTH_TOKEN="${TOKEN_TYPE} ${ACCESS_TOKEN}"

BYTES=`wc -c ${CSVFILE} | cut -d" " -f1`
if [ ${BYTES} -gt 104857600 ]
then
    echo "Chunk too big: ${CSVFILE}"
    break
fi
${HOME}/bin/ftsql.py POST "SELECT count() FROM ${TABLEID}" > count.${TABLEID}.json
COUNT_BEFORE=`${HOME}/bin/ftparsecount.py count.${TABLEID}.json`
#curl -s "https://www.googleapis.com/upload/fusiontables/v1/tables/${TABLEID}/import?startLine=0&isStrict=false" -H "Authorization: ${AUTH_TOKEN}" -H "Content-Type: application/octet-stream" --data-binary @${CSVFILE} -o ${CSVFILE}.out
curl -s "https://www.googleapis.com/upload/fusiontables/v2/tables/${TABLEID}/import?startLine=0&isStrict=false" -H "Authorization: ${AUTH_TOKEN}" -H "Content-Type: application/octet-stream" --data-binary @${CSVFILE} -o ${CSVFILE}.out
NUMROWSRECEIVED=`grep numRowsReceived ${CSVFILE}.out | cut -d\" -f4`
HAS_NUMROWSRECEIVED=`grep numRowsReceived ${CSVFILE}.out | wc -l`
if [ ${HAS_NUMROWSRECEIVED} -eq 0 ]
then
    echo ${CSVFILE}
    cat ${CSVFILE}.out
    ${HOME}/bin/ftsql.py POST "SELECT count() FROM ${TABLEID}" > count.${TABLEID}.json
    COUNT_AFTER=`${HOME}/bin/ftparsecount.py count.${TABLEID}.json`
    echo "Count before: ${COUNT_BEFORE}"
    echo "Count after: ${COUNT_AFTER}"
    cat count.${TABLEID}.json
fi
rm count.${TABLEID}.json 2> /dev/null
