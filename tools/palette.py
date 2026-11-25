"""Single source of colors for the navy README (see readme-perfil-v2-design.md)."""
from __future__ import annotations

NAVY, PANEL, EDGE = "#0A1428", "#101E3A", "#1B2C52"
BLUE, ICE, PERI, PALE = "#2F6FED", "#5CC8FF", "#8AA4FF", "#B9D0FF"
TEXT, MUTED = "#E6ECF8", "#6B7FA3"
PALETTE = {NAVY, PANEL, EDGE, BLUE, ICE, PERI, PALE, TEXT, MUTED}


def _rgb(c: str) -> tuple[int, int, int]:
    c = c.lstrip("#")
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)


def _lum(c: str) -> float:
    def f(v: int) -> float:
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = (f(v) for v in _rgb(c))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def ensure_contrast(fg: str, bg: str, minimum: float = 3.0) -> str:
    """Lighten fg toward white until it reaches the minimum contrast against bg."""
    if contrast(fg, bg) >= minimum:
        return fg
    r, g, b = _rgb(fg)
    for step in range(1, 21):
        t = step / 20
        mixed = "#%02x%02x%02x" % tuple(round(v + (255 - v) * t) for v in (r, g, b))
        if contrast(mixed, bg) >= minimum:
            return mixed
    return "#ffffff"
