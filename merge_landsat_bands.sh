#!/bin/bash

# Merges visible bands of Landsat images downloaded from Earth Explorer (GeoTiff)
# Further processing suggested on Photoshop / GIMP

if [ $# -lt 1 ]
then
    exit
fi

ID=$1

# Project the images we need
for BAND in {4,3,2}
do
    gdalwarp -t_srs EPSG:3857 LC${ID}LGN00_B$BAND.TIF LC${ID}LGN00_B$BAND-projected.tif
done

# Merge bands
convert -combine LC${ID}LGN00_B{4,3,2}-projected.tif LC${ID}LGN00_RGB.tif

# Correct the colours
#convert -sigmoidal-contrast 50x16% LC${ID}LGN00_RGB.tif LC${ID}LGN00_RGB-corrected.tif
