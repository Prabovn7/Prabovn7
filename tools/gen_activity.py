"""Generates assets/activity.svg: an animated, monochrome contribution grid.

CLI:  python gen_activity.py --user Prabovn7 --out assets/activity.svg
      (reads GitHub GraphQL via `gh api graphql`; needs GH_TOKEN/GITHUB_TOKEN)
      --source events  uses the public events API (last ~90 days only; fallback)
"""
from __future__ import annotations

import argparse
import json
import subprocess
from collections import defaultdict
from datetime import date, datetime, timedelta
from html import escape
from pathlib import Path

from build_svgs import FONT, icon
from palette import BLUE, EDGE, ICE, MUTED, PALE, PANEL, PERI, TEXT

CELL, GAP, LEFT, TOP = 15, 4, 52, 84
LEVEL_FILL = [EDGE, BLUE, PERI, ICE, PALE]


def _level(count: int, peak: int) -> int:
    if count <= 0 or peak <= 0:
        return 0
    return max(1, min(4, -(-4 * count // peak)))  # ceil(4*count/peak)


def _streak(counts: dict[date, int], today: date) -> int:
    day = today if counts.get(today, 0) > 0 else today - timedelta(days=1)
    n = 0
    while counts.get(day, 0) > 0:
        n += 1
        day -= timedelta(days=1)
    return n


def build_activity_svg(counts: dict[date, int], weeks: int = 26, today: date | None = None,
                       note: str | None = None) -> str:
    today = today or date.today()
    # Sunday-first rows; the last column holds the current week.
    today_row = (today.weekday() + 1) % 7
    first = today - timedelta(days=today_row + 7 * (weeks - 1))
    days = [first + timedelta(days=i) for i in range(weeks * 7)]
    days = [d for d in days if d <= today]
    peak = max((counts.get(d, 0) for d in days), default=0)
    total = sum(counts.get(d, 0) for d in days)
    streak = _streak(counts, today)

    width = LEFT + weeks * (CELL + GAP) + 14
    height = TOP + 7 * (CELL + GAP) + 54
    css = [
        f"text{{font-family:{FONT}}}",
        f".t{{font-size:18px;font-weight:600;fill:{TEXT}}}",
        f".s{{font-size:13px;fill:{PERI}}}",
        f".k{{font-size:11px;fill:{MUTED}}}",
        ".cell{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .5s ease-out both}",
        "@keyframes pop{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:scale(1)}}",
        f".today{{stroke:{ICE};stroke-width:1.5;animation:pop .5s ease-out both,pulse 2.4s ease-in-out infinite}}",
        "@keyframes pulse{0%,100%{stroke-opacity:1}50%{stroke-opacity:.15}}",
        ".flame{transform-box:fill-box;transform-origin:center bottom;animation:flicker 1.8s ease-in-out infinite}",
        "@keyframes flicker{0%,100%{transform:scale(1);opacity:1}40%{transform:scale(1.12,.94);opacity:.8}"
        "70%{transform:scale(.95,1.08);opacity:1}}",
    ] + [f".l{i}{{fill:{c}}}" for i, c in enumerate(LEVEL_FILL)] + [
        "@media (prefers-reduced-motion: reduce){.cell,.today{animation:none;opacity:1}.flame{animation:none}}",
    ]
    label = f"{total} contributions in the last {weeks} weeks"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'role="img" aria-label="Git activity: {label}, current streak {streak} days">',
        "<title>Git activity</title>",
        f"<style>{''.join(css)}</style>",
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="16" fill="{PANEL}" stroke="{EDGE}"/>',
        icon("activity", 24, 22, 22, ICE),
        '<text class="t" x="54" y="40">Git activity</text>',
        f'<text class="s" x="24" y="64">{escape(label)}</text>',
        f'<g class="flame">{icon("flame", width - 190, 46, 18, PERI)}</g>',
        f'<text class="s" x="{width - 168}" y="60">{streak}-day streak</text>',
    ]
    for r, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        parts.append(f'<text class="k" x="24" y="{TOP + r * (CELL + GAP) + 12}">{name}</text>')
    for d in days:
        col = (d - first).days // 7
        row = (d.weekday() + 1) % 7
        n = counts.get(d, 0)
        lvl = _level(n, peak)
        parts.append(
            f'<rect class="cell l{lvl}{" today" if d == today else ""}" data-level="{lvl}" data-date="{d.isoformat()}" '
            f'x="{LEFT + col * (CELL + GAP)}" y="{TOP + row * (CELL + GAP)}" width="{CELL}" height="{CELL}" rx="3" '
            f'style="animation-delay:{col * 0.035:.2f}s"><title>{d.isoformat()}: {n}</title></rect>'
        )
    ly = height - 28
    if note:
        parts.append(f'<text class="k" x="24" y="{ly + 10}">{escape(note)}</text>')
    parts.append(f'<text class="k" x="{width - 168}" y="{ly + 10}">Less</text>')
    for i, c in enumerate(LEVEL_FILL):
        parts.append(f'<rect x="{width - 136 + i * 19}" y="{ly}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>')
    parts.append(f'<text class="k" x="{width - 36}" y="{ly + 10}">More</text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def fetch_graphql(user: str) -> dict[date, int]:
    q = ("query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{weeks{contributionDays"
         "{date contributionCount}}}}}}")
    out = subprocess.run(["gh", "api", "graphql", "-f", f"query={q}", "-F", f"u={user}"],
                         check=True, capture_output=True, text=True).stdout
    weeks = json.loads(out)["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return {date.fromisoformat(d["date"]): d["contributionCount"] for w in weeks for d in w["contributionDays"]}


def fetch_events(user: str) -> dict[date, int]:
    out = subprocess.run(["gh", "api", f"users/{user}/events/public?per_page=100", "--paginate"],
                         check=True, capture_output=True, text=True).stdout
    counts: dict[date, int] = defaultdict(int)
    decoder, idx = json.JSONDecoder(), 0
    while idx < len(out):
        while idx < len(out) and out[idx].isspace():
            idx += 1
        if idx >= len(out):
            break
        page, idx = decoder.raw_decode(out, idx)
        for ev in page:
            if ev.get("type") == "PushEvent":
                day = datetime.fromisoformat(ev["created_at"].replace("Z", "+00:00")).date()
                counts[day] += len(ev["payload"].get("commits", [])) or 1
    return dict(counts)


def sample_counts(weeks: int = 26, today: date | None = None) -> dict[date, int]:
    """Deterministic preview data (a clearly-labelled placeholder until the Action runs)."""
    import random

    rng, today = random.Random(42), today or date.today()
    return {today - timedelta(days=i): rng.choice([0, 0, 1, 2, 3, 5, 8]) for i in range(weeks * 7)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--weeks", type=int, default=26)
    ap.add_argument("--source", choices=["graphql", "events", "sample"], default="graphql")
    a = ap.parse_args()
    note = None
    if a.source == "sample":
        counts, note = sample_counts(), "Preview data - replaced daily by the GitHub Action"
    else:
        counts = fetch_graphql(a.user) if a.source == "graphql" else fetch_events(a.user)
    Path(a.out).write_text(build_activity_svg(counts, a.weeks, note=note), encoding="utf-8")
    print(f"wrote {a.out}: {sum(counts.values())} contributions")


if __name__ == "__main__":
    main()
