import argparse, json, os, glob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--key', required=True)
parser.add_argument('--percent', action='store_true')
args = parser.parse_args()

files = glob.glob(args.input_path)
assert files, f"No files match {args.input_path}"

out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.makedirs(out_dir, exist_ok=True)

for fpath in files:
    with open(fpath) as f:
        counts = json.load(f)

    if args.percent:
        for k in counts[args.key]:
            counts[args.key][k] /= counts['_all'][k]

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
    out = os.path.join(out_dir, f'{os.path.basename(fpath).replace(".json", "")}_{args.key}_bar.png')
    plt.savefig(out)
    plt.close()
    print(f'Saved to {out}')
