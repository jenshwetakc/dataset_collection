from __future__ import annotations

import base64

from functools import lru_cache
from pathlib import Path


# ==========================================================
# Lucide Repository
# ==========================================================

LUCIDE_ROOT = Path(
    "/Users/shwetakc/pythonProject3/lucide"
)


# ==========================================================
# Discover Lucide Icons Directory
# ==========================================================

def discover_lucide_icon_root() -> Path:
    """
    Locate the actual Lucide icons directory.

    Expected first choice:

        /Users/pythonProject3/lucide/icons

    If that does not exist, recursively search for
    a directory containing wifi.svg.
    """

    # ------------------------------------------------------
    # Most likely location
    # ------------------------------------------------------

    direct = (
        LUCIDE_ROOT
        / "icons"
    )

    if (
        direct.is_dir()
        and
        (
            direct
            / "wifi.svg"
        ).exists()
    ):

        return direct


    # ------------------------------------------------------
    # Recursive fallback
    # ------------------------------------------------------

    for wifi_file in LUCIDE_ROOT.rglob(
        "wifi.svg"
    ):

        if wifi_file.is_file():

            return (
                wifi_file
                .parent
            )


    # ------------------------------------------------------
    # Nothing Found
    # ------------------------------------------------------

    raise FileNotFoundError(
        "\nCould not locate the Lucide icons directory.\n"
        f"Lucide repository root: {LUCIDE_ROOT}\n"
        "\nExpected to find something like:\n"
        "    lucide/icons/wifi.svg\n"
    )


# ==========================================================
# Resolved Icon Root
# ==========================================================

LUCIDE_ICON_ROOT = (
    discover_lucide_icon_root()
)


# ==========================================================
# Semantic Icon Map
# ==========================================================

ICON_MAP = {

    # ------------------------------------------------------
    # Connectivity
    # ------------------------------------------------------

    "wifi":
        "wifi",

    "wifi_zero":
        "wifi-zero",

    "wifi_low":
        "wifi-low",

    "wifi_high":
        "wifi-high",

    "wifi_off":
        "wifi-off",

    "bluetooth":
        "bluetooth",

    "signal":
        "signal",


    # ------------------------------------------------------
    # Navigation
    # ------------------------------------------------------

    "back":
        "chevron-left",

    "forward":
        "chevron-right",

    "up":
        "chevron-up",

    "down":
        "chevron-down",

    "close":
        "x",

    "more":
        "ellipsis",

    "menu":
        "menu",


    # ------------------------------------------------------
    # Search
    # ------------------------------------------------------

    "search":
        "search",

    "filter":
        "list-filter",


    # ------------------------------------------------------
    # System
    # ------------------------------------------------------

    "settings":
        "settings",

    "notifications":
        "bell",

    "lock":
        "lock",

    "unlock":
        "lock-open",

    "info":
        "info",

    "help":
        "circle-help",

    "check":
        "check",

    "plus":
        "plus",

    "minus":
        "minus",


    # ------------------------------------------------------
    # Battery / Device
    # ------------------------------------------------------

    "battery":
        "battery",

    "battery_low":
        "battery-low",

    "battery_charging":
        "battery-charging",

    "smartphone":
        "smartphone",

    "tablet":
        "tablet",


    # ------------------------------------------------------
    # Media
    # ------------------------------------------------------

    "camera":
        "camera",

    "flashlight":
        "flashlight",

    "image":
        "image",

    "play":
        "play",

    "pause":
        "pause",

    "skip_back":
        "skip-back",

    "skip_forward":
        "skip-forward",

    "volume":
        "volume-2",

    "volume_off":
        "volume-x",

    "music":
        "music",

    "video":
        "video",


    # ------------------------------------------------------
    # Communication
    # ------------------------------------------------------

    "phone":
        "phone",

    "phone_call":
        "phone-call",

    "phone_off":
        "phone-off",

    "mail":
        "mail",

    "message":
        "message-circle",

    "send":
        "send",


    # ------------------------------------------------------
    # Common UI
    # ------------------------------------------------------

    "calendar":
        "calendar",

    "clock":
        "clock",

    "map":
        "map",

    "navigation":
        "navigation",

    "home":
        "house",

    "user":
        "user",

    "users":
        "users",

    "folder":
        "folder",

    "file":
        "file",

    "trash":
        "trash-2",

    "share":
        "share",

    "download":
        "download",

    "upload":
        "upload",


    # ------------------------------------------------------
    # Appearance
    # ------------------------------------------------------

    "sun":
        "sun",

    "moon":
        "moon",

    "brightness":
        "sun-medium",

    "palette":
        "palette",


    # ------------------------------------------------------
    # Settings
    # ------------------------------------------------------

    "airplane":
        "plane",

    "globe":
        "globe",

    "location":
        "map-pin",

    "eye":
        "eye",

    "eye_off":
        "eye-off",

    "shield":
        "shield",

    "key":
        "key",

    "power":
        "power",

    "accessibility":
        "accessibility",

    "bell":
        "bell",

    "focus":
        "moon",

    "screen_time":
        "hourglass",

    "display":
        "sun",

    "hotspot":
        "radio",

    "cellular":
        "signal",

    "general":
        "settings",

    "control_center":
        "sliders-horizontal",
}


# ==========================================================
# Normalize Icon Name
# ==========================================================

def normalize_icon_name(
    icon_name: str,
) -> str:

    icon_name = (
        icon_name
        .strip()
    )

    if icon_name.endswith(
        ".svg"
    ):

        icon_name = (
            icon_name[:-4]
        )

    return icon_name


# ==========================================================
# Direct Icon Path
# ==========================================================

@lru_cache(
    maxsize=1024
)
def get_lucide_icon_path(
    icon_name: str,
) -> Path | None:

    icon_name = (
        normalize_icon_name(
            icon_name
        )
    )

    path = (
        LUCIDE_ICON_ROOT
        / f"{icon_name}.svg"
    )

    if path.exists():

        return path

    return None


# ==========================================================
# Semantic Icon Path
# ==========================================================

@lru_cache(
    maxsize=1024
)
def get_icon_path(
    semantic: str,
) -> Path | None:

    icon_name = (
        ICON_MAP.get(
            semantic
        )
    )

    if icon_name is None:

        return None

    return get_lucide_icon_path(
        icon_name
    )


# ==========================================================
# SVG -> Data URI
# ==========================================================

@lru_cache(
    maxsize=1024
)
def svg_to_data_uri(
    path_string: str,
) -> str | None:
    """
    Encode a local SVG as a base64 data URI.

    This deliberately does NOT use the common
    media_generator because that helper is primarily
    intended for raster image assets.
    """

    path = Path(
        path_string
    )

    if not path.is_file():

        return None

    try:

        svg_bytes = (
            path.read_bytes()
        )

    except OSError:

        return None


    encoded = (
        base64
        .b64encode(
            svg_bytes
        )
        .decode(
            "ascii"
        )
    )


    return (
        "data:image/svg+xml;base64,"
        + encoded
    )


# ==========================================================
# Semantic Icon
# ==========================================================

@lru_cache(
    maxsize=1024
)
def get_icon(
    semantic: str,
) -> str | None:

    path = (
        get_icon_path(
            semantic
        )
    )

    if path is None:

        return None

    return svg_to_data_uri(
        str(
            path
        )
    )


# ==========================================================
# Direct Lucide Icon
# ==========================================================

@lru_cache(
    maxsize=1024
)
def get_lucide_icon(
    icon_name: str,
) -> str | None:

    path = (
        get_lucide_icon_path(
            icon_name
        )
    )

    if path is None:

        return None

    return svg_to_data_uri(
        str(
            path
        )
    )


# ==========================================================
# Icon Exists
# ==========================================================

def has_icon(
    semantic: str,
) -> bool:

    return (
        get_icon_path(
            semantic
        )
        is not None
    )


# ==========================================================
# Wi-Fi Icon
# ==========================================================

def get_wifi_icon(
    level: int,
    connected: bool = True,
) -> str | None:

    if not connected:

        return get_icon(
            "wifi_off"
        )

    if level <= 0:

        return get_icon(
            "wifi_zero"
        )

    if level == 1:

        return get_icon(
            "wifi_low"
        )

    if level == 2:

        return get_icon(
            "wifi"
        )

    return get_icon(
        "wifi_high"
    )


# ==========================================================
# Battery Icon
# ==========================================================

def get_battery_icon(
    *,
    charging: bool = False,
    low: bool = False,
) -> str | None:

    if charging:

        return get_icon(
            "battery_charging"
        )

    if low:

        return get_icon(
            "battery_low"
        )

    return get_icon(
        "battery"
    )


# ==========================================================
# Debug Helper
# ==========================================================

def debug_icon(
    semantic: str,
) -> None:

    icon_name = (
        ICON_MAP.get(
            semantic
        )
    )

    path = (
        get_icon_path(
            semantic
        )
    )

    print(
        f"{semantic:24}",
        "|",
        f"{str(icon_name):24}",
        "|",
        path,
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n"
        "============================================================"
    )

    print(
        "LUCIDE ICON GENERATOR"
    )

    print(
        "============================================================"
    )


    print(
        "\nLucide repository root:"
    )

    print(
        LUCIDE_ROOT
    )


    print(
        "\nResolved Lucide icon root:"
    )

    print(
        LUCIDE_ICON_ROOT
    )


    print(
        "\nRepository exists:",
        LUCIDE_ROOT.exists(),
    )

    print(
        "Icon directory exists:",
        LUCIDE_ICON_ROOT.exists(),
    )


    print(
        "\n"
        "------------------------------------------------------------"
    )

    print(
        "DIRECT FILE TEST"
    )

    print(
        "------------------------------------------------------------"
    )


    direct_wifi = (
        LUCIDE_ICON_ROOT
        / "wifi.svg"
    )

    print(
        "Expected Wi-Fi path:"
    )

    print(
        direct_wifi
    )

    print(
        "exists():",
        direct_wifi.exists(),
    )

    print(
        "is_file():",
        direct_wifi.is_file(),
    )


    print(
        "\n"
        "------------------------------------------------------------"
    )

    print(
        "SEMANTIC ICON TEST"
    )

    print(
        "------------------------------------------------------------"
    )


    test_icons = [

        "wifi",
        "wifi_zero",
        "wifi_low",
        "wifi_high",
        "wifi_off",

        "bluetooth",

        "search",

        "settings",

        "camera",

        "flashlight",

        "back",

        "forward",

        "notifications",

        "battery",

        "battery_charging",

        "phone",

        "mail",

        "calendar",

        "home",

        "music",

        "airplane",

        "display",

        "accessibility",
    ]


    for semantic in test_icons:

        debug_icon(
            semantic
        )


    print(
        "\n"
        "------------------------------------------------------------"
    )

    print(
        "DATA URI TEST"
    )

    print(
        "------------------------------------------------------------"
    )


    wifi_uri = (
        get_icon(
            "wifi"
        )
    )

    print(
        "Wi-Fi loaded:",
        wifi_uri is not None,
    )


    if wifi_uri:

        print(
            "URI prefix:",
            wifi_uri[:80],
        )

        print(
            "URI length:",
            len(
                wifi_uri
            ),
        )


    print(
        "\n"
        "------------------------------------------------------------"
    )

    print(
        "DIRECT LUCIDE TEST"
    )

    print(
        "------------------------------------------------------------"
    )


    for icon_name in [

        "wifi",

        "wifi-high",

        "camera",

        "settings",

    ]:

        path = (
            get_lucide_icon_path(
                icon_name
            )
        )

        print(
            icon_name,
            "->",
            path,
        )