"""Builds assets/stack.svg and assets/timeline.svg (monochrome, CSS-animated)."""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
ICONS = json.loads((HERE / "icon_paths.json").read_text(encoding="utf-8"))

FONT = "-apple-system, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"
BG, EDGE, ICO, TXT, DIM = "#0a0a0a", "#1f1f1f", "#d0d0d0", "#9a9a9a", "#6b6b6b"

# The user's current stack — must not change (see tests/test_svgs.py).
STACK = [
    ("LANGUAGES", [("Python", "python"), ("Java", "java"), ("C", "c"), ("JavaScript", "javascript"),
                   ("TypeScript", "typescript")]),
    ("BACKEND & DATA", [("FastAPI", "fastapi"), ("Flask", "flask"), ("Spring", "spring"), ("Node.js", "nodejs"),
                        ("PostgreSQL", "postgresql"), ("SQLite", "sqlite"), ("Redis", "redis")]),
    ("TOOLS", [("Docker", "docker"), ("Git", "git"), ("GitHub", "github"), ("GitHub Actions", "github-actions"),
               ("VS Code", "vscode")]),
]


def icon(name: str, x: float, y: float, size: float, color: str = ICO, cls: str = "ico") -> str:
    spec = ICONS[name]
    k = size / 24
    if spec["type"] == "brand":
        body = f'<path fill="{color}" d="{spec["path"]}"/>'
    else:
        body = (f'<g fill="none" stroke="{color}" stroke-width="1.75" stroke-linecap="round" '
                f'stroke-linejoin="round">{spec["inner"]}</g>')
    return f'<g class="{cls}" transform="translate({x:.2f} {y:.2f}) scale({k:.4f})">{body}</g>'


def build_stack() -> str:
    iw, copies = 104, 3
    row_tops = [48, 152, 256]
    head_y = [36, 140, 244]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 350" width="800" height="350" role="img" '
        'aria-label="Tech stack: Python, Java, C, JavaScript, TypeScript; FastAPI, Flask, Spring, Node.js, '
        'PostgreSQL, SQLite, Redis; Docker, Git, GitHub, GitHub Actions, VS Code">',
        "<title>Tech stack</title>",
        "<defs>",
        '<linearGradient id="gradx" x1="0" x2="1" y1="0" y2="0">'
        '<stop offset="0" stop-color="#000"/><stop offset="0.06" stop-color="#fff"/>'
        '<stop offset="0.94" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>',
        '<mask id="edgemask" maskUnits="userSpaceOnUse" x="28" y="0" width="744" height="350">'
        '<rect x="28" y="0" width="744" height="350" fill="url(#gradx)"/></mask>',
        "<style>",
        f"text{{font-family:{FONT}}}",
        f".h{{font-size:11px;letter-spacing:3px;fill:{DIM};font-weight:600}}",
        f".lbl{{font-size:12.5px;fill:{TXT};text-anchor:middle}}",
    ]
    for r, (_, items) in enumerate(STACK):
        d = len(items) * iw
        dur = 22 + 5 * r
        frm, to = (0, -d) if r % 2 == 0 else (-d, 0)
        parts.append(f"@keyframes m{r}{{from{{transform:translateX({frm}px)}}to{{transform:translateX({to}px)}}}}")
        parts.append(f".t{r}{{animation:m{r} {dur}s linear infinite;transform:translateX({frm}px)}}")
    parts += [
        "@media (prefers-reduced-motion: reduce){.t0,.t1,.t2{animation:none;transform:none}.dup{display:none}}",
        "</style></defs>",
        f'<rect x="0.5" y="0.5" width="799" height="349" rx="16" fill="{BG}" stroke="{EDGE}"/>',
    ]
    for r, (title, items) in enumerate(STACK):
        parts.append(f'<text class="h" x="28" y="{head_y[r]}">{escape(title)}</text>')
        parts.append(f'<line x1="28" x2="772" y1="{head_y[r] + 6}" y2="{head_y[r] + 6}" stroke="{EDGE}"/>')
        parts.append(f'<g mask="url(#edgemask)"><g class="t{r}">')
        for c in range(copies):
            cls = "dup" if c else "set"
            parts.append(f'<g class="{cls}" transform="translate({28 + c * len(items) * iw} {row_tops[r]})">')
            for i, (label, key) in enumerate(items):
                cx = i * iw + iw / 2
                parts.append(icon(key, cx - 16, 14, 32))
                parts.append(f'<text class="lbl" x="{cx}" y="64">{escape(label)}</text>')
            parts.append("</g>")
        parts.append("</g></g>")
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


MILESTONES = [
    ("Oct 2022", "briefcase", "Corporate operations, insurance", "Contracts, documents, corporate systems"),
    ("Foundations", "python", "Python and backend basics", "OOP projects: Weather CLI, RPG, freight table"),
    ("API", "fastapi", "Delivery API", "FastAPI, JWT access/refresh, automated tests"),
    ("Security", "lock", "SecureVault", "AES-GCM + Scrypt file encryption, desktop app"),
    ("In progress", "bus", "Bus Ticket API", "Segment-based seat booking, no double-booking"),
    ("Now", "target", "Backend Software Engineer", "APIs · Architecture · Security"),
    ("Next", "docker", "Concurrency, Docker, CI", "PostgreSQL + Redis, GitHub Actions, security, English"),
]


def build_timeline() -> str:
    step, top, x = 88, 52, 44
    n = len(MILESTONES)
    height = top + (n - 1) * step + 56
    length = (n - 1) * step
    css = [
        f"text{{font-family:{FONT}}}",
        f".d{{font-size:12px;letter-spacing:2.5px;fill:{DIM};font-weight:600;text-transform:uppercase}}",
        ".t{font-size:19px;fill:#e8e8e8;font-weight:600}",
        f".s{{font-size:14px;fill:{TXT}}}",
        f".ln{{stroke-dasharray:{length};stroke-dashoffset:{length};animation:draw 3.2s ease-out .2s forwards}}",
        "@keyframes draw{to{stroke-dashoffset:0}}",
        ".m{opacity:0;animation:in .7s ease both}",
        "@keyframes in{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}",
        ".pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-out infinite}",
        "@keyframes pulse{0%{transform:scale(1);opacity:.55}100%{transform:scale(1.9);opacity:0}}",
        "@media (prefers-reduced-motion: reduce){.ln{animation:none;stroke-dashoffset:0}"
        ".m{animation:none;opacity:1}.pulse{animation:none;opacity:0}}",
    ]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 {height}" width="560" height="{height}" '
        'role="img" aria-label="Timeline: corporate operations in insurance since Oct 2022, Python and backend '
        'foundations, Delivery API, SecureVault, Bus Ticket API, Backend Software Engineer, next: concurrency, Docker, CI">',
        "<title>Timeline</title>",
        f"<style>{''.join(css)}</style>",
        f'<rect x="0.5" y="0.5" width="559" height="{height - 1}" rx="16" fill="{BG}" stroke="{EDGE}"/>',
        f'<line class="ln" x1="{x}" x2="{x}" y1="{top}" y2="{top + length}" stroke="#3a3a3a" stroke-width="2"/>',
    ]
    for i, (date, key, title, sub) in enumerate(MILESTONES):
        y = top + i * step
        delay = 0.35 + 0.42 * i
        extra = f'<circle class="pulse" cx="{x}" cy="{y}" r="19" fill="none" stroke="#bdbdbd"/>' if date == "Now" else ""
        parts.append(
            f'<g class="m" style="animation-delay:{delay:.2f}s">{extra}'
            f'<circle cx="{x}" cy="{y}" r="19" fill="{BG}" stroke="#4a4a4a" stroke-width="1.5"/>'
            f'{icon(key, x - 11, y - 11, 22, "#e0e0e0", "ico")}'
            f'<text class="d" x="84" y="{y - 12}">{escape(date)}</text>'
            f'<text class="t" x="84" y="{y + 9}">{escape(title)}</text>'
            f'<text class="s" x="84" y="{y + 29}">{escape(sub)}</text></g>'
        )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "stack.svg").write_text(build_stack(), encoding="utf-8")
    print("ok")
