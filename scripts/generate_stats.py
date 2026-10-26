#!/usr/bin/env python3
"""Generate animated SVG stats cards for the GitHub profile README.

Usage:
    GITHUB_TOKEN=... GH_USER=Prabovn7 python scripts/generate_stats.py
    python scripts/generate_stats.py --from-json scripts/stats_fixture.json

Only the standard library is used, so the workflow needs no pip install.
Output: assets/stats/languages.svg and assets/stats/overview.svg
"""
import argparse
import json
import os
import sys
import urllib.request
from html import escape

BG, ACC, FG, MUT, LINE = "#050505", "#E6E6E6", "#FFFFFF", "#A3A3A3", "#2A2A2A"
SANS = "system-ui,-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
EXCLUDE = {"Mako", "Jinja", "Dockerfile", "Makefile"}
# GitHub linguist colors, so each language is recognizable at a glance
LANG_COLORS = {
    "Python": "#3572A5", "TypeScript": "#3178C6", "JavaScript": "#F1E05A", "CSS": "#663399", "HTML": "#E34C26",
    "Java": "#B07219", "C": "#9CA3AF", "Shell": "#89E051", "Batchfile": "#C1F12E", "VBA": "#867DB1", "SQL": "#E38C00",
    "PLpgSQL": "#336790", "Go": "#00ADD8", "Rust": "#DEA584", "Other": "#6B7280",
}
TOP_N = 6
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "stats")


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
    track_x, track_w = 200, 590
    h = 96 + len(top) * 44
    rows = []
    for i, (name, size) in enumerate(top):
        pct = size / total * 100
        y = 96 + i * 44
        bar = max(track_w * pct / 100, 4)
        t0 = 0.2 + i * 0.12
        rows.append(
            f'<circle cx="40" cy="{y}" r="6" fill="{LANG_COLORS.get(name, ACC)}"/>'
            f'<text x="56" y="{y+6}" font-family="{SANS}" font-size="18" fill="{FG}">{escape(name)}</text>'
            f'<rect x="{track_x}" y="{y-6}" width="{track_w}" height="12" rx="6" fill="{LINE}"/>'
            f'<rect x="{track_x}" y="{y-6}" width="{bar:.1f}" height="12" rx="6" fill="{LANG_COLORS.get(name, ACC)}">'
            f'<animate attributeName="width" values="0;0;{bar:.1f}" keyTimes="0;{t0/1.8:.3f};1" dur="1.8s" fill="freeze"/></rect>'
            f'<text x="868" y="{y+6}" text-anchor="end" font-family="{MONO}" font-size="16" fill="{MUT}">{pct:.1f}%</text>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 {h}" width="100%" role="img" aria-label="Most used languages across public repositories">
<rect width="900" height="{h}" rx="16" fill="{BG}"/>
<rect x=".5" y=".5" width="899" height="{h-1}" rx="15.5" fill="none" stroke="{LINE}"/>
<text x="32" y="44" font-family="{SANS}" font-size="22" font-weight="600" fill="{FG}">Most used languages</text>
<text x="32" y="66" font-family="{SANS}" font-size="14" fill="{MUT}">By bytes of code, public repositories · refreshed daily by GitHub Actions</text>
{''.join(rows)}
</svg>
"""


def overview_svg(data):
    tiles = [
        (str(data["repos"]), "public repositories"),
        (str(data["stars"]), "stars received"),
        (str(data["followers"]), "followers"),
        (str(len([k for k in data["languages"] if k not in EXCLUDE])), "languages"),
    ]
    out = []
    for i, (num, label) in enumerate(tiles):
        x = 30 + i * 215
        out.append(
            f'<g opacity="1"><animate attributeName="opacity" values="0;0;1" keyTimes="0;{i*0.12:.2f};{i*0.12+0.3:.2f}" dur="1.4s" fill="freeze"/>'
            f'<rect x="{x}" y="24" width="195" height="92" rx="12" fill="#141414" stroke="{LINE}"/>'
            f'<text x="{x+22}" y="70" font-family="{SANS}" font-size="38" font-weight="700" fill="{FG}">{escape(num)}</text>'
            f'<text x="{x+22}" y="98" font-family="{SANS}" font-size="15" fill="{MUT}">{escape(label)}</text></g>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 140" width="100%" role="img" aria-label="GitHub overview">
<rect width="900" height="140" rx="16" fill="{BG}"/>
<rect x=".5" y=".5" width="899" height="139" rx="15.5" fill="none" stroke="{LINE}"/>
{''.join(out)}
</svg>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-json", help="read data from a JSON file instead of calling the GitHub API")
    args = ap.parse_args()
    if args.from_json:
        with open(args.from_json, encoding="utf-8") as f:
            data = json.load(f)
    else:
        user = os.environ.get("GH_USER")
        if not user:
            sys.exit("GH_USER is required")
        data = collect(user, os.environ.get("GITHUB_TOKEN"))
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "languages.svg"), "w", encoding="utf-8") as f:
        f.write(languages_svg(data["languages"]))
    with open(os.path.join(OUT_DIR, "overview.svg"), "w", encoding="utf-8") as f:
        f.write(overview_svg(data))
    print("stats written")


if __name__ == "__main__":
    main()
