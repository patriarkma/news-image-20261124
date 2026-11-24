#!/usr/bin/env python3
"""Draw the front page for news-image-20261124 with PIL (build machine only).

The submitted program (main.py) ships the finished image and copies it;
this script is the tool that drew it. Every story was re-verified against
reporting from 24 November 2026 before drawing (see README.md).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (245, 239, 227)
PANEL = (255, 253, 246)
INK = (28, 28, 28)
MUTED = (90, 85, 72)
RED = (158, 27, 27)
BLUE = (35, 64, 107)
LINE = (28, 28, 28)
SKY = (22, 35, 61)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_size(draw, text, fnt_path, start, max_w, max_lines):
    """Largest size <= start whose wrap fits max_lines lines."""
    size = start
    while size > 10:
        fnt = font(fnt_path, size)
        if len(wrap(draw, text, fnt, max_w)) <= max_lines:
            return fnt
        size -= 2
    return font(fnt_path, 10)


def draw_text_block(draw, x, y, text, fnt, fill, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=2, fill=LINE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- lead art
def draw_lead_art(draw, x, y, w, h):
    """Night scene: damaged block of flats, smoke, emergency lights."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # stars
    for sx, sy in [(18, 20), (60, 44), (120, 16), (200, 38), (260, 22),
                   (310, 50), (90, 70), (170, 60), (235, 76), (30, 90)]:
        draw.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                     fill=(220, 220, 200))
    # moon
    draw.ellipse([x + w - 52, y + 18, x + w - 18, y + 52], fill=(232, 226, 200))
    # ground
    draw.rectangle([x, y + h - 46, x + w, y + h], fill=(58, 63, 71))
    # main block of flats, broken top-right corner (jagged)
    bx, by, bw, bh = x + 24, y + 78, 190, h - 78 - 46
    draw.polygon([(bx, by + bh), (bx, by + 26), (bx + 60, by),
                  (bx + 96, by + 18), (bx + 130, by + 4), (bx + 168, by + 22),
                  (bx + bw, by + 46), (bx + bw, by + bh)],
                 fill=(138, 143, 150))
    # windows: some lit, some dark, some broken
    for row in range(5):
        for col in range(5):
            wx = bx + 14 + col * 34
            wy = by + 52 + row * 34
            if wx + 20 > bx + bw - 8 or wy + 24 > by + bh - 8:
                continue
            lit = (row + col) % 3 == 0
            draw.rectangle([wx, wy, wx + 20, wy + 24],
                           fill=(240, 200, 90) if lit else (44, 52, 66))
    # rubble at the broken corner
    for rx, ry, rw, rh in [(bx + 150, by + bh - 26, 34, 14),
                           (bx + 168, by + bh - 14, 26, 10),
                           (bx + 128, by + bh - 12, 22, 8)]:
        draw.rectangle([rx, ry, rx + rw, ry + rh], fill=(110, 108, 100))
    # smoke plume
    for cx, cy, r in [(bx + 150, by - 6, 26), (bx + 176, by - 26, 32),
                      (bx + 210, by - 48, 38)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(107, 114, 128))
    # fire glow at the base
    draw.polygon([(bx + 40, by + bh), (bx + 62, by + bh - 30),
                  (bx + 84, by + bh - 12), (bx + 104, by + bh - 26),
                  (bx + 124, by + bh)], fill=(217, 123, 41))
    # fire engine: red box + light bar
    ex, ey = x + w - 108, y + h - 46 - 26
    draw.rectangle([ex, ey, ex + 84, ey + 26], fill=(158, 27, 27))
    draw.rectangle([ex + 8, ey - 8, ex + 40, ey], fill=(120, 20, 20))
    draw.ellipse([ex + 46, ey - 10, ex + 58, ey + 2], fill=(240, 200, 90))
    draw.ellipse([ex + 62, ey - 10, ex + 74, ey + 2], fill=(120, 180, 240))
    draw.ellipse([ex + 12, ey + 20, ex + 28, ey + 36], fill=(20, 20, 20))
    draw.ellipse([ex + 56, ey + 20, ex + 72, ey + 36], fill=(20, 20, 20))
    # caption strip
    draw.rectangle([x, y + h - 24, x + w, y + h], fill=(20, 20, 20))
    draw.text((x + 8, y + h - 20),
              "A damaged block of flats in Zaporizhzhia.",
              font=font(SANS, 12), fill=(235, 235, 225))


# ------------------------------------------------------------- mini art
def art_korea(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(168, 196, 222))
    draw.polygon([(x + 20, y + h), (x + 70, y + 18), (x + 130, y + h)],
                 fill=(96, 140, 96))
    draw.polygon([(x + 70, y + 18), (x + 70, y + 6), (x + 82, y + 18)],
                 fill=(60, 100, 60))
    # jet, side profile: slim fuselage, swept wing, tail fin
    jx, jy = x + 148, y + 26
    draw.polygon([(jx, jy), (jx + 58, jy + 3), (jx + 66, jy + 6),
                  (jx + 58, jy + 9), (jx, jy + 8)], fill=(40, 40, 44))
    draw.polygon([(jx + 26, jy + 6), (jx + 40, jy + 20), (jx + 46, jy + 6)],
                 fill=(40, 40, 44))
    draw.polygon([(jx + 4, jy + 2), (jx + 12, jy - 8), (jx + 16, jy + 2)],
                 fill=(40, 40, 44))
    # warning triangle
    draw.polygon([(x + 196, y + 44), (x + 208, y + 62), (x + 184, y + 62)],
                 fill=(220, 160, 30))
    draw.text((x + 199, y + 48), "!", font=font(SANS_B, 12), fill=(28, 28, 28))


def art_space(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    for sx, sy in [(14, 10), (50, 22), (90, 8), (140, 18), (190, 10), (215, 26)]:
        draw.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                     fill=(230, 230, 220))
    draw.ellipse([x + 56, y + h - 12, x + 176, y + h + 44], fill=(52, 96, 160))
    draw.ellipse([x + 56, y + h - 12, x + 176, y + h + 44],
                 outline=(90, 140, 200))
    # satellite
    draw.rectangle([x + 92, y + 16, x + 132, y + 34], fill=(180, 184, 190))
    draw.rectangle([x + 60, y + 20, x + 92, y + 30], fill=(70, 110, 180))
    draw.rectangle([x + 132, y + 20, x + 164, y + 30], fill=(70, 110, 180))
    draw.line([(x + 112, y + 34), (x + 112, y + 44)], fill=(180, 184, 190), width=3)
    # red burst
    for dx, dy in [(0, -8), (6, -6), (8, 0), (6, 6), (0, 8), (-6, 6), (-8, 0), (-6, -6)]:
        draw.line([(x + 172, y + 16), (x + 172 + dx, y + 16 + dy)],
                  fill=(220, 60, 40), width=2)


def art_eu(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(28, 48, 96))
    import math
    cx, cy, r = x + w // 2 - 30, y + h // 2, 20
    for i in range(12):
        a = math.pi * 2 * i / 12 - math.pi / 2
        sx, sy = cx + int(r * math.cos(a)), cy + int(r * math.sin(a))
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(240, 210, 60))
    draw.text((x + w - 62, y + h // 2 - 14), "€", font=font(SANS_B, 28),
              fill=(240, 210, 60))


def art_iran(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(32, 64, 60))
    draw.ellipse([x + 30, y + 8, x + 86, y + h - 8], fill=(20, 40, 38))
    draw.text((x + 44, y + 12), "$", font=font(SANS_B, 30), fill=(220, 190, 90))
    for i in range(3):
        yy = y + 14 + i * 16
        draw.line([(x + 104, yy), (x + w - 16, yy)], fill=(220, 190, 90), width=3)
        draw.ellipse([x + w - 22, yy - 4, x + w - 14, yy + 4], fill=(220, 190, 90))


def art_gaza(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(196, 186, 168))
    draw.rectangle([x + 24, y + 30, x + 90, y + h - 6], fill=(120, 116, 108))
    draw.rectangle([x + 104, y + 18, x + 160, y + h - 6], fill=(96, 92, 86))
    for wx in (34, 56, 78):
        draw.rectangle([x + wx, y + 38, x + wx + 10, y + 50], fill=(60, 58, 52))
    # map pin
    px, py = x + 178, y + 30
    draw.ellipse([px - 12, py - 12, px + 12, py + 12], fill=(158, 27, 27))
    draw.polygon([(px - 12, py + 4), (px + 12, py + 4), (px, py + 24)],
                 fill=(158, 27, 27))
    draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(245, 239, 227))


def art_grok(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(52, 52, 58))
    draw.rectangle([x + 66, y + 6, x + 160, y + h - 6], fill=(20, 20, 24))
    draw.rectangle([x + 72, y + 12, x + 154, y + h - 12], fill=(120, 200, 240))
    draw.text((x + 100, y + 16), "G", font=font(SANS_B, 26), fill=(20, 20, 24))
    draw.polygon([(x + 22, y + 40), (x + 34, y + 56), (x + 10, y + 56)],
                 fill=(220, 160, 30))
    draw.text((x + 20, y + 44), "!", font=font(SANS_B, 12), fill=(28, 28, 28))


def art_india(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(240, 220, 180))
    # shield
    draw.polygon([(x + 40, y + 6), (x + 90, y + 6), (x + 90, y + 30),
                  (x + 65, y + h - 8), (x + 40, y + 30)], fill=(35, 64, 107))
    draw.line([(x + 50, y + 30), (x + 60, y + 40), (x + 82, y + 16)],
              fill=(255, 255, 255), width=4)
    # bank columns
    for i in range(3):
        cx = x + 130 + i * 30
        draw.rectangle([cx, y + 22, cx + 14, y + h - 14], fill=(120, 100, 70))
    draw.rectangle([x + 122, y + 14, x + 208, y + 22], fill=(120, 100, 70))
    draw.rectangle([x + 122, y + h - 14, x + 208, y + h - 8], fill=(120, 100, 70))


def art_congo(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(58, 52, 44))
    # cobalt crystal
    draw.polygon([(x + 60, y + 6), (x + 96, y + 22), (x + 88, y + h - 10),
                  (x + 52, y + h - 10), (x + 44, y + 22)], fill=(40, 90, 200))
    draw.polygon([(x + 60, y + 6), (x + 96, y + 22), (x + 70, y + 30),
                  (x + 52, y + 22)], fill=(90, 140, 235))
    draw.line([(x + 60, y + 6), (x + 70, y + h - 10)], fill=(160, 190, 250), width=2)
    # mine cart
    draw.rectangle([x + 130, y + 34, x + 200, y + 52], fill=(90, 82, 70))
    draw.ellipse([x + 140, y + 52, x + 156, y + 64], fill=(20, 20, 20))
    draw.ellipse([x + 176, y + 52, x + 192, y + 64], fill=(20, 20, 20))
    draw.line([(x + 130, y + 58), (x + 210, y + 58)], fill=(140, 132, 118), width=2)


STORIES = [
    ("KOREA", "SEOUL SCRAMBLES JETS AS RUSSIAN PLANES CLOSE IN",
     "Russian bombers and fighters entered South Korea's air-defence zone; "
     "islanders took shelter.",
     art_korea),
    ("SPACE", "NATO VOWS SPACE DEFENCE AFTER 'SPUTNIK-S' REPORT",
     "German media say Russia could launch a nuclear-armed satellite "
     "within weeks. Moscow denies it.",
     art_space),
    ("EUROPE", "EU UNVEILS 22ND SANCTIONS PACKAGE ON RUSSIA",
     "About 60 banks would be cut from SWIFT; shadow-fleet tankers, "
     "crypto and Russian sport also hit.",
     art_eu),
    ("IRAN", "US SANCTIONS IRAN SHADOW BANKS; QATAR PUSHES TALKS",
     "Washington blacklists dozens tied to Iran; Qatar's PM meets Vance "
     "and Rubio to revive talks.",
     art_iran),
    ("GAZA", "ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF IN GAZA",
     "Hamas security chief Naeem Abu Nahel was killed with six others, "
     "among them two police officers.",
     art_gaza),
    ("TECHNOLOGY", "TWO US STATES SUE SPACEX OVER GROK DEEPFAKES",
     "Oregon and Virginia accuse Grok of making nude deepfakes from real "
     "photos, including of children.",
     art_india),
    ("INDIA", "INDIA'S BANKS GET A 'STOP SWITCH' ON FRAUD",
     "The Reserve Bank proposes a one-move freeze on outgoing debits, "
     "plus a trusted person for big transfers.",
     art_grok),
    ("AFRICA", "CONGO HALTS COBALT EXPORTS FROM 30 NOVEMBER",
     "The world's biggest cobalt producer suspends exports, citing "
     "oversupply and weak prices.",
     art_congo),
]
# NOTE: art functions above are paired by index in draw(); the TECHNOLOGY
# card uses the phone art and the INDIA card the shield art (see draw()).

BRIEFS = [
    "Dymer toll rises to 12 after a woman pulled alive from the rubble "
    "dies in hospital.",
    "Russian war dead in Ukraine pass 700,000, a Mediazona count of "
    "leaked records finds.",
    "Germany is the first country given access to Ukraine's Delta "
    "battlefield system; Gripen deliveries to be coordinated.",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin
    X1 = W - M

    # ---- masthead
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 56)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 18), title, font=tf, fill=INK)
    rule(d, M, X1, 92, 1)
    sf = font(SANS_B, 16)
    d.text((M, 100), "TUESDAY, 24 NOVEMBER 2026", font=sf, fill=RED)
    right = "ONE DAY  ·  ONE PAGE  ·  THE WORLD"
    d.text((X1 - d.textlength(right, font=font(SANS, 13)), 102),
           right, font=font(SANS, 13), fill=MUTED)
    rule(d, M, X1, 126, 3)
    rule(d, M, X1, 131, 1)

    # ---- lead
    ly = 146
    kf = font(SANS_B, 15)
    d.text((M, ly), "UKRAINE  ·  WAR IN EUROPE", font=kf, fill=RED)
    headline = "2 KILLED AS RUSSIAN STRIKE HITS FLATS IN ZAPORIZHZHIA"
    hf = fit_size(d, headline, SERIF_B, 46, 600, 3)
    y = ly + 26
    y = draw_text_block(d, M, y, headline, hf, INK, 600, 52)
    deck = ("A five-storey block of flats was partly destroyed and a house "
            "flattened in a night attack on the southern city. More than 40 "
            "people were wounded, among them four children, the youngest a "
            "baby. Ukraine said 73 of 96 drones were shot down overnight.")
    df = font(SERIF, 19)
    y = draw_text_block(d, M, y + 6, deck, df, INK, 600, 25)
    # lead art, right column
    ax, ay, aw, ah = 652, ly + 4, X1 - 652, 472 - ly - 4
    draw_lead_art(d, ax, ay, aw, ah)

    rule(d, M, X1, 492, 1)

    # ---- story grid: 4 columns x 2 rows
    gx, gy = M, 508
    cw = (X1 - M - 3 * 12) // 4
    ch = 187
    # art pairing: TECHNOLOGY -> phone (art_grok), INDIA -> shield (art_india)
    arts = [art_korea, art_space, art_eu, art_iran,
            art_gaza, art_grok, art_india, art_congo]
    for i, (kicker, head, body, _art) in enumerate(STORIES):
        col, row = i % 4, i // 4
        cx = gx + col * (cw + 12)
        cy = gy + row * (ch + 12)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=PANEL,
                    outline=(200, 192, 172))
        arts[i](d, cx + 1, cy + 1, cw - 2, 56)
        d.text((cx + 8, cy + 64), kicker, font=font(SANS_B, 11), fill=RED)
        hf2 = fit_size(d, head, SANS_B, 16, cw - 16, 2)
        y2 = draw_text_block(d, cx + 8, cy + 80, head, hf2, INK, cw - 16, 18)
        draw_text_block(d, cx + 8, y2 + 3, body, font(SANS, 12), MUTED,
                        cw - 16, 14)

    # ---- in brief
    by = 906
    rule(d, M, X1, by, 1)
    d.text((M, by + 8), "IN BRIEF", font=font(SANS_B, 13), fill=RED)
    yy = by + 30
    bf = font(SANS, 13)
    for item in BRIEFS:
        yy = draw_text_block(d, M, yy, "•  " + item, bf, INK, X1 - M, 17)

    # ---- footer
    rule(d, M, X1, 994, 1)
    foot = "The World in One Day — Tuesday, 24 November 2026"
    ff = font(SANS, 11)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 1000), foot, font=ff,
           fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
