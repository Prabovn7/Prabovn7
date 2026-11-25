"""Builds the small animated assets: divider, contact buttons, roles line, 'Right now' cards, accent bars."""
from __future__ import annotations

from html import escape
from pathlib import Path

from build_svgs import FONT, icon
from palette import BLUE, EDGE, ICE, NAVY, PALE, PANEL, PERI, TEXT

ASSETS = Path(__file__).resolve().parent.parent / "assets"
RM = "@media (prefers-reduced-motion: reduce){%s}"


def _svg(w: int, h: int, label: str, css: str, body: str, defs: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-label="{escape(label)}"><title>{escape(label)}</title>{defs}<style>text{{font-family:{FONT}}}{css}</style>'
            f'{body}</svg>\n')


def build_divider() -> str:
    css = (".sw{animation:sweep 4.5s ease-in-out infinite}"
           "@keyframes sweep{0%{transform:translateX(0);opacity:0}15%{opacity:1}85%{opacity:1}100%{transform:translateX(560px);opacity:0}}"
           ".nd{transform-box:fill-box;transform-origin:center;animation:beat 2.4s ease-in-out infinite}"
           "@keyframes beat{0%,100%{transform:scale(1);opacity:.9}50%{transform:scale(1.6);opacity:.4}}"
           + RM % ".sw,.nd{animation:none}.sw{opacity:0}")
    defs = (f'<linearGradient id="ln" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="hl" x1="0" x2="1"><stop offset="0" stop-color="{ICE}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{ICE}"/><stop offset="1" stop-color="{ICE}" stop-opacity="0"/></linearGradient>')
    body = (f'<rect x="20" y="19" width="760" height="2" rx="1" fill="url(#ln)"/>'
            f'<rect class="sw" x="60" y="18" width="120" height="4" rx="2" fill="url(#hl)"/>'
            f'<circle class="nd" cx="400" cy="20" r="4" fill="{ICE}"/>'
            f'<circle cx="400" cy="20" r="2" fill="{TEXT}"/>')
    return _svg(800, 40, "Section divider", css, body, defs)


def build_button(label: str, icon_name: str, color: str) -> str:
    css = (".sh{animation:shimmer 3.6s ease-in-out infinite}"
           "@keyframes shimmer{0%,60%{transform:translateX(-80px)}100%{transform:translateX(260px)}}"
           + RM % ".sh{animation:none;opacity:0}")
    defs = '<clipPath id="cp"><rect x="1" y="1" width="198" height="46" rx="23"/></clipPath>'
    body = (f'<rect x="1" y="1" width="198" height="46" rx="23" fill="{PANEL}" stroke="{color}" stroke-width="1.5"/>'
            f'<g clip-path="url(#cp)"><rect class="sh" x="0" y="0" width="40" height="48" fill="{TEXT}" fill-opacity=".12" '
            f'transform="skewX(-20)"/></g>'
            + icon(icon_name, 28, 12, 24, color=color)
            + f'<text x="64" y="30" font-size="16" font-weight="600" fill="{TEXT}">{escape(label)}</text>')
    return _svg(200, 48, label, css, body, defs)


def build_roles() -> str:
    words = ["APIs", "Architecture", "Security"]
    css = (f".pre{{font-size:20px;fill:{PERI}}}.w{{font-size:24px;font-weight:700;fill:{ICE}}}"
           ".cycle{opacity:0;animation:role 7.5s ease-in-out infinite both}"
           "@keyframes role{0%{opacity:0;transform:translateY(8px)}5%,28%{opacity:1;transform:none}33%,100%{opacity:0;transform:translateY(-8px)}}"
           ".static{display:none}.ul{stroke-dasharray:60;animation:ul 2.5s ease-in-out infinite}"
           "@keyframes ul{0%,100%{stroke-dashoffset:60}40%,70%{stroke-dashoffset:0}}"
           + RM % ".cycle{display:none}.ul{display:none}.static{display:inline}")
    cyc = "".join(f'<text class="cycle w" x="104" y="34" style="animation-delay:{i * 2.5}s">{w}</text>'
                  for i, w in enumerate(words))
    body = (f'<text class="pre" x="0" y="34">Building</text>{cyc}'
            f'<line class="ul" x1="104" y1="42" x2="164" y2="42" stroke="{BLUE}" stroke-width="2" stroke-linecap="round"/>'
            f'<g class="static"><text class="w" x="104" y="34" style="font-size:20px">APIs · Architecture · Security</text></g>')
    return _svg(460, 52, "Building APIs, architecture and security", css, body)


def build_right_now(items: list[tuple[str, str]], title: str = "Right now") -> str:
    h = 70 + 46 * len(items)
    css = (f".t{{font-size:20px;font-weight:600;fill:{TEXT}}}.i{{font-size:15px;fill:{TEXT}}}"
           ".lv{animation:blink 2s ease-in-out infinite}@keyframes blink{0%,100%{opacity:1}50%{opacity:.25}}"
           ".ln{stroke-dasharray:480;stroke-dashoffset:480;animation:draw 1s ease-out forwards}"
           "@keyframes draw{to{stroke-dashoffset:0}}"
           ".r{animation:rise .6s ease-out both}@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"
           + RM % ".lv,.r{animation:none}.ln{animation:none;stroke-dashoffset:0}")
    rows = []
    for i, (name, text) in enumerate(items):
        y = 62 + i * 46
        d = 0.2 + i * 0.25
        rows.append(f'<g class="r" style="animation-delay:{d}s">{icon(name, 24, y, 24, color=ICE)}'
                    f'<text class="i" x="60" y="{y + 18}">{escape(text)}</text></g>'
                    f'<line class="ln" x1="24" y1="{y + 34}" x2="536" y2="{y + 34}" stroke="{EDGE}" '
                    f'style="animation-delay:{d}s"/>')
    body = (f'<rect x=".5" y=".5" width="559" height="{h - 1}" rx="16" fill="{PANEL}" stroke="{EDGE}"/>'
            f'<circle class="lv" cx="32" cy="34" r="5" fill="{ICE}"/><text class="t" x="48" y="41">{escape(title)}</text>'
            + "".join(rows))
    return _svg(560, h, title, css, body)


def build_bar(color: str) -> str:
    css = (".f{transform-box:fill-box;transform-origin:left;animation:grow 1.2s cubic-bezier(.2,.8,.2,1) both}"
           "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
           ".g{animation:glide 3s ease-in-out infinite 1.2s}"
           "@keyframes glide{0%{transform:translateX(-60px)}100%{transform:translateX(320px)}}"
           + RM % ".f,.g{animation:none}.g{opacity:0}")
    defs = '<clipPath id="bc"><rect width="300" height="8" rx="4"/></clipPath>'
    body = (f'<rect width="300" height="8" rx="4" fill="{EDGE}"/><g clip-path="url(#bc)">'
            f'<rect class="f" width="300" height="8" fill="{color}"/>'
            f'<rect class="g" width="50" height="8" fill="{TEXT}" fill-opacity=".35"/></g>')
    return _svg(300, 8, "Accent bar", css, body, defs)


RIGHT_NOW = {
    "right-now.svg": ("Right now", [
        ("database", "Concurrency-safe booking with PostgreSQL and Redis"),
        ("docker", "Containerizing my projects"),
        ("shield", "Security and software architecture"),
        ("book", "Technical English")]),
    "right-now-pt.svg": ("Agora", [
        ("database", "Reservas sem conflito com PostgreSQL e Redis"),
        ("docker", "Containerizando meus projetos"),
        ("shield", "Segurança e arquitetura de software"),
        ("book", "Inglês técnico")]),
}


def main() -> None:
    out = {"scene-divider.svg": build_divider(),
           "btn-linkedin.svg": build_button("LinkedIn", "linkedin", ICE),
           "btn-github.svg": build_button("GitHub", "github", PALE),
           "roles.svg": build_roles()}
    for fn, (title, items) in RIGHT_NOW.items():
        out[fn] = build_right_now(items, title)
    for i, c in enumerate((BLUE, ICE, PERI, PALE), start=1):
        out[f"bar-{i}.svg"] = build_bar(c)
    for fn, svg in out.items():
        (ASSETS / fn).write_text(svg, encoding="utf-8")
    print(f"wrote {len(out)} assets")


if __name__ == "__main__":
    main()
