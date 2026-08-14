# ZMK Keyboard for Cornix（日本語）

**現在の Cornix board revision:** `3.0.0`

> [!IMPORTANT]
> この日本語 README は AI により生成されたものです。開発者は日本語に詳しくないため、
> 表現や用語に不自然な点がある可能性があります。正確な内容は英語版
> [`README.md`](./README.md) を優先してください。

## Zephyr 4.1 / ZMK main へのアップグレード注意

このモジュールは Zephyr 4.1 ベースの ZMK `main` ブランチを対象にしています。
既存の `zmk-config` からこのモジュールを利用する場合は、まず west manifest 側で
ZMK `main`、または Zephyr 4.1 対応済みの ZMK revision を使っていることを確認してください。

Zephyr 4.1 では ZMK 用の修飾付き board target 構文が導入されています。
新しいビルド設定では、次の `board//zmk` 形式を推奨します。

- `cornix_left//zmk`
- `cornix_right//zmk`
- `cornix_ph_left//zmk`
- `nice_nano//zmk`（dongle / reset ビルド用）

従来の非修飾 board 名も互換性のため残していますが、新しい設定では上記の修飾付き board 名を使ってください。

## Boards と Shields

このリポジトリは Cornix split keyboard 用の ZMK firmware board/shield モジュールです。

### Boards

- `cornix_left`: dongle を使わない構成の左手側 central board。
- `cornix_right`: split keyboard の右手側 peripheral board。
- `cornix_ph_left`: dongle 構成で使う左手側 peripheral board。

### Shields

- `cornix_dongle_adapter`: custom dongle 構成で使う matrix / Bluetooth 用 shield。
- `cornix_dongle_eyelash`: dongle board 側に `zephyr,display` が無い場合の display 用 shield 例。
- `cornix_indicator`: 各 side の 2 個の RGB LED で battery / connection status を表示する shield。3.0.0 では external-power idle timeout を 1000 ms に設定して待機時の消費電力を抑えますが、点灯中は追加の電力を消費します。

## DYA Studio サポート

テンプレート構成では DYA Studio 拡張を既定で有効にする想定です。
通常の ZMK Studio は RPC transport として有効のまま使います。

利用する west manifest には、次の DYA Studio 関連モジュールが必要です。

- `zmk-module-ble-management`
- `zmk-module-battery-history`
- `zmk-module-settings-rpc`
- `zmk-module-runtime-input-processor`

無効化したい場合は、利用者側の `.conf` または build `cmake-args` で必要な項目を `n` に上書きしてください。
代表例:

```conf
CONFIG_ZMK_RUNTIME_INPUT_PROCESSOR=n
CONFIG_ZMK_RUNTIME_INPUT_PROCESSOR_STUDIO_RPC=n
CONFIG_ZMK_BLE_MANAGEMENT=n
CONFIG_ZMK_BLE_MANAGEMENT_STUDIO_RPC=n
CONFIG_ZMK_BATTERY_HISTORY=n
CONFIG_ZMK_BATTERY_HISTORY_STUDIO_RPC=n
CONFIG_ZMK_SETTINGS_RPC=n
CONFIG_ZMK_SETTINGS_RPC_STUDIO=n
```

## SoftDevice なしの flash layout について

元の Cornix firmware は SoftDevice なしの flash layout を使っています。
そのため、このプロジェクトでは nRF52840 board に `nrf52840-nosd` snippet を使う構成を推奨します。

もし dongle に firmware を書き込んだ後、既存 firmware と組み合わせて動かない場合は、次のどちらかを試してください。

1. `bootloader/` 以下の restore UF2 を flash して SoftDevice layout を復元する。
2. `nrf52840-nosd` snippet 付きで firmware をビルドし、ZMK 側も SoftDevice なし layout に合わせる。

詳細は [`bootloader/README.md`](./bootloader/README.md) を参照してください。

## ビルド方法の概要

### GitHub Actions を使う簡単な方法

1. このリポジトリを fork / clone します。
2. `config/*.keymap` や `.conf` を必要に応じて編集します。
3. GitHub Actions の build workflow を実行します。
4. 生成された UF2 を各 board に flash します。

### 既存の zmk-config に追加する場合

既存の `zmk-config` の west manifest にこの module を追加し、`west update` を実行してください。
Zephyr 4.1 / ZMK main を使っていること、また `board//zmk` 形式の board target を使っていることを確認してください。

代表的な build target:

- dongle: `nice_nano//zmk` + `cornix_dongle_adapter cornix_dongle_eyelash dongle_display`
- left: `cornix_left//zmk`
- right: `cornix_right//zmk`
- dongle 用 left peripheral: `cornix_ph_left//zmk`

## RGB について

3.0.0 では、optional の `cornix_indicator` shield と `zmk-rgbled-widget` により、各 side の 2 個の RGB LED で battery status と split connection status を表示できます。

待機時の消費電力を抑えるため、shield は `CONFIG_RGBLED_WIDGET_EXT_POWER_TIMEOUT_MS=1000` を既定値にします。animation が終了し、常時点灯する indicator が無い状態から 1000 ms 後に WS2812 の external-power rail を off にします。この値は widget の 15000 ms default を上書きしますが、意図的に点灯中の LED は消灯しません。利用者側の `.conf` で上書きできます。

## 注意

この日本語版は概要と実用上重要な注意点をまとめたものです。
詳細な手順、manifest 例、build.yaml 例、dongle adapter の説明は英語版 [`README.md`](./README.md) を参照してください。
