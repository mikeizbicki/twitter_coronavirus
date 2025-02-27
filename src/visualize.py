#!/usr/bin/env python3

import argparse
import os
import json
import matplotlib.pyplot as plt
import re

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True, help="Path to input JSON file")
parser.add_argument('--key', required=True, help="Hashtag or keyword to visualize")
parser.add_argument('--percent', action='store_true', help="Normalize counts as percentage")
args = parser.parse_args()

# Open the input JSON file
with open(args.input_path) as f:
    counts = json.load(f)

# Normalize counts if requested
if args.percent:
    for k in counts.get(args.key, {}):  # Using .get() to avoid KeyError
        counts[args.key][k] /= counts['_all'][k]

# Get the top 10 items sorted by value
items = sorted(counts.get(args.key, {}).items(), key=lambda item: item[1], reverse=True)[:10]
items = sorted(items, key=lambda item: item[1])  # Sort again for better visualization

if not items:
    print(f"No data found for key: {args.key}")
    exit()

keys = [k for k, v in items]
values = [v for k, v in items]

# Determine axis label based on input file
if "country" in args.input_path:
    x_label = "Country"
elif "lang" in args.input_path:
    x_label = "Language"
else:
    x_label = "Category"

# Create the bar graph
plt.figure(figsize=(10, 6))
plt.bar(keys, values, color='skyblue')
plt.xlabel(x_label)
plt.ylabel('Tweet Count' if not args.percent else 'Percentage')
plt.title(f'Top 10 {x_label}s for {args.key}')
plt.xticks(rotation=45)
plt.tight_layout()

# Generate output filename
input_base = os.path.splitext(os.path.basename(args.input_path))[0]
safe_key = re.sub(r'[^\w]', '_', args.key, flags=re.UNICODE)
output_filename = f'plot_{input_base}_{safe_key}.png'

plt.savefig(output_filename)
print(f'Bar graph saved as {output_filename}')

