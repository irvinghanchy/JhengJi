#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
JhengJi Fonts Builder using FontForge Python API
(正記體 FontForge 建置腳本)

Usage:
    fontforge -script scripts/build_with_fontforge.py
"""

import os
import sys

try:
    import fontforge
except ImportError:
    print("[ERROR] FontForge Python module not found.")
    print("Please run this script using fontforge:")
    print("    fontforge -script scripts/build_with_fontforge.py")
    sys.exit(1)

INPUT_DIR = "input"
DIST_DIR = "dist"

NOTO_FONTS = [
    ("NotoSerifTC-ExtraLight.otf", "JhengJiSong-ExtraLight", "ExtraLight", "極細", 200),
    ("NotoSerifTC-Light.otf", "JhengJiSong-Light", "Light", "細體", 300),
    ("NotoSerifTC-Regular.otf", "JhengJiSong-Regular", "Regular", "常規", 400),
    ("NotoSerifTC-Medium.otf", "JhengJiSong-Medium", "Medium", "中黑", 500),
    ("NotoSerifTC-SemiBold.otf", "JhengJiSong-SemiBold", "SemiBold", "半粗", 600),
    ("NotoSerifTC-Bold.otf", "JhengJiSong-Bold", "Bold", "粗體", 700),
    ("NotoSerifTC-Black.otf", "JhengJiSong-Black", "Black", "特黑", 900),
]


def update_fontforge_metadata(font, ps_name, en_family, zh_family, en_subfamily, zh_subfamily, weight_class):
    font.fontname = ps_name
    font.familyname = en_family
    font.fullname = f"{en_family} {en_subfamily}"
    font.version = "1.000"
    font.copyright = "JhengJi Font Project (正記體)"
    font.os2_weight = weight_class
    font.os2_vendor = "JHJI"

    # Set English and Chinese names
    font.appendSFNTName("English (US)", "Family", en_family)
    font.appendSFNTName("English (US)", "SubFamily", en_subfamily)
    font.appendSFNTName("English (US)", "Fullname", f"{en_family} {en_subfamily}")
    font.appendSFNTName("English (US)", "PostScriptName", ps_name)
    font.appendSFNTName("English (US)", "Preferred Family", en_family)
    font.appendSFNTName("English (US)", "Preferred Styles", en_subfamily)

    font.appendSFNTName("Chinese (Taiwan)", "Family", zh_family)
    font.appendSFNTName("Chinese (Taiwan)", "SubFamily", zh_subfamily)
    font.appendSFNTName("Chinese (Taiwan)", "Fullname", f"{zh_family} {zh_subfamily}")
    font.appendSFNTName("Chinese (Taiwan)", "PostScriptName", ps_name)
    font.appendSFNTName("Chinese (Taiwan)", "Preferred Family", zh_family)
    font.appendSFNTName("Chinese (Taiwan)", "Preferred Styles", zh_subfamily)


def build_fontforge_noto(fname, ps_name, en_sub, zh_sub, weight):
    src_path = os.path.join(INPUT_DIR, fname)
    if not os.path.exists(src_path):
        print(f"Skipping {src_path}: file not found.")
        return

    print(f"Building {ps_name} from {fname} using FontForge...")
    font = fontforge.open(src_path)

    # 1. Select '正' (0x6B63)
    font.selection.select(0x6B63)
    font.copy()

    # 2. Invert selection and clear all other glyphs except space
    font.selection.all()
    font.selection.select(("less",), 0x0020)
    font.clear()

    # 3. Paste '正' into 0x35 (5) and 0x1D376 (Tally 5)
    font.selection.select(0x0035)
    font.paste()
    font.selection.select(0x1D376)
    font.paste()

    # 4. Set metadata
    update_fontforge_metadata(font, ps_name, "JhengJi Song", "正記體-宋體", en_sub, zh_sub, weight)

    out_path = os.path.join(DIST_DIR, f"{ps_name}.otf")
    font.generate(out_path)
    print(f"  -> Generated {out_path}")
    font.close()


def main():
    os.makedirs(DIST_DIR, exist_ok=True)
    for cfg in NOTO_FONTS:
        build_fontforge_noto(*cfg)


if __name__ == "__main__":
    main()
