#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JhengJi Fonts Build Script (正記體 字型構建腳本)
Author: JhengJi Font Project
Description:
  Reads fonts from /input (7 weights of Noto Serif TC and TW-Kai TrueType),
  decomposes the 5 strokes of "正" (U+6B63), maps digits 1-5 and
  Unicode Ideographic Tally Marks (U+1D372..U+1D376), purges all other glyphs,
  rewrites font metadata tables (naming as 正記體-宋體 / 正記體-楷體),
  and exports both desktop (OTF/TTF) and web (WOFF2) font files.
"""

import os
import sys
import shutil
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._n_a_m_e import NameRecord
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.tables import ttProgram

INPUT_DIR = "input"
DIST_DIR = "dist"
DOCS_DIST_DIR = os.path.join("docs", "dist")
DOCS_FONTS_DIR = os.path.join("docs", "fonts")

NOTO_FONTS = [
    {
        "filename": "NotoSerifTC-ExtraLight.otf",
        "ps_name": "JhengJiSong-ExtraLight",
        "en_subfamily": "ExtraLight",
        "zh_subfamily": "極細",
        "weight_class": 200,
    },
    {
        "filename": "NotoSerifTC-Light.otf",
        "ps_name": "JhengJiSong-Light",
        "en_subfamily": "Light",
        "zh_subfamily": "細體",
        "weight_class": 300,
    },
    {
        "filename": "NotoSerifTC-Regular.otf",
        "ps_name": "JhengJiSong-Regular",
        "en_subfamily": "Regular",
        "zh_subfamily": "常規",
        "weight_class": 400,
    },
    {
        "filename": "NotoSerifTC-Medium.otf",
        "ps_name": "JhengJiSong-Medium",
        "en_subfamily": "Medium",
        "zh_subfamily": "中黑",
        "weight_class": 500,
    },
    {
        "filename": "NotoSerifTC-SemiBold.otf",
        "ps_name": "JhengJiSong-SemiBold",
        "en_subfamily": "SemiBold",
        "zh_subfamily": "半粗",
        "weight_class": 600,
    },
    {
        "filename": "NotoSerifTC-Bold.otf",
        "ps_name": "JhengJiSong-Bold",
        "en_subfamily": "Bold",
        "zh_subfamily": "粗體",
        "weight_class": 700,
    },
    {
        "filename": "NotoSerifTC-Black.otf",
        "ps_name": "JhengJiSong-Black",
        "en_subfamily": "Black",
        "zh_subfamily": "特黑",
        "weight_class": 900,
    },
]

KAI_FONT = {
    "filename": "TW-Kai-98_1.ttf",
    "ps_name": "JhengJiKai-Regular",
    "en_subfamily": "Regular",
    "zh_subfamily": "常規",
    "weight_class": 400,
}


def set_font_metadata(font, en_family, zh_family, en_subfamily, zh_subfamily, ps_name, weight_class):
    """Sets complete and clean font metadata to ensure identity as JhengJi."""
    # 1. OS/2 table
    if 'OS/2' in font:
        font['OS/2'].achVendID = b'JHJI'
        font['OS/2'].usWeightClass = weight_class
        if en_subfamily == 'Bold':
            font['OS/2'].fsSelection = 0x20
        else:
            font['OS/2'].fsSelection = 0x40

    # 2. CFF table
    if 'CFF ' in font:
        cff = font['CFF '].cff
        top_dict = cff[0]
        top_dict.FontName = ps_name
        top_dict.FullName = f"{en_family} {en_subfamily}"
        top_dict.FamilyName = en_family
        cff.fontNames = [ps_name]
        top_dict.Weight = en_subfamily
        top_dict.Notice = "JhengJi Font Project"

    # 3. Name table
    name_table = font['name']
    name_table.names = []

    def add_name(name_id, text, platform_id, enc_id, lang_id):
        nr = NameRecord()
        nr.nameID = name_id
        nr.platformID = platform_id
        nr.platEncID = enc_id
        nr.langID = lang_id
        if platform_id == 3:
            nr.string = text.encode('utf-16-be')
        else:
            nr.string = text.encode('latin-1', errors='replace')
        name_table.names.append(nr)

    full_name_en = f"{en_family} {en_subfamily}"
    full_name_zh = f"{zh_family} {zh_subfamily}"
    unique_id = f"1.000;JHJI;{ps_name};2026"
    version_str = "Version 1.000; JhengJi Font Project"

    # Windows English (platform 3, enc 1, lang 0x0409)
    add_name(1, en_family, 3, 1, 0x0409)
    add_name(2, en_subfamily, 3, 1, 0x0409)
    add_name(3, unique_id, 3, 1, 0x0409)
    add_name(4, full_name_en, 3, 1, 0x0409)
    add_name(5, version_str, 3, 1, 0x0409)
    add_name(6, ps_name, 3, 1, 0x0409)
    add_name(16, en_family, 3, 1, 0x0409)
    add_name(17, en_subfamily, 3, 1, 0x0409)

    # Windows Traditional Chinese (platform 3, enc 1, lang 0x0404)
    add_name(1, zh_family, 3, 1, 0x0404)
    add_name(2, zh_subfamily, 3, 1, 0x0404)
    add_name(3, unique_id, 3, 1, 0x0404)
    add_name(4, full_name_zh, 3, 1, 0x0404)
    add_name(5, version_str, 3, 1, 0x0404)
    add_name(6, ps_name, 3, 1, 0x0404)
    add_name(16, zh_family, 3, 1, 0x0404)
    add_name(17, zh_subfamily, 3, 1, 0x0404)

    # Macintosh English (platform 1, enc 0, lang 0)
    add_name(1, en_family, 1, 0, 0)
    add_name(2, en_subfamily, 1, 0, 0)
    add_name(3, unique_id, 1, 0, 0)
    add_name(4, full_name_en, 1, 0, 0)
    add_name(5, version_str, 1, 0, 0)
    add_name(6, ps_name, 1, 0, 0)


def setup_cmap(font, digit_glyph_map, zheng_glyph):
    """Configures cmap to map:
       - 0x0031..0x0035 -> strokes 1..5
       - 0x1D372..0x1D376 -> strokes 1..5
       - 0x6B63 -> stroke 5
       - 0x0020 -> space
    """
    cmap_table = font['cmap']
    base_cmap = font.getBestCmap()
    
    # Format 12 (SMP 32-bit subtable)
    cmap12 = None
    for t in cmap_table.tables:
        if t.format == 12:
            cmap12 = t
            break
    if not cmap12:
        cmap12 = CmapSubtable.newSubtable(12)
        cmap12.platformID = 3
        cmap12.platEncID = 10
        cmap12.language = 0
        cmap_table.tables.append(cmap12)

    new_map12 = {}
    if 0x0020 in base_cmap:
        new_map12[0x0020] = base_cmap[0x0020]

    for i in range(5):
        d_code = 0x0031 + i
        t_code = 0x1D372 + i
        gname = digit_glyph_map[d_code]
        new_map12[d_code] = gname
        new_map12[t_code] = gname

    # '正' (0x6B63) maps to tally 5 (same as digit 5)
    new_map12[0x6B63] = digit_glyph_map[0x35]
    cmap12.cmap = new_map12

    # Format 4 (BMP subtable for compatibility)
    cmap4 = None
    for t in cmap_table.tables:
        if t.format == 4:
            cmap4 = t
            break
    if not cmap4:
        cmap4 = CmapSubtable.newSubtable(4)
        cmap4.platformID = 3
        cmap4.platEncID = 1
        cmap4.language = 0
        cmap_table.tables.append(cmap4)

    new_map4 = {k: v for k, v in new_map12.items() if k <= 0xFFFF}
    cmap4.cmap = new_map4

    # Keep only cmap4 and cmap12
    cmap_table.tables = [cmap4, cmap12]


def clean_unused_tables(font):
    """Removes layout and metrics tables referencing deleted glyphs."""
    for tag in ['GSUB', 'GPOS', 'GDEF', 'BASE', 'VORG', 'vhea', 'vmtx', 'FFTM', 'TSI0', 'TSI1', 'TSI2', 'TSI3', 'TSI5']:
        if tag in font:
            del font[tag]


def build_noto_font(cfg):
    src_path = os.path.join(INPUT_DIR, cfg["filename"])
    print(f"\nProcessing Noto Serif TC: {cfg['filename']} -> {cfg['ps_name']}")

    # 1. Extract original '正' ops and metrics
    font_orig = TTFont(src_path)
    cmap_orig = font_orig.getBestCmap()
    orig_zheng_gname = cmap_orig[0x6B63]
    pen = RecordingPen()
    font_orig['CFF '].cff[0].CharStrings[orig_zheng_gname].draw(pen)
    ops = pen.value
    width, lsb = font_orig['hmtx'][orig_zheng_gname]

    # 2. Subset to only space, '1'..'5', and '正'
    options = subset.Options()
    options.set(layout_features=[])
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=[0x20, 0x31, 0x32, 0x33, 0x34, 0x35, 0x6B63])
    font = TTFont(src_path)
    subsetter.subset(font)

    cmap = font.getBestCmap()
    digit_glyph_map = {c: cmap[c] for c in [0x31, 0x32, 0x33, 0x34, 0x35]}
    zheng_glyph = cmap[0x6B63]

    # 3. Decompose 5 strokes
    s1 = [
        ('moveTo', ops[13][1]), ('lineTo', ops[14][1]), ('lineTo', ops[9][1]),
        ('curveTo', ops[10][1]), ('curveTo', ops[11][1]), ('lineTo', ops[12][1]),
        ('closePath', ())
    ]
    s2 = [
        ('moveTo', ops[13][1]), ('lineTo', ops[14][1]), ('lineTo', ops[15][1]),
        ('lineTo', ops[16][1]), ('lineTo', ops[1][1]), ('lineTo', ops[8][1]),
        ('lineTo', ops[9][1]), ('curveTo', ops[10][1]), ('curveTo', ops[11][1]),
        ('lineTo', ops[12][1]), ('closePath', ())
    ]
    s3 = [
        ('moveTo', ops[13][1]), ('lineTo', ops[14][1]), ('lineTo', ops[15][1]),
        ('lineTo', ops[16][1]), ('lineTo', ops[1][1]), ('lineTo', ops[2][1]),
        ('lineTo', ops[3][1]), ('curveTo', ops[4][1]), ('curveTo', ops[5][1]),
        ('lineTo', ops[6][1]), ('lineTo', ops[7][1]), ('lineTo', ops[8][1]),
        ('lineTo', ops[9][1]), ('curveTo', ops[10][1]), ('curveTo', ops[11][1]),
        ('lineTo', ops[12][1]), ('closePath', ())
    ]
    left_vert = [
        ('moveTo', ops[17][1]), ('lineTo', ops[18][1]), ('curveTo', ops[19][1]),
        ('lineTo', ops[20][1]), ('lineTo', ops[21][1]), ('closePath', ())
    ]
    s4 = s3 + left_vert
    s5 = ops

    stroke_ops = [s1, s2, s3, s4, s5]

    # 4. Replace CharStrings for digits 1..5
    cff = font['CFF '].cff[0]
    char_strings = cff.CharStrings

    for idx in range(5):
        d_code = 0x31 + idx
        gname = digit_glyph_map[d_code]
        old_cs = char_strings[gname]
        priv = old_cs.private
        nom = getattr(priv, 'nominalWidthX', 0)
        defw = getattr(priv, 'defaultWidthX', 0)
        w_target = 1000

        # Type 2 charstring width encoding:
        # If width == defaultWidthX, no width argument is encoded.
        # Otherwise, the argument is width - nominalWidthX.
        pen_width = (w_target - nom) if w_target != defw else None
        tpen = T2CharStringPen(pen_width, None)
        for op, args in stroke_ops[idx]:
            if op == 'moveTo': tpen.moveTo(args[0])
            elif op == 'lineTo': tpen.lineTo(args[0])
            elif op == 'curveTo': tpen.curveTo(*args)
            elif op == 'closePath': tpen.closePath()
        new_cs = tpen.getCharString()
        new_cs.private = priv
        char_strings[gname] = new_cs
        font['hmtx'][gname] = (w_target, lsb)

    # Stroke 5 is also assigned to '正'
    font['hmtx'][zheng_glyph] = (1000, lsb)

    # 5. Setup cmap with Ideographic Tally Marks
    setup_cmap(font, digit_glyph_map, zheng_glyph)

    # 6. Update metadata
    set_font_metadata(
        font=font,
        en_family="JhengJi Song",
        zh_family="正記體-宋體",
        en_subfamily=cfg["en_subfamily"],
        zh_subfamily=cfg["zh_subfamily"],
        ps_name=cfg["ps_name"],
        weight_class=cfg["weight_class"]
    )

    clean_unused_tables(font)

    # 7. Save OTF & WOFF2
    out_otf = os.path.join(DIST_DIR, f"{cfg['ps_name']}.otf")
    font.save(out_otf)
    print(f"  -> Generated OTF:   {out_otf} ({os.path.getsize(out_otf)} bytes)")

    # Also copy desktop font to docs/dist for direct web download
    docs_dist_otf = os.path.join(DOCS_DIST_DIR, f"{cfg['ps_name']}.otf")
    shutil.copy2(out_otf, docs_dist_otf)

    out_woff2 = os.path.join(DOCS_FONTS_DIR, f"{cfg['ps_name']}.woff2")
    font.flavor = "woff2"
    font.save(out_woff2)
    print(f"  -> Generated WOFF2: {out_woff2} ({os.path.getsize(out_woff2)} bytes)")


def build_kai_font(cfg):
    src_path = os.path.join(INPUT_DIR, cfg["filename"])
    print(f"\nProcessing TW-Kai: {cfg['filename']} -> {cfg['ps_name']}")

    # 1. Extract original '正' points and metrics
    font_orig = TTFont(src_path)
    cmap_orig = font_orig.getBestCmap()
    orig_zheng_gname = cmap_orig[0x6B63]
    orig_glyph = font_orig['glyf'][orig_zheng_gname]
    coords = orig_glyph.coordinates
    flags = orig_glyph.flags
    width, lsb = font_orig['hmtx'][orig_zheng_gname]

    # 2. Subset
    options = subset.Options()
    options.set(layout_features=[])
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=[0x20, 0x31, 0x32, 0x33, 0x34, 0x35, 0x6B63])
    font = TTFont(src_path)
    subsetter.subset(font)

    cmap = font.getBestCmap()
    digit_glyph_map = {c: cmap[c] for c in [0x31, 0x32, 0x33, 0x34, 0x35]}
    zheng_glyph = cmap[0x6B63]

    # 3. Decompose Kai strokes
    # Stroke 1: Top horizontal: points 8..48
    s1_pts = [coords[i] for i in range(8, 49)]
    s1_fls = [flags[i] for i in range(8, 49)]

    # Stroke 2: Top horizontal + Center vertical
    # Skipped points 60..84 completely (middle horizontal residue)
    # Point 59 is (543, 324) -> Point 85 is (543, 300) -> Point 86 is (540, 64) -> Point 1 is (481, 60)
    s2_idx = list(range(8, 60)) + [85, 86, 1] + list(range(2, 8))
    s2_pts = [coords[i] for i in s2_idx]
    s2_fls = [flags[i] for i in s2_idx]

    # Stroke 3: Top horizontal + Center vertical + Middle horizontal
    s3_idx = list(range(8, 49)) + list(range(49, 60)) + list(range(60, 80)) + list(range(80, 87)) + [1] + list(range(2, 8))
    s3_pts = [coords[i] for i in s3_idx]
    s3_fls = [flags[i] for i in s3_idx]

    # Stroke 4: Stroke 3 (contour 0) + Left vertical (contour 1: points 140..168, 0)
    s4_c0_pts = s3_pts
    s4_c0_fls = s3_fls
    s4_c1_idx = [140] + list(range(141, 169)) + [0]
    s4_c1_pts = [coords[i] for i in s4_c1_idx]
    s4_c1_fls = [flags[i] for i in s4_c1_idx]

    # Stroke 5: Full glyph (0..168)
    s5_pts = list(coords)
    s5_fls = list(flags)

    def make_simple_glyph(pts, fls, end_pts):
        g = Glyph()
        g.numberOfContours = len(end_pts)
        g.coordinates = pts
        g.flags = fls
        g.endPtsOfContours = end_pts
        g.program = ttProgram.Program()
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        g.xMin = min(xs) if xs else 0
        g.yMin = min(ys) if ys else 0
        g.xMax = max(xs) if xs else 0
        g.yMax = max(ys) if ys else 0
        return g

    g1 = make_simple_glyph(GlyphCoordinates(s1_pts), bytearray(s1_fls), [len(s1_pts) - 1])
    g2 = make_simple_glyph(GlyphCoordinates(s2_pts), bytearray(s2_fls), [len(s2_pts) - 1])
    g3 = make_simple_glyph(GlyphCoordinates(s3_pts), bytearray(s3_fls), [len(s3_pts) - 1])

    s4_pts_all = GlyphCoordinates(s4_c0_pts + s4_c1_pts)
    s4_fls_all = bytearray(s4_c0_fls + s4_c1_fls)
    s4_ends = [len(s4_c0_pts) - 1, len(s4_c0_pts) + len(s4_c1_pts) - 1]
    g4 = make_simple_glyph(s4_pts_all, s4_fls_all, s4_ends)

    g5 = make_simple_glyph(GlyphCoordinates(s5_pts), bytearray(s5_fls), [len(s5_pts) - 1])

    kai_glyphs = [g1, g2, g3, g4, g5]

    # Horizontally center each stroke glyph within the em-square (advance_width = 1024)
    for idx, g in enumerate(kai_glyphs):
        ink_w = g.xMax - g.xMin
        target_lsb = (width - ink_w) // 2
        dx = target_lsb - g.xMin
        if dx != 0:
            for i in range(len(g.coordinates)):
                x, y = g.coordinates[i]
                g.coordinates[i] = (x + dx, y)
            g.xMin += dx
            g.xMax += dx

    glyf_table = font['glyf']

    for idx in range(5):
        d_code = 0x31 + idx
        gname = digit_glyph_map[d_code]
        glyf_table[gname] = kai_glyphs[idx]
        font['hmtx'][gname] = (width, kai_glyphs[idx].xMin)

    font['hmtx'][zheng_glyph] = (width, kai_glyphs[4].xMin)

    # 4. Setup cmap
    setup_cmap(font, digit_glyph_map, zheng_glyph)

    # 5. Metadata
    set_font_metadata(
        font=font,
        en_family="JhengJi Kai",
        zh_family="正記體-楷體",
        en_subfamily=cfg["en_subfamily"],
        zh_subfamily=cfg["zh_subfamily"],
        ps_name=cfg["ps_name"],
        weight_class=cfg["weight_class"]
    )

    clean_unused_tables(font)

    # 6. Save TTF & WOFF2
    out_ttf = os.path.join(DIST_DIR, f"{cfg['ps_name']}.ttf")
    font.save(out_ttf)
    print(f"  -> Generated TTF:   {out_ttf} ({os.path.getsize(out_ttf)} bytes)")

    # Also copy desktop font to docs/dist for direct web download
    docs_dist_ttf = os.path.join(DOCS_DIST_DIR, f"{cfg['ps_name']}.ttf")
    shutil.copy2(out_ttf, docs_dist_ttf)

    out_woff2 = os.path.join(DOCS_FONTS_DIR, f"{cfg['ps_name']}.woff2")
    font.flavor = "woff2"
    font.save(out_woff2)
    print(f"  -> Generated WOFF2: {out_woff2} ({os.path.getsize(out_woff2)} bytes)")


def main():
    print("==================================================")
    print("  JhengJi Fonts Builder (正記體 字型構建器)")
    print("==================================================")
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(DOCS_DIST_DIR, exist_ok=True)
    os.makedirs(DOCS_FONTS_DIR, exist_ok=True)

    for cfg in NOTO_FONTS:
        build_noto_font(cfg)

    build_kai_font(KAI_FONT)

    print("\n==================================================")
    print("  All 8 fonts built successfully!")
    print(f"  Output directory (Desktop): {os.path.abspath(DIST_DIR)}")
    print(f"  Output directory (Docs Dist): {os.path.abspath(DOCS_DIST_DIR)}")
    print(f"  Output directory (Webfont): {os.path.abspath(DOCS_FONTS_DIR)}")
    print("==================================================")


if __name__ == "__main__":
    main()
