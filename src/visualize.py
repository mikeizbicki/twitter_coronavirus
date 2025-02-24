#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--key', required=True)
parser.add_argument('--percent', action='store_true')
args = parser.parse_args()

import os
import json
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import re

# Open the input JSON file
with open(args.input_path) as f:
    counts = json.load(f)

# Normalize counts if requested
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# Get the items sorted by value (top 10), then re-sort in ascending order for the graph
items = sorted(counts[args.key].items(), key=lambda item: item[1], reverse=True)
top_10 = items[:10]
top_10 = sorted(top_10, key=lambda item: item[1])

keys = [k for k, v in top_10]
values = [v for k, v in top_10]

# Create the bar graph
plt.figure(figsize=(10, 6))
plt.bar(keys, values, color='skyblue')
plt.xlabel('Keys')
plt.ylabel('Values')
plt.title(f'Top 10 Keys for {args.key}')
plt.xticks(rotation=45)
plt.tight_layout()

# Create a unique output filename based on the input file and key
input_base = os.path.splitext(os.path.basename(args.input_path))[0]
safe_key = re.sub(r'[^\w]', '_', args.key, flags=re.UNICODE)
output_filename = f'plot_{input_base}_{safe_key}.png'

plt.savefig(output_filename)
print('Bar graph saved as', output_filename)

