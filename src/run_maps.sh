#bin/sh

COUNT=0;
for FILE in /data/tweets_corona/*; do
    ./map.py --input_path=$FILE &
    COUNT=$COUNT+1
done
