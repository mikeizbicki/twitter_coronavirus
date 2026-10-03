import argparse, datetime, json, os, re, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

CJK = ('Noto Sans CJK', 'Noto Sans JP', 'Noto Sans KR', 'Source Han',
       'WenQuanYi', 'Droid Sans Fallback', 'IPAexGothic', 'Hiragino',
       'AppleGothic', 'Meiryo', 'Yu Gothic', 'MS Gothic')

def setup_fonts():
    plt.rcParams['axes.unicode_minus'] = False
    have = sorted({f.name for f in font_manager.fontManager.ttflist})
    fam = next((h for w in CJK for h in have if w.lower() in h.lower()), None)
    if fam:
        plt.rcParams['font.sans-serif'] = [fam, 'DejaVu Sans']

def day_of_year(name):
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', name)
    if not m:
        return None
    return datetime.date(*map(int, m.groups())).timetuple().tm_yday

def count_for(data, key):
    """Sum counts for `key`, tolerating {v: n}, a bare number, or absence."""
    block = data.get(key)
    if isinstance(block, dict):
        return sum(float(v) for v in block.values())
    if isinstance(block, (int, float)):
        return float(block)
    return 0.0

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--hashtags', nargs='+', required=True)
    p.add_argument('--input_dir', default='outputs')
    p.add_argument('--output_path', default='alternative_reduce.png')
    args = p.parse_args()

    files = sorted(f for f in os.listdir(args.input_dir) if f.endswith('.json'))
    series = {h: [0.0] * 366 for h in args.hashtags}

    for i, name in enumerate(files):
        doy = day_of_year(name) or i + 1
        if not 1 <= doy <= 366:
            continue
        with open(os.path.join(args.input_dir, name), encoding='utf-8') as f:
            data = json.load(f)
        for h in args.hashtags:
            series[h][doy - 1] += count_for(data, h)

    setup_fonts()
    fig, ax = plt.subplots(figsize=(12, 6))
    xs = list(range(1, 367))
    for h in args.hashtags:
        if not any(series[h]):
            print(f'warn: no data for {h!r}', file=sys.stderr)
        ax.plot(xs, series[h], linewidth=1.2, label=h)
    ax.set_xlabel('day of year')
    ax.set_ylabel('tweet count')
    ax.set_title('Daily tweet counts by hashtag')
    ax.legend()
    fig.tight_layout()
    fig.savefig(args.output_path, dpi=140)
    plt.close(fig)
    print(f'Saved to {args.output_path}')

if __name__ == '__main__':
    main()

