#!/usr/bin/env python3
"""Render entry.png: a one-image summary of world news for Saturday 21 November 2026.

A newspaper-style front page: masthead with the date, a lead story, and a grid of
the day's biggest stories, each labelled so a reader who missed the day can tell
what happened from the image alone.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (244, 239, 228)
INK = (26, 28, 32)
INK_SOFT = (72, 76, 84)
RED = (176, 32, 38)
BLUE = (28, 58, 96)
GOLD = (176, 128, 40)
LINE = (60, 60, 58)

FD = "/usr/share/fonts/truetype/dejavu"
def F(name, size):
    return ImageFont.truetype(f"{FD}/{name}", size)

SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_C = "DejaVuSansCondensed.ttf"
SANS_CB = "DejaVuSansCondensed-Bold.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"

def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def story_icon(d, kind, x, y, s, col):
    """Tiny pictograms, s = box size."""
    if kind == "mic":          # Trump press conference
        d.rounded_rectangle([x+s*.32, y, x+s*.68, y+s*.62], radius=s*.18, fill=col)
        d.arc([x+s*.18, y+s*.30, x+s*.82, y+s*.78], 0, 180, fill=col, width=max(2,int(s*.05)))
        d.line([x+s*.5, y+s*.78, x+s*.5, y+s*.95], fill=col, width=max(2,int(s*.05)))
        d.line([x+s*.3, y+s*.95, x+s*.7, y+s*.95], fill=col, width=max(2,int(s*.05)))
    elif kind == "fist":       # protests
        d.rounded_rectangle([x+s*.15, y+s*.30, x+s*.85, y+s*.80], radius=s*.10, fill=col)
        for i in range(4):
            d.rectangle([x+s*.15+i*s*.175, y+s*.12, x+s*.30+i*s*.175, y+s*.34], fill=col)
        d.rectangle([x+s*.33, y+s*.80, x+s*.67, y+s*.98], fill=col)
    elif kind == "scales":     # ICJ / court
        d.line([x+s*.5, y+s*.08, x+s*.5, y+s*.80], fill=col, width=max(2,int(s*.05)))
        d.line([x+s*.15, y+s*.22, x+s*.85, y+s*.22], fill=col, width=max(2,int(s*.05)))
        for sx in (x+s*.15, x+s*.85):
            d.line([sx, y+s*.22, sx-s*.10, y+s*.55], fill=col, width=max(1,int(s*.035)))
            d.line([sx, y+s*.22, sx+s*.10, y+s*.55], fill=col, width=max(1,int(s*.035)))
            d.pieslice([sx-s*.13, y+s*.48, sx+s*.13, y+s*.82], 0, 180, fill=col)
        d.line([x+s*.30, y+s*.86, x+s*.70, y+s*.86], fill=col, width=max(2,int(s*.05)))
    elif kind == "missile":    # Iran missile launcher
        d.polygon([(x+s*.5,y),(x+s*.63,y+s*.28),(x+s*.63,y+s*.75),(x+s*.37,y+s*.75),(x+s*.37,y+s*.28)], fill=col)
        d.polygon([(x+s*.37,y+s*.75),(x+s*.20,y+s*.98),(x+s*.37,y+s*.95)], fill=col)
        d.polygon([(x+s*.63,y+s*.75),(x+s*.80,y+s*.98),(x+s*.63,y+s*.95)], fill=col)
        d.polygon([(x+s*.42,y+s*.75),(x+s*.50,y+s*.98),(x+s*.58,y+s*.75)], fill=GOLD)
    elif kind == "flag":       # Denmark / Russia expulsion
        d.line([x+s*.25, y+s*.05, x+s*.25, y+s*.95], fill=col, width=max(2,int(s*.05)))
        d.polygon([(x+s*.25,y+s*.05),(x+s*.82,y+s*.18),(x+s*.25,y+s*.40)], fill=col)
        d.rectangle([x+s*.32, y+s*.13, x+s*.38, y+s*.32], fill=PAPER)
        d.rectangle([x+s*.28, y+s*.20, x+s*.60, y+s*.26], fill=PAPER)
    elif kind == "coins":      # Spain banking tax
        for i in range(3):
            d.ellipse([x+s*.10+i*s*.10, y+s*.55-i*s*.22, x+s*.55+i*s*.10, y+s*.95-i*s*.22], fill=col, outline=PAPER, width=2)
        d.ellipse([x+s*.48, y+s*.10, x+s*.92, y+s*.50], fill=col, outline=PAPER, width=2)
        d.text((x+s*.60, y+s*.16), "€", font=F(SANS_B, int(s*.34)), fill=PAPER)
    elif kind == "fire":       # Basra power station fire
        d.polygon([(x+s*.50,y+s*.02),(x+s*.68,y+s*.35),(x+s*.80,y+s*.28),(x+s*.88,y+s*.60),(x+s*.72,y+s*.92),(x+s*.28,y+s*.92),(x+s*.12,y+s*.60),(x+s*.22,y+s*.30),(x+s*.38,y+s*.42)], fill=col)
        d.polygon([(x+s*.50,y+s*.38),(x+s*.66,y+s*.65),(x+s*.55,y+s*.88),(x+s*.40,y+s*.88),(x+s*.34,y+s*.62)], fill=GOLD)
    elif kind == "plane":      # Trump Asia trip
        d.polygon([(x+s*.05,y+s*.55),(x+s*.95,y+s*.45),(x+s*.70,y+s*.55),(x+s*.90,y+s*.85),(x+s*.60,y+s*.62),(x+s*.35,y+s*.95),(x+s*.40,y+s*.60)], fill=col)

def card(d, x, y, w, h, tag, tag_col, icon, head, dek, head_lines=2):
    d.rectangle([x, y, x+w, y+h], fill=(252, 249, 242), outline=LINE, width=1)
    d.rectangle([x, y, x+6, y+h], fill=tag_col)
    pad = 14
    # tag
    d.text((x+pad+4, y+10), tag.upper(), font=F(SANS_CB, 17), fill=tag_col)
    # icon box
    isz = 56
    d.rounded_rectangle([x+pad, y+34, x+pad+isz, y+34+isz], radius=8, fill=(236, 231, 219), outline=LINE, width=1)
    story_icon(d, icon, x+pad+8, y+40, isz-16, tag_col)
    # headline
    tx = x + pad + isz + 12
    tw = w - isz - pad*2 - 12
    hf = F(SANS_B, 21)
    lines = wrap(d, head, hf, tw)[:head_lines]
    yy = y + 36
    for ln in lines:
        d.text((tx, yy), ln, font=hf, fill=INK)
        yy += 25
    # dek under icon+headline, full card width
    dy = y + 34 + isz + 10
    df = F(SANS_C, 17)
    for ln in wrap(d, dek, df, w - pad*2 - 6)[:3]:
        d.text((x+pad+4, dy), ln, font=df, fill=INK_SOFT)
        dy += 21

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ===== masthead =====
    d.rectangle([0, 0, W, 118], fill=INK)
    d.text((36, 16), "THE DAILY WORLD", font=F(SERIF_B, 44), fill=PAPER)
    d.text((36, 74), "make.fun one-day news image  ·  entries judged by AI", font=F(SANS_C, 17), fill=(170, 174, 182))
    # date block right
    d.rectangle([W-286, 16, W-20, 100], fill=RED)
    d.text((W-268, 22), "SATURDAY", font=F(SANS_B, 22), fill=PAPER)
    d.text((W-268, 50), "21 NOV 2026", font=F(SANS_B, 30), fill=(255, 214, 120))
    d.rectangle([0, 118, W, 124], fill=RED)

    # ===== lead story band =====
    ly = 142
    d.text((36, ly), "LEAD", font=F(SANS_CB, 16), fill=RED)
    lead_f = F(SERIF_B, 34)
    lead = "Trump, back from China, threatens Iran over 'dirty bomb' plot"
    hy = ly + 26
    for ln in wrap(d, lead, lead_f, 730)[:2]:
        d.text((36, hy), ln, font=lead_f, fill=INK)
        hy += 40
    hy += 4
    for ln in wrap(d, "At his first post-Asia press conference he defended ties with Putin, played down a wave of US outages and sought $50bn for air traffic control.", F(SANS_C, 19), 730)[:2]:
        d.text((36, hy), ln, font=F(SANS_C, 19), fill=INK_SOFT)
        hy += 23
    # lead icon
    d.rounded_rectangle([792, ly+22, 988, ly+140], radius=10, fill=(236, 231, 219), outline=LINE, width=1)
    story_icon(d, "mic", 838, ly+36, 100, BLUE)
    d.line([36, hy+26, 988, hy+26], fill=LINE, width=2)

    # ===== grid of six cards =====
    gy, gh, gw, gap = hy + 40, 202, 472, 10
    cards = [
        ("EUROPE", "youth strike", "fist", "Student 'youth strike' sweeps 25+ European countries", "Rallies in 73 German cities alone; demands run from school funding and climate justice to ending conscription.", BLUE),
        ("MIDDLE EAST", "Iran", "missile", "Iran shows new twin-missile launcher, tankers hit", "State TV aired an underground IRGC launcher said to fire two liquid-fuel missiles; three tankers were struck.", RED),
        ("ASIA / LAW", "ICJ ruling", "scales", "UN top court's Myanmar genocide ruling splits powers", "US reacts cautiously, EU praises the 'critical' court, China warns of judicial overreach.", GOLD),
        ("EUROPE", "Denmark–Russia", "flag", "Denmark expels Russian defence attache, curbs visas", "FM Rasmussen: 'enough is enough'; non-essential visas for Russians halted, Schengen talks to follow.", BLUE),
        ("IRAQ", "Basra", "fire", "Fire at Basra power station kills at least 4", "Blaze at the Hartha plant north of Basra leaves 35 injured; toll expected to rise.", RED),
        ("SPAIN", "housing", "coins", "Sanchez extends bank tax to fund housing", "Levy extended to 2027, cabinet vote Tuesday, as PM heads into a snap election on 29 November.", GOLD),
    ]
    for i, (tag, tc_txt, icon, head, dek, col) in enumerate(cards):
        r, c = divmod(i, 2)
        card(d, 36 + c*(gw+gap), gy + r*(gh+gap), gw, gh, tag + " · " + tc_txt, col, icon, head, dek)

    # ===== ticker =====
    ty = gy + 3*gh + 2*gap + 8
    d.rectangle([0, ty, W, H], fill=INK)
    d.text((36, ty+10), "ALSO TODAY", font=F(SANS_CB, 18), fill=GOLD)
    tick = "Merz urges a '360-degree partnership' with Qatar  ·  Houthi attacks cloud US-Saudi nuclear pact  ·  Trump fires cyber director Cairncross  ·  Thousands across Europe demand better wages and services"
    tf = F(SANS_C, 19)
    while d.textlength(tick, font=tf) > W - 72 and "  ·  " in tick:
        tick = tick.rsplit("  ·  ", 1)[0]
    d.text((36, ty+34), tick, font=tf, fill=PAPER)

    img.save("/root/bounties/news-entry/entry.png", optimize=True)
    print("wrote entry.png", os.path.getsize("/root/bounties/news-entry/entry.png"), "bytes")

if __name__ == "__main__":
    main()
