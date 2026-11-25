#!/usr/bin/env python3
"""Generate animated SVG stats cards (navy palette) for the GitHub profile README.

Usage:
    GITHUB_TOKEN=... GH_USER=Prabovn7 python scripts/generate_stats.py
    python scripts/generate_stats.py --from-json scripts/stats_fixture.json [--out-dir DIR]

Only the standard library is used, so the workflow needs no pip install.
Output: assets/stats/languages.svg and assets/stats/overview.svg
Motion is pure CSS (honors prefers-reduced-motion); colors come from tools/palette.py.
"""
import argparse
import json
import os
import sys
import urllib.request
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from palette import BLUE, EDGE, ICE, NAVY, PALE, PANEL, PERI, TEXT  # noqa: E402

SANS = "system-ui,-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif"
EXCLUDE = {"Mako", "Jinja", "Dockerfile", "Makefile"}
TOP_N = 6
OFFICIAL = {"Python": "python", "TypeScript": "typescript", "JavaScript": "javascript", "Java": "java", "C": "c"}
CYCLE = [BLUE, ICE, PERI, PALE]
OUT_DIR = os.path.join(HERE, "..", "assets", "stats")

CSS = """<style>
text{font-family:%s}
.row,.tile{animation:rise .6s ease-out both}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.bar{transform-box:fill-box;transform-origin:left;animation:grow 1.1s cubic-bezier(.2,.8,.2,1) both}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.dot{transform-box:fill-box;transform-origin:center;animation:pop .5s ease-out both}
.num{transform-box:fill-box;transform-origin:left bottom;animation:pop .7s ease-out both}
@keyframes pop{0%%{opacity:0;transform:scale(.5)}60%%{opacity:1;transform:scale(1.1)}100%%{opacity:1;transform:scale(1)}}
.live{animation:blink 2s ease-in-out infinite}
@keyframes blink{0%%,100%%{opacity:1}50%%{opacity:.25}}
@media (prefers-reduced-motion: reduce){.row,.tile,.bar,.dot,.num,.live{animation:none}}
</style>""" % SANS


def _icon_colors():
    try:
        with open(os.path.join(HERE, "..", "tools", "icon_paths.json"), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


ICONS = _icon_colors()


def lang_color(name, i):
    key = OFFICIAL.get(name)
    if key and key in ICONS and "color" in ICONS[key]:
        return ICONS[key]["color"]
    return CYCLE[i % len(CYCLE)]


def api(url, token):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-stats"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def collect(user, token):
    repos, page = [], 1
    while True:
        chunk = api(f"https://api.github.com/users/{user}/repos?per_page=100&page={page}&type=owner", token)
        repos += chunk
        if len(chunk) < 100:
            break
        page += 1
    repos = [r for r in repos if not r["fork"]]
    langs = {}
    for r in repos:
        for name, size in api(r["languages_url"], token).items():
            langs[name] = langs.get(name, 0) + size
    profile = api(f"https://api.github.com/users/{user}", token)
    return {
        "repos": len(repos),
        "stars": sum(r["stargazers_count"] for r in repos),
        "followers": profile["followers"],
        "languages": langs,
    }


def languages_svg(langs):
    items = sorted(((k, v) for k, v in langs.items() if k not in EXCLUDE), key=lambda kv: -kv[1])
    total = sum(v for _, v in items) or 1
    top = items[:TOP_N]
    rest = sum(v for _, v in items[TOP_N:])
    if rest:
        top.append(("Other", rest))
    h = 96 + max(len(top), 1) * 44
    rows = []
    for i, (name, size) in enumerate(top):
        pct, y = size / total * 100, 112 + i * 44
        color = lang_color(name, i)
        bar = max(300 * pct / 100, 4)
        d = 0.15 + i * 0.12
        rows.append(
            f'<g class="row" style="animation-delay:{d:.2f}s">'
            f'<circle class="dot" cx="32" cy="{y}" r="6" fill="{color}" style="animation-delay:{d:.2f}s"/>'
            f'<text x="48" y="{y + 6}" font-size="18" fill="{TEXT}">{escape(name)}</text>'
            f'<rect x="170" y="{y - 6}" width="300" height="12" rx="6" fill="{EDGE}"/>'
            f'<rect class="bar" x="170" y="{y - 6}" width="{bar:.1f}" height="12" rx="6" fill="{color}" '
            f'style="animation-delay:{d + 0.1:.2f}s"/>'
            f'<text x="528" y="{y + 5}" text-anchor="end" font-size="15" fill="{PERI}">{pct:.1f}%</text></g>'
        )
    if not top:
        rows.append(f'<text x="32" y="116" font-size="16" fill="{PERI}">No public code yet</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 {h}" width="100%" role="img" aria-label="Most used languages across public repositories">
{CSS}
<rect x=".5" y=".5" width="559" height="{h - 1}" rx="16" fill="{PANEL}" stroke="{EDGE}"/>
<text x="24" y="42" font-size="22" font-weight="600" fill="{TEXT}">Most used languages</text>
<circle class="live" cx="408" cy="36" r="4" fill="{ICE}"/>
<text x="420" y="41" font-size="13" fill="{PERI}">updated daily</text>
<text x="24" y="68" font-size="13" fill="{PERI}">By bytes of code, public repositories</text>
{''.join(rows)}
</svg>
"""


def overview_svg(data):
    tiles = [
        (str(data["repos"]), "public repositories", BLUE),
        (str(data["stars"]), "stars received", ICE),
        (str(data["followers"]), "followers", PERI),
        (str(len([k for k in data["languages"] if k not in EXCLUDE])), "languages", PALE),
    ]
    out = []
    for i, (num, label, accent) in enumerate(tiles):
        x, y = 20 + (i % 2) * 269, 20 + (i // 2) * 116
        d = 0.1 + i * 0.15
        out.append(
            f'<g class="tile" style="animation-delay:{d:.2f}s">'
            f'<rect x="{x}" y="{y}" width="251" height="100" rx="14" fill="{NAVY}" stroke="{EDGE}"/>'
            f'<rect x="{x + 20}" y="{y}" width="48" height="4" rx="2" fill="{accent}"/>'
            f'<text class="num" x="{x + 22}" y="{y + 62}" font-size="44" font-weight="700" fill="{TEXT}" '
            f'style="animation-delay:{d + 0.2:.2f}s">{escape(num)}</text>'
            f'<text x="{x + 22}" y="{y + 86}" font-size="15" fill="{PERI}">{escape(label)}</text></g>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 252" width="100%" role="img" aria-label="GitHub overview: public repositories, stars, followers and languages">
{CSS}
<rect x=".5" y=".5" width="559" height="251" rx="16" fill="{PANEL}" stroke="{EDGE}"/>
{''.join(out)}
</svg>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-json", help="read data from a JSON file instead of calling the GitHub API")
    ap.add_argument("--out-dir", default=OUT_DIR, help="where to write the SVGs (default: assets/stats)")
    args = ap.parse_args()
    if args.from_json:
        with open(args.from_json, encoding="utf-8") as f:
            data = json.load(f)
    else:
        user = os.environ.get("GH_USER")
        if not user:
            sys.exit("GH_USER is required")
        data = collect(user, os.environ.get("GITHUB_TOKEN"))
    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "languages.svg"), "w", encoding="utf-8") as f:
        f.write(languages_svg(data["languages"]))
    with open(os.path.join(args.out_dir, "overview.svg"), "w", encoding="utf-8") as f:
        f.write(overview_svg(data))
    print("stats written")


if __name__ == "__main__":
    main()
