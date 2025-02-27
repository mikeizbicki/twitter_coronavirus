#!/bin/bash

# Define paths
INPUT_DIR="/data/Twitter dataset/"
OUTPUT_JSON_DIR="outputs/json"
OUTPUT_LOG_DIR="outputs/logs"

# Create the output directories if they don't exist
mkdir -p "$OUTPUT_JSON_DIR"
mkdir -p "$OUTPUT_LOG_DIR"

# Loop over all files from 2020 in the dataset and run map.py in parallel
for file in '/data/Twitter dataset/'geoTwitter20-*-*.zip; do
    echo "Processing $file..."

    # Extract filename without path
    filename=$(basename "$file")

    # Run map.py, save JSON output to OUTPUT_JSON_DIR, and redirect logs to OUTPUT_LOG_DIR
    nohup python3 src/map.py --input_path="$file" --output_folder="$OUTPUT_JSON_DIR" > "$OUTPUT_LOG_DIR/$filename.log" 2>&1 &
done

echo "All map.py jobs have been started in the background."

