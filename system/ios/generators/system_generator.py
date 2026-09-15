from __future__ import annotations

import random

from datetime import (
    datetime,
    timedelta,
)

from system.ios.generators.icon_generator import (
    get_battery_icon,
    get_icon,
    get_lucide_icon,
    get_wifi_icon,
)


# ==========================================================
# iOS System Generator
# ==========================================================
#
# Generates synthetic iOS system chrome/state data for:
#
# - status bar
# - cellular connectivity
# - Wi-Fi
# - battery
# - focus modes
# - privacy indicators
# - Dynamic Island
#
# Icons are resolved from the local Lucide installation.
#
# Intended location:
#
# system/ios/generators/system_generator.py
#
# ==========================================================


# ==========================================================
# Constants
# ==========================================================

CELLULAR_TYPES = [
    "5G",
    "5G+",
    "LTE",
]


FOCUS_MODES = [
    None,
    "do_not_disturb",
    "personal",
    "work",
    "sleep",
]


STATUS_BAR_STYLES = [
    "light",
    "dark",
]


DYNAMIC_ISLAND_STATES = [
    "hidden",
    "idle",
    "compact",
]


PRIVACY_INDICATOR_STATES = [
    "hidden",
    "active",
]


# ==========================================================
# Safe Icon Resolver
# ==========================================================

def resolve_icon(
    semantic: str,
    fallback_name: str | None = None,
) -> str | None:
    """
    Resolve a semantic Lucide icon.

    If the semantic mapping does not exist, optionally
    try a direct Lucide filename.

    This prevents missing optional icons from breaking
    dataset generation.
    """

    icon = get_icon(
        semantic
    )

    if (
        icon is None
        and fallback_name
    ):

        icon = get_lucide_icon(
            fallback_name
        )

    return icon


# ==========================================================
# Time Generator
# ==========================================================

def generate_time_text() -> str:
    """
    Generate an iOS-style time string.

    Examples:

        9:41
        3:27
        11:08
    """

    base = datetime.now()

    offset = timedelta(
        minutes=random.randint(
            -600,
            600,
        )
    )

    value = (
        base
        + offset
    )

    return (
        value
        .strftime("%I:%M")
        .lstrip("0")
    )


# ==========================================================
# Cellular Icon Resolver
# ==========================================================

def get_cellular_icon(
    level: int,
    available: bool,
) -> str | None:
    """
    Resolve a Lucide icon for cellular strength.

    We use progressively stronger signal icons where
    available and gracefully fall back to `signal`.
    """

    if not available:

        return None

    # ------------------------------------------------------
    # Try Lucide signal variants
    # ------------------------------------------------------

    if level <= 1:

        candidates = [
            "signal-low",
            "signal-zero",
            "signal",
        ]

    elif level == 2:

        candidates = [
            "signal-medium",
            "signal-low",
            "signal",
        ]

    else:

        candidates = [
            "signal-high",
            "signal",
        ]


    for candidate in candidates:

        icon = get_lucide_icon(
            candidate
        )

        if icon is not None:

            return icon


    # ------------------------------------------------------
    # Semantic fallback
    # ------------------------------------------------------

    return resolve_icon(
        "signal"
    )


# ==========================================================
# Cellular Generator
# ==========================================================

def generate_cellular_data() -> dict:
    """
    Generate iPhone/iPad cellular connection state.
    """

    available = (
        random.random()
        < 0.96
    )

    if available:

        level = random.randint(
            1,
            4,
        )

        cellular_type = (
            random.choice(
                CELLULAR_TYPES
            )
        )

    else:

        level = 0

        cellular_type = None


    icon = (
        get_cellular_icon(
            level=
                level,

            available=
                available,
        )
    )


    return {

        "available":
            available,

        "level":
            level,

        "type":
            cellular_type,

        # Lucide SVG data URI
        "icon":
            icon,
    }


# ==========================================================
# Wi-Fi Generator
# ==========================================================

def generate_wifi_data() -> dict:
    """
    Generate Wi-Fi connectivity state and corresponding
    Lucide icon.
    """

    connected = (
        random.random()
        < 0.85
    )

    if connected:

        level = random.randint(
            1,
            3,
        )

    else:

        level = 0


    icon = (
        get_wifi_icon(
            level=
                level,

            connected=
                connected,
        )
    )


    return {

        "connected":
            connected,

        "level":
            level,

        # Lucide SVG data URI
        "icon":
            icon,
    }


# ==========================================================
# Battery Generator
# ==========================================================

def generate_battery_data() -> dict:
    """
    Generate iOS battery state.

    States:

    - normal
    - charging
    - low power mode
    - critical
    """

    level = random.randint(
        5,
        100,
    )


    charging = (
        random.random()
        < 0.16
    )


    low_power_mode = (
        not charging
        and level <= 30
        and random.random() < 0.55
    )


    critical = (
        not charging
        and level <= 10
    )


    # ======================================================
    # Resolve Lucide Battery Icon
    # ======================================================

    icon = (
        get_battery_icon(

            charging=
                charging,

            low=
                (
                    critical
                    or
                    level <= 20
                ),
        )
    )


    return {

        "level":
            level,

        "charging":
            charging,

        "low_power_mode":
            low_power_mode,

        "critical":
            critical,

        # Lucide SVG data URI
        "icon":
            icon,
    }


# ==========================================================
# Focus Icon Resolver
# ==========================================================

def get_focus_icon(
    focus_mode: str | None,
) -> str | None:

    if focus_mode is None:

        return None


    mapping = {

        "do_not_disturb":
            "moon",

        "personal":
            "user",

        "work":
            "briefcase",

        "sleep":
            "bed",
    }


    lucide_name = (
        mapping.get(
            focus_mode
        )
    )

    if lucide_name is None:

        return None


    return get_lucide_icon(
        lucide_name
    )


# ==========================================================
# Focus Mode Generator
# ==========================================================

def generate_focus_mode_data() -> dict:
    """
    Generate an iOS Focus state.

    Most screenshots remain in normal mode.
    """

    mode = random.choices(

        FOCUS_MODES,

        weights=[
            72,  # none
            8,   # do not disturb
            7,   # personal
            6,   # work
            7,   # sleep
        ],

        k=1,

    )[0]


    return {

        "mode":
            mode,

        "active":
            mode is not None,

        "icon":
            get_focus_icon(
                mode
            ),
    }


# ==========================================================
# Backward-Compatible Focus Generator
# ==========================================================

def generate_focus_mode():
    """
    Backward-compatible helper.

    Returns only the focus mode string.
    """

    return (
        generate_focus_mode_data()
        ["mode"]
    )


# ==========================================================
# Privacy Indicators
# ==========================================================

def generate_privacy_state() -> dict:
    """
    Generate iOS privacy indicator state.

    Includes Lucide icons for pages that want to show
    expanded privacy/status information.
    """

    microphone_active = (
        random.random()
        < 0.035
    )

    camera_active = (
        random.random()
        < 0.025
    )

    location_active = (
        random.random()
        < 0.08
    )


    microphone_state = (
        "active"
        if microphone_active
        else "hidden"
    )


    camera_state = (
        "active"
        if camera_active
        else "hidden"
    )


    location_state = (
        "active"
        if location_active
        else "hidden"
    )


    return {

        # --------------------------------------------------
        # Microphone
        # --------------------------------------------------

        "microphone":
            microphone_state,

        "microphone_icon":
            (
                resolve_icon(
                    "microphone",
                    "mic",
                )
                if microphone_active
                else None
            ),


        # --------------------------------------------------
        # Camera
        # --------------------------------------------------

        "camera":
            camera_state,

        "camera_icon":
            (
                resolve_icon(
                    "camera"
                )
                if camera_active
                else None
            ),


        # --------------------------------------------------
        # Location
        # --------------------------------------------------

        "location":
            location_state,

        "location_icon":
            (
                resolve_icon(
                    "location",
                    "map-pin",
                )
                if location_active
                else None
            ),
    }


# ==========================================================
# Dynamic Island Generator
# ==========================================================

def generate_dynamic_island_data(
    *,
    device_family: str,
) -> dict:
    """
    Generate Dynamic Island state.

    Dynamic Island remains decorative system chrome and
    therefore does not require its own icon.
    """

    if device_family != "iphone":

        return {

            "visible":
                False,

            "state":
                "hidden",
        }


    state = random.choices(

        DYNAMIC_ISLAND_STATES,

        weights=[
            18,  # hidden
            67,  # idle
            15,  # compact
        ],

        k=1,

    )[0]


    return {

        "visible":
            (
                state
                != "hidden"
            ),

        "state":
            state,
    }


# ==========================================================
# Status Bar Generator
# ==========================================================

def generate_status_bar_data() -> dict:
    """
    Generate basic iOS status bar information.
    """

    return {

        "time":
            generate_time_text(),

        "style":
            random.choice(
                STATUS_BAR_STYLES
            ),

        "visible":
            True,
    }


# ==========================================================
# Device Validation
# ==========================================================

def validate_device_family(
    device_family: str,
) -> None:

    valid_device_families = {
        "iphone",
        "ipad",
    }


    if (
        device_family
        not in valid_device_families
    ):

        raise ValueError(

            "device_family must be one of: "
            f"{sorted(valid_device_families)}. "
            f"Received: {device_family}"
        )


# ==========================================================
# Main System Generator
# ==========================================================

def generate_system_data(
    *,
    device_family: str = "iphone",
) -> dict:
    """
    Generate complete synthetic iOS system data.

    Parameters
    ----------
    device_family:
        iphone
        ipad

    Returns
    -------
    dict

    Template examples
    -----------------

        system.status_bar.time

        system.cellular.available
        system.cellular.level
        system.cellular.icon

        system.wifi.connected
        system.wifi.level
        system.wifi.icon

        system.battery.level
        system.battery.charging
        system.battery.icon

        system.focus_mode
        system.focus.mode
        system.focus.icon

        system.privacy.microphone
        system.privacy.camera

        system.dynamic_island.visible
    """

    validate_device_family(
        device_family
    )


    # ======================================================
    # Status Bar
    # ======================================================

    status_bar = (
        generate_status_bar_data()
    )


    # ======================================================
    # Connectivity
    # ======================================================

    cellular = (
        generate_cellular_data()
    )

    wifi = (
        generate_wifi_data()
    )


    # ======================================================
    # Battery
    # ======================================================

    battery = (
        generate_battery_data()
    )


    # ======================================================
    # Focus
    # ======================================================

    focus = (
        generate_focus_mode_data()
    )


    # ======================================================
    # Privacy
    # ======================================================

    privacy = (
        generate_privacy_state()
    )


    # ======================================================
    # Dynamic Island
    # ======================================================

    dynamic_island = (
        generate_dynamic_island_data(

            device_family=
                device_family
        )
    )


    # ======================================================
    # Common System Icons
    # ======================================================

    system_icons = {

        "lock":
            resolve_icon(
                "lock"
            ),

        "unlock":
            resolve_icon(
                "unlock"
            ),

        "camera":
            resolve_icon(
                "camera"
            ),

        "flashlight":
            resolve_icon(
                "flashlight"
            ),

        "search":
            resolve_icon(
                "search"
            ),

        "back":
            resolve_icon(
                "back"
            ),

        "forward":
            resolve_icon(
                "forward"
            ),

        "notifications":
            resolve_icon(
                "notifications"
            ),

        "settings":
            resolve_icon(
                "settings"
            ),

        "phone":
            resolve_icon(
                "phone"
            ),

        "phone_call":
            resolve_icon(
                "phone_call"
            ),

        "phone_off":
            resolve_icon(
                "phone_off"
            ),

        "play":
            resolve_icon(
                "play"
            ),

        "pause":
            resolve_icon(
                "pause"
            ),

        "skip_back":
            resolve_icon(
                "skip_back"
            ),

        "skip_forward":
            resolve_icon(
                "skip_forward"
            ),

        "volume":
            resolve_icon(
                "volume"
            ),

        "info":
            resolve_icon(
                "info"
            ),

        "check":
            resolve_icon(
                "check"
            ),

        "close":
            resolve_icon(
                "close"
            ),

        "more":
            resolve_icon(
                "more"
            ),
    }


    # ======================================================
    # Result
    # ======================================================

    return {

        # --------------------------------------------------
        # Device
        # --------------------------------------------------

        "device_family":
            device_family,


        # --------------------------------------------------
        # Status Bar
        # --------------------------------------------------

        "status_bar":
            status_bar,


        # --------------------------------------------------
        # Connectivity
        # --------------------------------------------------

        "cellular":
            cellular,

        "wifi":
            wifi,


        # --------------------------------------------------
        # Battery
        # --------------------------------------------------

        "battery":
            battery,


        # --------------------------------------------------
        # Focus
        # --------------------------------------------------

        # Existing templates may still use:
        #
        # system.focus_mode
        #
        "focus_mode":
            focus[
                "mode"
            ],

        # New richer structure:
        #
        # system.focus.mode
        # system.focus.active
        # system.focus.icon
        #
        "focus":
            focus,


        # --------------------------------------------------
        # Privacy
        # --------------------------------------------------

        "privacy":
            privacy,


        # --------------------------------------------------
        # Dynamic Island
        # --------------------------------------------------

        "dynamic_island":
            dynamic_island,


        # --------------------------------------------------
        # Shared Lucide System Icons
        # --------------------------------------------------

        "icons":
            system_icons,
    }


# ==========================================================
# Viewport -> Device Family
# ==========================================================

def get_device_family_from_viewport(
    viewport: dict,
) -> str:
    """
    Infer whether the configured viewport should behave
    like an iPhone or iPad.

    Current mapping:

        tablet -> ipad
        everything else -> iphone
    """

    category = (
        viewport.get(
            "category",
            ""
        )
    )


    if category == "tablet":

        return "ipad"


    return "iphone"


# ==========================================================
# Generate System Data From Viewport
# ==========================================================

def generate_system_data_for_viewport(
    viewport: dict,
) -> dict:
    """
    Convenience wrapper used by iOS page renderers.
    """

    device_family = (
        get_device_family_from_viewport(
            viewport
        )
    )


    return generate_system_data(

        device_family=
            device_family
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint


    print(
        "\n"
        "=========================================="
    )

    print(
        "iOS SYSTEM GENERATOR + LUCIDE"
    )

    print(
        "=========================================="
    )


    # ======================================================
    # iPhone
    # ======================================================

    print(
        "\n"
        "------------------------------------------"
    )

    print(
        "IPHONE"
    )

    print(
        "------------------------------------------"
    )


    iphone = (
        generate_system_data(
            device_family="iphone"
        )
    )


    pprint(
        iphone,
        sort_dicts=False,
    )


    # ======================================================
    # Icon Verification
    # ======================================================

    print(
        "\n"
        "------------------------------------------"
    )

    print(
        "IPHONE ICON STATUS"
    )

    print(
        "------------------------------------------"
    )


    print(
        "Cellular icon:",
        iphone[
            "cellular"
        ][
            "icon"
        ] is not None,
    )


    print(
        "Wi-Fi icon:",
        iphone[
            "wifi"
        ][
            "icon"
        ] is not None,
    )


    print(
        "Battery icon:",
        iphone[
            "battery"
        ][
            "icon"
        ] is not None,
    )


    print(
        "Lock icon:",
        iphone[
            "icons"
        ][
            "lock"
        ] is not None,
    )


    print(
        "Camera icon:",
        iphone[
            "icons"
        ][
            "camera"
        ] is not None,
    )


    print(
        "Flashlight icon:",
        iphone[
            "icons"
        ][
            "flashlight"
        ] is not None,
    )


    # ======================================================
    # iPad
    # ======================================================

    print(
        "\n"
        "------------------------------------------"
    )

    print(
        "IPAD"
    )

    print(
        "------------------------------------------"
    )


    ipad = (
        generate_system_data(
            device_family="ipad"
        )
    )


    pprint(
        ipad,
        sort_dicts=False,
    )


    # ======================================================
    # Viewport
    # ======================================================

    print(
        "\n"
        "------------------------------------------"
    )

    print(
        "VIEWPORT EXAMPLE"
    )

    print(
        "------------------------------------------"
    )


    example_viewport = {

        "name":
            "standard_iphone",

        "category":
            "mobile",

        "orientation":
            "portrait",

        "size_class":
            "compact",

        "width":
            390,

        "height":
            844,

        "dpr":
            3,
    }


    viewport_system = (
        generate_system_data_for_viewport(
            example_viewport
        )
    )


    pprint(
        viewport_system,
        sort_dicts=False,
    )


    print(
        "\n"
        "=========================================="
    )

    print(
        "SYSTEM GENERATOR TEST COMPLETE"
    )

    print(
        "=========================================="
    )