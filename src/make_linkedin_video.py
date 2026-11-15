"""Animated LinkedIn video (4:5 portrait, 1080x1350) with the key charts.

4:5 is the tallest format LinkedIn shows in the feed without cropping,
so the video fills the full width of the post on mobile and desktop.

Usage:
    python src/make_linkedin_video.py            # render the full video
    python src/make_linkedin_video.py --preview  # render a few still frames only
"""
import glob
import subprocess
import sys
import warnings
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib import patheffects as pe

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "video"
W, H, FPS = 1080, 1350, 30

# Inter font: Linux system folder, Windows (user or system install), or a local fonts/ folder
FONT_PATTERNS = [
    "/usr/share/fonts/opentype/inter/*.otf",
    str(Path.home() / "AppData/Local/Microsoft/Windows/Fonts/Inter*"),
    "C:/Windows/Fonts/Inter*",
    str(ROOT / "fonts" / "Inter*"),
]
for pattern in FONT_PATTERNS:
    for f in glob.glob(pattern):
        font_manager.fontManager.addfont(f)
_installed = {f.name for f in font_manager.fontManager.ttflist}
plt.rcParams["font.family"] = "Inter" if "Inter" in _installed else "DejaVu Sans"
DISPLAY = "Inter Display" if "Inter Display" in _installed else plt.rcParams["font.family"]

# palette
BG = np.array([9, 13, 27], dtype=np.float32) / 255
TEXT = "#F4F6FB"
MUTED = "#8E98AE"
DIM = "#4A5470"
GRID = "#1F2842"
CARD = "#121A31"
CARD_EDGE = "#243052"
CORAL = "#FF5C77"
HALO = [pe.withStroke(linewidth=5, foreground="#0B1022")]
TEAL = "#2DE3C3"
AMBER = "#FFC247"
BLUE = "#6C8CFF"


# ---------------------------------------------------------------- helpers
def clamp(x):
    return max(0.0, min(1.0, x))


def ease(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_io(x):
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def back(x):
    x = clamp(x)
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def prog(t, start, dur=0.5):
    return ease((t - start) / dur)


def txt(O, x, y, s, size, t, start=0.0, dur=0.5, color=TEXT, weight="regular",
        ha="left", va="baseline", rise=16, family="Inter", alpha=1.0, **kw):
    p = prog(t, start, dur)
    if p <= 0:
        return None
    lh = kw.pop("lh", None)
    if lh and "\n" in s:
        for j, line in enumerate(s.split("\n")):
            O.text(x, y - j * lh - rise * (1 - p), line, fontsize=size, color=color,
                   alpha=p * alpha, fontweight=weight, ha=ha, va=va, family=family, **kw)
        return None
    return O.text(x, y - rise * (1 - p), s, fontsize=size, color=color, alpha=p * alpha,
                  fontweight=weight, ha=ha, va=va, family=family, **kw)


def rbox(O, x, y, w, h, color, alpha=1.0, r=None, ec="none", lw=0, z=1):
    if w <= 0.5 or h <= 0.5:
        return
    r = min(h / 2, w / 2) if r is None else min(r, h / 2, w / 2)
    O.add_patch(FancyBboxPatch((x + r, y + r), max(w - 2 * r, 0.01), max(h - 2 * r, 0.01),
                               boxstyle=f"round,pad={r}", fc=color, ec=ec, lw=lw,
                               alpha=alpha, zorder=z))


def card(O, x, y, w, h, t, start, dur=0.5):
    p = prog(t, start, dur)
    if p <= 0:
        return 0
    rbox(O, x, y - 14 * (1 - p), w, h, CARD, alpha=0.92 * p, r=26, ec=CARD_EDGE, lw=1.2)
    return p


def dot(O, x, y, r, color, alpha=1.0, z=5):
    O.add_patch(Circle((x, y), r, fc=color, ec="none", alpha=alpha, zorder=z))


def header(O, t, chip, title, subtitle, accent):
    txt(O, 80, 1252, chip, 15, t, 0.0, 0.4, color=accent, weight="bold")
    txt(O, 80, 1228, title, 39, t, 0.08, 0.55, weight="bold", family=DISPLAY,
        va="top", lh=58)
    txt(O, 80, 1078, subtitle, 17, t, 0.25, 0.5, color=MUTED, va="top", lh=31)


def footer(O, t, source):
    txt(O, 80, 48, source, 12, t, 0.3, 0.6, color=DIM, rise=0)
    txt(O, 1000, 48, "Anna Hortiuc", 12, t, 0.3, 0.6, color=DIM, rise=0, ha="right",
        weight="semibold")


def legend(O, t, items, y=1000, start=0.4):
    x = 80
    for label, color in items:
        p = prog(t, start, 0.4)
        if p > 0:
            dot(O, x + 8, y + 7, 8, color, alpha=p)
            O.text(x + 26, y, label, fontsize=15, color=TEXT, alpha=p * 0.9)
        x += 30 + len(label) * 9.6 + 34
        start += 0.1


# ---------------------------------------------------------------- scenes
def s_hook(O, t, d):
    t = 99.0  # title card is shown complete from the first frame, so it doubles as the cover
    txt(O, 80, 1170, "THE GERMAN LABOUR MARKET PARADOX", 16, t, -1, 0.1, color=AMBER, weight="bold")
    lines = [("Germany has", TEXT), ("unemployment", CORAL), ("and a skills", TEXT),
             ("shortage.", TEAL)]
    for k, (s, c) in enumerate(lines):
        txt(O, 76, 1040 - k * 102, s, 66, t, -1 if k == 0 else 0.15 + 0.22 * k, 0.5,
            color=c, weight="bold", family=DISPLAY, rise=30)
    txt(O, 80, 560, "At the same time.", 34, t, 1.3, 0.6, color=MUTED, weight="semibold",
        family=DISPLAY)
    p = card(O, 80, 250, 920, 170, t, 2.4)
    if p:
        txt(O, 120, 360, "How can both be true?", 24, t, 2.55, 0.5, weight="bold")
        txt(O, 120, 300, "6 charts from official German labour market data", 17, t, 2.7, 0.5,
            color=MUTED)
    footer(O, t, "Data: Bundesagentur für Arbeit, IAB")


def s_mismatch(O, t, d):
    header(O, t, "01 · THE MISMATCH", "Half the unemployed\nlook for unskilled jobs",
           "Share of all unemployed vs. share of all vacancies, by skill level", CORAL)
    legend(O, t, [("Share of unemployed", CORAL), ("Share of vacancies", TEAL)], y=995)
    levels = [("Helfer", "unskilled", 50.5, 17.1), ("Fachkraft", "vocational training", 28.0, 60.7),
              ("Spezialist", "advanced vocational", 7.8, 12.9), ("Experte", "university degree", 8.1, 9.3)]
    sx = 11.6
    focus = prog(t, 4.0, 0.6)
    for k, (name, desc, u, v) in enumerate(levels):
        gy = 920 - k * 142
        st = 0.7 + 0.28 * k
        a = 1 - 0.6 * focus if k >= 2 else 1
        txt(O, 80, gy, name, 19, t, st, 0.4, weight="bold", alpha=a)
        txt(O, 1000, gy, desc, 15, t, st, 0.4, color=MUTED, ha="right", alpha=a)
        for j, (val, col) in enumerate([(u, CORAL), (v, TEAL)]):
            p = prog(t, st + 0.15 + 0.12 * j, 1.0)
            if p <= 0:
                continue
            by = gy - 52 - j * 40
            rbox(O, 80, by, 920, 30, GRID, alpha=0.5 * a)
            w = val * sx * p
            rbox(O, 80, by, max(w, 31), 30, col, alpha=a)
            O.text(80 + max(w, 31) + 12, by + 7, f"{val * p:.1f}%", fontsize=16, color=col,
                   fontweight="bold", alpha=a)
    for k, (num, line1, line2, col, st) in enumerate([
        (13.3, "unemployed per vacancy", "Helfer (unskilled)", CORAL, 4.4),
        (2.1, "unemployed per vacancy", "Fachkraft (vocational)", TEAL, 4.7),
    ]):
        x = 80 + k * 470
        p = card(O, x, 130, 450, 210, t, st)
        if p:
            n = num * ease((t - st) / 1.0)
            O.text(x + 34, 245, f"{n:.1f}", fontsize=56, color=col, fontweight="bold",
                   family=DISPLAY, alpha=p)
            O.text(x + 36, 205, line1, fontsize=16, color=TEXT, alpha=p)
            O.text(x + 36, 172, line2, fontsize=15, color=MUTED, alpha=p)
    footer(O, t, "Source: BA, Arbeitsmarkt nach Berufen, Oct 2026")


TREND = {
    "years": np.arange(2019, 2026),
    "Fachkräfte": np.array([95, 66, 72, 106, 99, 91, 84]),
    "Spezialisten": np.array([44, 31, 40, 56, 55, 47, 48]),
    "Experten": np.array([39, 29, 34, 40, 32, 25, 25]),
}


def s_trend(O, t, d):
    header(O, t, "02 · THE CYCLE", "Shortages follow\nthe business cycle",
           "Number of shortage occupations in Germany, by skill level", TEAL)
    legend(O, t, [("Fachkraft", TEAL), ("Spezialist", BLUE), ("Experte", AMBER)], y=995)
    x0, x1, y0, ymax, vmax = 140, 960, 330, 900, 250
    X = lambda yr: x0 + (yr - 2019) / 6 * (x1 - x0)
    Y = lambda v: y0 + v / vmax * (ymax - y0)
    pg = prog(t, 0.4, 0.6)
    for v in range(0, 201, 50):
        if pg > 0:
            O.plot([x0, x1], [Y(v), Y(v)], color=GRID, lw=1.2, alpha=pg, zorder=0)
            O.text(x0 - 18, Y(v) - 6, str(v), fontsize=13, color=MUTED, ha="right", alpha=pg)
    for yr in range(2019, 2026):
        if pg > 0:
            O.text(X(yr), y0 - 38, str(yr), fontsize=14, color=MUTED, ha="center", alpha=pg)
    yrs = TREND["years"]
    xc = 2019 + 6 * ease_io((t - 0.9) / 4.2)
    if t > 0.9:
        xs = np.linspace(2019, xc, 240)
        f = np.interp(xs, yrs, TREND["Fachkräfte"])
        s = np.interp(xs, yrs, TREND["Spezialisten"])
        e = np.interp(xs, yrs, TREND["Experten"])
        px = [X(v) for v in xs]
        O.fill_between(px, Y(0), [Y(v) for v in f], color=TEAL, alpha=0.85, lw=0, zorder=2)
        O.fill_between(px, [Y(v) for v in f], [Y(v) for v in f + s], color=BLUE, alpha=0.85,
                       lw=0, zorder=2)
        O.fill_between(px, [Y(v) for v in f + s], [Y(v) for v in f + s + e], color=AMBER,
                       alpha=0.85, lw=0, zorder=2)
        tot = f + s + e
        O.plot(px, [Y(v) for v in tot], color=TEXT, lw=3, zorder=3, solid_capstyle="round")
        dot(O, px[-1], Y(tot[-1]), 16, TEXT, alpha=0.18, z=4)
        dot(O, px[-1], Y(tot[-1]), 8, TEXT, z=5)
        cur = tot[-1]
        O.text(x1, 930, f"{cur:.0f}", fontsize=52, color=TEXT, fontweight="bold",
               family=DISPLAY, ha="right")
        O.text(x1, 905, f"shortage occupations · {int(round(xc - 0.49))}", fontsize=14,
               color=MUTED, ha="right")
    for yr, val, label, dy in [(2020, 126, "Covid", 30), (2022, 202, "Peak", 30),
                               (2025, 157, "2025", 30)]:
        st = 0.9 + 4.2 * (yr - 2019) / 6 * 0.85
        p = prog(t, st, 0.5)
        if p > 0 and xc >= yr - 0.02:
            O.text(X(yr), Y(val) + dy, f"{label}\n{val}" if dy < 0 else f"{label}: {val}",
                   fontsize=15, color=TEXT, fontweight="bold", ha="center", alpha=p, zorder=6,
                   linespacing=1.2, path_effects=HALO)
    p = card(O, 80, 110, 920, 120, t, 5.6)
    if p:
        O.text(116, 180, "Shortages at Experte level fell fastest since 2022:", fontsize=17,
               color=TEXT, alpha=p)
        O.text(116, 142, "40 → 25 occupations (−38%). Software development is no longer one.",
               fontsize=15, color=MUTED, alpha=p)
    footer(O, t, "Source: BA, Engpassanalyse 2019–2025")


GROWTH = [
    ("IT & communication", 67.2), ("Humanities, social sciences & economics", 54.5),
    ("Education & social work", 43.8), ("Geology, geography & environment", 41.6),
    ("Architecture & surveying", 31.8), ("Law & administration", 28.1),
    ("Arts, crafts & product design", -3.6), ("Plastics & wood", -10.6),
    ("Paper & printing", -12.9), ("Glass, ceramics & raw materials", -14.4),
    ("Metalworking", -17.2), ("Textiles & leather", -18.8),
]


def s_growth(O, t, d):
    header(O, t, "03 · STRUCTURAL CHANGE", "Production shrinks,\nwork with people grows",
           "Employment change 2015–2025: fastest-growing and\nshrinking occupation groups (6 each, out of 36)", TEAL)
    sx = 9.4
    zx = 80 + 20 * sx
    top, rh = 955, 53
    pg = prog(t, 0.3, 0.5)
    for k, (name, v) in enumerate(GROWTH):
        y = top - k * rh - (40 if k >= 6 else 0)
        st = (0.6 + 0.11 * k) if k < 6 else (2.3 + 0.11 * (k - 6))
        p = prog(t, st, 0.9)
        if p <= 0:
            continue
        col = TEAL if v > 0 else CORAL
        O.text(80, y, name, fontsize=14, color=TEXT, alpha=min(1, p * 1.5) * 0.92,
               path_effects=HALO, zorder=6)
        by = y - 32
        w = abs(v) * sx * p
        if v > 0:
            rbox(O, zx, by, w, 22, col, r=5)
            O.text(zx + w + 10, by + 4, f"+{v * p:.1f}%", fontsize=15, color=col,
                   fontweight="bold")
        else:
            rbox(O, zx - w, by, w, 22, col, r=5)
            O.text(zx + 12, by + 4, f"{v * p:.1f}%".replace("-", "−"), fontsize=15, color=col, fontweight="bold")
    if t > 2.0:
        txt(O, 80, top - 6 * rh - 10, "· · ·   25 groups in between", 13, t, 2.0, 0.4,
            color=DIM, rise=0)
    if pg > 0:
        O.plot([zx, zx], [250, 975], color=MUTED, lw=1.2, alpha=0.5 * pg, zorder=0)
    pa = prog(t, 3.8, 0.6)
    if pa > 0:
        ax = zx + 13.4 * sx
        O.plot([ax, ax], [250, 975], color=AMBER, lw=1.6, ls=(0, (4, 4)), alpha=pa, zorder=0)
        O.text(ax + 8, 228, "All jobs: +13.4%", fontsize=14, color=AMBER, fontweight="bold",
               alpha=pa)
    p = card(O, 80, 95, 920, 105, t, 4.6)
    if p:
        O.text(116, 160, "Metalworking lost 228,000 jobs.", fontsize=17, color=TEXT, alpha=p)
        O.text(116, 124, "Education & social work gained 669,000 — the largest absolute gain.",
               fontsize=15, color=MUTED, alpha=p)
    footer(O, t, "Source: BA, Beschäftigungsstatistik (June 2015 vs June 2025)")


AUTO = [
    ("Agriculture & gardening", 50.3, 9), ("Production", 87.9, -15),
    ("Production technology", 74.8, 6), ("Construction", 42.5, 14),
    ("Food & hospitality", 49.5, 10), ("Healthcare", 26.5, 22),
    ("Social & cultural services", 13.5, 39), ("Retail & trade", 65.9, 8),
    ("Management & organisation", 68.0, 11), ("Business services", 66.5, 17),
    ("IT & science services", 52.5, 46), ("Security", 42.5, 20),
    ("Transport & logistics", 61.2, 14), ("Cleaning", 45.4, 13),
]
def s_auto(O, t, d):
    header(O, t, "04 · AUTOMATION", "The more automatable,\nthe slower the growth",
           "14 occupation segments: share of tasks that could be automated\n(IAB 2022) vs. employment change 2015–2025", AMBER)
    x0, x1, y0, y1 = 150, 990, 300, 930
    X = lambda v: x0 + v / 100 * (x1 - x0)
    Y = lambda v: y0 + (v + 20) / 70 * (y1 - y0)
    pg = prog(t, 0.4, 0.6)
    if pg > 0:
        for v in range(-20, 51, 10):
            O.plot([x0, x1], [Y(v), Y(v)], color=TEXT if v == 0 else GRID,
                   lw=1.2, alpha=pg * (0.35 if v == 0 else 1), zorder=0)
            O.text(x0 - 16, Y(v) - 6, f"{v:+d}%".replace("-", "−") if v else "0", fontsize=13, color=MUTED,
                   ha="right", alpha=pg)
        for v in range(0, 101, 25):
            O.text(X(v), y0 - 34, f"{v}%", fontsize=13, color=MUTED, ha="center", alpha=pg)
        O.text((x0 + x1) / 2, y0 - 70, "Share of automatable tasks →", fontsize=14,
               color=MUTED, ha="center", alpha=pg)
        O.text(48, (y0 + y1) / 2, "Employment change →", fontsize=14, color=MUTED,
               ha="center", va="center", rotation=90, alpha=pg)
    xs = np.array([a for _, a, _ in AUTO])
    ys = np.array([g for _, _, g in AUTO])
    m, b = np.polyfit(xs, ys, 1)
    pl = ease_io((t - 2.8) / 1.0)
    if pl > 0:
        xa, xb = 10, 10 + (90 - 10) * pl
        O.plot([X(xa), X(xb)], [Y(m * xa + b), Y(m * xb + b)], color=TEXT, lw=2.4,
               alpha=0.55, zorder=2, solid_capstyle="round")
    hl = prog(t, 4.4, 0.5)
    special = {"Production": CORAL, "Social & cultural services": TEAL,
               "IT & science services": AMBER}
    for k, (name, a, g) in enumerate(AUTO):
        p = back((t - (0.8 + 0.12 * k)) / 0.5)
        if p <= 0:
            continue
        col = special.get(name, BLUE)
        alpha = 1 - 0.55 * hl if name not in special else 1
        dot(O, X(a), Y(g), 13 * p, col, alpha=alpha, z=5)
        dot(O, X(a), Y(g), 22 * p, col, alpha=0.18 * alpha, z=4)
    if hl > 0:
        O.text(X(87.9) - 26, Y(-15), "Production: 88% automatable,\n−15% jobs",
               fontsize=14, color=CORAL, fontweight="bold", ha="right", va="center",
               alpha=hl, linespacing=1.25, path_effects=HALO, zorder=7)
        O.text(X(13.5) - 10, Y(39) + 26, "Social & cultural: 13.5% → +39%", fontsize=14,
               color=TEAL, fontweight="bold", alpha=hl, path_effects=HALO, zorder=7)
        pulse = 1 + 0.25 * np.sin((t - 4.4) * 5)
        O.add_patch(Circle((X(52.5), Y(46)), 30 * pulse, fc="none", ec=AMBER, lw=2,
                           alpha=hl * 0.8, zorder=6))
        O.text(X(52.5) + 44, Y(46) - 6, "IT: the exception", fontsize=15, color=AMBER,
               fontweight="bold", alpha=hl)
    p = card(O, 620, 690, 330, 120, t, 3.6)
    if p:
        O.text(650, 750, "r = −0.69", fontsize=34, color=TEXT, fontweight="bold",
               family=DISPLAY, alpha=p)
        O.text(652, 715, "strong negative correlation", fontsize=13, color=MUTED, alpha=p)
    p = card(O, 80, 95, 920, 105, t, 5.2)
    if p:
        O.text(116, 160, "IT's automation potential rose most (generative AI) —", fontsize=17,
               color=TEXT, alpha=p)
        O.text(116, 124, "yet it grew fastest. An early signal of change?", fontsize=15,
               color=MUTED, alpha=p)
    footer(O, t, "Source: BA, Strukturwandel nach Berufen; IAB-Kurzbericht 5/2024")


REGIONS = [("Berlin", 39.8, 5.0), ("Bremen", 27.5, 2.6), ("Hamburg", 18.9, 2.7),
           ("Saarland", 17.6, 2.5), ("Nordrhein-Westfalen", 17.5, 2.1),
           ("Sachsen-Anhalt", 17.3, 2.3), ("Sachsen", 16.7, 2.3),
           ("Mecklenburg-Vorpommern", 13.3, 2.0), ("Niedersachsen", 12.2, 2.0),
           ("Schleswig-Holstein", 11.9, 1.9), ("Hessen", 11.3, 2.3), ("Thüringen", 10.8, 2.2),
           ("Brandenburg", 10.7, 1.9), ("Rheinland-Pfalz", 10.0, 1.8),
           ("Baden-Württemberg", 9.7, 2.0), ("Bayern", 7.7, 1.4)]


def s_regions(O, t, d):
    header(O, t, "05 · REGIONS", "The paradox exists\nin every state",
           "Unemployed per vacancy, by state and skill level", BLUE)
    legend(O, t, [("Fachkraft (vocational)", TEAL), ("Helfer (unskilled)", CORAL)], y=1000)
    x0, x1 = 400, 960
    X = lambda v: x0 + v / 42 * (x1 - x0)
    top, rh = 940, 39
    pg = prog(t, 0.3, 0.5)
    if pg > 0:
        for v in range(0, 41, 10):
            O.plot([X(v), X(v)], [top - 16 * rh + 10, top + 22], color=GRID, lw=1.2,
                   alpha=pg, zorder=0)
            O.text(X(v), top - 16 * rh - 18, str(v), fontsize=13, color=MUTED, ha="center",
                   alpha=pg)
    for k, (name, hf, fk) in enumerate(REGIONS):
        y = top - k * rh
        st = 0.6 + 0.09 * k
        p = prog(t, st, 0.4)
        if p <= 0:
            continue
        is_home = name == "Hessen"   # highlight the author's home state
        O.text(80, y - 5, name + ("  · Frankfurt" if is_home else ""), fontsize=14,
               color=AMBER if is_home else TEXT, fontweight="bold" if is_home else "regular",
               alpha=p * 0.92)
        pl = ease_io((t - st - 0.2) / 0.9)
        xe = X(fk + (hf - fk) * pl)
        O.plot([X(fk), xe], [y, y], color=CORAL, lw=3, alpha=0.45, zorder=3,
               solid_capstyle="round")
        dot(O, X(fk), y, 8 * p, TEAL, z=5)
        if pl > 0:
            dot(O, xe, y, 8, CORAL, z=5)
            O.text(xe + 14, y - 5, f"{hf * pl:.1f}", fontsize=13, color=CORAL,
                   fontweight="bold", alpha=pl)
    p = card(O, 80, 95, 920, 105, t, 4.8)
    if p:
        O.text(116, 160, "Unskilled: 7.7 (Bayern) to 39.8 (Berlin) unemployed per vacancy.",
               fontsize=17, color=TEXT, alpha=p)
        O.text(116, 124, "Vocational level: only 1.4 to 5.0 everywhere.", fontsize=15,
               color=MUTED, alpha=p)
    footer(O, t, "Source: BA, Arbeitsmarkt nach Berufen, Oct 2026")


def s_next(O, t, d):
    header(O, t, "06 · WHAT COMES NEXT", "Three signals\nfor the future",
           "Demography, wages and AI are already moving the gap", AMBER)
    items = [
        ("+67%", AMBER, ["IT employment since 2015 —", "yet only 7% of IT occupations",
                         "are still in shortage"], 1.0, None),
        ("22.4%", CORAL, ["of employees are 55–64:", "7.8 million retire within",
                          "about ten years"], 1.8, None),
        ("+14.2%", TEAL, ["wage growth in shortage", "occupations vs. +10.4%",
                          "in non-shortage ones"], 2.6, None),
    ]
    for k, (num, col, lines, st, _) in enumerate(items):
        y = 770 - k * 235
        p = card(O, 80, y, 920, 205, t, st)
        if not p:
            continue
        rbox(O, 80, y, 8, 205, col, alpha=p, r=4)
        val = float(num.strip("+%"))
        n = val * ease((t - st) / 1.1)
        sign = "+" if num.startswith("+") else ""
        O.text(124, y + 78, f"{sign}{n:.1f}%" if "." in num else f"{sign}{n:.0f}%", fontsize=58,
               color=col, fontweight="bold", family=DISPLAY, alpha=p)
        for j, line in enumerate(lines):
            O.text(470, y + 138 - j * 36, line, fontsize=18,
                   color=TEXT if j == 0 else MUTED, alpha=p)
    txt(O, 80, 175, "Will AI close the gap —", 24, t, 4.0, 0.6, weight="bold", family=DISPLAY)
    txt(O, 80, 132, "or shift unemployment towards office jobs?", 24, t, 4.2, 0.6,
        weight="bold", family=DISPLAY, color=AMBER)
    footer(O, t, "Source: BA Beschäftigungs- & Entgeltstatistik, Engpassanalyse")


def s_outro(O, t, d):
    txt(O, 80, 1170, "IN ONE SENTENCE", 16, t, 0.0, 0.4, color=AMBER, weight="bold")
    txt(O, 76, 1050, "Germany doesn’t", 60, t, 0.15, 0.5, weight="bold", family=DISPLAY, rise=26)
    txt(O, 76, 960, "lack people.", 60, t, 0.3, 0.5, weight="bold", family=DISPLAY, rise=26)
    txt(O, 76, 850, "It lacks people with", 60, t, 1.0, 0.5, weight="bold", family=DISPLAY,
        rise=26, color=TEAL)
    txt(O, 76, 760, "the right skills.", 60, t, 1.15, 0.5, weight="bold", family=DISPLAY,
        rise=26, color=TEAL)
    txt(O, 80, 660, "Half of the unemployed look for unskilled jobs,", 19, t, 1.8, 0.5,
        color=MUTED)
    txt(O, 80, 628, "while six in ten vacancies need vocational training.", 19, t, 1.9, 0.5,
        color=MUTED)
    p = card(O, 80, 250, 920, 250, t, 2.6)
    if p:
        O.text(120, 440, "Full analysis, data & code", fontsize=16, color=MUTED, alpha=p)
        O.text(120, 390, "github.com/anna-hortiuc/", fontsize=24, color=TEXT,
               fontweight="semibold", alpha=p)
        O.text(120, 350, "german-labour-market-paradox", fontsize=24, color=TEXT,
               fontweight="semibold", alpha=p)
        O.text(120, 290, "Anna Hortiuc · Data analysis", fontsize=16, color=AMBER,
               fontweight="semibold", alpha=p)
    footer(O, t, "Data: Bundesagentur für Arbeit, IAB · own calculations")


SCENES = [(s_hook, 5.0), (s_mismatch, 8.5), (s_trend, 8.5), (s_growth, 8.0),
          (s_auto, 9.0), (s_regions, 8.0), (s_next, 7.5), (s_outro, 6.5)]
STARTS = np.cumsum([0] + [d for _, d in SCENES])
TOTAL = STARTS[-1]
FADE = 0.3

# ---------------------------------------------------------------- frame rendering
YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
VGRAD = (1.0 - 0.35 * (YY / H))[..., None]


def background(gt):
    img = np.empty((H, W, 3), dtype=np.float32)
    img[:] = BG
    img *= VGRAD
    blobs = [
        (W * (0.85 + 0.08 * np.sin(gt * 0.25)), H * (0.12 + 0.05 * np.cos(gt * 0.2)), 420,
         np.array([0.16, 0.22, 0.55]), 0.30),
        (W * (0.10 + 0.08 * np.cos(gt * 0.18)), H * (0.88 + 0.04 * np.sin(gt * 0.22)), 380,
         np.array([0.10, 0.45, 0.42]), 0.16),
    ]
    for cx, cy, r, col, amp in blobs:
        g = np.exp(-((XX - cx) ** 2 + (YY - cy) ** 2) / (2 * r * r))
        img += g[..., None] * col * amp
    return img


def progress_bar(img, scene_idx, t, d):
    n = len(SCENES)
    x0, x1, gap, y, h = 40, W - 40, 8, 26, 5
    seg = (x1 - x0 - gap * (n - 1)) / n
    for k in range(n):
        a = int(x0 + k * (seg + gap))
        b = int(a + seg)
        img[y:y + h, a:b] = img[y:y + h, a:b] * 0.75 + 0.25 * 0.6
        frac = 1.0 if k < scene_idx else (clamp(t / d) if k == scene_idx else 0)
        e = int(a + (b - a) * frac)
        if e > a:
            img[y:y + h, a:e] = 0.95


def render(i):
    gt = i / FPS
    k = int(np.searchsorted(STARTS, gt, side="right") - 1)
    k = min(k, len(SCENES) - 1)
    fn, d = SCENES[k]
    t = gt - STARTS[k]
    fade = 1.0
    if k > 0:
        fade = min(fade, clamp(t / FADE))
    if k < len(SCENES) - 1:
        fade = min(fade, clamp((d - t) / FADE))
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    fig.patch.set_alpha(0)
    O = fig.add_axes([0, 0, 1, 1])
    O.set_xlim(0, W)
    O.set_ylim(0, H)
    O.axis("off")
    O.patch.set_alpha(0)
    fn(O, t, d)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).astype(np.float32) / 255
    plt.close(fig)
    a = buf[..., 3:4] * fade
    img = background(gt) * (1 - a) + buf[..., :3] * a
    progress_bar(img, k, t, d)
    return (np.clip(img, 0, 1) * 255).astype(np.uint8).tobytes()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if "--preview" in sys.argv:
        from PIL import Image
        times = [float(x) for x in sys.argv[sys.argv.index("--preview") + 1:]] or \
            [s + d - 0.4 for s, (_, d) in zip(STARTS[:-1], SCENES)]
        for tt in times:
            arr = np.frombuffer(render(int(tt * FPS)), np.uint8).reshape(H, W, 3)
            Image.fromarray(arr).save(OUT / f"preview_{tt:05.1f}.png")
        return
    n = int(TOTAL * FPS)
    out = OUT / "linkedin_labour_market_paradox_4x5.mp4"
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow",
         "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)],
        stdin=subprocess.PIPE)
    with Pool() as pool:
        for j, frame in enumerate(pool.imap(render, range(n), chunksize=6)):
            ff.stdin.write(frame)
            if j % 150 == 0:
                print(f"frame {j}/{n}", flush=True)
    ff.stdin.close()
    ff.wait()
    # cover image (end of the hook scene) for the LinkedIn thumbnail
    from PIL import Image
    arr = np.frombuffer(render(int((SCENES[0][1] - 0.5) * FPS)), np.uint8).reshape(H, W, 3)
    Image.fromarray(arr).save(OUT / "linkedin_cover_4x5.png")
    print("saved", out)


if __name__ == "__main__":
    main()
