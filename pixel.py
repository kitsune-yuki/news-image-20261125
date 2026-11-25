#!/usr/bin/env python3
"""Pixel-art dawn launch for the 25 November 2026 front page.

Shenzhou-24 climbs away from its pad at Jiuquan in the Gobi desert
on the morning of 25 November 2026, carrying Tang Hongbo, Wu Yi and
Muhammad Zeeshan Ali — the first Pakistani in orbit, and the first
foreigner aboard China's Tiangong station. The picture is built one
pixel at a time on a 234 by 48 grid: a graded dawn sky with fading
stars, a low sun, desert ridges, the Long March 2F with its layered
flame plume, smoke billowing from the pad and the launch tower in
silhouette. It is scaled up with NEAREST so every pixel stays crisp.

Deterministic: one fixed seed, no network, no clock.

Run:  python3 pixel.py
Writes scene.png beside this file: 936 by 192.
"""
import random

from PIL import Image, ImageDraw

W, H = 234, 48
SCALE = 4
SEED = 1125

PAL = {
    "night": (16, 20, 48),
    "violet": (62, 46, 96),
    "magenta": (148, 62, 96),
    "ember": (220, 110, 52),
    "amber": (255, 160, 64),
    "sun": (255, 224, 140),
    "glow": (255, 170, 80),
    "star": (220, 222, 240),
    "star_dim": (150, 152, 180),
    "ridge": (44, 34, 56),
    "sand_dark": (52, 38, 34),
    "sand": (76, 54, 44),
    "sand_light": (122, 92, 66),
    "sand_lit": (196, 150, 96),
    "rock": (30, 24, 26),
    "steel": (24, 26, 34),
    "steel_light": (64, 68, 80),
    "hull": (232, 232, 226),
    "hull_shade": (168, 168, 164),
    "band": (178, 34, 34),
    "dark": (20, 20, 24),
    "lamp": (255, 214, 104),
    "flame_white": (255, 250, 220),
    "flame_yellow": (255, 214, 90),
    "flame_orange": (255, 150, 40),
    "flame_red": (230, 70, 20),
    "smoke_dark": (96, 96, 100),
    "smoke": (148, 148, 150),
    "smoke_light": (198, 198, 200),
    "smoke_pale": (228, 228, 230),
    "smoke_warm": (255, 180, 90),
}


def build():
    rng = random.Random(SEED)
    canvas = Image.new("RGB", (W, H), PAL["night"])
    pen = ImageDraw.Draw(canvas)

    def dot(x, y, name):
        if 0 <= x < W and 0 <= y < H:
            canvas.putpixel((x, y), PAL[name])

    def stripe(y0, y1, name):
        pen.rectangle([0, y0, W - 1, y1], fill=PAL[name])

    def speckle(y, first, second):
        for x in range(W):
            dot(x, y, first if (x + y) % 2 == 0 else second)

    def disc(cx, cy, rx, ry, name):
        pen.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=PAL[name])

    def diamond(cx, cy, radius, name):
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if abs(dx) + abs(dy) <= radius:
                    dot(cx + dx, cy + dy, name)

    def plume(cx, top, depth, name, chance):
        for dy in range(depth):
            half = 9 - dy // 2
            for dx in range(-half, half + 1):
                if rng.random() < chance:
                    dot(cx + dx, top + dy, name)

    # Dawn sky, graded from night at the top to amber at the horizon.
    for y0, y1, name in [
        (0, 4, "night"), (5, 9, "violet"), (10, 14, "magenta"),
        (15, 18, "ember"), (19, 20, "amber"),
    ]:
        stripe(y0, y1, name)
    speckle(9, "violet", "magenta")
    speckle(14, "magenta", "ember")
    speckle(18, "ember", "amber")

    # Fading stars in the upper sky, brighter ones sparse.
    for _ in range(46):
        x = rng.randint(0, W - 1)
        y = rng.randint(0, 8)
        dot(x, y, "star" if rng.random() < 0.35 else "star_dim")

    # Sun rising on the right, half above the horizon line.
    diamond(198, 15, 7, "glow")
    diamond(198, 15, 4, "sun")
    dot(198, 15, "flame_white")

    # Desert ridges along the horizon, broken and uneven.
    for x in range(0, 96):
        top = 19 - (x % 7) // 3
        for y in range(top, 21):
            dot(x, y, "ridge")
    for x in range(150, W):
        top = 20 - (x % 5) // 3
        for y in range(top, 21):
            dot(x, y, "ridge")

    # Desert floor: darker bands toward the bottom, lit by the dawn.
    stripe(21, 26, "sand_dark")
    stripe(27, 35, "sand")
    stripe(36, H - 1, "sand_light")
    speckle(26, "sand_dark", "sand")
    speckle(35, "sand", "sand_light")
    for x in range(W):
        y = 40 + int(2.5 * (1 + ((x * 7) % 11) / 11.0))
        if y < H:
            dot(x, y, "sand_lit" if x % 3 == 0 else "sand")
    for rx, ry in [(8, 44), (30, 42), (52, 45), (176, 43), (205, 45),
                   (222, 42), (150, 44), (66, 46)]:
        dot(rx, ry, "rock")
        dot(rx + 1, ry, "rock")

    # Launch tower in dark steel, left of the rocket, with crossbars.
    pen.rectangle([92, 14, 96, 34], fill=PAL["steel"])
    pen.rectangle([92, 14, 96, 15], fill=PAL["steel_light"])
    for y in (18, 22, 26, 30):
        pen.rectangle([92, y, 100, y], fill=PAL["steel"])
    for i in range(8):
        dot(97 + i, 15 - i // 4, "steel_light")

    # Low pad buildings with lit windows, either side of the pad.
    pen.rectangle([70, 30, 82, 34], fill=PAL["steel"])
    pen.rectangle([138, 30, 150, 34], fill=PAL["steel"])
    for wx in (73, 77, 141, 146):
        dot(wx, 32, "lamp")

    # The Long March 2F, climbing: tapered nose, white body, red band.
    for y, half in [(5, 1), (6, 2), (7, 3), (8, 4)]:
        pen.rectangle([112 - half, y, 112 + half - 1, y], fill=PAL["hull"])
    pen.rectangle([108, 9, 117, 22], fill=PAL["hull"])
    pen.rectangle([116, 9, 117, 22], fill=PAL["hull_shade"])
    pen.rectangle([108, 18, 117, 19], fill=PAL["band"])
    dot(108, 9, "flame_white")
    for y in range(9, 23):
        if y % 4 == 0:
            dot(108, y, "flame_white")
    # Fins flaring at the base of the body.
    pen.rectangle([105, 22, 107, 25], fill=PAL["hull_shade"])
    pen.rectangle([118, 22, 120, 25], fill=PAL["hull_shade"])
    dot(105, 25, "dark")
    dot(120, 25, "dark")
    # A thin vapour trail curling off the nose.
    for i in range(6):
        dot(109 - i, 4 - i // 3, "smoke_pale" if i % 2 else "smoke_light")

    # Flame plume below the rocket, layered white to deep red.
    plume(112, 26, 12, "flame_red", 0.75)
    plume(112, 26, 10, "flame_orange", 0.8)
    for dy in range(8):
        half = 3 - dy // 3
        for dx in range(-half, half + 1):
            dot(112 + dx, 26 + dy, "flame_yellow")
    for dy in range(6):
        for dx in range(-1, 2):
            dot(112 + dx, 26 + dy, "flame_white")
    # Bright glow where the plume meets the pad.
    for dx in range(-12, 13):
        for dy in range(3):
            if rng.random() < 0.6:
                dot(112 + dx, 34 + dy,
                    "flame_orange" if (dx + dy) % 2 else "flame_yellow")

    # Smoke clouds billowing out from the pad, drifting wide.
    for cx, cy, rx, ry, name in [
        (112, 36, 16, 5, "smoke_dark"), (96, 38, 14, 5, "smoke_dark"),
        (130, 38, 14, 5, "smoke"), (82, 40, 12, 4, "smoke"),
        (144, 40, 12, 4, "smoke_light"), (68, 42, 10, 4, "smoke_light"),
        (158, 42, 10, 4, "smoke_light"), (108, 33, 8, 3, "smoke"),
        (120, 33, 8, 3, "smoke_light"), (98, 35, 6, 3, "smoke_pale"),
        (126, 35, 6, 3, "smoke_pale"), (54, 43, 9, 3, "smoke_light"),
        (186, 43, 9, 3, "smoke_light"),
    ]:
        disc(cx, cy, rx, ry, name)
    for _ in range(70):
        x = rng.randint(52, 172)
        y = rng.randint(31, 44)
        if rng.random() < 0.6:
            dot(x, y, "smoke_pale" if rng.random() < 0.5 else "smoke_light")
    # Warm rim light on the smoke, on the side facing the flame.
    for x, y in [(104, 35), (105, 37), (103, 39), (121, 35), (120, 37),
                 (122, 39), (106, 33), (119, 33), (102, 41), (123, 41)]:
        dot(x, y, "smoke_warm" if (x + y) % 2 else "flame_orange")

    # Pad floodlights: tiny bright dots along the ground.
    for lx in (86, 104, 122, 140):
        dot(lx, 35, "lamp")
        dot(lx, 36, "lamp")

    big = canvas.resize((W * SCALE, H * SCALE), Image.NEAREST)
    big.save("scene.png", format="PNG", optimize=True)
    print("wrote scene.png", big.size)


if __name__ == "__main__":
    build()
