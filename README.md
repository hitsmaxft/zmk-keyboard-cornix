# ZMK Keyboard for Cornix

[日本語版 README（AI-generated）](./README_jp.md)

**Current Cornix board revision:** `3.0.0`

> [!IMPORTANT]
> **Zephyr 4.1 / ZMK main upgrade note**
>
> This module targets the Zephyr 4.1-based ZMK main branch. If you are using this
> module from an existing `zmk-config`, make sure your west manifest follows ZMK
> `main` (or another Zephyr 4.1-compatible ZMK revision) before updating this
> module.
>
> Zephyr 4.1 also introduces the qualified ZMK board target syntax. Prefer the
> new `board//zmk` names for ZMK builds:
>
> - `cornix_left//zmk`
> - `cornix_right//zmk`
> - `cornix_ph_left//zmk`
> - `nice_nano//zmk` for dongle / reset builds
>
> Zephyr 4.1 no longer stores the argument to `sys_reboot()` in the nRF52
> `GPREGRET` register. Cornix boards therefore include ZMK's
> `nrf52840_uf2_boot_mode.dtsi`, which enables the retention boot-mode API and
> maps `&bootloader` to the Adafruit nRF52 UF2 magic value (`0x57`). Without
> this migration, invoking `&bootloader` only performs a normal reboot.
>
> The older unqualified names are kept for compatibility, but new build configs
> should use the qualified board names above.

### Pre-Zephyr 4.1 migration groundwork (2025-12-22 to 2025-12-23)

Three downstream configuration commits prepared the move to ZMK `main` before
the later Zephyr 4.1-specific fixes:

1. `2cb3502` (2025-12-22) changed the ZMK baseline from `v0.3.0` to `main`,
   moved `zmk-dongle-display` from `main` to `zephyr4`, moved this Cornix module
   from `dev` to `zephyr4`, and replaced every `nice_nano_v2` build target with
   `nice_nano`. It also disabled the then-incompatible RGB/status/GPIO/dongle
   screen, Tako, Snake, and Prospector modules.
2. `cc3ff97` (2025-12-23) adapted the Cornix eyelash SH1106 overlay to the new
   LVGL requirements by changing `width` from `129` to `128` and
   `segment-offset` from `1` to `2`.
3. `932da8f` (2025-12-23) applied `width = 128` and `segment-offset = 2` to
   `dongle_oled_sh1106.overlay`, then replaced the incorrectly selected Cornix
   eyelash shield on the Velvet dongle with `dongle_oled_sh1106`.

Together these commits moved ZMK `v0.3.0` to `main`, retired `nice_nano_v2`,
selected Zephyr 4-compatible module branches, adapted SH1106 geometry for the
new LVGL, and corrected the Velvet display overlay. They are migration
prerequisites, not proof that the later Zephyr 4.1 settings and bootloader
contracts were already correct.

### Zephyr 4.1 upgrade record: qualified board targets

The `nice_nano` qualifier is functionally significant under Zephyr 4.1. An
unqualified `board: nice_nano` selects the generic defconfig and may produce
`CONFIG_SETTINGS_NONE=y`. The firmware then creates a new Bluetooth identity on
every boot, cannot reuse stored split bonds, and ultimately fails SMP
authentication. A downstream `issues.md` recorded `pairing failed (peer reason
0x3)`, `No ID address. App must call settings_load()`, `Unable to store name`,
and `Failed to save Database Hash (err -2)`.

Downstream commit `91d0dd2` changed the Velvet dongle to `nice_nano//zmk` and
enabled all four DYA extensions: BLE Management, Battery History, Settings RPC,
and Runtime Input Processor. Commit `bb552ac` qualified the Cornix dongle,
`cornix_ph_left`, `cornix_left`, and `cornix_right` targets with `//zmk`.

Compilation alone is insufficient validation. After every Zephyr 4.1 board
migration, inspect `.build/{artifact}/zephyr/.config`: the nice!nano target must
be `nice_nano@2.0.0/nrf52840/zmk`, `CONFIG_NVS=y` and
`CONFIG_SETTINGS_NVS=y` must be present, and `CONFIG_SETTINGS_NONE=y` must not
be present. Use `nice_nano//zmk` for every Zephyr 4.1 nice!nano target.

## Introduction to Boards and Shields

This repository contains the ZMK firmware configuration for the Cornix split keyboard. Below is an explanation of the different boards and shields available in this project:

### Boards

The project includes three main board definitions:

- **`cornix_left`**: The left half of the Cornix split keyboard, used when building firmware without a dongle configuration.
- **`cornix_right`**: The right half of the Cornix split keyboard, used for the slave side in split keyboard setup.
- **`cornix_ph_left`**: Alternative left half board configuration, specifically designed for use with a dongle setup.

### Shields

The project includes several specialized shields that provide additional functionality:

- **`cornix_dongle_adapter`**: Provides common functionality for the matrix and Bluetooth functionality for dongle configurations. This shield is required when using the Cornix with a custom dongle.
- **`cornix_dongle_eyelash`**: An example shield for setting up display device for the dongle board. This is used when the board doesn't already have `zephyr,display` in the device tree.
- **`cornix_indicator`**: Enables the two RGB LEDs on each half for battery and connection status. Version 3.0.0 defaults its external-power idle timeout to 1000 ms to reduce idle power consumption; illuminated LEDs still consume additional power.

---

This community firmware has been tested with Cornix using ZMK and provides full split-role configuration, battery power management, and Bluetooth central/peripheral setup per ZMK split guidelines


![image](images/cornix_with_dongle.png)
![image](images/cornix_layout.png)

## warning：device breakdown recovery

the original cornix use flash layout without softdevice
so in the project. all board use nosd layout as default 

if you flash firmware into dongle and found it can't work with the original  firmware 
you have two solutions 

1. （recommend）flash the sd restore uf2 under boooader direcotry（its for nice nano 2 ，but i think it works for most of nrf52840 device） other boards https://github.com/hitsmaxft/Adafruit_nRF52_Bootloader/actions/runs/18398554358
2. build your firmware  with snippet  'nrf
52840-nosd', make zmk ignore soft device 


## TODO LIST

- [x] 52 keys full layout keymap, since v2.0
- [x] ec11 encoder, since v2.2
- [x] no-SD image, since v2.3
- [x] support various of dongles
- [x] upgrade to zephyr4.1 and lvgl9 , since v2.7, no dongle screen support yet
- [x] RGB battery and connection indicators via `cornix_indicator`, since v3.0.0


### about RGB

Version 3.0.0 supports the two RGB LEDs on each half through the optional
`cornix_indicator` shield and `zmk-rgbled-widget`. The indicators display
battery and split-connection status.

To reduce idle consumption, the shield sets
`CONFIG_RGBLED_WIDGET_EXT_POWER_TIMEOUT_MS=1000`. After all animations finish
and no static indicator remains lit, the widget waits 1000 ms and then turns
off the WS2812 external-power rail. This overrides the widget's 15000 ms
default; it does not turn off LEDs that are intentionally kept lit. Users may
override the value in their own `.conf`.

## Supported Hardware: Cornix Split Keyboard

Cornix Split Tented Low‑Profile Ergo Keyboard (Jezail Funder)

Cornix is a Corne‑inspired split ergonomic keyboard featuring a compact 3×6 column‑staggered layout with six thumb‑cluster keys (three per half). It offers adjustable tenting angles at 10°, 18°, and 25°, allowing users to reduce wrist strain and find a custom ergonomic alignment

- **Split, column‑staggered layout** (3×6 + thumb cluster layout).
- **Adjustable tenting support** at 10°, 18°, 25° (hardware‑based, no firmware hacks).
- **Kailh Choc V2 hot‑swap sockets** and support for LAK or LCK low‑profile keycaps.
- **Dual‑mode connectivity**: Wired USB‑C or Bluetooth wireless (left half as master).
- **Firmware**: Fully VIAL‑supported for keymaps and layer customization, stock firmware is RMK.
- Premium **CNC‑machined aluminum chassis**, custom damping foam, and portable storage pouch.

> this project owner is RMK contributor too, support RMK https://rmk.rs/ please

## --Bootloader Recovery Instructions--

-- The original RMK firmware removed the SoftDevice, so before flashing `zmk.uf2`, you need to restore the SoftDevice first. For specific steps, please refer to [bootloader/README.md](./bootloader/README.md). --

Since v2.3 this board' flash partitions has updated, removed SD (reducing sd partitionsize size from 150K to 4K), so You can flash firmware directly.

> You may need to reset fw by reset.uf2 from ealier version

> You can rollback to stock firmware by flash orgin uf2 file, backup files under rmkfw/

## 🔰 Easy Method: Clone This Repository and Build with GitHub Actions

If you're new to ZMK and don't want to deal with `west.yml` or module management, you can simply use this repository directly to customize your firmware.

### Steps

1. **Fork or Clone This Repository**
   - Click **Fork** in the top right to copy this repo to your GitHub account, or
   - Run `git clone` locally.

   > Forking is recommended, because GitHub Actions will automatically build your firmware.

2. **Edit Your Keymap**
   - Locate the keymap file in `config/cornix.keymap` (or whichever `.keymap` file you want to customize).
   - You can edit it directly or use the [ZMK Keymap Editor](https://nickcoutsos.github.io/keymap-editor/):
     - Open the editor and load your `.keymap` file.
     - Make changes with the visual editor.
     - Download the updated file and replace it in your repository.
     - Commit and push the changes to GitHub.

3. **Build with GitHub Actions**
   - After pushing, GitHub Actions will automatically run the build.
   - Once the workflow finishes, go to **Actions → your latest run → Artifacts** and download the firmware (`.uf2`) files.

4. **Flash Your Keyboard**
   - Put your board into UF2 bootloader mode (usually by double-tapping the reset button).
   - Drag and drop the `.uf2` file onto the mounted drive.

### Who Is This For?

- Beginners to ZMK
- Users who only want to customize keymaps
- Anyone who doesn't need to modify drivers or hardware definitions

## How to build Cornix Zmk firmware from scratch

This section will guide you through building the Cornix ZMK firmware from scratch using the official ZMK firmware development process.


### Prerequisites

Before starting, ensure you have the following:
- A GitHub account
 Git installed on your system
- Basic understanding of Git and GitHub
- Your Cornix keyboard PCBs ready

### Step 1: Initialize ZMK Config Repository

1. **Create a new repository** using the official ZMK config template:
   - Visit: https://github.com/zmkfirmware/unified-zmk-config-template
   - Click "Use this template" → "Create a new repository"
   - Name your repository (e.g., `cornix-zmk-config`)
   - Choose "Public" or "Private" as preferred
   - Click "Create repository"

2. **Clone your new repository locally**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

3. **Initialize ZMK development environment**:
   ```bash
   west init -l config/
   west update
   west zephyr-export
   ```

> **Important**: You should thoroughly read the ZMK documentation before proceeding, as ZMK firmware development has a learning curve.
> - ZMK Customization Guide: https://zmk.dev/docs/customization
> - ZMK Configuration: https://zmk.dev/docs/user-setup

### Step 2: Add Cornix Shield to Your Project

After initializing your zmk-config repository, follow the steps in the next section to integrate the Cornix shield.

## How to Add Cornix Shield to Existing ZMK Project

For users with existing zmk-config, add this repository dependency via west.yml and pull the latest version via west update:

### 1. Modify west.yml

Edit the `config/west.yml` file, add to the `manifest/remotes` section:

```yaml
remotes:
  - name: zmkfirmware
    url-base: https://github.com/zmkfirmware
  - name: cornix-shield
    url-base: https://github.com/hitsmaxft
  - name: urob
    url-base: https://github.com/urob
```

Add to the `manifest/projects` section:

```yaml
projects:
  - name: zmk
    remote: zmkfirmware
    revision: main
    import: app/west.yml
  - name: zmk-keyboard-cornix
    remote: cornix-shield
    revision: main
  - name: zmk-helpers
    remote: urob
    revision: main
```

### 2. Update Dependencies

```bash
west update
```

### 3. Configure Build

Edit the `build.yaml` file, add:

> [!NOTE]
> 1. If you are using (default) cornix without dongle, choose "cornix_left", "cornix_right" and "reset".
> 2. If you are using cornix with dongle, choose "cornix_dongle". "cornix_left_for_dongle", "cornix_right" and "reset".
> 3. Add `cornix_indicator` to enable RGB battery/connection indicators. Its 1000 ms idle power-off default reduces standby draw, but illuminated LEDs still consume additional power.

```yaml
include:
  # Use cornix with dongle
  - board: nice_nano//zmk
    shield: cornix_dongle_adaptor cornix_dongle_eyelash dongle_display
    snippet: studio-rpc-usb-uart
    artifact-name: cornix_dongle

  - board: cornix_ph_left//zmk
    # shield: cornix_indicator
    artifact-name: cornix_left_for_dongle

  # Use cornix without dongle
  - board: cornix_left//zmk
    # shield: cornix_indicator
    artifact-name: cornix_left

  - board: cornix_right//zmk
    # shield: cornix_indicator
    artifact-name: cornix_right

  - board: cornix_right//zmk
    shield: settings_reset
    artifact-name: reset
```

### 4. Build Firmware

Use your preferred method to build

- no need to recovery the sd since 2.3
- falsh reset.uf2 both side of cornix
- flash left and right uf2 files
- reset both side at the same time.

### 5. Flash Firmware

Flash the generated `.uf2` files to the corresponding microcontroller:
- Left half: `build/left/zephyr/zmk.uf2`
- Right half: `build/right/zephyr/zmk.uf2`

## Dongle Adapter Shield for Custom Dongle Users

For users who want to create their own custom dongle configurations, this repository provides a adapter shield. The complete configuration for the Cornix dongle can use multiple shields:

1. **`cornix_dongle_adapter`** - This is the common shield for the matrix and Bluetooth functionality
2. **`dongle_display`** - This is the display module for the dongle screen (or another display project)
3. **`cornix_dongle_eyelash`** - This is an example shield for setting up display device for the board (if the board already has `zephyr,display` in the device tree, this display overlay shield is not needed)

The configuration in the `build.yaml` file shows how to use these shields for the eyelash dongle:
```yaml
include:
  # Use cornix with dongle
  - board: nice_nano//zmk
    shield: cornix_dongle_adapter cornix_dongle_eyelash dongle_display
    snippet: studio-rpc-usb-uart
    artifact-name: cornix_dongle
```

To create a custom shield for the display part:
1. The `dongle_display` module is a module contains display widgets, included as part of the project dependencies via west or locally
2. If you need to create a custom shield for your display hardware, you can create a new shield that provides the appropriate display configuration. Here shows `cornix_dongle_eyelash` as an example
3. If your board already has `zephyr,display` in the device tree, you can omit the `cornix_dongle_eyelash` shield
4. Include your custom shield in the build configuration

For custom dongle screens, add a new target in build.yaml for your custom dongle:
```yaml
- board: nice_nano//zmk
  shield: cornix_dongle_adapter cornix_dongle_eyelash dongle_display
  snippet: studio-rpc-usb-uart zmk-usb-logging
  artifact-name: cornix_dongle
```

To create a custom shield for your display:
1. Use `cornix_dongle_adapter` as the base shield for the matrix and Bluetooth functionality
2. Add your custom shield in the `build.yaml` file with the appropriate board and configuration
3. Use `cornix_dongle_eyelash` as an example and modify the display parts to match your custom board
4. You can copy the `cornix_dongle_eyelash` into your project's `boards/shield/` directory, and use the same name or rename it as a new shield

The configuration in the `west.yml` file remains the same:
```yaml
remotes:
  - name: zmkfirmware
    url-base: https://github.com/zmkfirmware
  - name: cornix-shield
    url-base: https://github.com/hitsmaxft
  - name: urob
    url-base: https://github.com/urob
```
```yaml
projects:
  - name: zmk
    remote: zmkfirmware
    revision: main
    import: app/west.yml
  - name: zmk-keyboard-cornix
    remote: cornix-shield
    revision: main
  - name: zmk-helpers
    remote: urob
    revision: main
```

## Build This Project Locally (Without west.yaml Dependency)

If you prefer to build this project locally without adding it as a dependency in your west.yaml, you can use the ZMK_EXTRA_MODULES cmake argument.

### Prerequisites

1. Have a working ZMK development environment set up
2. Clone this repository to a local directory

### Build Steps

1. **Clone this repository**:
   ```bash
   git clone https://github.com/hitsmaxft/zmk-keyboard-cornix.git
   ```

2. **Configure your ZMK build with the extra module**:

   Edit your `.west/config` file and add the cmake argument under the `[build]` section:

   ```ini
   [build]
   cmake-args = -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DZMK_EXTRA_MODULES=/full/absolute/path/to/zmk-keyboard-cornix
   ```

   Replace `/full/absolute/path/to/zmk-keyboard-cornix` with the actual absolute path where you cloned this repository.

3. **Build the firmware**:
   ```bash
   west build -b cornix_left//zmk
   west build -b cornix_right//zmk
   ```

This method allows you to use the Cornix shield without modifying your existing ZMK configuration's west.yaml file.
