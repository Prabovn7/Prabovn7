"""Renders the cinematic, monochrome hero (hero.webp + hero-static.png).

Composition: a procedural web (own geometry) spreads from the top-right,
dimmed on the left where the text sits; letterbox bars, vignette and fine
grain; name/subtitle revealed by a left-to-right wipe. Loop starts and ends
on near-black.
"""
from __future__ import annotations

import math
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 540
S = 2  # supersampling factor
BAR = 46
CENTER = (1040.0, 120.0)
FONT_DIR = Path("/usr/share/fonts/opentype/inter")
NAME = "PABLO SANTOS"
SUB = "BACKEND SOFTWARE ENGINEER"
TAG = "APIs  ·  Architecture  ·  Security"


def _font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / f"Inter-{weight}.otf"), size * S)


def _tracked(draw: ImageDraw.ImageDraw, xy, text, font, tracking, fill=255):
    x, y = xy
    for ch in text:
        draw.text((x * S, y * S), ch, font=font, fill=fill)
        x += font.getlength(ch) / S + tracking


def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def _ease(v: float) -> float:
    v = _clamp(v)
    return v * v * (3 - 2 * v)


def _web_geometry():
    rng = np.random.default_rng(7)
    n = 14
    angles = [2 * math.pi * i / n + rng.uniform(-0.06, 0.06) for i in range(n)]
    radii = [58 * (1.55 ** k) for k in range(7)]
    cx, cy = CENTER
    rings = []
    for k, r in enumerate(radii):
        pts = []
        for j in range(n + 1):
            a0 = angles[j % n]
            a1 = angles[(j + 1) % n] + (2 * math.pi if (j + 1) % n == 0 else 0)
            p0 = (cx + r * math.cos(a0), cy + r * math.sin(a0))
            p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
            mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
            ctrl = (cx + (mid[0] - cx) * 0.84, cy + (mid[1] - cy) * 0.84)
            for s in range(0, 8):
                u = s / 8
                x = (1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * ctrl[0] + u**2 * p1[0]
                y = (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * ctrl[1] + u**2 * p1[1]
                pts.append((x, y))
        rings.append(pts)
    return angles, rings


ANGLES, RINGS = _web_geometry()


def _web_layer(t: float) -> np.ndarray:
    img = Image.new("L", (W * S, H * S), 0)
    d = ImageDraw.Draw(img)
    cx, cy = CENTER
    for i, a in enumerate(ANGLES):
        p = _ease((t - 0.05 * i) / 1.3)
        if p <= 0:
            continue
        L = 1000 * p
        d.line([(cx * S, cy * S), ((cx + L * math.cos(a)) * S, (cy + L * math.sin(a)) * S)],
               fill=105, width=2)
    for k, pts in enumerate(RINGS):
        p = _ease((t - (0.9 + 0.33 * k)) / 1.1)
        if p <= 0:
            continue
        m = max(2, int(len(pts) * p))
        d.line([(x * S, y * S) for x, y in pts[:m]], fill=95, width=2, joint="curve")
    arr = np.asarray(img.resize((W, H), Image.LANCZOS)).astype(np.float32)
    return arr


def _static_masks():
    xs = np.linspace(0, 1, W, dtype=np.float32)[None, :]
    ys = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    # dim the web on the left where text sits
    web_mask = 0.18 + 0.82 * np.clip((xs - 0.30) / 0.45, 0, 1) ** 1.2
    web_mask = np.broadcast_to(web_mask, (H, W)).copy()
    # vignette
    vx = (xs - 0.5) * 1.15
    vy = (ys - 0.5) * 1.35
    vig = np.clip(1 - (vx**2 + vy**2) * 1.05, 0.15, 1.0)
    return web_mask, vig.astype(np.float32)


WEB_MASK, VIGNETTE = _static_masks()


def _text_layers():
    """Return list of (layer ndarray 0..1 at 1x, wipe_start, brightness)."""
    def layer(font, y, text, tracking, x=96):
        img = Image.new("L", (W * S, H * S), 0)
        _tracked(ImageDraw.Draw(img), (x, y), text, font, tracking)
        return np.asarray(img.resize((W, H), Image.LANCZOS)).astype(np.float32) / 255.0

    return [
        (layer(_font("Bold", 92), 196, NAME, 7), 3.0, 242.0),
        (layer(_font("Medium", 30), 306, SUB, 9), 3.7, 170.0),
        (layer(_font("Regular", 24), 352, TAG, 3), 4.2, 120.0),
    ]


def _bars_layer():
    img = Image.new("L", (W * S, H * S), 0)
    d = ImageDraw.Draw(img)
    f = _font("Medium", 15)
    _tracked(d, (96, 14), "SCENE 01  —  BACKEND", f, 3)
    _tracked(d, (W - 190, 14), "PORTFOLIO  2026", f, 3)
    _tracked(d, (96, H - BAR + 14), "APIs  /  DATA  /  SECURITY", f, 3)
    arr = np.asarray(img.resize((W, H), Image.LANCZOS)).astype(np.float32) / 255.0
    return arr * 70.0


TEXTS = _text_layers()
BAR_TEXT = _bars_layer()
COLS = np.arange(W, dtype=np.float32)[None, :]
XX, YY = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))


def frame_at(t: float, seconds: float, rng: np.random.Generator) -> Image.Image:
    web = _web_layer(t) * WEB_MASK
    # light sweep along the web (diagonal band)
    sp = _clamp((t - 3.4) / 3.0)
    pos = -300 + sp * (W + 900)
    band = np.exp(-(((XX + YY * 0.6) - pos) / 130.0) ** 2)
    web = web * (1 + 0.9 * band)

    out = web.copy()
    for layer, start, bright in TEXTS:
        p = _clamp((t - start) / 1.3)
        reach = _ease(p) * (W + 260) - 260 * (1 - _ease(p))
        a = np.clip((reach - COLS) / 260.0, 0, 1)
        out = np.maximum(out, layer * a * bright)

    out = out * VIGNETTE
    out[:BAR, :] = 0
    out[H - BAR:, :] = 0
    out[BAR - 1:BAR + 1, :] = np.maximum(out[BAR - 1:BAR + 1, :], 28)
    out[H - BAR - 1:H - BAR + 1, :] = np.maximum(out[H - BAR - 1:H - BAR + 1, :], 28)
    out = np.maximum(out, BAR_TEXT * _ease((t - 0.4) / 0.8))

    fade = _ease(t / 0.5) * (1 - _ease((t - (seconds - 0.7)) / 0.6))
    out = 7 + out * fade * 0.97
    out = out + rng.normal(0, 3.2, out.shape).astype(np.float32)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "L").convert("RGB")


def render_hero(out_dir: Path, fps: int = 16, seconds: float = 7.0, quality: int = 62):
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
        frame_at(min(seconds - 1.0, 6.0), seconds, np.random.default_rng(3)).save(static, optimize=True)
        return webp, static
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    import sys

    q = int(sys.argv[1]) if len(sys.argv) > 1 else 62
    here = Path(__file__).resolve().parent.parent
    w, s = render_hero(here / "assets", quality=q)
    print(w, w.stat().st_size, s, s.stat().st_size)
