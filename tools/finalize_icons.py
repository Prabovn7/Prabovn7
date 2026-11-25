"""Renders assets/icons/*.svg as dark tiles with a readable colored glyph.

Reads tools/icon_paths.json (from build_icons.js), picks each glyph color
(official brand color, or a blue by role) guaranteeing contrast >= 3 against
the tile, writes the SVGs and stores the chosen color back as "color".
"""
from __future__ import annotations

import json
from pathlib import Path

from palette import BLUE, ICE, PALE, PANEL, PERI, ensure_contrast

HERE = Path(__file__).resolve().parent
ICONS = HERE.parent / "assets" / "icons"
JSON_PATH = HERE / "icon_paths.json"

ROLE = {  # generic (lucide) icons: one blue per role
    "user": ICE, "activity": ICE, "target": ICE, "bus": ICE, "weather": ICE, "terminal": ICE, "sparkles": ICE,
    "briefcase": PERI, "shield": PERI, "chart": PERI, "vscode": PERI, "grad": PERI, "history": PERI,
    "mail": PALE, "linkedin": PALE, "book": PALE, "globe": PALE, "badge": PALE, "key": PALE,
}


def render(name: str, spec: dict, color: str) -> str:
    if spec["type"] == "brand":
        glyph = f'<path fill="{color}" d="{spec["path"]}"/>'
    else:
        glyph = (f'<g fill="none" stroke="{color}" stroke-width="1.75" stroke-linecap="round" '
                 f'stroke-linejoin="round">{spec["inner"]}</g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32" role="img">'
            f'<title>{name}</title><rect width="32" height="32" rx="8" fill="{PANEL}"/>'
            f'<g transform="translate(6 6) scale(0.8333)">{glyph}</g></svg>\n')


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    ICONS.mkdir(parents=True, exist_ok=True)
    for name, spec in data.items():
        base = spec["hex"] if spec["type"] == "brand" else ROLE.get(name, BLUE)
        color = ensure_contrast(base, PANEL, 4.5)
        spec["color"] = color
        (ICONS / f"{name}.svg").write_text(render(name, spec, color), encoding="utf-8")
    JSON_PATH.write_text(json.dumps(data, indent=1), encoding="utf-8")
    print(len(data), "icons")


if __name__ == "__main__":
    main()
