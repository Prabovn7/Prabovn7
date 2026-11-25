"""Generates assets/activity.svg: an animated 30-day contribution bar chart.

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


def build_activity_svg(counts: dict[date, int], days: int = 30, today: date | None = None,
                       note: str | None = None) -> str:
    """Animated bar chart of the last `days` days of contributions (one bar per day, today on the right)."""
    today = today or date.today()
    span = [today - timedelta(days=days - 1 - i) for i in range(days)]
    peak = max((counts.get(d, 0) for d in span), default=0)
    total = sum(counts.get(d, 0) for d in span)
    streak = _streak(counts, today)

    width, height, left, base, ch = 560, 250, 24, 208, 104
    slot = (width - 2 * left) / days
    bw = slot - 5
    label = f"{total} contributions in the last {days} days"
    css = [
        f"text{{font-family:{FONT}}}",
        f".t{{font-size:18px;font-weight:600;fill:{TEXT}}}",
        f".s{{font-size:13px;fill:{PERI}}}",
        f".k{{font-size:11px;fill:{MUTED}}}",
        ".bar{transform-box:fill-box;transform-origin:bottom;animation:grow .8s cubic-bezier(.2,.8,.2,1) both}",
        "@keyframes grow{from{transform:scaleY(0);opacity:0}to{transform:scaleY(1);opacity:1}}",
        f".today{{stroke:{PALE};stroke-width:1.5;animation:grow .8s cubic-bezier(.2,.8,.2,1) both,pulse 2.4s ease-in-out infinite}}",
        "@keyframes pulse{0%,100%{stroke-opacity:1}50%{stroke-opacity:.2}}",
        ".flame{transform-box:fill-box;transform-origin:center bottom;animation:flicker 1.8s ease-in-out infinite}",
        "@keyframes flicker{0%,100%{transform:scale(1);opacity:1}40%{transform:scale(1.12,.94);opacity:.8}"
        "70%{transform:scale(.95,1.08);opacity:1}}",
    ] + [f".l{i}{{fill:{c}}}" for i, c in enumerate(LEVEL_FILL)] + [
        "@media (prefers-reduced-motion: reduce){.bar,.today{animation:none}.flame{animation:none}}",
    ]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'role="img" aria-label="Git activity: {label}, current streak {streak} days">',
        "<title>Git activity</title>",
        f"<style>{''.join(css)}</style>",
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="16" fill="{PANEL}" stroke="{EDGE}"/>',
        icon("activity", 24, 22, 22, ICE),
        '<text class="t" x="54" y="40">Git activity</text>',
        f'<text class="s" x="24" y="68">{escape(label)}</text>',
        f'<g class="flame">{icon("flame", width - 150, 24, 18, PERI)}</g>',
        f'<text class="s" x="{width - 128}" y="38">{streak}-day streak</text>',
        f'<line x1="{left}" y1="{base + 4}" x2="{width - left}" y2="{base + 4}" stroke="{EDGE}"/>',
    ]
    for i, d in enumerate(span):
        n = counts.get(d, 0)
        lvl = _level(n, peak)
        h = 5 if n <= 0 else max(8, round(ch * n / peak))
        x = left + i * slot + 2.5
        cls = f"bar l{lvl}" + (" today" if d == today else "")
        parts.append(
            f'<rect class="{cls}" data-level="{lvl}" data-date="{d.isoformat()}" x="{x:.1f}" y="{base - h}" '
            f'width="{bw:.1f}" height="{h}" rx="3" style="animation-delay:{i * 0.03:.2f}s">'
            f'<title>{d.isoformat()}: {n}</title></rect>'
        )
    parts.append(f'<text class="k" x="{left}" y="{base + 22}">{span[0].strftime("%b %d")}</text>')
    parts.append(f'<text class="k" x="{width // 2}" y="{base + 22}" text-anchor="middle">{span[days // 2].strftime("%b %d")}</text>')
    parts.append(f'<text class="k" x="{width - left}" y="{base + 22}" text-anchor="end">Today</text>')
    if note:
        parts.append(f'<text class="k" x="{left}" y="{height - 6}">{escape(note)}</text>')
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
    ap.add_argument("--source", choices=["graphql", "events", "sample"], default="graphql")
    a = ap.parse_args()
    note = None
    if a.source == "sample":
        counts, note = sample_counts(), "Preview data - replaced daily by the GitHub Action"
    else:
        counts = fetch_graphql(a.user) if a.source == "graphql" else fetch_events(a.user)
    Path(a.out).write_text(build_activity_svg(counts, note=note), encoding="utf-8")
    print(f"wrote {a.out}: {sum(counts.values())} contributions")


if __name__ == "__main__":
    main()
