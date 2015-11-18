#!/bin/bash

SEP='	'

while (( "$#" )); do
    if [ ! -s $1 ]
    then
	shift
	continue
    fi
    file=`file $1 | tr [A-Z] [a-z] | cut -d: -f2-`
    if [[ "$file" == *image* ]]
    then
        typ="image"
    	W=`identify -format "%w" $1`
	H=`identify -format "%h" $1`
	F=`basename $1`
	M=`echo "$H / $W" | bc -l`
	HM=`printf "%.4f" "${M}"`
        IDESC=`exiftool $1 | grep "Image Description" | cut -d: -f2- | sed 's/^ \+//g'`
        BYLINE=`exiftool $1 | grep "By-line" | head -1 | cut -d: -f2- | sed 's/^ \+//g'`
        CREDIT=`exiftool $1 | grep "Credit" | head -1 | cut -d: -f2- | sed 's/^ \+//g'`
	echo "$F$SEP$HM$SEP$IDESC$SEP$BYLINE/$CREDIT"
    fi
    shift
done
