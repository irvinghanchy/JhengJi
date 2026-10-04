#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verification Script for JhengJi Fonts
Verifies character maps, glyph outlines, name tables, metrics, and formats.
"""

import os
import glob
from fontTools.ttLib import TTFont

DIST_DIR = "dist"
DOCS_FONTS_DIR = os.path.join("docs", "fonts")

REQUIRED_CODEPOINTS = [
    0x0020,  # space
    0x0031, 0x0032, 0x0033, 0x0034, 0x0035,  # '1'..'5'
    0x1D372, 0x1D373, 0x1D374, 0x1D375, 0x1D376,  # Tally marks 1..5
    0x6B63   # '正'
]

FORBIDDEN_KEYWORDS = ["noto", "source han", "思源", "tw-kai", "全字庫", "cns11643"]


def verify_font_file(path):
    print(f"\nVerifying: {os.path.basename(path)}")
    font = TTFont(path)
    
    # 1. Check cmap
    cmap = font.getBestCmap()
    assert cmap is not None, "Cmap table missing or empty!"
    
    for cp in REQUIRED_CODEPOINTS:
        assert cp in cmap, f"Required codepoint {hex(cp)} missing from cmap!"
    
    # Check that cmap only contains allowed codepoints
    allowed = set(REQUIRED_CODEPOINTS)
    extra = set(cmap.keys()) - allowed
    if extra:
        print(f"  [WARN] Extra codepoints in cmap: {[hex(c) for c in extra]}")
    else:
        print(f"  [OK] Cmap has exactly the required {len(cmap)} codepoints.")

    # Check 1..5 map to same glyph as 1D372..1D376
    for i in range(5):
        d = 0x0031 + i
        t = 0x1D372 + i
        assert cmap[d] == cmap[t], f"Mismatch between {hex(d)} and {hex(t)}: {cmap[d]} != {cmap[t]}"
    print("  [OK] Digits 1-5 correctly map to tally marks 1-5 glyphs.")

    # Check 6B63 maps to same glyph as 5 / 1D376
    assert cmap[0x6B63] == cmap[0x1D376], f"'正' (0x6B63) does not map to tally 5 ({cmap[0x6B63]} != {cmap[0x1D376]})"
    print("  [OK] '正' (0x6B63) maps to tally mark 5.")

    # 2. Check name table
    name_table = font['name']
    all_name_strings = []
    family_en = ""
    family_zh = ""
    for r in name_table.names:
        u_str = r.toUnicode()
        all_name_strings.append(u_str.lower())
        if r.nameID == 1 and r.platformID == 3:
            if r.langID == 0x0409: family_en = u_str
            elif r.langID == 0x0404: family_zh = u_str

    print(f"  [OK] Family EN: '{family_en}', Family ZH: '{family_zh}'")
    assert "jhengji" in family_en.lower(), f"Unexpected English family name: {family_en}"
    assert "正記體" in family_zh, f"Unexpected Chinese family name: {family_zh}"

    for s in all_name_strings:
        for kw in FORBIDDEN_KEYWORDS:
            assert kw not in s, f"Found legacy keyword '{kw}' in name record: {s}"
    print("  [OK] No legacy identifiers found in name table.")

    # 3. Check outline drawing & metrics
    glyph_set = font.getGlyphSet()
    for gname in glyph_set.keys():
        from fontTools.pens.recordingPen import RecordingPen
        pen = RecordingPen()
        glyph_set[gname].draw(pen)
    print(f"  [OK] All {len(glyph_set)} glyphs draw without errors.")

    # 4. Check metrics and centering
    if 'glyf' in font:
        # TrueType (Kai)
        for i in range(5):
            d = 0x31 + i
            gname = cmap[d]
            g = font['glyf'][gname]
            adv, lsb = font['hmtx'][gname]
            assert lsb == g.xMin, f"Kai {d} lsb ({lsb}) != xMin ({g.xMin})!"
            center = (g.xMin + g.xMax) / 2
            assert abs(center - adv / 2) <= 1.5, f"Kai {d} center ({center}) not centered in {adv}!"
        print("  [OK] Kai strokes are correctly centered and hmtx lsb matches glyf xMin.")
    elif 'CFF ' in font:
        # CFF (Song)
        cff = font['CFF '].cff[0]
        for i in range(5):
            d = 0x31 + i
            gname = cmap[d]
            cs = cff.CharStrings[gname]
            cs.decompile()
            nom = cs.private.nominalWidthX
            defw = cs.private.defaultWidthX
            first = cs.program[0] if isinstance(cs.program[0], (int, float)) else None
            decoded = (nom + first) if first is not None else defw
            adv, lsb = font['hmtx'][gname]
            assert decoded == 1000, f"Song {d} decoded CFF width ({decoded}) != 1000!"
            assert adv == 1000, f"Song {d} hmtx advance ({adv}) != 1000!"
        print("  [OK] Song advance and CFF decoded widths are exactly 1000.")


def main():
    print("==================================================")
    print("  Starting JhengJi Font Verification Suite")
    print("==================================================")

    dist_fonts = sorted(glob.glob(os.path.join(DIST_DIR, "*.*")))
    woff2_fonts = sorted(glob.glob(os.path.join(DOCS_FONTS_DIR, "*.woff2")))

    assert len(dist_fonts) == 8, f"Expected 8 dist fonts, found {len(dist_fonts)}"
    assert len(woff2_fonts) == 8, f"Expected 8 woff2 fonts, found {len(woff2_fonts)}"

    for f in dist_fonts:
        verify_font_file(f)

    for f in woff2_fonts:
        verify_font_file(f)

    print("\n==================================================")
    print("  ALL VERIFICATION TESTS PASSED SUCCESSFULLY!  ")
    print("==================================================")


if __name__ == "__main__":
    main()
