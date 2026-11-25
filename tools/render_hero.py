"""Renders the navy cinematic hero (hero.webp + hero-static.png).

A procedural web (own geometry) spreads from the top-right in icy blue over a
deep navy grade with a soft blue glow, letterbox bars, vignette and fine grain.
Name/role/tags are revealed by a left-to-right wipe. The loop starts and ends
on near-black navy.
"""
from __future__ import annotations

import math
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from palette import EDGE, ICE, MUTED, NAVY, PALE, PERI, TEXT

W, H = 1280, 540
S = 2  # supersampling
BAR = 46
CENTER = (1040.0, 120.0)
HERE = Path(__file__).resolve().parent
INTER_DIR = Path("/usr/share/fonts/opentype/inter")
DISPLAY_FONT = HERE / "fonts" / "BigShouldersDisplay-800.woff"
NAME, SUB, TAG = "PABLO SANTOS", "BACKEND SOFTWARE ENGINEER", "APIs  ·  Architecture  ·  Security"


def _rgb(c: str) -> np.ndarray:
    c = c.lstrip("#")
    return np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)


C_NAVY, C_ICE, C_PALE, C_PERI, C_TEXT, C_MUTED, C_EDGE = (_rgb(x) for x in (NAVY, ICE, PALE, PERI, TEXT, MUTED, EDGE))
C_FLOOR, C_BAR = np.array([5, 10, 22], np.float32), np.array([6, 12, 26], np.float32)
C_GLOW = np.array([20, 55, 120], np.float32)


def _inter(weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(INTER_DIR / f"Inter-{weight}.otf"), size * S)


def _display(size: int) -> ImageFont.FreeTypeFont:
    if DISPLAY_FONT.exists():
        return ImageFont.truetype(str(DISPLAY_FONT), size * S)
    return _inter("Bold", int(size * 0.72))


def _tracked(draw, xy, text, font, tracking, fill=255):
    x, y = xy
    for ch in text:
        draw.text((x * S, y * S), ch, font=font, fill=fill)
        x += font.getlength(ch) / S + tracking


def _clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def _ease(v):
    v = _clamp(v)
    return v * v * (3 - 2 * v)


def _web_geometry():
    rng = np.random.default_rng(7)
    n = 14
    angles = [2 * math.pi * i / n + rng.uniform(-0.06, 0.06) for i in range(n)]
    radii = [58 * (1.55 ** k) for k in range(7)]
    cx, cy = CENTER
    rings = []
    for r in radii:
        pts = []
        for j in range(n + 1):
            a0 = angles[j % n]
            a1 = angles[(j + 1) % n] + (2 * math.pi if (j + 1) % n == 0 else 0)
            p0 = (cx + r * math.cos(a0), cy + r * math.sin(a0))
            p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
            mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
            ctrl = (cx + (mid[0] - cx) * 0.84, cy + (mid[1] - cy) * 0.84)
            for s in range(8):
                u = s / 8
                pts.append(((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * ctrl[0] + u ** 2 * p1[0],
                            (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * ctrl[1] + u ** 2 * p1[1]))
        rings.append(pts)
    return angles, rings


ANGLES, RINGS = _web_geometry()


def _web_layer(t: float) -> np.ndarray:
    img = Image.new("L", (W * S, H * S), 0)
    d = ImageDraw.Draw(img)
    cx, cy = CENTER
    for i, a in enumerate(ANGLES):
        p = _ease((t - 0.05 * i) / 1.3)
        if p > 0:
            L = 1000 * p
            d.line([(cx * S, cy * S), ((cx + L * math.cos(a)) * S, (cy + L * math.sin(a)) * S)], fill=125, width=2)
    for k, pts in enumerate(RINGS):
        p = _ease((t - (0.9 + 0.33 * k)) / 1.1)
        if p > 0:
            m = max(2, int(len(pts) * p))
            d.line([(x * S, y * S) for x, y in pts[:m]], fill=110, width=2, joint="curve")
    return np.asarray(img.resize((W, H), Image.LANCZOS)).astype(np.float32)


def _static_fields():
    xs = np.linspace(0, 1, W, dtype=np.float32)[None, :]
    ys = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    web_mask = np.broadcast_to(0.18 + 0.82 * np.clip((xs - 0.30) / 0.45, 0, 1) ** 1.2, (H, W)).copy()
    vig = np.clip(1 - (((xs - 0.5) * 1.15) ** 2 + ((ys - 0.5) * 1.35) ** 2) * 1.05, 0.2, 1.0).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d2 = ((xx - CENTER[0]) ** 2 + (yy - CENTER[1]) ** 2) / (520.0 ** 2)
    glow = (np.exp(-d2) * 0.55).astype(np.float32)
    return web_mask, vig, glow, xx, yy


WEB_MASK, VIGNETTE, GLOW, XX, YY = _static_fields()
COLS = np.arange(W, dtype=np.float32)[None, :]


def _text_layers():
    def layer(font, y, text, tracking, x=96):
        img = Image.new("L", (W * S, H * S), 0)
        _tracked(ImageDraw.Draw(img), (x, y), text, font, tracking)
        return np.asarray(img.resize((W, H), Image.LANCZOS)).astype(np.float32)[..., None] / 255.0

    return [
        (layer(_display(150), 142, NAME, 5), 3.0, C_TEXT),
        (layer(_inter("Medium", 30), 306, SUB, 9), 3.7, C_PERI),
        (layer(_inter("Regular", 24), 352, TAG, 3), 4.2, C_MUTED),
    ]


def _bar_text():
    img = Image.new("L", (W * S, H * S), 0)
    d, f = ImageDraw.Draw(img), _inter("Medium", 15)
    _tracked(d, (96, 14), "SCENE 01  —  BACKEND", f, 3)
    _tracked(d, (W - 190, 14), "PORTFOLIO  2026", f, 3)
    _tracked(d, (96, H - BAR + 14), "APIs  /  DATA  /  SECURITY", f, 3)
    return np.asarray(img.resize((W, H), Image.LANCZOS)).astype(np.float32)[..., None] / 255.0


TEXTS, BAR_TEXT = _text_layers(), _bar_text()


def frame_at(t: float, seconds: float, rng: np.random.Generator, grain: float = 3.2) -> Image.Image:
    web = _web_layer(t) * WEB_MASK
    sp = _clamp((t - 3.4) / 3.0)
    band = np.exp(-(((XX + YY * 0.6) - (-300 + sp * (W + 900))) / 130.0) ** 2)[..., None]
    w = np.clip(web / 125.0, 0, 1.6)[..., None]

    img = C_NAVY * 0.92 + GLOW[..., None] * C_GLOW
    img = img + w * C_ICE * 0.95 + (w * band) * (C_PALE - C_ICE) * 0.9 + (w * band) * 40
    for layer, start, color in TEXTS:
        p = _ease((t - start) / 1.3)
        reach = p * (W + 260) - 260 * (1 - p)
        a = layer * np.clip((reach - COLS) / 260.0, 0, 1)[..., None]
        img = img * (1 - a) + color * a
    img = img * VIGNETTE[..., None]

    img[:BAR], img[H - BAR:] = C_BAR, C_BAR
    for y in (BAR - 1, BAR, H - BAR - 1, H - BAR):
        img[y, :] = C_EDGE
    a = BAR_TEXT * _ease((t - 0.4) / 0.8)
    mask = np.zeros((H, W, 1), np.float32)
    mask[:BAR], mask[H - BAR:] = 1, 1
    img = img * (1 - a * mask) + C_MUTED * (a * mask)

    fade = _ease(t / 0.5) * (1 - _ease((t - (seconds - 0.7)) / 0.6))
    img = C_FLOOR + (img - C_FLOOR) * fade
    img = img + rng.normal(0, grain, (H, W, 1)).astype(np.float32)
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")


def render_hero(out_dir: Path, fps: int = 16, seconds: float = 7.0, quality: int = 52):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(11)
    n = int(fps * seconds)
    tmp = Path(tempfile.mkdtemp(prefix="hero_"))
    try:
        for i in range(n):
            frame_at(i / fps, seconds, rng).save(tmp / f"f{i:04d}.png")
        webp = out_dir / "hero.webp"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmp / "f%04d.png"),
             "-c:v", "libwebp_anim", "-lossless", "0", "-quality", str(quality),
             "-compression_level", "6", "-loop", "0", str(webp)],
            check=True,
        )
        static = out_dir / "hero-static.png"
        frame_at(min(seconds - 1.0, 6.0), seconds, np.random.default_rng(3), grain=0.8).save(static, optimize=True)
        return webp, static
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    import sys

    q = int(sys.argv[1]) if len(sys.argv) > 1 else 52
    w, s = render_hero(HERE.parent / "assets", quality=q)
    print(w, w.stat().st_size, s, s.stat().st_size)
