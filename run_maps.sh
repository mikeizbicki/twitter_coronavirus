#bin/sh

for FILE in /data/tweets_corona/*; do
    ./src/map.py --input_path=$FILE &
done
