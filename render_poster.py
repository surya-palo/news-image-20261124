#!/usr/bin/env python3
"""Render the news poster for Tuesday 24 November 2026.

Pure standard library: a hand-built 5x7 bitmap font, a pixel buffer,
and a minimal PNG encoder (zlib + struct). No network, no fonts on disk,
no third-party packages. Deterministic: same bytes every run.
"""
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
GOLD = (176, 132, 24)
TEAL = (14, 110, 110)
GREEN = (34, 110, 54)
GREY = (90, 86, 78)
LIGHT = (232, 226, 212)
WHITE = (255, 255, 255)
SEA = (24, 64, 96)
SKY = (214, 228, 238)

# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 rows of 5 bits, "1" = ink.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "a": ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    "b": ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    "c": ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
    "d": ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "f": ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    "g": ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    "h": ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "j": ("00010", "00000", "00110", "00010", "00010", "00010", "10110"),
    "k": ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "n": ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "p": ("00000", "00000", "11110", "10001", "10001", "11110", "10000"),
    "q": ("00000", "00000", "01111", "10001", "10001", "01111", "00001"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "s": ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    "t": ("01000", "01000", "11100", "01000", "01000", "01001", "00110"),
    "u": ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    "v": ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    "w": ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    "x": ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    "y": ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    "z": ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "*": ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
}

# ---------------------------------------------------------------- canvas
buf = bytearray(W * H * 3)
for i in range(0, len(buf), 3):
    buf[i], buf[i + 1], buf[i + 2] = PAPER


def set_px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        o = (y * W + x) * 3
        buf[o], buf[o + 1], buf[o + 2] = color


def rect(x, y, w, h, color):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            set_px(xx, yy, color)


def hline(x, y, w, color, t=1):
    rect(x, y, w, t, color)


def vline(x, y, h, color, t=1):
    rect(x, y, t, h, color)


def circle(cx, cy, r, color):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                set_px(xx, yy, color)


def ring(cx, cy, r, color, t=2):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            d = (xx - cx) ** 2 + (yy - cy) ** 2
            if (r - t) ** 2 <= d <= r * r:
                set_px(xx, yy, color)


def triangle(x1, y1, x2, y2, x3, y3, color):
    # fill triangle by scanline
    xs = sorted([(x1, y1), (x2, y2), (x3, y3)], key=lambda p: p[1])
    (ax, ay), (bx, by), (cx, cy) = xs
    for y in range(ay, cy + 1):
        def interp(p, q, yy):
            if q[1] == p[1]:
                return p[0]
            return p[0] + (q[0] - p[0]) * (yy - p[1]) / (q[1] - p[1])
        if y < by:
            xa, xb = interp((ax, ay), (bx, by), y), interp((ax, ay), (cx, cy), y)
        else:
            xa, xb = interp((bx, by), (cx, cy), y), interp((ax, ay), (cx, cy), y)
        for x in range(int(min(xa, xb)), int(max(xa, xb)) + 1):
            set_px(x, y, color)


# ---------------------------------------------------------------- text
def text_width(s, scale):
    return len(s) * 6 * scale - scale


def draw_char(ch, x, y, scale, color):
    g = FONT.get(ch)
    if g is None:
        g = FONT["?"]
    for row in range(7):
        bits = g[row]
        for col in range(5):
            if bits[col] == "1":
                rect(x + col * scale, y + row * scale, scale, scale, color)


def draw_text(s, x, y, scale, color):
    cx = x
    for ch in s:
        draw_char(ch, cx, y, scale, color)
        cx += 6 * scale
    return cx


def draw_text_centered(s, cx, y, scale, color):
    draw_text(s, cx - text_width(s, scale) // 2, y, scale, color)


def wrap_text(s, scale, max_w):
    """Greedy word wrap; returns list of lines."""
    words = s.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_width(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_para(s, x, y, scale, max_w, color, leading=None):
    lh = leading if leading is not None else 10 * scale
    for i, line in enumerate(wrap_text(s, scale, max_w)):
        draw_text(line, x, y + i * lh, scale, color)
    return y + len(wrap_text(s, scale, max_w)) * lh

# ---------------------------------------------------------------- layout
M = 36                      # outer margin
CW = W - 2 * M              # content width = 952

# --- masthead -------------------------------------------------------------
y = 30
draw_text_centered("THE WORLD IN ONE DAY", W // 2, y, 5, INK)
y += 5 * 7 + 14
hline(M, y, CW, RED, 5)
y += 12
draw_text("TUESDAY, 24 NOVEMBER 2026", M, y, 3, RED)
right = "ONE DAY - ONE PAGE - THE WORLD'S NEWS"
draw_text(right, W - M - text_width(right, 2), y + 3, 2, GREY)
y += 3 * 7 + 12
hline(M, y, CW, INK, 2)
y += 14

# --- lead story -----------------------------------------------------------
LEAD_H = 296
lead_top = y
# kicker
draw_text("WAR AT SEA  -  KYIV SAYS", M, lead_top, 2, RED)
# illustration panel on the right: sea, ship, drones, burst
IX, IY, IW, IH = W - M - 330, lead_top + 4, 330, LEAD_H - 40
rect(IX, IY, IW, IH, SKY)
rect(IX, IY + 150, IW, IH - 150, SEA)
# sun / clouds
circle(IX + 52, IY + 42, 26, GOLD)
rect(IX + 190, IY + 30, 90, 14, WHITE)
rect(IX + 210, IY + 48, 70, 12, WHITE)
# ship hull + superstructure (silhouette)
rect(IX + 40, IY + 168, 250, 26, INK)
triangle(IX + 40, IY + 168, IX + 40, IY + 194, IX + 14, IY + 194, INK)
rect(IX + 120, IY + 138, 70, 30, INK)
rect(IX + 138, IY + 118, 10, 22, INK)
rect(IX + 168, IY + 128, 34, 10, INK)
# waves (clipped to the panel)
for wx in range(IX + 8, IX + IW - 8, 34):
    w1 = min(22, IX + IW - 4 - wx)
    w2 = min(22, IX + IW - 4 - (wx + 12))
    if w1 > 0:
        hline(wx, IY + 210, w1, WHITE, 3)
    if w2 > 0:
        hline(wx + 12, IY + 232, w2, WHITE, 3)
# explosion burst above the ship
bx, by = IX + 155, IY + 96
for ang in range(0, 360, 30):
    import math
    r1, r2 = 12, 34
    x1 = bx + int(r1 * math.cos(math.radians(ang)))
    y1 = by + int(r1 * math.sin(math.radians(ang)))
    x2 = bx + int(r2 * math.cos(math.radians(ang)))
    y2 = by + int(r2 * math.sin(math.radians(ang)))
    # draw a thick spoke as a small rect line
    steps = max(abs(x2 - x1), abs(y2 - y1), 1)
    for s in range(steps + 1):
        px = x1 + (x2 - x1) * s // steps
        py = y1 + (y2 - y1) * s // steps
        rect(px - 2, py - 2, 5, 5, RED if s % 2 == 0 else GOLD)
circle(bx, by, 14, RED)
circle(bx, by, 7, GOLD)
# seven sea drones: small dots with wakes heading for the ship
for i, dx in enumerate(range(IX + 30, IX + 300, 42)):
    dy = IY + IH - 26 - (i % 2) * 12
    circle(dx, dy, 4, WHITE)
    hline(dx - 16, dy, 12, WHITE, 2)
cap = "SEVEN SEA DRONES"
rect(IX + 4, IY + IH - 20, text_width(cap, 1) + 12, 15, INK)
draw_text(cap, IX + 10, IY + IH - 17, 1, WHITE)
# headline + body on the left
HX = M
HW = W - 2 * M - 330 - 28
hy = lead_top + 26
draw_text("UKRAINE SINKS", HX, hy, 4, INK)
hy += 4 * 7 + 6
draw_text("RUSSIAN WARSHIP", HX, hy, 4, INK)
hy += 4 * 7 + 6
draw_text("OFF LIBYA", HX, hy, 4, RED)
hy += 4 * 7 + 14
body = ("Kyiv says seven sea drones sank the corvette Merkury near "
        "Benghazi, destroying a Ka-27 helicopter and hitting the cargo "
        "ship MV Angara. Moscow has not confirmed the loss.")
draw_para(body, HX, hy, 2, HW, INK, leading=19)
y = lead_top + LEAD_H
hline(M, y, CW, INK, 2)
y += 12

# --- card grid: 2 columns x 3 rows ---------------------------------------
CARDS = [
    ("TECH  -  CHIPS", BLUE,
     "HUANG IS BACK AT NVIDIA",
     "The board reinstates Jensen Huang as CEO, days after rejecting his "
     "return. Trump pushed for it; shares jumped a third.", "chip"),
    ("SPORT  -  FOOTBALL", GREEN,
     "WOMEN'S WORLD CUP HOSTS SET",
     "FIFA confirms the USA, Mexico, Costa Rica and Jamaica for 2031, and "
     "the four UK nations for 2035. Both grow to 48 teams.", "ball"),
    ("CLIMATE  -  COP31", TEAL,
     "CLIMATE TALKS END WITH NO DEAL",
     "Nearly 200 nations leave Antalya without a deal, split over fossil "
     "fuels. The longest COP on record.", "globe"),
    ("ASIA  -  INDONESIA", RED,
     "SEARCH AFTER FACTORY FIRE",
     "24 dead are confirmed after the candy factory blaze near Jakarta, "
     "and about 30 workers are still missing.", "flame"),
    ("SPORT  -  CHESS", GOLD,
     "CHESS CROWN BATTLE BEGINS TODAY",
     "Game 1 in Geneva: champion Gukesh, 20, defends against Sindarov, "
     "20, in the youngest title match ever.", "board"),
    ("EUROPE  -  DENMARK", BLUE,
     "DENMARK BACKS 'GHETTO LAW'",
     "The top court rules ending 91 leases was not ethnic discrimination, "
     "backing the hard line on immigration.", "scales"),
]
CARD_W = (CW - 20) // 2
CARD_H = 138
GAP = 20


def draw_icon(kind, x, y, color):
    """Small 44x44 pictogram inside a card."""
    if kind == "chip":
        rect(x + 8, y + 8, 28, 28, color)
        rect(x + 16, y + 16, 12, 12, PAPER)
        for px in (12, 22, 32):
            rect(x + px, y + 2, 3, 6, color)
            rect(x + px, y + 36, 3, 6, color)
            rect(x + 2, y + px, 6, 3, color)
            rect(x + 36, y + px, 6, 3, color)
    elif kind == "ball":
        circle(x + 22, y + 22, 20, color)
        circle(x + 22, y + 22, 8, PAPER)
        for dx, dy in ((-14, -10), (14, -10), (-14, 10), (14, 10), (0, -18)):
            circle(x + 22 + dx, y + 22 + dy, 3, PAPER)
    elif kind == "globe":
        circle(x + 22, y + 22, 20, color)
        ring(x + 22, y + 22, 20, PAPER, 2)
        rect(x + 12, y + 14, 20, 4, PAPER)
        rect(x + 16, y + 26, 12, 4, PAPER)
        vline(x + 22, y + 4, 36, PAPER, 2)
    elif kind == "flame":
        triangle(x + 22, y + 4, x + 6, y + 34, x + 38, y + 34, color)
        triangle(x + 22, y + 16, x + 14, y + 34, x + 30, y + 34, GOLD)
        rect(x + 6, y + 38, 32, 4, color)
    elif kind == "board":
        for r in range(4):
            for c in range(4):
                if (r + c) % 2 == 0:
                    rect(x + 4 + c * 9, y + 4 + r * 9, 9, 9, color)
    elif kind == "scales":
        vline(x + 22, y + 6, 32, color, 3)
        hline(x + 8, y + 8, 28, color, 3)
        triangle(x + 8, y + 12, x + 2, y + 26, x + 14, y + 26, color)
        triangle(x + 36, y + 12, x + 30, y + 26, x + 42, y + 26, color)
        hline(x + 10, y + 38, 24, color, 3)


for idx, (kicker, color, head, text, icon) in enumerate(CARDS):
    cx = M + (idx % 2) * (CARD_W + GAP)
    cy = y + (idx // 2) * (CARD_H + 12)
    rect(cx, cy, CARD_W, CARD_H, WHITE)
    rect(cx, cy, CARD_W, 4, color)
    draw_icon(icon, cx + 10, cy + 18, color)
    tx = cx + 64
    tw = CARD_W - 64 - 14
    draw_text(kicker, tx, cy + 12, 2, color)
    hlen = text_width(head, 2)
    hscale = 2 if hlen <= tw else 2
    # headline: wrap to at most 2 lines at scale 2
    hlines = wrap_text(head, 2, tw)
    hyy = cy + 32
    for ln in hlines[:2]:
        draw_text(ln, tx, hyy, 2, INK)
        hyy += 16
    draw_para(text, tx, cy + 32 + len(hlines[:2]) * 16 + 4, 2, tw, INK, leading=17)
    if idx == 5:
        y = cy + CARD_H
y += 14
hline(M, y, CW, INK, 2)
y += 12

# --- also-today strip -------------------------------------------------------
draw_text("ALSO TODAY", M, y, 2, RED)
strip = ("BEAVER SUPERMOON: the full Moon peaks today and passes the "
         "Pleiades, the Seven Sisters.  -  A supermoon series runs to "
         "January 2027.")
draw_para(strip, M + text_width("ALSO TODAY  ", 2) + 10, y, 2, CW - text_width("ALSO TODAY  ", 2) - 10, INK, leading=17)
y += 46
hline(M, y, CW, INK, 2)
y += 10
draw_text("Stories as reported on Tuesday 24 November 2026. Sources: Reuters, AP, BBC, FIFA, FIDE.",
          M, y, 1, GREY)
y += 12
draw_text("An image of one day's world news - 24 November 2026.", M, y, 1, GREY)

# ---------------------------------------------------------------- PNG encode
def chunk(typ, data):
    c = struct.pack(">I", len(data)) + typ + data
    return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)


def write_png(path):
    raw = b"".join(b"\x00" + bytes(buf[y * W * 3:(y + 1) * W * 3]) for y in range(H))
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    size = write_png(out)
    print(f"wrote {out} ({size} bytes)")
