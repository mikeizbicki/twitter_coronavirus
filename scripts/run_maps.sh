#!/bin/sh

# this command creates a log folder if it doesn't already exist
mkdir -p log

# by default, python uses what's called "buffered" output;
# buffered output causes python to 
export PYTHONUNBUFFERED=True

# this is the main loop for your analysis
# this loop processes each file in /data/twitter_corona
# and passes the file to your map.py file as input
for path in /data/twitter_corona/*; do

    # extracts the filename from the path variable
    filename=$(basename "$path")

    # run the map.py program on the input $path,
    # and save all output into log/$filename
    nohup src/map.py "--input_path=$path" > log/$filename
done
