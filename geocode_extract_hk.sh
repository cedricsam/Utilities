#!/bin/bash

COUNT=0
FOLDER="geocode"
FIELDS="2-"
IDFIELDS="1"
BBOX_HK="22.562040, 114.441788|22.153549, 113.835083"

D=`date +%s`

if [ $# -lt 1 ]
then
    echo "Missing file"
    exit
fi
if [ $# -gt 1 ]
then
    FOLDER=$2
fi
if [ $# -gt 2 ]
then
    FIELDS=$3
fi
if [ $# -gt 3 ]
then
    IDFIELDS=$4
fi

while read line
do
    id=`echo "${line}" | cut -d, -f${IDFIELDS}`
    address=`echo "${line}" | cut -d, -f${FIELDS}`
    address_url=`echo ${address} | sed 's/ /+/g' `
    echo $address
    FO="${FOLDER}/${id}.json"
    if [ -s "${FO}" ]
    then
	echo "Already OK: ${FO}"
	continue
    fi
    #URL="http://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=en&region=hk&address=${address_url}&components=country:HK"
    URL="http://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=en&region=hk&address=${address_url}"
    echo "${URL}"
    curl -s "${URL}" -o "${FO}"
    echo "${FO}"
    let COUNT=${COUNT}+1
    if [ ${COUNT} -gt 2480 ] || [ `grep OVER_QUERY_LIMIT "${FO}" 2> /dev/null | wc -l` -eq 1 ]
    then
	echo "MARK SET -- ${COUNT}: `date`"
	DNEXT=`date -d"tomorrow" +%s`
	DNOW=`date +%s`
	let SLEEPTIME=${DNEXT}-${DNOW}
	SLEEPTIME=86400
	echo "SLEEPING ${SLEEPTIME} SECONDS -- until `date -d"+1 day"`"
	sleep ${SLEEPTIME}
        curl -s "${URL}" -o "${FO}"
	COUNT=0
    fi
    sleep 0.5
done < $1

