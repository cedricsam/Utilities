#!/bin/bash

for i in `find -type f -name \*.jpg | grep -v "_"`
do
    FO=`echo "$i" | sed 's/^\.\///' | sed 's/\.\?\//_/' | tr [A-Z] [a-z]`
    W=`identify -format "%w" $i`
    H=`identify -format "%h" $i`
    M=`echo "$W / $H" | bc -l`
    echo $FO $HM $W $H
    HM=`printf "%.2f" "${M}"`
    if [ $W -gt $H ]
    then
	if [ "$HM" == "1.50" ]
	then
	    convert $i -resize 1500x\> $FO
	else
	    convert $i -resize 1600x\> $FO
	fi
    else
	convert $i -resize \>x1500 $FO
    fi
done
