# -*- coding: utf-8 -*-
"""Генерирует PWA-скриншоты радара для manifest.webmanifest (rich install card).
Рисует стилизованный кадр сонара в фирменной палитре (fallback, без headless-браузера).
Запуск: python gen_screenshots.py -> screenshot-narrow.png (540x720), screenshot-wide.png (720x540)."""
import math
from PIL import Image, ImageDraw, ImageFont

BG      = (2, 16, 11)      # #02100b
PANEL   = (6, 41, 27)      # #06291b
ACCENT  = (34, 255, 155)   # #22ff9b
DIM     = (63, 122, 95)    # #3f7a5f
TEXT    = (231, 255, 242)  # #e7fff2
BLIP    = (255, 106, 122)  # #ff6a7a
SS = 4  # супер-сэмплинг


def _font(size):
    for name in ("segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _fontb(size):
    for name in ("segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return _font(size)


def _center(d, cx, y, text, font, fill):
    l, t, r, b = d.textbbox((0, 0), text, font=font)
    d.text((cx - (r - l) / 2, y), text, font=font, fill=fill)
    return b - t


def draw_radar(d, cx, cy, R):
    # концентрические кольца
    for k in (1.0, 0.72, 0.44, 0.18):
        rr = R * k
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=DIM, width=SS)
    # оси
    d.line([cx - R, cy, cx + R, cy], fill=DIM, width=SS)
    d.line([cx, cy - R, cx, cy + R], fill=DIM, width=SS)
    # сектор развёртки (клин)
    a0 = -35
    pts = [(cx, cy)]
    for a in range(a0 - 32, a0 + 1, 2):
        pts.append((cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))))
    d.polygon(pts, fill=(ACCENT[0], ACCENT[1], ACCENT[2]))
    # линия развёртки
    d.line([cx, cy, cx + R * math.cos(math.radians(a0)), cy + R * math.sin(math.radians(a0))],
           fill=ACCENT, width=SS)
    # блики-джинны
    for bx, by, br, col in [(0.35, -0.28, 9, ACCENT), (-0.42, 0.2, 8, ACCENT),
                            (0.1, 0.5, 7, BLIP), (-0.15, -0.55, 6, ACCENT),
                            (0.6, 0.12, 6, ACCENT)]:
        px, py = cx + R * bx, cy + R * by
        rr = br * SS
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=col)
    # центр — «ТЫ»
    d.ellipse([cx - 6 * SS, cy - 6 * SS, cx + 6 * SS, cy + 6 * SS], fill=TEXT)


def render(w, h, path):
    W, H = w * SS, h * SS
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # мягкое радиальное свечение фона
    for i, k in enumerate((0.9, 0.6, 0.3)):
        rr = int(min(W, H) * k)
        cx, cy = W // 2, int(H * 0.5)
        glow = (int(BG[0] + 6 * (3 - i)), int(BG[1] + 10 * (3 - i)), int(BG[2] + 8 * (3 - i)))
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=glow)
    # заголовок
    pad = int(H * 0.06)
    _center(d, W // 2, pad, "СОНАР ДЖИННОВ", _fontb(int(W * 0.072)), ACCENT)
    _center(d, W // 2, pad + int(W * 0.095), "jinnradar.com", _font(int(W * 0.036)), DIM)
    # радар
    R = int(min(W, H) * (0.34 if w < h else 0.30))
    cy = int(H * 0.53)
    draw_radar(d, W // 2, cy, R)
    # счётчик снизу
    by = int(H * 0.86)
    _center(d, W // 2, by, "1 480 219", _fontb(int(W * 0.078)), TEXT)
    _center(d, W // 2, by + int(W * 0.10), "джиннов на Земле прямо сейчас", _font(int(W * 0.034)), DIM)
    img = img.resize((w, h), Image.LANCZOS)
    img.save(path, "PNG")
    print("saved", path, img.size)


if __name__ == "__main__":
    render(540, 720, "screenshot-narrow.png")
    render(720, 540, "screenshot-wide.png")
