# Agent Instructions for zmk-keyboard-cornix

This module is the Cornix ZMK board/shield module. Keep edits scoped to this
module unless the user explicitly asks otherwise.

Before changing board definitions, shield configs, manifests, or build targets,
read `README.md` in full and follow its development notes, especially:

- Zephyr 4.1 / ZMK `main` compatibility requirements.
- Qualified ZMK board names such as `cornix_left//zmk`, `cornix_right//zmk`,
  `cornix_ph_left//zmk`, and `nice_nano//zmk`.
- The no-SoftDevice / `nrf52840-nosd` flashing and recovery guidance.
- Cornix board/shield roles and dongle build notes.
- DYA Studio dependency and configuration notes, if present.

Prefer minimal compatibility changes. Preserve legacy board targets unless the
README or user request says to remove them. Validate with the current west/ZMK
build environment when possible, and inspect `.config` for settings backend
correctness (`CONFIG_NVS=y`, `CONFIG_SETTINGS_NVS=y`, and no
`CONFIG_SETTINGS_NONE=y`) after settings-related changes.
