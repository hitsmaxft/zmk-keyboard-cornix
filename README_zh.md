# ZMK Keyboard Cornix

用于 Cornix 分体式人体工学键盘的 ZMK 开发板与扩展板模块。

[在线文档：English / 简体中文](http://gh.bhee.online/zmk-keyboard-cornix/) ·
[English README](./README.md) ·
[日本語 README（AI 生成）](./README_jp.md)

**当前板卡版本：** [`v3.0.0`](https://github.com/hitsmaxft/zmk-keyboard-cornix/releases/tag/v3.0.0)

**ZMK 基线：** 基于 Zephyr 4.1 的 `main`

![带 dongle 的 Cornix](images/cornix_with_dongle.png)

## 项目内容

- `cornix_left//zmk`：标准分体构建的左半侧
- `cornix_right//zmk`：右侧外围设备
- `cornix_ph_left//zmk`：dongle 构建的左侧外围设备
- `cornix_dongle_adapter`：中央 dongle 的矩阵与蓝牙角色
- `cornix_dongle_eyelash`：可选的显示硬件 overlay
- `cornix_indicator`：已可用于生产的 RGB 电量与连接状态指示

Cornix 采用紧凑的 3×6 列交错布局，每侧有三个拇指键。硬件支持 USB-C、
蓝牙、Kailh Choc V2 热插拔轴座，以及 10°、18°、25° 三档帐篷角度。

## Zephyr 4.1 要求

必须使用 `nice_nano//zmk` 等带限定符的 ZMK 板名。未限定的 `nice_nano`
可能选中 `CONFIG_SETTINGS_NONE=y`，导致重启后丢失蓝牙身份并破坏已有分体绑定。

每次构建 nice!nano dongle 或 reset 固件后，须检查最终 `.config` 含有：

```text
CONFIG_NVS=y
CONFIG_SETTINGS_NVS=y
```

且不得含有 `CONFIG_SETTINGS_NONE=y`。

## 构建目标

标准分体：

```yaml
include:
  - board: cornix_left//zmk
    artifact-name: cornix_left

  - board: cornix_right//zmk
    artifact-name: cornix_right

  - board: cornix_right//zmk
    shield: settings_reset
    artifact-name: cornix_reset
```

Dongle 集成：

```yaml
include:
  - board: nice_nano//zmk
    shield: cornix_dongle_adapter cornix_dongle_eyelash dongle_display
    snippet: studio-rpc-usb-uart
    artifact-name: cornix_dongle

  - board: cornix_ph_left//zmk
    artifact-name: cornix_left_for_dongle

  - board: cornix_right//zmk
    artifact-name: cornix_right

  - board: nice_nano//zmk
    shield: settings_reset
    artifact-name: dongle_reset
```

仅当 dongle 开发板尚未提供 `zephyr,display` 时，方需加入
`cornix_dongle_eyelash`；`dongle_display` 模块负责提供显示组件。

## RGB 指示灯

3.0.0 已使可选的 `cornix_indicator` shield 达到生产可用状态。它通过
`zmk-rgbled-widget` 显示电量及分体连接状态。

该 shield 设置 `CONFIG_RGBLED_WIDGET_EXT_POWER_TIMEOUT_MS=1000`。动画结束且无
常亮指示后，WS2812 外部供电将在 1000 ms 后关闭，以降低空闲功耗；持续点亮的
LED 仍会耗电。RGB 须主动启用，默认 v3.0.0 发布包并未开启。

## 刷写与恢复

1. 若需清除绑定，为涉及的每个角色刷入对应的 settings-reset UF2。
2. 将左、右及可选 dongle UF2 分别刷入对应设备。
3. 同时复位两侧，再由主机重新连接。

Cornix 自 v2.3 起使用无 SoftDevice 的闪存布局。若使用旧固件、需兼容原厂 RMK，
或设备已无法进入 UF2 模式，请依[引导程序恢复指南](./bootloader/README.md)处理。
切勿在未重置相关设备时混用固件角色或闪存布局。

## 文档与支持

- [中文安装指南](http://gh.bhee.online/zmk-keyboard-cornix/zh/)
- [English installation guide](http://gh.bhee.online/zmk-keyboard-cornix/en/)
- [ZMK 官方文档](https://zmk.dev/docs/)
- [问题追踪](https://github.com/hitsmaxft/zmk-keyboard-cornix/issues)
- [RMK 固件项目](https://rmk.rs/)
