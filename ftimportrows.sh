#!/bin/bash

if [ $# -lt 2 ]
then
    echo "ftimportrows.sh [table sql] [ft table id] [OPT: starting db row] [OPT: chunk size] [OPT: seconds to wait between FT imports]"
    exit
fi
TABLENAME=$1
TABLEID=$2
START=0
ROWS=100000
WAITSECS=900

if [ $# -gt 2 ]
then
    START=$3
    if [ $# -gt 3 ]
    then
        ROWS=$4
        if [ $# -gt 4 ]
        then
            WAITSECS=$5
        fi
    fi
fi

COUNT=`psql -h 127.0.0.1 -U lp -tAc "SELECT COUNT(*) FROM ${TABLENAME}"`
let PAGES=$COUNT/$ROWS
let START=$START/$ROWS

ACCESS_TOKEN=`grep access_token ${HOME}/google.fusiontables.token | cut -d\" -f4`
TOKEN_TYPE=`grep token_type ${HOME}/google.fusiontables.token | cut -d\" -f4`
AUTH_TOKEN="${TOKEN_TYPE} ${ACCESS_TOKEN}"

#TABLEDATA=`${HOME}/bin/fttables.py $1`

#echo $TABLEDATA
for i in `seq ${START} ${PAGES}`
do
    let OFFSET=$i*$ROWS
    SQL="SELECT * FROM ${TABLENAME} LIMIT ${ROWS} OFFSET ${OFFSET}"
    echo "$SQL"
    FNAME=${TABLENAME}.${OFFSET}.csv
    psql -h 127.0.0.1 -U lp -c "\\copy (${SQL}) to '${FNAME}' csv header"
    #psql -h 127.0.0.1 -U lp -F~ -tAc "${SQL}" -o "${FNAME}"
    #sed -i 's/"/\\"/g' ${FNAME}
    BYTES=`wc -c ${FNAME} | cut -d" " -f1`
    if [ ${BYTES} -gt 104857600 ]
    then
        echo "Chunk too big: ${FNAME}"
        break
    fi
    curl -s "https://www.googleapis.com/upload/fusiontables/v1/tables/${TABLEID}/import?startLine=1" -H "Authorization: ${AUTH_TOKEN}" -H "Content-Type: application/octet-stream" --data-binary @${FNAME} -o ${FNAME}.out
    NUMROWSRECEIVED=`grep numRowsReceived ${FNAME}.out | cut -d\" -f4`
    HAS_NUMROWSRECEIVED=`grep numRowsReceived ${FNAME}.out | wc -l`
    if [ ${HAS_NUMROWSRECEIVED} -eq 0 ] || [ ${NUMROWSRECEIVED} -ne ${ROWS} ]
    then
        echo ${FNAME}
        cat ${FNAME}.out
        break
    else
        rm ${FNAME} # ${FNAME}.out
    fi
    sleep ${WAITSECS}
done
