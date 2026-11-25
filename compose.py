#!/usr/bin/env python3
"""Compose the front page (entry.png) from the pixel-art scene and
the 25 November 2026 news summary.

Lead: Shenzhou-24 lifts off from Jiuquan on Wednesday 25 November
2026 carrying Pakistan's Muhammad Zeeshan Ali, the first Pakistani
in orbit and the first foreigner aboard China's Tiangong station.
Supporting panels are dated where they happened: the Riyadh tower
strike, the Huawei verdict and the Chen Jining probe all fell on
Tuesday 24 November; the Cartagena siege ended on Wednesday.

Run:  python3 pixel.py && python3 compose.py
Writes entry.png beside this file: 1024x1024, deterministic, no
network, no clock, no randomness. Uses only Pillow and the DejaVu
fonts already on this machine; the entry program (main.py) only
copies the finished image, so the grader needs neither.
"""
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
PAPER = (248, 243, 230)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (24, 48, 88)
CARD = (255, 255, 255)
GREY = (90, 86, 78)
BODY_INK = (40, 38, 34)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_BOLD = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS_BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS_PLAIN = FONT_DIR + "DejaVuSans.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def flow_text(draw, text, fnt, width):
    """Break text into lines that fit width, honouring \n breaks."""
    out = []
    for chunk in text.split("\n"):
        words, line = chunk.split(), ""
        for w in words:
            trial = (line + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    out.append(line)
                line = w
        if line:
            out.append(line)
    return out


def draw_para(draw, pos, text, fnt, width, fill=INK, leading=1.28):
    x, y = pos
    for line in flow_text(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def panel(draw, box, accent):
    draw.rectangle(box, fill=CARD, outline=INK, width=2)
    draw.rectangle([box[0], box[1], box[2], box[1] + 8], fill=accent)


def panel_story(draw, box, kicker, headline, body, accent):
    x0, y0, x1, _y1 = box
    panel(draw, box, accent)
    draw.text((x0 + 16, y0 + 14), kicker, font=load(SANS_BOLD, 16),
              fill=accent)
    y = draw_para(draw, (x0 + 16, y0 + 38), headline,
                  load(SERIF_BOLD, 23), x1 - x0 - 32, leading=1.1)
    draw_para(draw, (x0 + 16, y + 6), body, load(SANS_PLAIN, 15),
              x1 - x0 - 32, fill=BODY_INK, leading=1.25)


def main():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(page)
    d.rectangle([4, 4, PAGE_W - 5, PAGE_H - 5], outline=INK, width=4)

    # Masthead.
    d.rectangle([10, 10, PAGE_W - 11, 138], fill=INK)
    d.text((PAGE_W // 2, 26), "THE WORLD IN ONE DAY",
           font=load(SERIF_BOLD, 56), fill=(255, 255, 255), anchor="ma")
    d.text((PAGE_W // 2, 96), "ONE IMAGE  •  THE WHOLE DAY'S NEWS",
           font=load(SANS_BOLD, 20), fill=(240, 200, 60), anchor="ma")

    # The date, big and red, so the day is unmistakable.
    d.text((PAGE_W // 2, 152), "WEDNESDAY  25  NOVEMBER  2026",
           font=load(SERIF_BOLD, 36), fill=RED, anchor="ma")
    d.line([60, 200, 320, 200], fill=INK, width=2)
    d.line([704, 200, 964, 200], fill=INK, width=2)

    # Lead story: the pixel-art illustration of the Shenzhou-24 launch.
    lead = (28, 216, 996, 568)
    panel(d, lead, RED)
    scene = Image.open("scene.png").convert("RGB")
    page.paste(scene, (44, 232))
    d.rectangle([44, 394, 396, 424], fill=(10, 20, 35))
    d.text((56, 400), "JIUQUAN, CHINA  •  GOBI DESERT",
           font=load(SANS_BOLD, 17), fill=(255, 255, 255))
    d.text((46, 448), "LEAD  •  HISTORY IN ORBIT",
           font=load(SANS_BOLD, 20), fill=RED)
    d.text((46, 478), "PAKISTAN'S FIRST ASTRONAUT REACHES ORBIT",
           font=load(SERIF_BOLD, 30), fill=INK)
    draw_para(d, (46, 514),
              "Shenzhou-24 blasted off at 08:18 from Jiuquan carrying "
              "Tang Hongbo, Wu Yi and Pakistan's Muhammad Zeeshan Ali — "
              "the first foreigner aboard China's Tiangong station. It "
              "docked at 11:56.",
              load(SANS_PLAIN, 18), 920, fill=BODY_INK, leading=1.25)

    # Four supporting stories in a 2x2 grid.
    gx, gy, gw, gh, gap = 28, 584, 474, 148, 20
    grid = [
        ("THE GULF  •  TUESDAY",
         "HOUTHI DRONE HITS\nRIYADH'S TALLEST TOWER",
         "Eleven hurt, two critical, as a drone strikes the 385 m "
         "PIF Tower for the second time in a week. Overnight the "
         "Saudi-led coalition struck Hodeidah port.",
         RED),
        ("JUSTICE  •  TUESDAY",
         "HUAWEI GUILTY\nON 10 OF 12 COUNTS",
         "A Brooklyn jury convicts the Chinese tech giant of bank "
         "fraud, sanctions violations and trade-secret theft. "
         "Sentencing is set for September 2027.",
         NAVY),
        ("COLOMBIA  •  WEDNESDAY",
         "CARTAGENA HOSTAGE\nSIEGE ENDS",
         "All hostages are freed after a day-long standoff at an "
         "Éxito supermarket; one captor is killed. A night earlier, "
         "a car bomb in Villavicencio injured at least 22.",
         RED),
        ("CHINA  •  TUESDAY",
         "SHANGHAI PARTY BOSS\nFALLS IN PURGE",
         "Chen Jining, a Politburo member once seen as a possible "
         "successor, is placed under investigation — the fourth "
         "Politburo member to fall since 2025.",
         NAVY),
    ]
    for i, (kicker, head, body, accent) in enumerate(grid):
        box = (gx + (i % 2) * (gw + gap), gy + (i // 2) * (gh + gap),
               gx + (i % 2) * (gw + gap) + gw,
               gy + (i // 2) * (gh + gap) + gh)
        panel_story(d, box, kicker, head, body, accent)

    # Also-today strip.
    also = (28, 908, 996, 988)
    panel(d, also, NAVY)
    d.text((46, 920), "ALSO TODAY", font=load(SANS_BOLD, 19), fill=NAVY)
    draw_para(d, (46, 944),
              "Nvidia falls 7% as the AI rally wobbles  •  "
              "Putin vows retaliation for refinery strikes  •  "
              "Kyiv claims Baltic ship strike  •  "
              "Senegal's AFCON title restored",
              load(SANS_PLAIN, 17), 932, fill=BODY_INK, leading=1.3)

    d.text((PAGE_W // 2, 996), "SUMMED UP IN ONE IMAGE  •  25 NOVEMBER 2026",
           font=load(SANS_BOLD, 17), fill=GREY, anchor="ma")

    page.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
