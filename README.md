# ZMK Keyboard Cornix

This project has been tested with Cornix using ZMK and provides full split-role configuration, battery power management, and Bluetooth central/peripheral setup per ZMK split guidelines 


![image](images/cornix_with_dongle.png)
![image](images/cornix_layout.png)

## TODO LIST

- [x] 52 keys full layout keymap, since v2.0
- [x] ec11 encoder, since v2.2,but cornix-left works since 2.6.1
- [x] no-SD image, since v2.3
- [x] rgb since v3


### about RGB

Cornix shield has 2 RGB LEDs on each side, controled by PWM in the stock firmware.

The replacement solution is adapting the RGB indicator module to light up these RGBs, to achieve the same effect as the stock firmware, which uses the RGB LEDs to indicate battery status and connection status. 

But it is not supported yet in this repository.  PR is welcome!

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
  - name: cornix
    url-base: https://github.com/hitsmaxft
```

Add to the `manifest/projects` section:

```yaml
projects:
  - name: zmk
    remote: zmkfirmware
    revision: main
    import: app/west.yml
  - name: zmk-keyboard-cornix
    remote: cornix
    revision: main
```

### 2. Update Dependencies

```bash
west update
```

### 3. Configure Build

Edit the `build.yaml` file, add:

```yaml
include:
  - board: cornix_main_left
    artifact-name: cornix_left

  - board: cornix_right
    artifact-name: cornix_right
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
   west build -b cornix_e73 -- -DSHIELD=cornix_main_left
   west build -b cornix_e73 -- -DSHIELD=cornix_right
   ```

This method allows you to use the Cornix shield without modifying your existing ZMK configuration's west.yaml file.
