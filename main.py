#!/usr/bin/env python3
"""The World in One Day -- Thursday 19 November 2026.
Draws a one-page newspaper front page (1024x1024 PNG) summing up the
world news of Thursday 19 November 2026, verified against reporting
from Reuters, AP, CNN, Yonhap, ABS and the ICJ on 19-20 Nov 2026.
Stdlib + Pillow only. Deterministic: no time, random or network use.
Run:  python3 main.py   -> writes entry.png next to this file.
"""
import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

CREAM = (245, 236, 214)
PAPER = (250, 243, 226)
INK = (20, 20, 20)
RED = (178, 30, 30)
DARKRED = (140, 20, 20)
BLUE = (24, 62, 110)
NAVY = (16, 42, 84)
GOLD = (198, 148, 40)
GREY = (90, 86, 76)
LGREY = (120, 116, 104)
GREEN = (28, 110, 60)
ORANGE = (214, 110, 20)
TEAL = (16, 110, 110)
BORDER = (60, 52, 40)
LIGHT = (232, 222, 198)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF_R = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s) if os.path.exists(
    FD + "DejaVuSerif-Italic.ttf") else font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, width, text, fnt, fill=INK, leading=None):
    lh = leading or int(fnt.size * 1.28)
    for ln in wrap(draw, text, fnt, width):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def hline(draw, x0, y, x1, width=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def card(draw, x, y, w, h, fill=PAPER):
    draw.rectangle([x, y, x + w, y + h], fill=fill, outline=BORDER, width=1)
    return (x, y, w, h)


def tag(draw, x, y, text, fill=RED):
    f = SANS_B(8)
    tw = draw.textlength(text, font=f) + 8
    draw.rectangle([x, y, x + tw, y + 11], fill=fill)
    draw.text((x + 4, y + 1), text, font=f, fill=(255, 255, 255))
    return tw


def num_badge(draw, x, y, n, d=18):
    draw.ellipse([x, y, x + d, y + d], fill=RED, outline=(255, 255, 255), width=1)
    f = SANS_B(10)
    t = str(n)
    tw = draw.textlength(t, font=f)
    draw.text((x + (d - tw) / 2, y + 3), t, font=f, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 14  # margin
    CW = W - 2 * M  # 996

    # ---------- masthead ----------
    d.text((M, 8), "THE WORLD IN ONE DAY", font=SANS_B(11), fill=INK)
    d.text((W - M - d.textlength("DAY 323 OF 2026  ·  ONE-PAGE EDITION",
            font=SANS_B(9)), 10), "DAY 323 OF 2026  ·  ONE-PAGE EDITION",
           font=SANS_B(9), fill=GREY)
    hline(d, M, 26, W - M, 2)
    d.text((M, 30), "Thursday 19 November 2026", font=SERIF(40), fill=INK)
    # date box, top right
    bx, by, bw, bh = W - M - 92, 30, 92, 66
    d.rectangle([bx, by, bx + bw, by + bh], fill=(255, 255, 255),
                outline=RED, width=2)
    d.text((bx + 8, by + 3), "NOVEMBER 2026", font=SANS_B(8), fill=RED)
    d.text((bx + 22, by + 15), "19", font=SERIF(30), fill=INK)
    d.text((bx + 24, by + 48), "THURSDAY", font=SANS_B(9), fill=INK)
    d.text((M, 82), "Trump, Xi and Putin share one table  ·  World Court finds "
           "genocide in Myanmar  ·  a 13-year wait for a game ends",
           font=SERIF_I(13), fill=RED)
    hline(d, M, 102, W - M, 2)

    # ---------- stats row: 8 boxes ----------
    stats = [
        ("3", "one table: US, China, Russia"),
        ("$81.3bn", "raised by Anthropic, a record IPO"),
        ("13 yrs", "between GTA V and GTA VI"),
        ("730,000+", "Rohingya fled Myanmar in 2017"),
        ("204,070", "listed to evacuate in Odisha"),
        ("551,864", "candidates in Korea's exam"),
        ("4.9%", "Australian jobless, 5-year high"),
        ("48 hrs", "left at COP31 in Antalya"),
    ]
    sy, sh = 108, 44
    sw = CW / 8
    for i, (big, small) in enumerate(stats):
        x = M + i * sw
        if i:
            d.line([(x, sy + 3), (x, sy + sh - 3)], fill=LGREY, width=1)
        d.text((x + 5, sy + 2), big, font=SANS_B(17), fill=RED)
        para(d, x + 5, sy + 21, sw - 9, small, SANS(10), GREY, leading=11)
    hline(d, M, sy + sh, W - M, 1)
    d.text((M, sy + sh + 4), "25 STORIES FROM 6 REGIONS   ●  ASIA-PACIFIC 8   "
           "●  EUROPE 6   ●  MIDDLE EAST 4   ●  AMERICAS 5   ●  AFRICA 1   "
           "●  WORLDWIDE 1", font=SANS_B(10), fill=INK)

    # ---------- the day by hours ----------
    hy = 170
    d.text((M, hy), "THE DAY BY HOURS", font=SANS_B(10), fill=INK)
    d.text((M + 118, hy), "local time, in order", font=SERIF_I(9), fill=GREY)
    hours = [
        ("00:00", "AUCKLAND", "GTA VI unlocks"),
        ("08:40", "SEOUL", "exam begins"),
        ("04:42", "RIYADH", "air-raid sirens"),
        ("09:30", "JAKARTA", "law passed"),
        ("P.M.", "SHENZHEN", "three leaders meet"),
        ("10:00", "THE HAGUE", "genocide ruling"),
        ("09:30", "NEW YORK", "market opens"),
    ]
    hx = M
    hw = CW / 7
    for t, city, what in hours:
        d.text((hx, hy + 14), t, font=SANS_B(10), fill=RED)
        d.text((hx + 38, hy + 14), city, font=SANS_B(10), fill=INK)
        d.text((hx, hy + 27), what, font=SANS(10), fill=GREY)
        hx += hw
    hline(d, M, hy + 40, W - M, 1)

    # ---------- lead cards ----------
    ly, lh = 214, 196
    lw = (CW - 12) / 3
    leads = [
        ("1", "APEC 2026 · SHENZHEN", "SHENZHEN · SUMMIT",
         "Trump, Xi and Putin sit down together for the first time",
         "The leaders of the US, China and Russia met beside the APEC "
         "summit, with nuclear arms and Iran on the agenda. No joint "
         "statement came by evening. Earlier, Trump and Putin spoke "
         "alone for about 40 minutes, mostly on Ukraine.",
         "REPORTED", GREEN),
        ("2", "VI — OUT NOW", "WORLDWIDE · GAMES",
         "GTA VI is out, 13 years after the last one",
         "Grand Theft Auto VI unlocked at midnight local time in New "
         "Zealand first. Reviews average 99 on Metacritic. Analysts at "
         "Sensor Tower estimate 17.1m pre-orders, worth about $1.65bn. "
         "It is on PS5 and Xbox only, with no PC version.",
         "REPORTED", GREEN),
        ("3", "ANT — NASDAQ · FIRST DAY", "NEW YORK · MARKETS",
         "Anthropic heads to Nasdaq after the biggest IPO on record",
         "The maker of the Claude AI models raised about $81.3bn, "
         "pricing 980m shares at $83 each on Wednesday and passing "
         "SpaceX's $75bn record. The shares, ticker ANT, are due to "
         "begin trading today after the New York open.",
         "FORECAST", ORANGE),
    ]
    for i, (num, banner, kicker, head, body, lbl, lblc) in enumerate(leads):
        x = M + i * (lw + 6)
        card(d, x, ly, lw, lh)
        # illustration band
        ix, iy, iw, ih = x + 1, ly + 1, lw - 2, 78
        if i == 0:
            draw_apec(d, ix, iy, iw, ih)
        elif i == 1:
            draw_gta(d, ix, iy, iw, ih)
        else:
            draw_ant(d, ix, iy, iw, ih)
        # banner strip over illustration bottom
        d.rectangle([x + 1, iy + ih - 15, x + lw - 1, iy + ih], fill=NAVY)
        d.text((x + 6, iy + ih - 13), banner, font=SANS_B(10),
               fill=(255, 255, 255))
        num_badge(d, x - 4, ly - 8, num)
        ty = iy + ih + 5
        d.text((x + 6, ty), kicker, font=SANS_B(9), fill=GREY)
        tag(d, x + lw - 52, ty, lbl, lblc)
        ty += 14
        ty = para(d, x + 6, ty, lw - 12, head, SERIF(17), INK, leading=20)
        para(d, x + 6, ty + 3, lw - 12, body, SANS(10), INK, leading=12.5)

    return img, d, M, CW


def draw_apec(d, x, y, w, h):
    """Shenzhen summit table: three seated figures, three flags."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 70, 130))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 60, 40))
    # oval table
    d.ellipse([x + w * 0.12, y + h - 40, x + w * 0.88, y + h - 8],
              fill=(214, 178, 110), outline=(120, 90, 40))
    for i, (fx, col) in enumerate([(0.20, (180, 30, 30)),
                                   (0.50, (200, 30, 30)),
                                   (0.80, (30, 60, 160))]):
        cx = x + w * fx
        # flag
        d.rectangle([cx - 16, y + 8, cx + 16, y + 22], fill=(255, 255, 255),
                    outline=(0, 0, 0))
        d.rectangle([cx - 16, y + 8, cx + 16, y + 22], fill=col)
        d.text((cx - 9, y + 10), "***", font=SANS_B(7), fill=(255, 255, 255))
        # seated figure: head + shoulders
        d.ellipse([cx - 11, y + 26, cx + 11, y + 48], fill=(232, 196, 150))
        d.pieslice([cx - 16, y + 46, cx + 16, y + 74], 180, 360,
                   fill=(40, 40, 40) if i != 1 else (90, 20, 20))
    d.text((x + w * 0.20 - 12, y + h - 22), "USA", font=SANS_B(7), fill=INK)
    d.text((x + w * 0.50 - 16, y + h - 22), "CHINA", font=SANS_B(7), fill=INK)
    d.text((x + w * 0.80 - 16, y + h - 22), "RUSSIA", font=SANS_B(7), fill=INK)


def draw_gta(d, x, y, w, h):
    """Vice City at dusk: purple sky, lit towers, pink car, VI sign."""
    d.rectangle([x, y, x + w, y + h], fill=(58, 28, 88))
    d.ellipse([x + w - 26, y + 6, x + w - 6, y + 26], fill=(255, 210, 120))
    import random as _r
    rng = _r.Random(19)
    for i in range(9):
        bx = x + 6 + i * (w - 12) / 9
        bh = rng.randint(22, 52)
        d.rectangle([bx, y + h - 30 - bh, bx + (w - 12) / 9 - 3,
                     y + h - 30], fill=(24, 12, 44))
        for wy in range(2):
            d.rectangle([bx + 3, y + h - 26 - bh + wy * 12, bx + 8,
                         y + h - 21 - bh + wy * 12], fill=(255, 220, 90))
    # road
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(30, 30, 34))
    for i in range(6):
        d.rectangle([x + 8 + i * (w / 6), y + h - 16, x + 26 + i * (w / 6),
                     y + h - 13], fill=(255, 255, 255))
    # pink car
    cx, cy = x + w * 0.30, y + h - 26
    d.rounded_rectangle([cx, cy, cx + 46, cy + 12], radius=4, fill=(230, 60, 140))
    d.rounded_rectangle([cx + 10, cy - 8, cx + 34, cy + 2], radius=3,
                        fill=(230, 60, 140))
    d.ellipse([cx + 6, cy + 9, cx + 14, cy + 17], fill=(10, 10, 10))
    d.ellipse([cx + 32, cy + 9, cx + 40, cy + 17], fill=(10, 10, 10))
    # VI sign
    d.rounded_rectangle([x + w * 0.68, y + 8, x + w * 0.94, y + 38], radius=4,
                        fill=(20, 10, 30), outline=(255, 90, 180), width=2)
    d.text((x + w * 0.74, y + 10), "VI", font=SERIF(20), fill=(255, 120, 200))
    d.text((x + w * 0.70, y + 30), "OUT NOW", font=SANS_B(6),
           fill=(255, 255, 255))


def draw_ant(d, x, y, w, h):
    """Nasdaq debut: candlestick chart climbing, $83 price tag."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 26, 48))
    # grid
    for gy in range(4):
        yy = y + 10 + gy * (h - 24) / 3
        d.line([(x + 8, yy), (x + w - 8, yy)], fill=(40, 70, 110), width=1)
    candles = [(0.10, 62, 78, 70, 82), (0.24, 58, 74, 66, 78),
               (0.38, 50, 68, 58, 72), (0.52, 44, 62, 52, 66),
               (0.66, 34, 56, 44, 60), (0.80, 22, 46, 32, 50)]
    for fx, lo, hi, o, c in candles:
        cx = x + w * fx
        d.line([(cx, y + h - 12 - hi), (cx, y + h - 12 - lo)],
               fill=(90, 220, 130), width=2)
        top, bot = max(o, c), min(o, c)
        d.rectangle([cx - 6, y + h - 12 - top, cx + 6, y + h - 12 - bot],
                    fill=(90, 220, 130))
    d.text((x + 8, y + 4), "$81.3bn", font=SANS_B(11), fill=(255, 255, 255))
    d.text((x + w - 74, y + 4), "BIGGEST IPO", font=SANS_B(7),
           fill=(140, 220, 160))
    d.rounded_rectangle([x + w * 0.42, y + h - 52, x + w * 0.72, y + h - 30],
                        radius=3, fill=(255, 255, 255))
    d.text((x + w * 0.44, y + h - 50), "IPO PRICE  $83", font=SANS_B(9),
           fill=(10, 26, 48))


def mini_cards(d, M, CW, y0):
    """12 numbered mini-cards, 4 per row x 3 rows."""
    minis = [
        ("THE HAGUE · LAW", "World Court: Myanmar committed genocide",
         "Ruled 9-6: Myanmar meant to destroy the Rohingya. About 10,000 "
         "killed. No appeal.",
         "REPORTED", GREEN, "scales"),
        ("ANTALYA · CLIMATE", "COP31 enters its last 48 hours",
         "Ministers take over. A fossil-fuel phase-out and $120bn a year "
         "are in the draft.",
         "FORECAST", ORANGE, "globe"),
        ("ODISHA · STORM", "Cyclone Akvan: 204,070 listed to move",
         "204,070 listed for evacuation; 11 districts on red alert. "
         "Landfall due Friday.",
         "FORECAST", ORANGE, "spiral"),
        ("CRIMEA · WAR", "Crimean Bridge hit for third time in a week",
         "The rail section was hit overnight and traffic halted, the "
         "governor said.",
         "REPORTED", GREEN, "bridge"),
        ("GAZA · CEASEFIRE", "Israel says its Gaza tank raid is over",
         "The push past the Yellow Line is complete; residents may return, "
         "the army said.",
         "CLAIM", GOLD, "tank"),
        ("RIYADH · GULF", "Houthi missile shot down over Riyadh",
         "Sirens at 04:42; debris caused damage. An airport-hit claim is "
         "unverified.",
         "CLAIM", GOLD, "missile"),
        ("FLORIDA · WEATHER", "Floods shut South Florida schools again",
         "Up to 15.3 inches fell in a day. Broward closed schools; more "
         "rain forecast.",
         "FORECAST", ORANGE, "flood"),
        ("SEOUL · EDUCATION", "551,864 sit South Korea's big exam",
         "Flights paused 35 minutes for listening. A 100m-won reward "
         "targets AI cheating.",
         "REPORTED", GREEN, "exam"),
        ("PARIS · POLITICS", "French left splits over Mélenchon pact",
         "Faure regrets the Greens' offer. An Elabe poll has Le Pen "
         "winning 68.5 to 31.5.",
         "REPORTED", GREEN, "poll"),
        ("JAKARTA · LAW", "Indonesia passes asset-seizure law",
         "After an 18-year wait, the state may seize assets of Rp1bn or "
         "more, no conviction.",
         "REPORTED", GREEN, "gavel"),
        ("BOGOTÁ · LABOUR", "Colombia's unions hold a national strike",
         "Teachers and workers march in Bogotá, Medellín and Cali against "
         "the rescue bill.",
         "REPORTED", GREEN, "crowd"),
        ("CANBERRA · ECONOMY", "Australian jobless rate jumps to 4.9%",
         "A five-year high, up from 4.7%. Lost 43,500 jobs; 25,000 were "
         "forecast.",
         "REPORTED", GREEN, "chart"),
    ]
    cw = (CW - 18) / 4
    ch = 114
    for i, (kicker, head, body, lbl, lblc, icon) in enumerate(minis):
        x = M + (i % 4) * (cw + 6)
        y = y0 + (i // 4) * (ch + 6)
        card(d, x, y, cw, ch)
        num_badge(d, x - 4, y - 8, i + 4)
        ty = y + 6
        d.text((x + 6, ty), kicker, font=SANS_B(8), fill=GREY)
        tag(d, x + cw - 52, ty - 1, lbl, lblc)
        ty += 11
        ty = para(d, x + 6, ty, cw - 12, head, SERIF(17), INK, leading=20)
        para(d, x + 6, ty + 2, cw - 12, body, SANS(15), INK, leading=17)
    return y0 + 3 * ch + 12


def draw_icon(d, x, y, w, h, kind):
    """Small flat illustration strip for a mini-card."""
    cx, cy = x + w / 2, y + h / 2
    if kind == "scales":
        d.rectangle([x, y, x + w, y + h], fill=(214, 190, 150))
        d.line([(cx, y + 3), (cx, y + h - 5)], fill=INK, width=2)
        d.line([(cx - 16, y + 6), (cx + 16, y + 6)], fill=INK, width=2)
        d.polygon([(cx - 20, y + 12), (cx - 12, y + 12), (cx - 16, y + 20)],
                  fill=GOLD)
        d.polygon([(cx + 12, y + 12), (cx + 20, y + 12), (cx + 16, y + 20)],
                  fill=GOLD)
        d.rectangle([x + 4, y + h - 6, x + w - 4, y + h - 3], fill=(150, 90, 40))
    elif kind == "globe":
        d.rectangle([x, y, x + w, y + h], fill=(120, 190, 220))
        d.ellipse([cx - 12, y + 2, cx + 12, y + h - 2], fill=(40, 140, 80))
        d.ellipse([cx - 6, y + 6, cx + 2, y + 12], fill=(120, 190, 220))
        d.ellipse([cx + 2, y + 14, cx + 9, y + 20], fill=(120, 190, 220))
    elif kind == "spiral":
        d.rectangle([x, y, x + w, y + h], fill=(200, 225, 235))
        for r in (11, 8, 5):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=TEAL, width=2)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)
    elif kind == "bridge":
        d.rectangle([x, y, x + w, y + h], fill=(190, 215, 235))
        d.rectangle([x + 4, y + h - 8, x + w - 4, y + h - 4], fill=(120, 90, 60))
        d.line([(x + 14, y + h - 8), (cx, y + 2)], fill=INK, width=2)
        d.line([(x + w - 14, y + h - 8), (cx, y + 2)], fill=INK, width=2)
        d.line([(cx, y + 2), (cx, y + h - 8)], fill=INK, width=2)
    elif kind == "tank":
        d.rectangle([x, y, x + w, y + h], fill=(225, 210, 160))
        d.line([(cx - 4, y + 8), (cx + 22, y + 8)], fill=INK, width=3)
        d.rectangle([cx - 14, y + 10, cx + 10, y + 18], fill=(90, 110, 60))
        d.rectangle([cx - 18, y + 18, cx + 16, y + 23], fill=(60, 80, 40))
        for wx in range(-16, 16, 6):
            d.ellipse([cx + wx, y + 18, cx + wx + 5, y + 23], fill=INK)
    elif kind == "missile":
        d.rectangle([x, y, x + w, y + h], fill=(20, 30, 60))
        d.polygon([(cx, y + 2), (cx - 5, y + 12), (cx + 5, y + 12)], fill=RED)
        d.rectangle([cx - 5, y + 12, cx + 5, y + 22], fill=(220, 220, 220))
        d.polygon([(cx - 5, y + 22), (cx - 9, y + 26), (cx - 5, y + 24)],
                  fill=(220, 220, 220))
        d.polygon([(cx + 5, y + 22), (cx + 9, y + 26), (cx + 5, y + 24)],
                  fill=(220, 220, 220))
        for sx, sy in [(x + 10, y + 8), (x + w - 12, y + 16), (x + 22, y + 20)]:
            d.text((sx, sy), "*", font=SANS_B(10), fill=(255, 220, 90))
    elif kind == "flood":
        d.rectangle([x, y, x + w, y + h], fill=(150, 200, 225))
        d.rectangle([x + 8, y + 6, x + 30, y + 16], fill=(200, 120, 80))
        d.polygon([(x + 8, y + 6), (x + 19, y - 1), (x + 30, y + 6)],
                  fill=(160, 60, 40))
        for wy in (18, 22):
            d.line([(x + 4, y + wy), (x + w - 4, y + wy)], fill=BLUE, width=2)
    elif kind == "exam":
        d.rectangle([x, y, x + w, y + h], fill=(210, 225, 190))
        d.rectangle([cx - 16, y + 12, cx + 16, y + 22], fill=(255, 255, 255),
                    outline=INK)
        for ly in (15, 18):
            d.line([(cx - 12, y + ly), (cx + 12, y + ly)], fill=GREY, width=1)
        d.ellipse([cx - 4, y + 2, cx + 4, y + 10], fill=(232, 196, 150))
    elif kind == "poll":
        d.rectangle([x, y, x + w, y + h], fill=(235, 230, 220))
        d.rectangle([x + 10, y + 16, x + w - 10, y + 22], fill=(200, 200, 200))
        d.rectangle([x + 10, y + 16, x + 10 + (w - 20) * 0.685, y + 22],
                    fill=RED)
        d.text((x + 10, y + 4), "68.5%", font=SANS_B(8), fill=RED)
        d.text((x + w - 34, y + 4), "31.5%", font=SANS_B(8), fill=BLUE)
    elif kind == "gavel":
        d.rectangle([x, y, x + w, y + h], fill=(220, 210, 190))
        d.rectangle([cx - 14, y + 6, cx + 14, y + 12], fill=(120, 80, 40))
        d.line([(cx, y + 12), (cx + 10, y + 22)], fill=(120, 80, 40), width=3)
        d.rectangle([cx - 12, y + 20, cx + 12, y + 24], fill=(90, 60, 30))
    elif kind == "crowd":
        d.rectangle([x, y, x + w, y + h], fill=(235, 220, 180))
        for i, col in enumerate([(200, 60, 60), (60, 90, 180), (60, 150, 90),
                                 (220, 150, 40), (140, 80, 180)]):
            hx = x + 12 + i * 16
            d.ellipse([hx, y + 5, hx + 10, y + 15], fill=(232, 196, 150))
            d.pieslice([hx - 2, y + 15, hx + 12, y + 26], 180, 360, fill=col)
        d.rectangle([x + 30, y + 2, x + w - 30, y + 6], fill=(255, 255, 255))
        d.text((x + 34, y + 2), "PARO NACIONAL", font=SANS_B(5), fill=RED)
    else:  # chart
        d.rectangle([x, y, x + w, y + h], fill=(235, 230, 220))
        pts = [(x + 8, y + 18), (x + 26, y + 14), (x + 44, y + 16),
               (x + 62, y + 10), (x + 80, y + 6)]
        d.line(pts, fill=RED, width=2)
        for px, py in pts:
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        d.text((x + w - 26, y + 2), "4.9%", font=SANS_B(9), fill=RED)


def bottom_band(d, M, CW, y0):
    """Map | also-on-this-page | verdict / how sure / markets."""
    y1 = y0
    h = 168
    colw = (CW - 12) / 3
    # --- map ---
    x = M
    card(d, x, y1, colw, h)
    d.text((x + 6, y1 + 4), "WHERE IT HAPPENED", font=SANS_B(10), fill=INK)
    mx, my, mw, mh = x + 6, y1 + 18, colw - 12, h - 24
    d.rectangle([mx, my, mx + mw, my + mh], fill=(228, 216, 178))
    # simplified continents
    d.ellipse([mx + 8, my + 38, mx + 78, my + 76], fill=(196, 178, 120))
    d.ellipse([mx + 88, my + 50, mx + 150, my + 90], fill=(196, 178, 120))
    d.ellipse([mx + 150, my + 34, mx + 205, my + 70], fill=(196, 178, 120))
    d.ellipse([mx + 60, my + 86, mx + 120, my + 116], fill=(196, 178, 120))
    d.ellipse([mx + 205, my + 86, mx + 235, my + 116], fill=(196, 178, 120))
    dots = [(30, 54), (60, 50), (95, 58), (120, 54), (150, 52), (175, 46),
            (100, 79), (130, 84), (160, 79), (215, 64), (75, 99), (200, 104)]
    for i, (dx, dy) in enumerate(dots):
        px, py = mx + dx, my + dy
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                  outline=(255, 255, 255))
        d.text((px - 2, py - 4), str(i + 1), font=SANS_B(6),
               fill=(255, 255, 255))
    # --- also on this page ---
    x = M + colw + 6
    card(d, x, y1, colw, h)
    d.text((x + 6, y1 + 4), "ALSO ON THIS PAGE", font=SANS_B(10), fill=INK)
    items = [
        ("KYIV", "Zelenskyy in Berlin for talks."),
        ("SHENZHEN", "Xi pledges $20bn for APEC."),
        ("PARIS", "IEA: Hormuz is top energy threat."),
        ("DHAKA", "League shutdown; two killed."),
        ("SANAA", "Saudi strikes hit the capital."),
        ("RIYADH", "Prince meets US general."),
        ("KENYA", "Jepchirchir banned 3 years."),
        ("OTTAWA", "China deal: pork tariff relief."),
        ("SYDNEY", "Rate cut priced for mid-2027."),
        ("BOGOTÁ", "Strike goes on; VAT dropped."),
    ]
    yy = y1 + 18
    for city, txt in items:
        d.text((x + 6, yy), city, font=SANS_B(13), fill=RED)
        tx = x + 6 + d.textlength(city, font=SANS_B(13)) + 8
        f = SANS(13)
        while d.textlength("— " + txt, font=f) > x + colw - 6 - tx and " " in txt:
            txt = txt.rsplit(" ", 1)[0] + "…"
        d.text((tx, yy), "— " + txt, font=f, fill=INK)
        yy += 15
    # --- verdict / how sure / markets ---
    x = M + 2 * (colw + 6)
    card(d, x, y1, colw, h, fill=NAVY)
    d.text((x + 6, y1 + 4), "THE VERDICT", font=SANS_B(10), fill=(255, 255, 255))
    _vt = "THE HAGUE · 10:00"
    d.text((x + colw - 6 - d.textlength(_vt, font=SANS_B(8)), y1 + 5), _vt,
           font=SANS_B(8), fill=(180, 200, 230))
    yy = para(d, x + 6, y1 + 18, colw - 12,
              "Myanmar committed genocide, 9 to 6 — first state the court "
              "holds liable. Must allow return and pay reparations.",
              SERIF(12.5), (255, 255, 255), leading=15)
    hline(d, x + 6, yy + 3, x + colw - 6, 1, fill=(120, 150, 200))
    yy += 8
    d.text((x + 6, yy), "HOW SURE ARE WE?", font=SANS_B(9),
           fill=(255, 255, 255))
    yy += 12
    for lbl, txt, col in [("REPORTED", "confirmed by named sources", GREEN),
                          ("CLAIM", "one side says; unverified", GOLD),
                          ("FORECAST", "poll, draft or schedule", ORANGE)]:
        tag(d, x + 6, yy, lbl, col)
        d.text((x + 62, yy + 1), txt, font=SANS(9.5), fill=(220, 225, 240))
        yy += 11
    hline(d, x + 6, yy + 1, x + colw - 6, 1, fill=(120, 150, 200))
    yy += 6
    d.text((x + 6, yy), "MARKETS & MONEY", font=SANS_B(9),
           fill=(255, 255, 255))
    yy += 11
    for a, b in [("ANT  $83", "IPO price, set Wed"),
                 ("$81.3bn", "largest IPO on record"),
                 ("JOBLESS  4.9%", "up from 4.7%")]:
        d.text((x + 6, yy), a, font=SANS_B(9.5), fill=(255, 255, 255))
        d.text((x + colw - 6 - d.textlength(b, font=SANS(9.5)), yy), b,
               font=SANS(9.5), fill=(200, 210, 235))
        yy += 10
    return y1 + h


def date_check(d, M, CW, y0):
    y = y0 + 6
    d.rectangle([M, y, M + CW, y + 52], fill=(255, 255, 255), outline=RED,
                width=1)
    d.text((M + 6, y + 3), "DATE CHECK", font=SANS_B(11), fill=RED)
    d.text((M + 92, y + 3),
           "In the headlines today, but NOT Thursday's news, so left off "
           "this page:", font=SANS_B(10), fill=INK)
    txt = ("Anthropic's $83 pricing (Wed 18) · Israel's Gaza push (Wed 18) · "
           "Greens' offer to Mélenchon (Wed 18) · Voyager 1 one light-day "
           "out (Wed 18) · Van Gogh sold for $190.4m (Wed 18) · EU €45bn "
           "Ukraine loan (Wed 18) · İmamoğlu sentenced (Wed 18)")
    para(d, M + 6, y + 16, CW - 12, txt, SANS(14), INK, leading=17)


def build():
    img, d, M, CW = main()
    y = mini_cards(d, M, CW, 416)
    y = bottom_band(d, M, CW, y + 4)
    date_check(d, M, CW, y)
    d.text((M, 1008), "Every story on this page happened, or was first "
           "reported, on Thursday 19 November 2026. Disputed claims are "
           "attributed, not stated as fact. Times are local. Sources: "
           "Reuters, AP, BBC, Al Jazeera, Xinhua, Yonhap, Antara, ABS, ICJ.",
           font=SANS(8), fill=GREY)
    img.save(OUT, format="PNG", optimize=True)
    data = open(OUT, "rb").read()
    print("wrote", OUT, len(data), "bytes")
    print("sha256", hashlib.sha256(data).hexdigest())
    print("size", Image.open(OUT).size)


if __name__ == "__main__":
    build()
