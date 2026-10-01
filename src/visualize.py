#!/usr/bin/env python3
import argparse, json, os, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--key', required=True)
parser.add_argument('--percent', action='store_true')
args = parser.parse_args()

with open(args.input_path) as f:
    counts = json.load(f)

if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# Top 10 by value, sorted low->high for display
top10 = sorted(sorted(counts[args.key].items(), key=lambda x: x[1], reverse=True)[:10],
               key=lambda x: x[1])

cols = [k for k, _ in top10]
vals = [v for _, v in top10]

plt.figure(figsize=(12, 6))
plt.bar(range(len(cols)), vals)
plt.xticks(range(len(cols)), cols, rotation=45, ha='right')
plt.ylabel('Value')
plt.title(f'Top 10 Keys for {args.key}')
plt.tight_layout()
plt.savefig(f'{args.key}_bar_graph.png')
print(f'Saved to {args.key}_bar_graph.png')
