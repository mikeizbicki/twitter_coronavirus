#bin/sh

for FILE in /data/Twitter\ dataset/geoTwitter20*; do
    /home/chom/proj/twitter_coronavirus/src/map.py --input_path="$FILE" &
done

