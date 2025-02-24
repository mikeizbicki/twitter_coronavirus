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
import matplotlib.pyplot as plt  # Import matplotlib for plotting

# Open the input JSON file
with open(args.input_path) as f:
    counts = json.load(f)

# If the percent flag is used, normalize the counts
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# Sort items by value in descending order first to get the top 10 keys
items = sorted(counts[args.key].items(), key=lambda item: item[1], reverse=True)
top_10 = items[:10]

# Now sort these top 10 keys in ascending order (low to high) by value
top_10 = sorted(top_10, key=lambda item: item[1])

# Separate the keys and values for plotting
keys = [k for k, v in top_10]
values = [v for k, v in top_10]

# Create the bar graph
plt.figure(figsize=(10, 6))
plt.bar(keys, values, color='skyblue')
plt.xlabel('Keys')
plt.ylabel('Values')
plt.title('Top 10 Keys for {}'.format(args.key))
plt.xticks(rotation=45)
plt.tight_layout()

# Generate a filename that is safe (remove any special characters from the key)
import re
safe_key = re.sub(r'[^A-Za-z0-9_]', '', args.key)
output_filename = 'plot_{}.png'.format(safe_key)

# Save the plot as a PNG file
plt.savefig(output_filename)
print('Bar graph saved as', output_filename)

