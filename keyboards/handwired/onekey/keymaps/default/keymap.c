// Copyright 2020 QMK
// SPDX-License-Identifier: GPL-2.0-or-later
#include QMK_KEYBOARD_H

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    LAYOUT_ortho_1x1(KC_BTN3)
};

bool encoder_update_user(uint8_t index, bool clockwise) {
  if (clockwise) {
    tap_code(KC_WH_D);
  } else {
    tap_code(KC_WH_U);
  }
  return true;
}
