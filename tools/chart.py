import json, sys, datetime as dt
h = json.load(open(sys.argv[1]))
pts = []
for o in h:
    d = dt.date.fromisoformat(o['date'])
    if pts and pts[-1][0] == d: pts[-1] = (d, o['after'])
    else: pts.append((d, o['after']))
end = dt.date(2026, 11, 22)
W, H, L, R, T, B = 1000, 380, 50, 20, 20, 40
x0, x1 = dt.date(2022, 10, 1), dt.date(2026, 12, 31)
X = lambda d: L + (d - x0).days / (x1 - x0).days * (W - L - R)
Y = lambda v: T + (1 - v / 60) * (H - T - B)
path = []
for i, (d, v) in enumerate(pts):
    if i == 0: path.append(f"M{X(d):.1f},{Y(v):.1f}")
    else: path.append(f"H{X(d):.1f}V{Y(v):.1f}")
path.append(f"H{X(end):.1f}")
s = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="esmeta-ignore.json の件数の推移">']
for v in (0, 20, 40, 60):
    s.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" class="grid"/><text x="{L-8}" y="{Y(v)+5:.1f}" class="ytick">{v}</text>')
for yr in range(2023, 2027):
    xx = X(dt.date(yr, 1, 1))
    s.append(f'<line x1="{xx:.1f}" x2="{xx:.1f}" y1="{T}" y2="{H-B}" class="grid"/><text x="{xx:.1f}" y="{H-B+26}" class="xtick">{yr}</text>')
s.append(f'<path d="{"".join(path)}" class="line"/>')
notes = [("2022-11-02", 51, "導入 51", 26, "start"), ("2022-11-30", 55, "最大 55", -12, "start"),
         ("2024-11-21", 43, "v0.5.0", -14, "middle"), ("2025-01-22", 10, "10", 24, "middle"),
         ("2025-02-18", 15, "Import Attributes", -14, "start"), ("2026-11-12", 13, "13", 28, "middle")]
for d, v, t, dy, anc in notes:
    d = dt.date.fromisoformat(d)
    s.append(f'<circle cx="{X(d):.1f}" cy="{Y(v):.1f}" r="5" class="dot"/><text x="{X(d)+(8 if anc=="start" else 0):.1f}" y="{Y(v)+dy:.1f}" text-anchor="{anc}" class="note">{t}</text>')
s.append('</svg>')
print("\n".join(s))
