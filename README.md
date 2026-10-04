# 正記體 (JhengJi Fonts) - Ideographic Tally Marks 正字計數符號字型

[![License: OFL-1.1](https://img.shields.io/badge/License-OFL_1.1-blue.svg)](https://scripts.sil.org/OFL)
[![Unicode](https://img.shields.io/badge/Unicode-11.0_SMP-green.svg)](https://unicode.org/charts/PDF/U1D360.pdf)
[![Font Size](https://img.shields.io/badge/WOFF2_Size-~1.2KB-orange.svg)]()

**正記體（JhengJi Fonts）** 是一套專門為「正字計數法」量身打造的極致輕量化開源字型。本專案將思源宋體（Noto Serif TC）的 7 種字重與全字庫正楷體（TW-Kai），精確解構為「正」字一至五劃的演進筆順，並完整支援 Unicode 算籌與計數標準區塊（Counting Rod Numerals）。

---

## 🌟 核心特色

1. **雙模無縫輸入**：
   - **鍵盤數字輸入**：在套用本字型的區域，直接鍵入鍵盤數字 `1`、`2`、`3`、`4`、`5`，即可立即渲染出正字的第一筆至第五筆！
   - **Unicode 標準字符**：完整支援 Unicode 11.0 收錄之 Ideographic Tally Marks 碼位（`U+1D372` ～ `U+1D376`），並保留原漢字 `正`（`U+6B63`）。
2. **極致輕量化（~1.2 KB）**：
   - 清除了原字型中數萬個無關字符，僅保留計數所需的核心符號，單個 WOFF2 網頁字型僅約 1.1 ～ 1.3 KB，桌面 OTF/TTF 僅約 2 ～ 4 KB，秒開零延遲。
3. **豐富風格與字重**：
   - **正記體-宋體 (JhengJi Song)**：涵蓋 7 種完整字重（極細 ExtraLight、細體 Light、常規 Regular、中黑 Medium、半粗 SemiBold、粗體 Bold、特黑 Black）。
   - **正記體-楷體 (JhengJi Kai)**：提供傳統毛筆楷書筆韻的常規體（Regular）。
4. **乾淨的字型元數據**：
   - 完整重構 `name`、`OS/2` 與 `CFF` 資訊表格，命名為獨立字族「正記體-宋體」與「正記體-楷體」，安裝於 Windows、macOS 或 Linux 時不會與思源宋體或全字庫正楷體產生任何識別或快取衝突。

---

## 📊 字符編碼對照表

| 筆劃序 | 筆劃名稱 | 鍵盤快捷鍵 | Unicode 碼位 | Unicode 字符 | 宋體預覽 | 楷體預覽 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 首橫 | `1` | `U+1D372` | 𝍲 | 一 | 一 |
| **2** | 首橫 + 中豎 | `2` | `U+1D373` | 𝍳 | 丅 | 丅 |
| **3** | 首橫 + 中豎 + 中橫 | `3` | `U+1D374` | 𝍴 | 丅+短橫 | 丅+短橫 |
| **4** | 首橫 + 中豎 + 中橫 + 左豎 | `4` | `U+1D375` | 𝍵 | 四畫未封底 | 四畫未封底 |
| **5** | 完整「正」字（加底橫） | `5` 或 `正` | `U+1D376` / `U+6B63` | 𝍶 / 正 | 正 | 正 |

---

## 💻 網頁使用方式 (Webfont CSS)

### 1. 引入字型
```css
@font-face {
  font-family: 'JhengJi Song';
  src: url('fonts/JhengJiSong-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'JhengJi Kai';
  src: url('fonts/JhengJiKai-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

/* 應用至正字計數類別 */
.tally {
  font-family: 'JhengJi Song', serif;
  font-size: 28px;
}

.tally-kai {
  font-family: 'JhengJi Kai', cursive;
  font-size: 28px;
}
```

### 2. HTML 範例
```html
<!-- 鍵盤直接輸入數字 1~5 -->
<p>開票統計結果：<span class="tally">5553</span> (共 18 票)</p>

<!-- 亦可使用標準 Unicode 字符 -->
<p>Unicode 符號：<span class="tally">𝍲 𝍳 𝍴 𝍵 𝍶</span></p>

<!-- 混合漢字 '正' -->
<p>漢字正：<span class="tally">正正正3</span></p>
```

---

## 🛠️ 開發與建置

### 依賴環境
- Python 3.9+
- `fonttools`、`brotli`

```bash
pip install -r requirements.txt
```

### 重新建置全部字型
```bash
python scripts/build_fonts.py
```

### 執行完整性驗證測試
```bash
python scripts/verify_fonts.py
```

### FontForge 專用腳本
若在安裝有 FontForge 的環境下，亦可使用 FontForge Python 腳本：
```bash
fontforge -script scripts/build_with_fontforge.py
```

---

## 📁 專案目錄結構

```text
├── input/                      # 原始字型 (思源宋體 7 字重 + 全字庫正楷體)
├── dist/                       # 產出的桌面字型 (OTF / TTF)
├── docs/                       # GitHub Pages 展示網站
│   ├── index.html              # 互動展示網站首頁
│   ├── style.css               # 網站樣式
│   ├── app.js                  # 互動預覽與正字計數器腳本
│   ├── dist/                   # 桌面字型下載鏡像
│   └── fonts/                  # 產出的網頁字型 (WOFF2)
├── scripts/                    # 建置與驗證腳本
│   ├── build_fonts.py          # Python + fontTools 主建置程式
│   ├── build_with_fontforge.py # FontForge 專用腳本
│   └── verify_fonts.py         # 字型驗證測試套件
├── requirements.txt            # Python 依賴清單
├── LICENSE                     # SIL Open Font License 1.1
└── README.md                   # 專案說明文檔
```

---

## 🤝 推薦相關開源字型

若您需要更多計數風格或西式五槓劃記符號，特別推薦以下優秀專案：
1. **[Huahua画划 - 计数符号字体 / Tally Mark Font](https://github.com/hshsilver/Huahua-Tally-Marks-Font)**  
   支援多國計數符號（正字計數、西方劃線、方格斜線等）的專用開源字型。
2. **[Google Noto Sans Symbols 2](https://fonts.google.com/noto/specimen/Noto+Sans+Symbols+2)**  
   Google 官方收錄完整 Unicode 算籌與計數符號區塊的通用符號字體。

---

## 📄 授權條款 (License)

本專案衍生自 Adobe / Google 的思源宋體（Source Han Serif / Noto Serif CJK）與全字庫正楷體，遵循 [SIL Open Font License 1.1 (OFL-1.1)](LICENSE) 開源授權協議發布。任何人皆可自由免費使用、客製與散布。
