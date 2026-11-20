#!/usr/bin/env python3
"""Draw the front page for Friday 20 November 2026.

A newspaper front page, drawn entirely with Pillow flat shapes and text:
no photographs, no borrowed artwork. Every story on the page happened or
was first reported on 20 November 2026; see NEWS.md for the sources.
"""

import math
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
PAPER = (248, 244, 234)
INK = (17, 17, 17)
RED = (163, 30, 34)
BLUE = (31, 78, 121)
GREY = (110, 108, 100)
SKY = (223, 232, 238)
RIVER = (157, 184, 198)
ORANGE = (232, 120, 40)
GOLD = (245, 190, 60)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)              # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)         # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)                # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Wrap text to a pixel width, word by word."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, text, fnt, x, y, max_w, lh, fill=INK):
    """Draw a wrapped paragraph; return the y just below it."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def starburst(draw, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def bridge_scene(draw, x, y, w, h):
    """A river bridge under missile bursts: flat shapes only."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # distant skyline
    for bx, bw, bh in [(0, 60, 26), (80, 44, 40), (150, 70, 22), (900, 56, 34)]:
        draw.rectangle([x + bx, y + h - 78 - bh, x + bx + bw, y + h - 78], fill=(190, 200, 205))
    # river
    draw.rectangle([x, y + h - 46, x + w, y + h], fill=RIVER)
    for wx in range(0, w, 64):
        draw.line([x + wx, y + h - 30, x + wx + 34, y + h - 30], fill=(220, 232, 238), width=2)
    # bridge deck and towers
    deck_y = y + h - 78
    draw.rectangle([x, deck_y, x + w, deck_y + 10], fill=(43, 43, 43))
    for tx in (w * 0.30, w * 0.68):
        draw.rectangle([x + tx - 7, deck_y - 58, x + tx + 7, deck_y], fill=(43, 43, 43))
        draw.line([x + tx, deck_y - 58, x + 40, deck_y], fill=(90, 90, 90), width=2)
        draw.line([x + tx, deck_y - 58, x + w - 40, deck_y], fill=(90, 90, 90), width=2)
    # bursts on the deck
    starburst(draw, x + w * 0.52, deck_y - 26, 34, 14, 9, ORANGE)
    starburst(draw, x + w * 0.52, deck_y - 26, 18, 8, 9, GOLD)
    starburst(draw, x + w * 0.80, deck_y - 18, 22, 10, 8, ORANGE)
    # smoke (sy is already absolute: deck_y minus an offset; keep inside the scene)
    for sx, sy, sr in [(w * 0.52 - 52, deck_y - 18, 9), (w * 0.52 - 30, deck_y - 24, 11),
                       (w * 0.80 + 34, deck_y - 16, 8)]:
        draw.ellipse([x + sx - sr, sy - sr, x + sx + sr, sy + sr], fill=(150, 148, 140))


def icon(draw, kind, x, y, s=36):
    """Tiny flat icon per story, drawn with primitives."""
    if kind == "tower":  # Gulf: a tall tower with a burst
        draw.rectangle([x + s * 0.35, y + s * 0.25, x + s * 0.65, y + s], fill=BLUE)
        draw.polygon([(x + s * 0.35, y + s * 0.25), (x + s * 0.5, y), (x + s * 0.65, y + s * 0.25)], fill=BLUE)
        starburst(draw, x + s * 0.78, y + s * 0.22, 11, 5, 8, ORANGE)
    elif kind == "venn":  # UK-EU: two overlapping circles
        draw.ellipse([x, y + 4, x + s * 0.62, y + s - 4], outline=BLUE, width=4)
        draw.ellipse([x + s * 0.38, y + 4, x + s, y + s - 4], outline=RED, width=4)
    elif kind == "ban":  # US sanctions: prohibition sign
        draw.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], outline=RED, width=4)
        draw.line([x + 7, y + s - 7, x + s - 7, y + 7], fill=RED, width=4)
    elif kind == "placard":  # Tokyo protest: placard on a stick
        draw.line([x + s * 0.5, y + s * 0.3, x + s * 0.5, y + s], fill=INK, width=3)
        draw.rectangle([x + s * 0.12, y, x + s * 0.88, y + s * 0.42], fill=RED)
    elif kind == "chip":  # Nvidia probe: a chip
        draw.rectangle([x + 7, y + 7, x + s - 7, y + s - 7], fill=BLUE)
        draw.rectangle([x + 13, y + 13, x + s - 13, y + s - 13], fill=PAPER)
        for px in (x + 12, x + s // 2 - 2, x + s - 16):
            draw.line([px, y + 1, px, y + 7], fill=BLUE, width=3)
            draw.line([px, y + s - 7, px, y + s - 1], fill=BLUE, width=3)
    elif kind == "leaf":  # COP31: a leaf
        draw.pieslice([x, y, x + s, y + s], 180, 360, fill=(46, 125, 60))
        draw.line([x + 4, y + s - 4, x + s - 4, y + 6], fill=(46, 125, 60), width=3)


def kicker(draw, text, x, y, fnt):
    draw.text((x, y), text, font=fnt, fill=RED)
    return y + int(fnt.size * 1.5)


def story(draw, x, y, w, kick, head, deck, hfont, dfont, icon_kind=None):
    """One story block; returns the y just below it."""
    if icon_kind:
        icon(draw, icon_kind, x, y, 34)
        y = kicker(draw, kick, x + 44, y + 8, SANS_B(15))
    else:
        y = kicker(draw, kick, x, y, SANS_B(15))
    y = para(draw, head, hfont, x, y, w, int(hfont.size * 1.18))
    y += 4
    y = para(draw, deck, dfont, x, y, w, int(dfont.size * 1.32), fill=(40, 40, 40))
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = MARGIN

    # Masthead
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(56)
    d.text(((W - d.textlength(title, font=tf)) / 2, y), title, font=tf, fill=INK)
    y += 72
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 10
    d.text((MARGIN, y), "FRIDAY  ·  20 NOVEMBER 2026", font=SANS_B(20), fill=INK)
    right = "SEVEN STORIES THAT DEFINED THE DAY"
    d.text((W - MARGIN - d.textlength(right, font=SANS_B(15)), y + 3), right,
           font=SANS_B(15), fill=GREY)
    y += 26
    d.line([MARGIN, y, W - MARGIN, y], fill=RED, width=4)
    y += 12

    # Lead: Kyiv
    y = kicker(d, "UKRAINE  —  LEAD STORY", MARGIN, y, SANS_B(16))
    y = para(d, "KYIV'S BRIDGES HIT IN OVERNIGHT MISSILE BARRAGE",
             SERIF_B(43), MARGIN, y, W - 2 * MARGIN, 52)
    y += 6
    y = para(d,
             "Russia struck the capital with ballistic missiles after midnight, "
             "damaging three bridges over the Dnipro and setting fires across "
             "several districts. No casualties were reported yet.",
             SANS(21), MARGIN, y, W - 2 * MARGIN, 27, fill=(40, 40, 40))
    y += 12
    bridge_scene(d, MARGIN, y, W - 2 * MARGIN, 118)
    y += 118 + 10
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 14

    # Row 2: Gulf + UK-EU
    col_w = (W - 2 * MARGIN - 24) // 2
    y2 = story(d, MARGIN, y, col_w,
               "THE GULF",
               "Houthis claim four Saudi targets; tanker hits mine",
               "Saudi defences shot down Houthi drones as the rebels "
               "claimed strikes across the kingdom; a tanker caught "
               "fire after hitting a mine near Hormuz.",
               SANS_B(25), SANS(18), "tower")
    y2 = max(y2, story(d, MARGIN + col_w + 24, y, col_w,
                       "BRITAIN  ·  EUROPE",
                       "UK and EU agree youth mobility scheme",
                       "Young people will be able to live and work on either "
                       "side under a deal London and Brussels reached, the "
                       "BBC understands.",
                       SANS_B(25), SANS(18), "venn"))
    d.line([MARGIN + col_w + 12, y, MARGIN + col_w + 12, y2], fill=GREY, width=1)
    y = y2 + 12
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 14

    # Row 3: three columns
    col3 = (W - 2 * MARGIN - 48) // 3
    y3 = story(d, MARGIN, y, col3,
               "UNITED STATES",
               "US sanctions bikie gang and 'Ndrangheta",
               "Washington blocked the assets of Australia's Comancheros "
               "and Italy's 'Ndrangheta mafia network.",
               SANS_B(21), SANS(17), "ban")
    y3 = max(y3, story(d, MARGIN + col3 + 24, y, col3,
                       "JAPAN",
                       "13,000 march in Tokyo against Takaichi",
                       "Protesters filled the streets of the capital over "
                       "the government's policies.",
                       SANS_B(21), SANS(17), "placard"))
    y3 = max(y3, story(d, MARGIN + 2 * (col3 + 24), y, col3,
                       "TECHNOLOGY",
                       "California probes Nvidia over China chips",
                       "The state opened an inquiry into AI chips sold "
                       "to Chinese buyers.",
                       SANS_B(21), SANS(17), "chip"))
    y = y3 + 12
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 12

    # Row 4: climate, full width
    y = story(d, MARGIN, y, W - 2 * MARGIN,
              "CLIMATE  —  COP31",
              "Outcry as fossil fuels are cut from the draft climate deal",
              "Negotiators removed fossil fuels from the draft text, drawing protests from climate campaigners.",
              SANS_B(23), SANS(18), "leaf")
    y += 10

    # Ticker strip
    d.rectangle([MARGIN, y, W - MARGIN, y + 40], fill=INK)
    tick = ("US war with Iran cost $48bn+   •   "
            "Genoa airport halts flights over drones   •   "
            "5.6 quake near New Caledonia")
    tf2 = SANS_B(14)
    tw = d.textlength(tick, font=tf2)
    assert tw <= W - 2 * MARGIN - 16, f"ticker too wide: {tw}"
    d.text(((W - tw) / 2, y + 11), tick, font=tf2, fill=PAPER)
    y += 40 + 10

    # Footer
    foot = "Sources: Kyiv Independent · Reuters · BBC · AP · Le Monde · SPA — Drawn by a program, no photographs"
    ff = SANS(13)
    d.text(((W - d.textlength(foot, font=ff)) / 2, y), foot, font=ff, fill=GREY)
    y += 18
    assert y <= H - 8, f"layout overflow: y={y}"
    img.save("entry.png")
    print(f"saved entry.png {img.size}, bottom y={y}")


if __name__ == "__main__":
    main()
