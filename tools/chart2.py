import json, sys, datetime as dt
hist = json.load(open(sys.argv[1]))
yet = [l.split('\t') for l in open(sys.argv[2]).read().strip().split('\n')]
def series(pairs):
    out=[]
    for d,v in pairs:
        if out and out[-1][0]==d: out[-1]=(d,v)
        else: out.append((d,v))
    return out
ign = series([(dt.date.fromisoformat(o['date']), o['after']) for o in hist])
ys  = series([(dt.date.fromisoformat(r[0]), int(r[6])) for r in yet])
end = dt.date(2026, 11, 22)
W, L, R = 1000, 60, 20
x0, x1 = dt.date(2022, 7, 1), dt.date(2026, 12, 31)
X = lambda d: L + (d - x0).days / (x1 - x0).days * (W - L - R)
out = []
def panel(top, h, pts, ymax, ticks, title, notes):
    Y = lambda v: top + (1 - v / ymax) * h
    out.append(f'<text x="{L}" y="{top-10}" class="ptitle">{title}</text>')
    for v in ticks:
        out.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" class="grid"/><text x="{L-8}" y="{Y(v)+5:.1f}" class="ytick">{v}</text>')
    p=[]
    for i,(d,v) in enumerate(pts):
        p.append(f"M{X(d):.1f},{Y(v):.1f}" if i==0 else f"H{X(d):.1f}V{Y(v):.1f}")
    p.append(f"H{X(end):.1f}")
    out.append(f'<path d="{"".join(p)}" class="line"/>')
    for d,v,t,dy,anc in notes:
        d=dt.date.fromisoformat(d)
        out.append(f'<circle cx="{X(d):.1f}" cy="{Y(v):.1f}" r="5" class="dot"/><text x="{X(d)+(8 if anc=="start" else 0):.1f}" y="{Y(v)+dy:.1f}" text-anchor="{anc}" class="note">{t}</text>')
H = 470
out.insert(0, f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="esmeta-ignore.json の件数とパースできないステップ数の推移">')
for yr in range(2023, 2027):
    xx = X(dt.date(yr, 1, 1))
    out.append(f'<line x1="{xx:.1f}" x2="{xx:.1f}" y1="30" y2="{H-40}" class="grid"/><text x="{xx:.1f}" y="{H-14}" class="xtick">{yr}</text>')
panel(40, 170, ign, 60, (0, 30, 60), "esmeta-ignore.json の件数（型エラーが残るアルゴリズム）",
      [("2022-11-02", 51, "導入 51", 26, "start"), ("2024-11-21", 43, "v0.5.0", -14, "middle"),
       ("2025-01-22", 10, "10", 24, "middle"), ("2026-11-12", 13, "13", 28, "middle")])
panel(270, 160, ys, 1000, (0, 500, 1000), "パースが完全でないステップ数（ESMeta が対応する版）",
      [("2022-08-20", 785, "785", -14, "start"), ("2026-11-21", 707, "707", -14, "middle")])
out.append('</svg>')
print("\n".join(out))
