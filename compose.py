#!/usr/bin/env python3
"""Lay out the 25 November 2026 front page (entry.png).

The lead is Shenzhou-24 lifting off from Jiuquan on Wednesday
25 November 2026 with Pakistan's Muhammad Zeeshan Ali aboard — the
first Pakistani in orbit and the first foreigner on China's Tiangong
station. The four supporting panels are dated where they happened:
the Riyadh tower strike, the Huawei verdict and the Chen Jining
probe all fell on Tuesday 24 November; the Cartagena siege ended on
Wednesday. The pixel-art scene comes from pixel.py (scene.png).

Run:  python3 pixel.py && python3 compose.py
Writes entry.png beside this file: 1024 by 1024, deterministic, no
network, no clock, no randomness. Pillow and the DejaVu fonts already
on this machine; main.py only copies the finished image, so the
grader needs neither.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (24, 48, 88)
CARD = (255, 255, 255)
GREY = (90, 86, 78)
BODY = (40, 38, 34)
GOLD = (240, 200, 60)

FONTS = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


def serif(size):
    return font("DejaVuSerif-Bold.ttf", size)


def sans(size, bold=True):
    return font("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size)


def wrap(draw, text, fnt, width):
    """Split text into lines that fit width, keeping \n breaks."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        line = ""
        for word in words:
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=1.28):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def centre(draw, y, text, fnt, fill):
    draw.text((W // 2, y), text, font=fnt, fill=fill, anchor="ma")


def card(draw, box, accent):
    draw.rectangle(box, fill=CARD, outline=INK, width=2)
    draw.rectangle([box[0], box[1], box[2], box[1] + 8], fill=accent)


def story(draw, box, kicker, headline, body, accent):
    x0, y0, x1, _ = box
    card(draw, box, accent)
    draw.text((x0 + 16, y0 + 14), kicker, font=sans(16), fill=accent)
    end = para(draw, x0 + 16, y0 + 38, headline, serif(23),
               x1 - x0 - 32, leading=1.1)
    para(draw, x0 + 16, end + 6, body, sans(15, bold=False),
         x1 - x0 - 32, fill=BODY, leading=1.25)


def build_page():
    page = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(page)
    draw.rectangle([4, 4, W - 5, H - 5], outline=INK, width=4)

    # Masthead: black band, paper name, one-line promise.
    draw.rectangle([10, 10, W - 11, 138], fill=INK)
    centre(draw, 26, "THE WORLD IN ONE DAY", serif(56), (255, 255, 255))
    centre(draw, 96, "ONE IMAGE  •  THE WHOLE DAY'S NEWS", sans(20), GOLD)

    # The date, big and red, so the day is unmistakable.
    centre(draw, 152, "WEDNESDAY  25  NOVEMBER  2026", serif(36), RED)
    draw.line([60, 200, 320, 200], fill=INK, width=2)
    draw.line([704, 200, 964, 200], fill=INK, width=2)

    # Lead story: the pixel-art launch, caption chip, headline, standfirst.
    lead = (28, 216, 996, 568)
    card(draw, lead, RED)
    scene = Image.open("scene.png").convert("RGB")
    page.paste(scene, (44, 232))
    draw.rectangle([44, 394, 396, 424], fill=(10, 20, 35))
    draw.text((56, 400), "JIUQUAN, CHINA  •  GOBI DESERT",
              font=sans(17), fill=(255, 255, 255))
    draw.text((46, 448), "LEAD  •  HISTORY IN ORBIT",
              font=sans(20), fill=RED)
    draw.text((46, 478), "PAKISTAN'S FIRST ASTRONAUT REACHES ORBIT",
              font=serif(30), fill=INK)
    para(draw, 46, 514,
         "Shenzhou-24 blasted off at 08:18 from Jiuquan carrying "
         "Tang Hongbo, Wu Yi and Pakistan's Muhammad Zeeshan Ali — "
         "the first foreigner aboard China's Tiangong station. It "
         "docked at 11:56.",
         sans(18, bold=False), 920, fill=BODY, leading=1.25)

    # A thin red rule between the lead story and the grid below it.
    draw.line([28, 576, 996, 576], fill=RED, width=2)

    # Four supporting stories in a two-by-two grid.
    stories = [
        {"kicker": "THE GULF  •  TUESDAY",
         "head": "HOUTHI DRONE HITS\nRIYADH'S TALLEST TOWER",
         "body": "Eleven hurt, two critical, as a drone strikes the 385 m "
                 "PIF Tower for the second time in a week. Overnight the "
                 "Saudi-led coalition struck Hodeidah port.",
         "accent": RED},
        {"kicker": "JUSTICE  •  TUESDAY",
         "head": "HUAWEI GUILTY\nON 10 OF 12 COUNTS",
         "body": "A Brooklyn jury convicts the Chinese tech giant of bank "
                 "fraud, sanctions violations and trade-secret theft. "
                 "Sentencing is set for September 2027.",
         "accent": NAVY},
        {"kicker": "COLOMBIA  •  WEDNESDAY",
         "head": "CARTAGENA HOSTAGE\nSIEGE ENDS",
         "body": "All hostages are freed after a day-long standoff at an "
                 "Éxito supermarket; one captor is killed. A night earlier, "
                 "a car bomb in Villavicencio injured at least 22.",
         "accent": RED},
        {"kicker": "CHINA  •  TUESDAY",
         "head": "SHANGHAI PARTY BOSS\nFALLS IN PURGE",
         "body": "Chen Jining, a Politburo member once seen as a possible "
                 "successor, is placed under investigation — the fourth "
                 "Politburo member to fall since 2025.",
         "accent": NAVY},
    ]
    gx, gy, gw, gh, gap = 28, 584, 474, 148, 20
    for i, item in enumerate(stories):
        x = gx + (i % 2) * (gw + gap)
        y = gy + (i // 2) * (gh + gap)
        story(draw, (x, y, x + gw, y + gh), item["kicker"], item["head"],
              item["body"], item["accent"])

    # Also-today strip, then the footer line.
    strip = (28, 908, 996, 988)
    card(draw, strip, NAVY)
    draw.text((46, 920), "ALSO TODAY", font=sans(19), fill=NAVY)
    para(draw, 46, 944,
         "Nvidia falls 7% as the AI rally wobbles  •  "
         "Putin vows retaliation for refinery strikes  •  "
         "Kyiv claims Baltic ship strike  •  "
         "Senegal's AFCON title restored",
         sans(17, bold=False), 932, fill=BODY, leading=1.3)
    centre(draw, 996, "SUMMED UP IN ONE IMAGE  •  25 NOVEMBER 2026",
           sans(17), GREY)

    page.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    build_page()
