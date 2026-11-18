import zipfile, json, sys
import itertools
from collections import Counter
from collections import defaultdict

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("--numdp", type=int)
args = parser.parse_args()

# load from file
hashtags = ['parola', 'para']
lang_counter = defaultdict(lambda: Counter())

print(f"args.filename={args.filename}")

with zipfile.ZipFile(args.filename) as z:
    for name in z.namelist():
        print('name=', name)
        with z.open(name) as f:
            for i, line in itertools.islice(enumerate(f), args.numdp):
                print(f"i={i}")
                data = json.loads(line)
                text = data['text']
                #print(f"text={text}")
                lang = data['lang']
                counter = lang_counter[lang]
                for hashtag in hashtags:
                    if hashtag in text:
                        counter[hashtag] += 1


# need two counters, one for languaes and one for countries
print(f"lang_counter={lang_counter}")
