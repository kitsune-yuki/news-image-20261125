#!/usr/bin/env python3
"""Draw the lead illustration as pixel art and save it as scene.png.

The scene is the Shenzhou-24 launch at dawn on 25 November 2026: a
Long March 2F rocket climbing away from its pad at Jiuquan in the
Gobi desert, carrying three astronauts including Muhammad Zeeshan
Ali, the first Pakistani in orbit and the first foreigner aboard
China's Tiangong station. It is drawn on a tiny 234x48 grid, one
pixel at a time, with a small dawn palette, then scaled up with
NEAREST so every pixel stays crisp. Deterministic: a fixed seed, no
network, no clock.

Run:  python3 pixel.py
Writes scene.png beside this file: 936x192.
"""
import random

from PIL import Image, ImageDraw

GW, GH = 234, 48
PX = 4

# Dawn sky: deep indigo at the top, violet, magenta, ember, amber.
INDIGO = (16, 20, 48)
VIOLET = (62, 46, 96)
MAGENTA = (148, 62, 96)
EMBER = (220, 110, 52)
HORIZON = (255, 160, 64)
SUN = (255, 224, 140)
GLOW = (255, 170, 80)
STAR = (220, 222, 240)
STAR_DIM = (150, 152, 180)
# Desert ground and distant mountains.
MOUNTAIN = (44, 34, 56)
DESERT_D = (52, 38, 34)
DESERT_M = (76, 54, 44)
DESERT_L = (122, 92, 66)
SAND_LIT = (196, 150, 96)
ROCK = (30, 24, 26)
# Rocket and pad structures.
STEEL = (24, 26, 34)
STEEL_L = (64, 68, 80)
BODY = (232, 232, 226)
BODY_D = (168, 168, 164)
RED_BAND = (178, 34, 34)
DARK = (20, 20, 24)
PAD_LIT = (255, 214, 104)
# Flame: white core out to deep red, no outline.
FLAME_W = (255, 250, 220)
FLAME_L = (255, 214, 90)
FLAME_M = (255, 150, 40)
FLAME_D = (230, 70, 20)
# Smoke, grey with a warm lit edge on the flame side.
SMOKE_D = (96, 96, 100)
SMOKE_M = (148, 148, 150)
SMOKE_L = (198, 198, 200)
SMOKE_T = (228, 228, 230)
SMOKE_WARM = (255, 180, 90)


def main():
    img = Image.new("RGB", (GW, GH), INDIGO)
    d = ImageDraw.Draw(img)
    rnd = random.Random(25)

    def px(x, y, c):
        if 0 <= x < GW and 0 <= y < GH:
            img.putpixel((x, y), c)

    def band(y0, y1, c):
        d.rectangle([0, y0, GW - 1, y1], fill=c)

    def dither(y, c1, c2):
        for x in range(GW):
            px(x, y, c1 if (x + y) % 2 == 0 else c2)

    # Sky: indigo at the top, violet, magenta, ember, amber horizon.
    band(0, 4, INDIGO)
    band(5, 9, VIOLET)
    dither(9, VIOLET, MAGENTA)
    band(10, 14, MAGENTA)
    dither(14, MAGENTA, EMBER)
    band(15, 18, EMBER)
    dither(18, EMBER, HORIZON)
    band(19, 20, HORIZON)

    # Fading stars in the upper sky.
    for _ in range(46):
        x = rnd.randint(0, GW - 1)
        y = rnd.randint(0, 8)
        px(x, y, STAR if rnd.random() < 0.35 else STAR_DIM)

    # Sun rising on the right, half above the horizon.
    for dx in range(-7, 8):
        for dy in range(-7, 8):
            if abs(dx) + abs(dy) <= 7:
                px(198 + dx, 15 + dy, GLOW)
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            if abs(dx) + abs(dy) <= 4:
                px(198 + dx, 15 + dy, SUN)
    px(198, 15, FLAME_W)

    # Distant mountains along the horizon, darkest at the left.
    for x in range(0, 96):
        h = 19 - (x % 7) // 3
        for y in range(h, 21):
            px(x, y, MOUNTAIN)
    for x in range(150, GW):
        h = 20 - (x % 5) // 3
        for y in range(h, 21):
            px(x, y, MOUNTAIN)

    # Desert ground: darker bands toward the bottom, lit by the dawn.
    band(21, 26, DESERT_D)
    band(27, 35, DESERT_M)
    band(36, GH - 1, DESERT_L)
    dither(26, DESERT_D, DESERT_M)
    dither(35, DESERT_M, DESERT_L)
    # Dune curves and scattered rocks.
    for x in range(0, GW):
        y = 40 + int(2.5 * (1 + ((x * 7) % 11) / 11.0))
        if y < GH:
            px(x, y, SAND_LIT if (x % 3) == 0 else DESERT_M)
    for rx, ry in [(8, 44), (30, 42), (52, 45), (176, 43), (205, 45),
                   (222, 42), (150, 44), (66, 46)]:
        px(rx, ry, ROCK)
        px(rx + 1, ry, ROCK)

    # Launch tower, dark steel, standing left of the rocket.
    d.rectangle([92, 14, 96, 34], fill=STEEL)
    d.rectangle([92, 14, 96, 15], fill=STEEL_L)
    for y in (18, 22, 26, 30):
        d.rectangle([92, y, 100, y], fill=STEEL)
    # Crane arm reaching toward the rocket.
    for i in range(8):
        px(97 + i, 15 - i // 4, STEEL_L)
    # Small pad buildings with lit windows.
    d.rectangle([70, 30, 82, 34], fill=STEEL)
    d.rectangle([138, 30, 150, 34], fill=STEEL)
    for wx in (73, 77, 141, 146):
        px(wx, 32, PAD_LIT)

    # The Long March 2F, climbing: nose cone, white body, red band.
    # Nose cone, tapering to a point.
    for i, w in enumerate([2, 4, 6, 8]):
        d.rectangle([112 - w // 2, 5 + i, 112 + w // 2 - 1, 5 + i],
                    fill=BODY)
    # Body with a shaded right edge and a lit left edge.
    d.rectangle([108, 9, 117, 22], fill=BODY)
    d.rectangle([116, 9, 117, 22], fill=BODY_D)
    px(108, 9, FLAME_W)
    for y in range(9, 23):
        px(108, y, FLAME_W if y % 4 == 0 else BODY)
    # Red band around the body.
    d.rectangle([108, 18, 117, 19], fill=RED_BAND)
    # Fins flaring at the base.
    d.rectangle([105, 22, 107, 25], fill=BODY_D)
    d.rectangle([118, 22, 120, 25], fill=BODY_D)
    px(105, 25, DARK)
    px(120, 25, DARK)
    # A thin vapour trail curling off the nose.
    for i in range(6):
        px(109 - i, 4 - i // 3, SMOKE_T if i % 2 else SMOKE_L)

    # Flame: layered plume below the rocket, white core to deep red.
    for dx in range(-9, 10):
        for dy in range(0, 12):
            spread = 9 - dy // 2
            if abs(dx) <= spread and rnd.random() < 0.75:
                px(112 + dx, 26 + dy, FLAME_D)
    for dx in range(-6, 7):
        for dy in range(0, 10):
            spread = 6 - dy // 2
            if abs(dx) <= spread and rnd.random() < 0.8:
                px(112 + dx, 26 + dy, FLAME_M)
    for dx in range(-3, 4):
        for dy in range(0, 8):
            spread = 3 - dy // 3
            if abs(dx) <= spread:
                px(112 + dx, 26 + dy, FLAME_L)
    for dx in range(-1, 2):
        for dy in range(0, 6):
            px(112 + dx, 26 + dy, FLAME_W)
    # Bright glow where the plume meets the pad.
    for dx in range(-12, 13):
        for dy in range(0, 3):
            if rnd.random() < 0.6:
                px(112 + dx, 34 + dy, FLAME_M if (dx + dy) % 2 else FLAME_L)

    # Smoke: thick clouds billowing out from the pad, drifting wide.
    for cx, cy, rx, ry, c in [
        (112, 36, 16, 5, SMOKE_D), (96, 38, 14, 5, SMOKE_D),
        (130, 38, 14, 5, SMOKE_M), (82, 40, 12, 4, SMOKE_M),
        (144, 40, 12, 4, SMOKE_L), (68, 42, 10, 4, SMOKE_L),
        (158, 42, 10, 4, SMOKE_L), (108, 33, 8, 3, SMOKE_M),
        (120, 33, 8, 3, SMOKE_L), (98, 35, 6, 3, SMOKE_T),
        (126, 35, 6, 3, SMOKE_T),
    ]:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=c)
    for _ in range(70):
        x = rnd.randint(52, 172)
        y = rnd.randint(31, 44)
        if rnd.random() < 0.6:
            px(x, y, SMOKE_T if rnd.random() < 0.5 else SMOKE_L)
    # Warm rim light on the smoke, on the side facing the flame.
    for x, y in [(104, 35), (105, 37), (103, 39), (121, 35), (120, 37),
                 (122, 39), (106, 33), (119, 33), (102, 41), (123, 41)]:
        px(x, y, SMOKE_WARM if (x + y) % 2 else FLAME_M)

    # Pad floodlights: tiny bright dots along the ground.
    for lx in (86, 104, 122, 140):
        px(lx, 35, PAD_LIT)
        px(lx, 36, PAD_LIT)

    big = img.resize((GW * PX, GH * PX), Image.NEAREST)
    big.save("scene.png", format="PNG", optimize=True)
    print("wrote scene.png", big.size)


if __name__ == "__main__":
    main()
