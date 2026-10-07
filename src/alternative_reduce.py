#!/usr/bin/env python3
import argparse, os, json, glob
from collections import defaultdict
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # CRITICAL: prevents interactive backend issues
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--hashtags', nargs='+', required=True, help='Hashtags to plot')
parser.add_argument('--output_file', default='hashtag_lineplot.png', help='Output PNG')
args = parser.parse_args()

data = defaultdict(lambda: defaultdict(int))
files = sorted(glob.glob('outputs/*.lang'))
print(f"Processing {len(files)} files...")

for fp in files:
    fn = os.path.basename(fp)
    try:
        d = fn.split('geoTwitter')[1].split('.zip')[0]
        year = 2000 + int(d.split('-')[0])
        doy = datetime(year, int(d.split('-')[1]), int(d.split('-')[2])).timetuple().tm_yday
    except Exception:
        print(f"skip {fn}"); continue

    with open(fp) as f: counts = json.load(f)
    for ht in args.hashtags:
        if ht in counts:
            data[ht][doy] = sum(counts[ht].values())

fig, ax = plt.subplots(figsize=(14,8))
for ht in args.hashtags:
    if ht in data:
        days = sorted(data[ht])
        ax.plot(days, [data[ht][d] for d in days], marker='o', ms=2, label=ht, lw=1.5)
    else:
        print(f"No data: {ht}")

ax.set_xlabel('Day of Year (2020)', fontsize=12)
ax.set_ylabel('Tweets', fontsize=12)
ax.set_title('Hashtag Usage Over Time in 2020', fontsize=14, fontweight='bold')
ax.legend(loc='best'); ax.grid(alpha=.3); fig.tight_layout()
fig.savefig(args.output_file, dpi=150)
print(f"Saved {args.output_file}")

