#!/bin/python3

# load command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--output_folder', default='map_outputs')
args = parser.parse_args()

# imports
from collections import Counter
import datetime
import json
import os
import time
import zipfile

# define mapping variables
lang = Counter()

# loop over input file
with zipfile.ZipFile(args.input_path, 'r') as zip_ref:
    print("args.input_path=", args.input_path)
    for file_info in zip_ref.infolist():
        file_name = file_info.filename
        print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {file_name}')
        
        with zip_ref.open(file_name) as file:
            for linenum, line in enumerate(file.readlines()):
                # standard way to read
                # jsonl files
                data = json.loads(line)
                lang[data['lang']] += 1
                #print("data['lang']=", data['lang'])
                #import code
                #code.interact(local=locals())
                if linenum > 10:
                    break
            #print(file_name, contents)
        break

import pprint
pprint.pprint(lang)

# save results to file
os.makedirs(args.output_folder, exist_ok=True)
output_filename = args.output_folder + '/' + os.path.basename(args.input_path)
with open(output_filename, 'w') as fout:
    json.dump(lang, fout)

    # json.dumps # s = str
