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
        ".w{animation:wave 6s ease-in-out infinite}",
        "@keyframes wave{0%,100%{opacity:1}50%{opacity:.5}}",
        ".tw{opacity:0;animation:twinkle 3.4s ease-in-out infinite}",
        f".tw{{fill:{TEXT}}}",
        "@keyframes twinkle{0%,70%,100%{opacity:0}85%{opacity:.4}}",
        f".ping{{fill:none;stroke:{ICE};stroke-width:1.5;transform-box:fill-box;transform-origin:center;"
        "animation:ping 2.4s ease-out infinite}",
        "@keyframes ping{0%{transform:scale(1);opacity:.9}100%{transform:scale(2.2);opacity:0}}",
        ".scan{animation:scan 5.5s ease-in-out infinite}",
        "@keyframes scan{0%{transform:translateX(0);opacity:0}12%{opacity:1}88%{opacity:1}"
        "100%{transform:translateX(var(--sw));opacity:0}}",
        "@media (prefers-reduced-motion: reduce){.cell,.today{animation:none;opacity:1}.flame{animation:none}"
        ".w,.tw,.ping,.scan{animation:none;opacity:0}.w{opacity:1}}",
    ]
    label = f"{total} contributions in the last {weeks} weeks"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'role="img" aria-label="Git activity: {label}, current streak {streak} days">',
        "<title>Git activity</title>",
        f'<defs><linearGradient id="scg" x1="0" x2="1"><stop offset="0" stop-color="{ICE}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{ICE}" stop-opacity=".35"/><stop offset="1" stop-color="{ICE}" stop-opacity="0"/>'
        "</linearGradient></defs>",
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
    gw = weeks * (CELL + GAP)
    parts.append(f'<g style="--sw:{gw}px"><rect class="scan" x="{LEFT - 40}" y="{TOP - 4}" width="40" '
                 f'height="{7 * (CELL + GAP) + 4}" fill="url(#scg)"/></g>')
    for d in days:
        col = (d - first).days // 7
        row = (d.weekday() + 1) % 7
        n = counts.get(d, 0)
        lvl = _level(n, peak)
        x, y = LEFT + col * (CELL + GAP), TOP + row * (CELL + GAP)
        parts.append(
            f'<g class="w" style="animation-delay:{1.2 + col * 0.12:.2f}s"><rect class="cell l{lvl}'
            f'{" today" if d == today else ""}" data-level="{lvl}" data-date="{d.isoformat()}" '
            f'x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
            f'style="animation-delay:{col * 0.035:.2f}s"><title>{d.isoformat()}: {n}</title></rect></g>'
        )
        if lvl >= 3:
            parts.append(f'<rect class="tw" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
                         f'style="animation-delay:{(col * 0.37 + row * 0.53) % 3.4:.2f}s"/>')
        if d == today:
            parts.append(f'<rect class="ping" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3"/>')
    ly = height - 28
    if note:
        parts.append(f'<text class="k" x="24" y="{ly + 10}">{escape(note)}</text>')
    parts.append(f'<text class="k" x="{width - 168}" y="{ly + 10}">Less</text>')
    for i, c in enumerate(LEVEL_FILL):
        parts.append(f'<rect x="{width - 136 + i * 19}" y="{ly}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>')
    parts.append(f'<text class="k" x="{width - 36}" y="{ly + 10}">More</text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def build_months_svg(counts: dict[date, int], today: date | None = None, months: int = 6) -> str:
    """Animated per-month bar chart shown inside the README's expandable 'By month' block."""
    today = today or date.today()
    keys = []
    y, m = today.year, today.month
    for _ in range(months):
        keys.append((y, m))
        y, m = (y, m - 1) if m > 1 else (y - 1, 12)
    keys.reverse()
    totals = {k: 0 for k in keys}
    for d, n in counts.items():
        if (d.year, d.month) in totals and d <= today:
            totals[(d.year, d.month)] += n
    peak = max(totals.values(), default=0)
    width, height, left, base, ch = 560, 230, 24, 172, 110
    slot = (width - 2 * left) / months
    bw = slot - 22
    css = [
        f"text{{font-family:{FONT}}}",
        f".k{{font-size:13px;fill:{PERI}}}",
        f".v{{font-size:16px;font-weight:700;fill:{TEXT}}}",
        ".mbar{transform-box:fill-box;transform-origin:bottom;animation:grow .9s cubic-bezier(.2,.8,.2,1) both}",
        "@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}",
        ".vv{animation:fade .6s ease-out both}@keyframes fade{from{opacity:0}to{opacity:1}}",
    ] + [f".l{i}{{fill:{c}}}" for i, c in enumerate(LEVEL_FILL)] + [
        "@media (prefers-reduced-motion: reduce){.mbar,.vv{animation:none}}",
    ]
    total = sum(totals.values())
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'role="img" aria-label="Contributions per month, last {months} months: {total} in total">',
        "<title>Contributions per month</title>",
        f"<style>{''.join(css)}</style>",
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="16" fill="{PANEL}" stroke="{EDGE}"/>',
        f'<line x1="{left}" y1="{base + 4}" x2="{width - left}" y2="{base + 4}" stroke="{EDGE}"/>',
    ]
    for i, k in enumerate(keys):
        n = totals[k]
        h = 6 if n <= 0 else max(10, round(ch * n / peak))
        x = left + i * slot + 11
        lvl = _level(n, peak)
        label = date(k[0], k[1], 1).strftime("%b")
        dl = f"{i * 0.1:.1f}s"
        parts.append(
            f'<rect class="mbar l{lvl}" data-total="{n}" x="{x:.1f}" y="{base - h}" width="{bw:.1f}" height="{h}" rx="6" '
            f'style="animation-delay:{dl}"><title>{label}: {n}</title></rect>'
            f'<text class="vv v" x="{x + bw / 2:.1f}" y="{base - h - 8}" text-anchor="middle" style="animation-delay:{dl}">{n}</text>'
            f'<text class="k" x="{x + bw / 2:.1f}" y="{base + 24}" text-anchor="middle">{label}</text>'
        )
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
    ap.add_argument("--months", help="also write the per-month chart SVG")
    ap.add_argument("--source", choices=["graphql", "events", "sample"], default="graphql")
    a = ap.parse_args()
    note = None
    if a.source == "sample":
        counts, note = sample_counts(), "Preview data - replaced daily by the GitHub Action"
    else:
        counts = fetch_graphql(a.user) if a.source == "graphql" else fetch_events(a.user)
    Path(a.out).write_text(build_activity_svg(counts, a.weeks, note=note), encoding="utf-8")
    if a.months:
        Path(a.months).write_text(build_months_svg(counts), encoding="utf-8")
    print(f"wrote {a.out}: {sum(counts.values())} contributions")


if __name__ == "__main__":
    main()
