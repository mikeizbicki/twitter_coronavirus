#!/usr/bin/env python3
"""Top-N bar charts for reduced hashtag/geo counts.

Handles both {"all": ...} (lang.json) and {"_all": ...} (country.json)
baselines, CJK hashtags (#코로나바이러스, #コロナウイルス), and --percent.
"""
import argparse, hashlib, json, os, re, sys, unicodedata
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

DEFAULT_KEYS = ['#coronavirus', '#코로나바이러스']
CJK = ('Noto Sans CJK', 'Noto Sans JP', 'Noto Sans KR', 'Noto Serif CJK',
       'Source Han', 'WenQuanYi', 'Droid Sans Fallback', 'IPAexGothic',
       'Hiragino', 'AppleGothic', 'Meiryo', 'Yu Gothic', 'MS Gothic')

def setup_fonts():
    plt.rcParams['axes.unicode_minus'] = False
    have = sorted({f.name for f in font_manager.fontManager.ttflist})
    fam = next((h for w in CJK for h in have if w.lower() in h.lower()), None)
    if fam:
        plt.rcParams['font.sans-serif'] = [fam, 'DejaVu Sans']
    else:
        print('warn: no CJK font; non-Latin ticks may show as boxes', file=sys.stderr)

def slug(s):
    a = re.sub(r'[^A-Za-z0-9]+', '_', unicodedata.normalize('NFKD', s)
               .encode('ascii', 'ignore').decode()).strip('_')
    return a[:40] or 'h_' + hashlib.sha1(s.encode()).hexdigest()[:8]

def baseline(counts):
    for k in ('_all', 'all'):
        if isinstance(counts.get(k), dict):
            return counts[k]
    raise SystemExit('no "_all"/"all" baseline in input')

def top_items(counts, key, top, percent, base):
    block = counts.get(key)
    if not isinstance(block, dict):
        print(f'warn: key {key!r} absent', file=sys.stderr)
        return []
    rows = []
    for k, v in block.items():
        v = float(v)
        if percent:
            d = base.get(k)
            if not d:
                print(f'warn: {key}: no baseline for {k!r}, skipped', file=sys.stderr)
                continue
            v /= float(d)
        rows.append((v, k))
    rows.sort(reverse=True)          # rank on the *plotted* quantity
    return sorted(rows[:top])        # low->high for display

def render(key, rows, percent, log, outdir, top):
    labels, vals = [k for _, k in rows], [v for v, _ in rows]
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(range(len(vals)), vals, color='#3b6ea5')
    if log:
        ax.set_yscale('log')
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_ylabel('share of _all' if percent else 'count')
    ax.set_title(f'Top {top} keys for {key}')
    for i, v in enumerate(vals):
        ax.text(i, v, f'{v:.3%}' if percent else f'{v:,.0f}',
                ha='center', va='bottom', fontsize=8)
    fig.tight_layout()
    path = os.path.join(outdir, f'{slug(key)}_bar_graph.png')
    fig.savefig(path, dpi=140)
    plt.close(fig)
    print(f'Saved to {path}')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input_path', required=True)
    p.add_argument('--key', action='append',
                   help=f'repeatable; default {DEFAULT_KEYS}')
    p.add_argument('--percent', action='store_true')
    p.add_argument('--log', action='store_true')
    p.add_argument('--top', type=int, default=10)
    p.add_argument('--outdir', default='.')
    args = p.parse_args()

    with open(args.input_path, encoding='utf-8') as f:
        counts = json.load(f)
    setup_fonts()
    os.makedirs(args.outdir, exist_ok=True)
    base = baseline(counts) if args.percent else {}
    for key in (args.key or DEFAULT_KEYS):
        rows = top_items(counts, key, args.top, args.percent, base)
        if rows:
            render(key, rows, args.percent, args.log, args.outdir, args.top)

if __name__ == '__main__':
    main()

