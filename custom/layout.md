<!-- markdownlint-disable MD033 -->

# Cornix LP キーボードレイアウト仕様書 (Layout Specification)

[Cornix LP](https://jezailfunder.jp/products/cornix-lp-keyboard) は、40%配列のロープロファイル分割型キーボードです。  
本ドキュメントは、Cornix LP における全レイヤー (Layer 0〜10) のキーマップ論理仕様および運指設計をまとめた公式リファレンスです。

---

## 1. 全体構造

### 物理配列の特徴

- **キー数**:
  - 48キー + 左右ロータリーエンコーダー (回転 ＆ 押し込み)
- **列構成**:
  - 外側3列 (外端列・小指列・中指列) は4段、内側3列 (薬指列・人指列・中央列) は3段
- **親指キー**:
  - 左右各3キー (外側・中央・内側)

### 凡例 (Explanatory Notes)

- `[none]`: 何も送信しない無効なキー（空欄と同様）。
- `MO(n)`: キーを押している間（ホールド中）のみ一時的に Layer n を有効化する（モメンタリ動作）。
- `TO(n)`: Layer n に切り替えてそのまま固定する（レイヤー移動・復帰）。
- 文字・記号キーは下記表の表記ルールに従い Shift による出力文字の変更を行う。
- 文字・記号以外のキーは Shift 付与を表記せず、状態に合わせた Shift 付与を実施する。
  - 対象キーは以下の通り
    - **カーソル・移動**: 矢印 (← / → / ↑ / ↓), Home, End, Page Up, Page Down
    - **編集・基本制御**: Enter, Space, Tab, Esc, Bspc, Del, Insert, Menu
    - **ファンクション**: F1 〜 F12
    - **特殊・ロック**: PrintScreen, Pause, ScrollLock, CapsLock
    - **ロータリーエンコーダー**: 音量 (アップ / ダウン / ミュート), 明るさ (アップ / ダウン), スクロール (水平 / 垂直)

|表記|単押し|Shift + 単押し|長押し|Shift + 長押し|
|:-:|:-:|:-:|:-:|:-:|
|0|0|0|0|0|
|k <strong>K</strong>|k|K|k|K|
|6 <strong>&</strong>|6|&|6|&|
|←|←|Shift + ←|←|Shift + ←|
|Shift + ↓|Shift + ↓|Shift + ↓|Shift + ↓|Shift + ↓|
|t <strong>T</strong><br><ins>L-Shift</ins>|t|T|L-Shift|Shift + L-Shift|
|4 <br><ins>R-Ctrl</ins>|4|4|R-Ctrl|Shift + R-Ctrl|
|<ins>L-Alt</ins>|\[none]|\[none]|L-Alt|Shift + L-Alt|
||\[none]|\[none]|\[none]|\[none]|

---

### キー番号定義

このファイル上でキーを一意に指定するための番号定義。  

| 左端 | 左小指 | 左薬指 | 左中指 | 左人指 | 左中央 | ギャップ | 右中央 | 右人指 | 右中指 | 右薬指 | 右小指 | 右端 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|L16|L15|L14|L13|L12|L11|❌|R11|R12|R13|R14|R15|R16|
|L26|L25|L24|L23|L22|L21|❌|R21|R22|R23|R24|R25|R26|
|L36|L35|L34|L33|L32|L31|❌|R31|R32|R33|R34|R35|R36|
|L43|L42|L41|❌|❌|❌|❌|❌|❌|❌|R41|R42|R43|
|❌|❌|❌|LT3|LT2|LT1|❌|RT1|RT2|RT3|❌|❌|❌|

---

### レイヤー構成 (Layer Map)

| レイヤー | 名称 | 主な役割 | 主な遷移先 |
|:-:|:--|:--|:--|
| **Layer 0** | **Latin** | ラテン面 | Symbols / Neovim / Naginata / Left-Navigation / Right-Navigation / Mod-Latin |
| **Layer 1** | **Symbols** | 記号面 | Latin / Neovim / Naginata / Mod-Symbols |
| **Layer 2** | **Neovim** | Neovim移動面 | Latin / Symbols |
| **Layer 3** | **Naginata** | 薙刀式基本面 | Latin / Naginata-Ext / Naginata-Symbols / Left-Navigation / Right-Navigation / Mod-Latin |
| **Layer 4** | **Naginata-Ext** | 薙刀式補完面 | Naginata / Mod-Latin |
| **Layer 5** | **Naginata-Symbols** | 薙刀式記号面 | Latin / Naginata / Mod-Symbols |
| **Layer 6** | **Left-Navigation** | 左手ナビゲーション面 | Latin / Naginata / System |
| **Layer 7** | **Right-Navigation** | 右手ナビゲーション面 | Latin / Naginata / System |
| **Layer 8** | **System** | システム管理面 | Latin / Naginata |
| **Layer 9** | **Mod-Latin** | 修飾キーラテン面 | Latin / Naginata / Mod-Symbols |
| **Layer 10** | **Mod-Symbols** | 修飾キー記号面 | Symbols / Naginata-Symbols |

---

## 2. 各レイヤー詳細

### ロータリーエンコーダー (ダイアル)

| レイヤー | 左ダイアル: 反時計回り | 左ダイアル: 押し込み | 左ダイアル: 時計回り | 右ダイアル: 反時計回り | 右ダイアル: 押し込み | 右ダイアル: 時計回り |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|
| **ナビゲーション面 (Layer 6, 7)** | 水平スクロール (左) | 無反応 | 水平スクロール (右) | 垂直スクロール (上) | 無反応 | 垂直スクロール (下) |
| **上記以外 (Layer 0〜5, 8〜10)** | 音量ダウン | ミュート / 解除 | 音量アップ | 明るさダウン | 画面ロック (Gui + L) | 明るさアップ |

---

### Layer 0: Latin (ラテン面)

[Graphite](https://github.com/rdavison/graphite-layout)配列をベースに設定。

From:

- 初期状態
- **Layer 3: Naginata (薙刀式基本面)**
  - LT1 (Enter) + R16 または RT1 (Enter) + R16 -> `TO(0)`
- **Layer 5: Naginata-Symbols (薙刀式記号面)**
  - R16 -> `TO(0)`
- **Layer 6: Left-Navigation (左手ナビゲーション面)**
  - R16 -> `TO(0)`
- **Layer 7: Right-Navigation (右手ナビゲーション面)**
  - R16 -> `TO(0)`
- **Layer 8: System (システム管理面)**
  - R16 または L41 -> `TO(0)`

| 左端 | 左小指 | 左薬指 | 左中指 | 左人指 | 左中央 | ギャップ | 右中央 | 右人指 | 右中指 | 右薬指 | 右小指 | 右端 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
||b <strong>B</strong>|l <strong>L</strong>|d <strong>D</strong>|w <strong>W</strong>|z <strong>Z</strong>|❌|, <strong>!</strong>|f <strong>F</strong>|o <strong>O</strong>|u <strong>U</strong>|j <strong>J</strong>||
|` <strong>~</strong>|n <strong>N</strong>|r <strong>R</strong>|t <strong>T</strong>|s <strong>S</strong>|g <strong>G</strong>|❌|y <strong>Y</strong>|h <strong>H</strong>|a <strong>A</strong>|e <strong>E</strong>|i <strong>I</strong>|' <strong>"</strong>|
|L-Ctrl + MO(9)*|q <strong>Q</strong>|x <strong>X</strong>|p <strong>P</strong>|c <strong>C</strong>|v <strong>V</strong>|❌|k <strong>K</strong>|m <strong>M</strong>|. <strong>?</strong>|- <strong>_</strong>|/ <strong>\\</strong>|R-Ctrl + MO(9)*|
|L-Alt + MO(9)*|L-Gui + MO(9)*|Tab|❌|❌|❌|❌|❌|❌|❌|Esc|Menu|R-Alt + MO(9)*|
|❌|❌|❌|Del|Space<br><ins>L-Shift</ins>|Enter<br><ins>MO(1)</ins>|❌|Enter<br><ins>MO(1)</ins>|Space<br><ins>R-Shift</ins>|Bspc|❌|❌|❌|

- L36 (`L-Ctrl + MO(9)*`) または R36 (`R-Ctrl + MO(9)*`)
  - L-Ctrl または R-Ctrl をホールド状態で `MO(9)` **Layer 9: Mod-Latin (修飾キーラテン面)**
- L43 (`L-Alt + MO(9)*`) または R43 (`R-Alt + MO(9)*`)
  - L-Alt または R-Alt をホールド状態で `MO(9)` **Layer 9: Mod-Latin (修飾キーラテン面)**
- L42 (`L-Gui + MO(9)*`)
  - L-Gui をホールド状態で `MO(9)` **Layer 9: Mod-Latin (修飾キーラテン面)**

Combos:

- L23 (t) + L22 (s) + LT1 (Enter)
  - `MO(2)` **Layer 2: Neovim (Neovim移動面)**
- LT1 (Enter) + L16 または RT1 (Enter) + L16
  - `` Alt + ` `` 送信後 `TO(3)` **Layer 3: Naginata (薙刀式基本面)**
- LT1 (Enter) + R16 または RT1 (Enter) + R16
  - `` Alt + ` ``
- L34 (x) + L33 (p) + L32 (c)
  - `MO(6)` **Layer 6: Left-Navigation (左手ナビゲーション面)**
- R32 (m) + R33 (.) + R34 (-)
  - `MO(7)` **Layer 7: Right-Navigation (右手ナビゲーション面)**

---

### Layer 1: Symbols (記号面)

From:

- **Layer 0: Latin (ラテン面)**
  - LT1 (Enter) または RT1 (Enter) -> `MO(1)`

| 左端 | 左小指 | 左薬指 | 左中指 | 左人指 | 左中央 | ギャップ | 右中央 | 右人指 | 右中指 | 右薬指 | 右小指 | 右端 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|TO(3)*|\{|\}|\[|\]|\^|❌|%|#|<|>|\$|Alt + `|
||;|\||\&|0|:|❌|@|1|\(|\)|=||
|L-Ctrl + MO(10)*|6|7|8|9|+|❌|\*|2|3|4|5|R-Ctrl + MO(10)*|
|L-Alt + MO(10)*|L-Gui + MO(10)*|Tab|❌|❌|❌|❌|❌|❌|❌|Esc|Menu|R-Alt + MO(10)*|
|❌|❌|❌|Bspc|Space<br><ins>L-Shift</ins>|Enter|❌|Enter|Space<br><ins>R-Shift</ins>|Del|❌|❌|❌|

- L36 (`L-Ctrl + MO(10)*`) または R36 (`R-Ctrl + MO(10)*`)
  - L-Ctrl または R-Ctrl をホールド状態で `MO(10)` **Layer 10: Mod-Symbols (修飾キー記号面)**
- L43 (`L-Alt + MO(10)*`) または R43 (`R-Alt + MO(10)*`)
  - L-Alt または R-Alt をホールド状態で `MO(10)` **Layer 10: Mod-Symbols (修飾キー記号面)**
- L42 (`L-Gui + MO(10)*`)
  - L-Gui をホールド状態で `MO(10)` **Layer 10: Mod-Symbols (修飾キー記号面)**
- L16 (`TO(3)*`)
  - `` Alt + ` `` 送信後 `TO(3)` **Layer 3: Naginata (薙刀式基本面)**

Combos:

- L23 (&) + L22 (0)
  - `MO(2)` **Layer 2: Neovim (Neovim移動面)**

---

### Layer 2: Neovim (Neovim移動面)

From:

- **Layer 0: Latin (ラテン面)**
  - L23 (t) + L22 (s) + LT1 (Enter) -> `MO(2)`
- **Layer 1: Symbols (記号面)**
  - L23 (&) + L22 (0) -> `MO(2)`

| 左端 | 左小指 | 左薬指 | 左中指 | 左人指 | 左中央 | ギャップ | 右中央 | 右人指 | 右中指 | 右薬指 | 右小指 | 右端 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|||||||❌|b||e|w|H||
|||||||❌|h|j|k|l|M||
|||||||❌|0|||$|L||
||||❌|❌|❌|❌|❌|❌|❌|Esc|||
|❌|❌|❌||||❌||||❌|❌|❌|

---

### Layer 3: Naginata (薙刀式基本面)

[薙刀式配列 v18](https://oookaworks.seesaa.net/article/521080503.html)をベースに設定。

From:

- **Layer 0: Latin (ラテン面)**
  - LT1 (Enter) + L16 または RT1 (Enter) + L16 -> `TO(3)`
- **Layer 1: Symbols (記号面)**
  - L16 -> `TO(3)`
- **Layer 6: Left-Navigation (左手ナビゲーション面)**
  - L16 -> `TO(3)`
- **Layer 7: Right-Navigation (右手ナビゲーション面)**
  - L16 -> `TO(3)`
- **Layer 8: System (システム管理面)**
  - L16 または R41 -> `TO(3)`

| 左端 | 左小指 | 左薬指 | 左中指 | 左人指 | 左中央 | ギャップ | 右中央 | 右人指 | 右中指 | 右薬指 | 右小指 | 右端 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|||き|て|し|←|❌|→|さ|る|す|へ||
||ろ|け|と|か|っ|❌|く|あ|い|う|ー||
|L-Ctrl + MO(9)*|ほ|ひ|は|こ|そ|❌|た|な|ん|ら|れ|R-Ctrl + MO(9)*|
|L-Alt + MO(9)*|L-Gui + MO(9)*|Tab|❌|❌|❌|❌|❌|❌|❌|Esc|Menu|R-Alt + MO(9)*|
|❌|❌|❌|Del|Space<br><ins>MO(4)</ins>|Enter<br><ins>MO(5)</ins>|❌|Enter<br><ins>MO(5)</ins>|Space<br><ins>MO(4)</ins>|Bspc|❌|❌|❌|

- L36 (`L-Ctrl + MO(9)*`) または R36 (`R-Ctrl + MO(9)*`)
  - L-Ctrl または R-Ctrl をホールド状態で `MO(9)` **Layer 9: Mod-Latin (修飾キーラテン面)**
- L43 (`L-Alt + MO(9)*`) または R43 (`R-Alt + MO(9)*`)
  - L-Alt または R-Alt をホールド状態で `MO(9)` **Layer 9: Mod-Latin (修飾キーラテン面)**
- L42 (`L-Gui + MO(9)*`)
  - L-Gui をホールド状態で `MO(9)` **Layer 9: Mod-Latin (修飾キーラテン面)**

Combos:

- LT1 (Enter) + L16 または RT1 (Enter) + L16
  - `` Alt + ` ``
- LT1 (Enter) + R16 または RT1 (Enter) + R16
  - `` Alt + ` `` 送信後 `TO(0)` **Layer 0: Latin (ラテン面)**
- L34 (ひ) + L33 (は) + L32 (こ)
  - `MO(6)` **Layer 6: Left-Navigation (左手ナビゲーション面)**
- R32 (な) + R33 (ん) + R34 (ら)
  - `MO(7)` **Layer 7: Right-Navigation (右手ナビゲーション面)**
- 濁音・半濁音・拗音などの同時押しコンボ仕様は [naginata_combos.md](./naginata_combos.md) を参照。

---

### Layer 4: Naginata-Ext (薙刀式補完面)

From:

- **Layer 3: Naginata (薙刀式基本面)**
  - LT2 (Space) または RT2 (Space) -> `MO(4)`

| 左端 | 左小指 | 左薬指 | 左中指 | 左人指 | 左中央 | ギャップ | 右中央 | 右人指 | 右中指 | 右薬指 | 右小指 | 右端 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|||ね|り|め|Shift + ←|❌|Shift + →|さ|よ|え|ゆ||
||せ|み|に|ま|ち|❌|や|の|も|つ|ふ||
|Shift + L-Ctrl + MO(9)*|ほ|ひ|を|、|ぬ|❌|お|。|む|わ|れ|Shift + R-Ctrl + MO(9)*|
|Shift + L-Alt + MO(9)*|Shift + L-Gui + MO(9)*|Shift + Tab|❌|❌|❌|❌|❌|❌|❌|Shift + Esc|Shift + Menu|Shift + R-Alt + MO(9)*|
|❌|❌|❌|Shift + Del|Shift + Space|Shift + Enter<br><ins>MO(5)</ins>|❌|Shift + Enter<br><ins>MO(5)</ins>|Shift + Space|Shift + Bspc|❌|❌|❌|

- L36 (`Shift + L-Ctrl + MO(9)*`) または R36 (`Shift + R-Ctrl + MO(9)*`)
  - Shift + L-Ctrl または Shift + R-Ctrl をホールド状態で `MO(9)` **Layer 9: Mod-Latin (修飾キーラテン面)**
- L43 (`Shift + L-Alt + MO(9)*`) または R43 (`Shift + R-Alt + MO(9)*`)
  - Shift + L-Alt または Shift + R-Alt をホールド状態で `MO(9)` **Layer 9: Mod-Latin (修飾キーラテン面)**
- L42 (`Shift + L-Gui + MO(9)*`)
  - Shift + L-Gui をホールド状態で `MO(9)` **Layer 9: Mod-Latin (修飾キーラテン面)**
- 濁音・半濁音・拗音などの同時押しコンボ仕様は [naginata_combos.md](./naginata_combos.md) を参照。

---

### Layer 5: Naginata-Symbols (薙刀式記号面)

From:

- **Layer 3: Naginata (薙刀式基本面)**
  - LT1 (Enter) または RT1 (Enter) -> `MO(5)`
- **Layer 4: Naginata-Ext (薙刀式補完面)**
  - LT1 (Enter) または RT1 (Enter) -> `MO(5)`

| 左端 | 左小指 | 左薬指 | 左中指 | 左人指 | 左中央 | ギャップ | 右中央 | 右人指 | 右中指 | 右薬指 | 右小指 | 右端 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|Alt + \`|（|）|『|』|↑|❌|↓|１|２|３|L-Gui + /|TO(0)*|
||「|」|？|・|L-Ctrl + c|❌|L-Ctrl + x|４|５|６|L-Ctrl + a||
|L-Ctrl + MO(10)*|＜|＞|！|〜|L-Ctrl + v|❌|０|７|８|９||R-Ctrl + MO(10)*|
|L-Alt + MO(10)*|L-Gui + MO(10)*|Tab|❌|❌|❌|❌|❌|❌|❌|Esc|Menu|R-Alt + MO(10)*|
|❌|❌|❌|Bspc|Space<br><ins>L-Shift</ins>|Enter|❌|Enter|Space<br><ins>R-Shift</ins>|Del|❌|❌|❌|

- L36 (`L-Ctrl + MO(10)*`) または R36 (`R-Ctrl + MO(10)*`)
  - L-Ctrl または R-Ctrl をホールド状態で `MO(10)` **Layer 10: Mod-Symbols (修飾キー記号面)**
- L43 (`L-Alt + MO(10)*`) または R43 (`R-Alt + MO(10)*`)
  - L-Alt または R-Alt をホールド状態で `MO(10)` **Layer 10: Mod-Symbols (修飾キー記号面)**
- L42 (`L-Gui + MO(10)*`)
  - L-Gui をホールド状態で `MO(10)` **Layer 10: Mod-Symbols (修飾キー記号面)**
- R16 (`TO(0)*`)
  - `` Alt + ` `` 送信後 `TO(0)` **Layer 0: Latin (ラテン面)**
- R12 (`Gui + /`)
  - Windows での再変換ショートカット

---

### Layer 6: Left-Navigation (左手ナビゲーション面)

From:

- **Layer 0: Latin (ラテン面)**
  - L34 (x) + L33 (p) + L32 (c) -> `MO(6)`
- **Layer 3: Naginata (薙刀式基本面)**
  - L34 (ひ) + L33 (は) + L32 (こ) -> `MO(6)`

| 左端 | 左小指 | 左薬指 | 左中指 | 左人指 | 左中央 | ギャップ | 右中央 | 右人指 | 右中指 | 右薬指 | 右小指 | 右端 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|TO(3)|F1|F2|F3|F4|F5|❌|PrintScreen|Home|↑|End|Page Up|TO(0)|
|Pause|F6|F7|F8|F9|F10|❌|CapsLock|←|↓|→|Page Down|R-Gui|
|L-Ctrl|F11||||F12|❌|ScrollLock|L-Shift||R-Shift|Insert|R-Ctrl|
|L-Alt|L-Gui|Tab|❌|❌|❌|❌|❌|❌|❌|Esc|Menu|R-Alt|
|❌|❌|❌|Del|Space<br><ins>L-Shift</ins>|TO(8)|❌|Enter|Space<br><ins>R-Shift</ins>|Bspc|❌|❌|❌|

---

### Layer 7: Right-Navigation (右手ナビゲーション面)

From:

- **Layer 0: Latin (ラテン面)**
  - R32 (m) + R33 (.) + R34 (-) -> `MO(7)`
- **Layer 3: Naginata (薙刀式基本面)**
  - R32 (な) + R33 (ん) + R34 (ら) -> `MO(7)`

| 左端 | 左小指 | 左薬指 | 左中指 | 左人指 | 左中央 | ギャップ | 右中央 | 右人指 | 右中指 | 右薬指 | 右小指 | 右端 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|TO(3)|F1|F2|F3|F4|F5|❌|PrintScreen|Home|↑|End|Page Up|TO(0)|
|Pause|F6|F7|F8|F9|F10|❌|CapsLock|←|↓|→|Page Down|R-Gui|
|L-Ctrl|F11|L-Shift||R-Shift|F12|❌|ScrollLock||||Insert|R-Ctrl|
|L-Alt|L-Gui|Tab|❌|❌|❌|❌|❌|❌|❌|Esc|Menu|R-Alt|
|❌|❌|❌|Del|Space<br><ins>L-Shift</ins>|Enter|❌|TO(8)|Space<br><ins>R-Shift</ins>|Bspc|❌|❌|❌|

---

### Layer 8: System (システム管理面)

From:

- **Layer 6: Left-Navigation (左手ナビゲーション面)**
  - LT1 -> `TO(8)`
- **Layer 7: Right-Navigation (右手ナビゲーション面)**
  - RT1 -> `TO(8)`

| 左端 | 左小指 | 左薬指 | 左中指 | 左人指 | 左中央 | ギャップ | 右中央 | 右人指 | 右中指 | 右薬指 | 右小指 | 右端 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|TO(3)||||||❌||||||TO(0)|
||Out USB|Out BLE|EP ON|EP OFF|Bootloader (L)|❌|Bootloader (R)|BT 1|BT 2|BT 3|BT Clear||
||||||Sys Reset (L)|❌|Sys Reset (R)||||||
|||TO(0)|❌|❌|❌|❌|❌|❌|❌|TO(3)|||
|❌|❌|❌||||❌||||❌|❌|❌|

- `Out USB`
  - USB 有線接続を出力優先に設定。
- `Out BLE`
  - Bluetooth 無線接続を出力優先に設定。
- `EP ON`
  - LED インジケーター等の外部給電を ON。
- `EP OFF`
  - LED インジケーター等の外部給電を OFF。
- `Bootloader (L) / (R)`
  - 左右それぞれを UF2 ファームウェア書き込みモードへ移行。
- `Sys Reset (L) / (R)`
  - 左右それぞれのマイコンをソフトウェア再起動。

---

### Layer 9: Mod-Latin (修飾キーラテン面)

From:

- **Layer 0: Latin (ラテン面)**
  - L36 (L-Ctrl) または R36 (R-Ctrl) -> `MO(9)`
  - L43 (L-Alt) または R43 (R-Alt) -> `MO(9)`
  - L42 (L-Gui) -> `MO(9)`
- **Layer 3: Naginata (薙刀式基本面)**
  - L36 (L-Ctrl) または R36 (R-Ctrl) -> `MO(9)`
  - L43 (L-Alt) または R43 (R-Alt) -> `MO(9)`
  - L42 (L-Gui) -> `MO(9)`
- **Layer 4: Naginata-Ext (薙刀式補完面)**
  - L36 (Shift + L-Ctrl) または R36 (Shift + R-Ctrl) -> `MO(9)`
  - L43 (Shift + L-Alt) または R43 (Shift + R-Alt) -> `MO(9)`
  - L42 (Shift + L-Gui) -> `MO(9)`

| 左端 | 左小指 | 左薬指 | 左中指 | 左人指 | 左中央 | ギャップ | 右中央 | 右人指 | 右中指 | 右薬指 | 右小指 | 右端 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
||b <strong>B</strong>|l <strong>L</strong>|d <strong>D</strong>|w <strong>W</strong>|z <strong>Z</strong>|❌|, <strong>!</strong>|f <strong>F</strong>|o <strong>O</strong>|u <strong>U</strong>|j <strong>J</strong>||
|` <strong>~</strong>|n <strong>N</strong>|r <strong>R</strong>|t <strong>T</strong>|s <strong>S</strong>|g <strong>G</strong>|❌|y <strong>Y</strong>|h <strong>H</strong>|a <strong>A</strong>|e <strong>E</strong>|i <strong>I</strong>|' <strong>"</strong>|
|L-Ctrl|q <strong>Q</strong>|x <strong>X</strong>|p <strong>P</strong>|c <strong>C</strong>|v <strong>V</strong>|❌|k <strong>K</strong>|m <strong>M</strong>|. <strong>?</strong>|- <strong>_</strong>|/ <strong>\\</strong>|R-Ctrl|
|L-Alt|L-Gui|Tab|❌|❌|❌|❌|❌|❌|❌|Esc|Menu|R-Alt|
|❌|❌|❌|Del|Space<br><ins>L-Shift</ins>|Enter<br><ins>MO(10)</ins>|❌|Enter<br><ins>MO(10)</ins>|Space<br><ins>R-Shift</ins>|Bspc|❌|❌|❌|

---

### Layer 10: Mod-Symbols (修飾キー記号面)

From:

- **Layer 1: Symbols (記号面)**
  - L36 (L-Ctrl) または R36 (R-Ctrl) -> `MO(10)`
  - L43 (L-Alt) または R43 (R-Alt) -> `MO(10)`
  - L42 (L-Gui) -> `MO(10)`
- **Layer 5: Naginata-Symbols (薙刀式記号面)**
  - L36 (L-Ctrl) または R36 (R-Ctrl) -> `MO(10)`
  - L43 (L-Alt) または R43 (R-Alt) -> `MO(10)`
  - L42 (L-Gui) -> `MO(10)`
- **Layer 9: Mod-Latin (修飾キーラテン面)**
  - LT1 (Enter) または RT1 (Enter) -> `MO(10)`

| 左端 | 左小指 | 左薬指 | 左中指 | 左人指 | 左中央 | ギャップ | 右中央 | 右人指 | 右中指 | 右薬指 | 右小指 | 右端 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
||\{|\}|\[|\]|\^|❌|%|#|<|>|\$||
||;|\||\&|0|:|❌|@|1|\(|\)|=||
|L-Ctrl|6|7|8|9|+|❌|\*|2|3|4|5|R-Ctrl|
|L-Alt|L-Gui|Tab|❌|❌|❌|❌|❌|❌|❌|Esc|Menu|R-Alt|
|❌|❌|❌|Bspc|Space<br><ins>L-Shift</ins>|Enter|❌|Enter|Space<br><ins>R-Shift</ins>|Del|❌|❌|❌|
