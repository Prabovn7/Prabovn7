"""Builds assets/stack.svg (navy, official icon colors, animated) and the shared icon() helper."""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

from palette import BLUE, EDGE, ICE, PALE, PANEL, PERI, TEXT

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
ICONS = json.loads((HERE / "icon_paths.json").read_text(encoding="utf-8"))

FONT = "-apple-system, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"

# The user's current stack — must not change (see tests).
STACK = [
    ("Languages", ICE, [("Python", "python"), ("Java", "java"), ("C", "c"), ("JavaScript", "javascript"),
                        ("TypeScript", "typescript")]),
    ("Backend & data", PERI, [("FastAPI", "fastapi"), ("Flask", "flask"), ("Spring", "spring"), ("Node.js", "nodejs"),
                              ("PostgreSQL", "postgresql"), ("SQLite", "sqlite"), ("Redis", "redis")]),
    ("Tools", PALE, [("Docker", "docker"), ("Git", "git"), ("GitHub", "github"), ("GitHub Actions", "github-actions"),
                     ("VS Code", "vscode"), ("IntelliJ IDEA", "intellij")]),
]


def icon(name: str, x: float, y: float, size: float, color: str | None = None, cls: str = "ico") -> str:
    spec = ICONS[name]
    color = color or spec.get("color", TEXT)
    k = size / 24
    if spec["type"] == "brand":
        body = f'<path fill="{color}" d="{spec["path"]}"/>'
    else:
        body = (f'<g fill="none" stroke="{color}" stroke-width="1.75" stroke-linecap="round" '
                f'stroke-linejoin="round">{spec["inner"]}</g>')
    return f'<g class="{cls}" transform="translate({x:.2f} {y:.2f}) scale({k:.4f})">{body}</g>'


def build_stack() -> str:
    iw, copies = 104, 3
    row_tops, head_y = [48, 152, 256], [36, 140, 244]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 350" width="800" height="350" role="img" '
        'aria-label="Tech stack: Python, Java, C, JavaScript, TypeScript; FastAPI, Flask, Spring, Node.js, '
        'PostgreSQL, SQLite, Redis; Docker, Git, GitHub, GitHub Actions, VS Code, IntelliJ IDEA">',
        "<title>Tech stack</title>",
        "<defs>",
        '<linearGradient id="gradx" x1="0" x2="1" y1="0" y2="0">'
        '<stop offset="0" stop-color="#000"/><stop offset="0.06" stop-color="#fff"/>'
        '<stop offset="0.94" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>',
        '<mask id="edgemask" maskUnits="userSpaceOnUse" x="28" y="0" width="744" height="350">'
        '<rect x="28" y="0" width="744" height="350" fill="url(#gradx)"/></mask>',
        "<style>",
        f"text{{font-family:{FONT}}}",
        ".h{font-size:13px;font-weight:600;letter-spacing:.4px}",
        f".lbl{{font-size:12.5px;fill:{TEXT};fill-opacity:.8;text-anchor:middle}}",
        ".dl{stroke-dasharray:744;stroke-dashoffset:744;animation:drawline 1.4s ease-out forwards}",
        "@keyframes drawline{to{stroke-dashoffset:0}}",
        ".fl{animation:float 4.2s ease-in-out infinite}",
        "@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}",
    ]
    for r, (_, _, items) in enumerate(STACK):
        d = len(items) * iw
        dur = 22 + 5 * r
        frm, to = (0, -d) if r % 2 == 0 else (-d, 0)
        parts.append(f"@keyframes m{r}{{from{{transform:translateX({frm}px)}}to{{transform:translateX({to}px)}}}}")
        parts.append(f".t{r}{{animation:m{r} {dur}s linear infinite;transform:translateX({frm}px)}}")
    parts += [
        "@media (prefers-reduced-motion: reduce){.t0,.t1,.t2{animation:none;transform:none}.dup{display:none}"
        ".fl{animation:none}.dl{animation:none;stroke-dashoffset:0}}",
        "</style></defs>",
        f'<rect x="0.5" y="0.5" width="799" height="349" rx="16" fill="{PANEL}" stroke="{EDGE}"/>',
    ]
    for r, (title, color, items) in enumerate(STACK):
        parts.append(f'<text class="h" x="28" y="{head_y[r]}" fill="{color}">{escape(title)}</text>')
        parts.append(f'<line class="dl" x1="28" x2="772" y1="{head_y[r] + 6}" y2="{head_y[r] + 6}" stroke="{BLUE}" '
                     f'stroke-width="1.5" style="animation-delay:{0.2 + r * 0.25:.2f}s"/>')
        parts.append(f'<g mask="url(#edgemask)"><g class="t{r}">')
        for c in range(copies):
            cls = "dup" if c else "set"
            parts.append(f'<g class="{cls}" transform="translate({28 + c * len(items) * iw} {row_tops[r]})">')
            for i, (label, key) in enumerate(items):
                cx = i * iw + iw / 2
                parts.append(f'<g class="fl" style="animation-delay:{i * 0.35:.2f}s">{icon(key, cx - 16, 14, 32)}</g>')
                parts.append(f'<text class="lbl" x="{cx}" y="64">{escape(label)}</text>')
            parts.append("</g>")
        parts.append("</g></g>")
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "stack.svg").write_text(build_stack(), encoding="utf-8")
    print("ok")
