#!/bin/bash

# Will convert images in the . directory, or the directories you specify (space-separated, quoted first arg on command-line)
# The resulting images can be used for Laziest Loader, a JS library for lazy loading by NYT's Josh Williams: https://github.com/sjwilliams/laziestloader

X1="1 .6 .25"
worig=1500
dirout="responsive"
if [ $# -ge 1 ]
then
    directories=$1
else
    directories="."
fi

for F in ${directories}
do
    f=`echo $F | tr [A-Z] [a-z]`
    if [ $f == "." ]
    then
        f=""
    else
        f="${f}_"
    fi
    for i in `ls $F`
    do
        if [ -d "${i}" ]
        then
            continue
        fi
        out=`echo "$i" | sed 's/[ _]\+/_/g' | tr [A-Z] [a-z]`
        DIMS=`identify $F/$i | cut -d" " -f3`
        ftype=`identify $F/$i | cut -d" " -f2`
        if [ $ftype != "JPEG" ]
        then
            continue
        fi
        W=`echo $DIMS | cut -dx -f1`
        H=`echo $DIMS | cut -dx -f2`
        P=`echo "scale=1; 1.0 * $W / $H" | bc`
        w=1500
        if [ $P == .6 ]
            then w=1000
        elif [ $P = 1.7 ]
            then w=1600
        fi
        fout="${f}`echo ${out} | sed 's/\.jpe\?g$//'`"
        echo $fout
        for x1 in $X1
        do
            #echo $x1
            wfname=`printf %.0f $(echo "$worig * $x1" | bc -l)`
            wfactual=`printf %.0f $(echo "$w * $x1" | bc -l)`
            wfactualret=`printf %.0f $(echo "$w * $x1 * 2" | bc -l)`
            mkdir -p "${dirout}"
            convert $F/$i -resize ${wfactual}x\> -quality 92 "${dirout}/${fout}-$wfname.jpg"
            convert $F/$i -resize ${wfactualret}x\> -quality 92 "${dirout}/${fout}-$wfname@2x.jpg"
        done
        #sleep .5
    done
done
