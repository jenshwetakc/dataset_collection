from __future__ import annotations

import random

from common.system_generator import (
    generate_system_data,
)


# ==========================================================
# Constants
# ==========================================================

NAVIGATION_MODES = [
    "gesture",
    "three_button",
]


# ==========================================================
# Android System Generator
# ==========================================================

def generate_android_system_data() -> dict:
    """
    Extend the shared system generator with Android-specific
    operating-system state.

    The common system generator remains unchanged.
    """

    system = generate_system_data()

    airplane_mode = (
        random.random()
        < 0.06
    )

    if airplane_mode:

        system["cellular"]["available"] = False

        system["cellular"]["type"] = None

    update({

        # --------------------------------------------------
        # Navigation
        # --------------------------------------------------

        "navigation_mode":
            random.choices(
                NAVIGATION_MODES,
                weights=[
                    0.82,
                    0.18,
                ],
                k=1,
            )[0],

        "navigation_bar_visible":
            True,


        # --------------------------------------------------
        # Android System State
        # --------------------------------------------------

        "airplane_mode":
            airplane_mode,

        "location_enabled":
            random.random()
            < 0.86,

        "nfc_enabled":
            random.random()
            < 0.38,

        "hotspot_enabled":
            random.random()
            < 0.10,

        "orientation_locked":
            random.random()
            < 0.40,
    })

    return system


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_android_system_data()
    )