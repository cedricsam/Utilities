#!/bin/bash

if [ $# -lt 1 ]
then
    echo "Missing file..."
    exit
fi

echo "Starting..."

D=`date +%Y%m%d%H%M`

CONCUR=10
MAXTIME=30

COUNT=0
i=-1
IDS=""
WC=`wc -l $1 | cut -d" " -f1`
let WC=$WC-1

while read line
do
    url=`echo $line | cut -d, -f1`
    out=`echo $line | cut -d, -f2`
    F="${out}.html"
    let i=$i+1
    if [ -s "${F}" ]
    then
        continue
    fi
    let COUNT=$COUNT+1
    echo $i $COUNT
    let CYCLE=$COUNT%$CONCUR
    echo ${CYCLE}
    IDS="${IDS} ${line}"
    echo ${IDS}
    if [ ${CYCLE} -eq 0 ] || [ ${WC} -le $i ]
    then
        ${HOME}/bin/parallel -j ${CONCUR} -t ${MAXTIME} -r "${HOME}/bin/parallelcurl.sh *" ${IDS}
        IDS=""
	sleep 1
        date
    fi
done < $1

if [ ${CYCLE} -ne 0 ]
then
    ${HOME}/bin/parallel -j ${CONCUR} -t ${MAXTIME} -r "${HOME}/bin/parallelcurl.sh *" ${IDS}
    date
    echo "COMPLETE"
fi
