import argparse, json, os, glob, re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Try CJK fonts for Korean support (qwen created function)
def setup_cjk_font():
    from matplotlib import font_manager
    cjk_fonts = ['Noto Sans CJK KR', 'Noto Sans CJK', 'WenQuanYi Zen Hei',
                 'WenQuanYi Micro Hei', 'SimHei', 'AR PL UMing CN', 'DejaVu Sans']
    available = {f.name for f in font_manager.fontManager.ttflist}
    for f in cjk_fonts:
        if f in available:
            plt.rcParams['font.sans-serif'] = [f, 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
            return f
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    return 'DejaVu Sans'

parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--key', required=True)
args = parser.parse_args()

files = glob.glob(args.input_path)
assert files, f"No files match {args.input_path}"

font_used = setup_cjk_font()

out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.makedirs(out_dir, exist_ok=True)

for fpath in files:
    with open(fpath) as f:
        counts = json.load(f)

    # Infer label from filename
    base = os.path.basename(fpath)
    if 'lang' in base.lower():
        entity = 'Languages'
    elif 'country' in base.lower():
        entity = 'Countries'
    else:
        entity = os.path.splitext(base)[0].capitalize()

    title_suffix = f' for Tweets with {args.key}'

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
    plt.ylabel(f'Count')
    plt.title(f'Top 10 {entity}{title_suffix}')
    plt.tight_layout()
    out = os.path.join(out_dir, f'{os.path.splitext(base)[0]}_{re.sub(r"\\W", "_", args.key)}_bar.png')
    plt.savefig(out)
    plt.close()
    print(f'Saved to {out}')
