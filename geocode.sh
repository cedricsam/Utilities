#!/bin/bash

COUNT=0
FOLDER="json"
FIELDS="2-"
BBOX_MTL="45.402161,-73.999939|45.704788,-73.476097"

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

while read line
do
    #echo ${line}
    id=`echo "${line}" | cut -d, -f1`
    address=`echo "${line}" | cut -d, -f${FIELDS}`
    address_url=`echo ${address} | sed 's/ /+/g' `
    echo $address
    FO="${FOLDER}/${id}.json"
    if [ -s "${FO}" ]
    then
	echo "Already OK: ${FO}"
	continue
    fi
    #URL="http://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=fr&region=ca&address=${address_url}&bounds=${BBOX_MTL}&components=country:CA"
    URL="http://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=fr&region=ca&address=${address_url}&components=administrative_area:QC|country:CA"
    #URL="http://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=fr&region=ca&address=${address_url}&components=administrative_area:Montreal|administrative_area:QC|country:CA"
    echo "${URL}"
    curl -s "${URL}" -o "${FO}"
    echo "${FO}"
    let COUNT=${COUNT}+1
    if [ ${COUNT} -gt 2450 ] || [ `grep OVER_QUERY_LIMIT "${FO}" 2> /dev/null | wc -l` -eq 1 ]
    then
	echo "MARK SET -- ${COUNT}: `date`"
	#NEXTMIDNIGHT=`date -d"tomorrow" +%Y-%m-%d `
	#DNEXT=`date -d${NEXTMIDNIGHT} +%s`
	DNEXT=`date -d"tomorrow" +%s`
	DNOW=`date +%s`
	let SLEEPTIME=${DNEXT}-${DNOW}
	SLEEPTIME=86400
	echo "SLEEPING ${SLEEPTIME} SECONDS -- until `date -d"+1 day"`"
	sleep ${SLEEPTIME}
	COUNT=0
    fi
    sleep 0.75
done < $1

