#!/bin/bash

MY_JS_FILE="hongkong.js"
GOOGLE_SHEETS_KEY="YOUR_OWN_GOOGLE_SHEETS_KEY"
SLIDES_TAB="od6" # Probably od6
PLACES_TAB="ox0xxxx" # Change this -- should be a 7-character long string

../spreadsheet2csv.py ${GOOGLE_SHEETS_KEY} ${SLIDES_SHEET} > slides.csv
../spreadsheet2csv.py ${GOOGLE_SHEETS_KEY} ${PLACES_SHEET} > places.csv

./merge.py slides.csv places.csv > ${MY_JS_FILE}

sed -i 's/"\(lat\|lng\|heading\|infotype\|type\)": "\([^"]*\)"/"\1": \2/g' ${MY_JS_FILE}
