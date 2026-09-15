"""
==========================================================
Synthetic Accessible Palette Generator
==========================================================

Features
--------
- Random seed colors
- Tonal palette generation
- Tinted neutral palettes
- Semantic color roles
- Light / dark themes
- Status colors
- Foreground/background role pairing
- WCAG validation
"""

import colorsys
import random

from typing import Tuple

from social_media.common.wcag import (
    contrast_ratio,
    contrast_result,
)


# ==========================================================
# Seed Color Families
# ==========================================================

BLUE = [
    "#1D4ED8",
    "#2563EB",
    "#3B82F6",
    "#60A5FA",
]

INDIGO = [
    "#4338CA",
    "#4F46E5",
    "#6366F1",
]

PURPLE = [
    "#7E22CE",
    "#8B5CF6",
    "#A855F7",
]

PINK = [
    "#DB2777",
    "#EC4899",
    "#F472B6",
]

RED = [
    "#DC2626",
    "#EF4444",
    "#F87171",
]

ORANGE = [
    "#EA580C",
    "#F97316",
    "#FB923C",
]

YELLOW = [
    "#CA8A04",
    "#EAB308",
    "#FACC15",
]

GREEN = [
    "#15803D",
    "#16A34A",
    "#22C55E",
]

TEAL = [
    "#0F766E",
    "#14B8A6",
    "#2DD4BF",
]

CYAN = [
    "#0891B2",
    "#06B6D4",
    "#22D3EE",
]


PRIMARY_SEEDS = (
    BLUE
    + INDIGO
    + PURPLE
    + PINK
    + RED
    + ORANGE
    + YELLOW
    + GREEN
    + TEAL
    + CYAN
)


# ==========================================================
# Tonal Levels
# ==========================================================

TONES = (
    0,
    10,
    20,
    30,
    40,
    50,
    60,
    70,
    80,
    90,
    94,
    95,
    97,
    98,
    99,
    100,
)


# ==========================================================
# Seed Selection
# ==========================================================

def random_seed_color() -> str:
    """
    Return a random primary seed.
    """

    return random.choice(
        PRIMARY_SEEDS
    )


# ==========================================================
# Color Utilities
# ==========================================================

def hex_to_hls(
    hex_color: str,
) -> Tuple[float, float, float]:

    value = hex_color.strip().lstrip("#")

    if len(value) != 6:
        raise ValueError(
            f"Invalid hex color: {hex_color}"
        )

    r = int(
        value[0:2],
        16,
    ) / 255.0

    g = int(
        value[2:4],
        16,
    ) / 255.0

    b = int(
        value[4:6],
        16,
    ) / 255.0

    return colorsys.rgb_to_hls(
        r,
        g,
        b,
    )


def hls_to_hex(
    h: float,
    l: float,
    s: float,
) -> str:

    r, g, b = colorsys.hls_to_rgb(
        h,
        l,
        s,
    )

    return "#{:02X}{:02X}{:02X}".format(
        round(r * 255),
        round(g * 255),
        round(b * 255),
    )


def blend(
    color1: str,
    color2: str,
    ratio: float,
) -> str:
    """
    Blend color1 toward color2.

    ratio=0 -> color1
    ratio=1 -> color2
    """

    ratio = max(
        0.0,
        min(
            1.0,
            ratio,
        ),
    )

    c1 = color1.lstrip("#")
    c2 = color2.lstrip("#")

    rgb1 = (
        int(c1[0:2], 16),
        int(c1[2:4], 16),
        int(c1[4:6], 16),
    )

    rgb2 = (
        int(c2[0:2], 16),
        int(c2[2:4], 16),
        int(c2[4:6], 16),
    )

    values = []

    for first, second in zip(
        rgb1,
        rgb2,
    ):
        value = round(
            first * (1 - ratio)
            + second * ratio
        )

        values.append(value)

    return "#{:02X}{:02X}{:02X}".format(
        *values
    )


def mix_with_white(
    color: str,
    amount: float,
) -> str:

    return blend(
        color,
        "#FFFFFF",
        amount,
    )


def mix_with_black(
    color: str,
    amount: float,
) -> str:

    return blend(
        color,
        "#000000",
        amount,
    )


# ==========================================================
# Foreground Selection
# ==========================================================

def choose_foreground_color(
    background: str,
) -> str:
    """
    Choose black or white depending on which has
    the highest contrast against the background.
    """

    white = "#FFFFFF"
    black = "#000000"

    white_ratio = contrast_ratio(
        white,
        background,
    )

    black_ratio = contrast_ratio(
        black,
        background,
    )

    if white_ratio >= black_ratio:
        return white

    return black


# ==========================================================
# Brand Tonal Palette
# ==========================================================

def generate_brand_palette(
    seed: str,
) -> dict[int, str]:
    """
    Generate a tonal brand palette.

    Tone 40 preserves the seed.
    """

    seed = seed.upper()

    palette = {}

    for tone in TONES:

        # Absolute anchors
        if tone == 0:
            palette[tone] = "#000000"
            continue

        if tone == 100:
            palette[tone] = "#FFFFFF"
            continue

        # Seed anchor
        if tone == 40:
            palette[tone] = seed
            continue

        # Darker than seed
        if tone < 40:

            amount = (
                40 - tone
            ) / 40.0

            palette[tone] = mix_with_black(
                seed,
                amount * 0.90,
            )

        # Lighter than seed
        else:

            amount = (
                tone - 40
            ) / 60.0

            palette[tone] = mix_with_white(
                seed,
                amount * 0.95,
            )

    return palette


# ==========================================================
# Neutral Tonal Palette
# ==========================================================

def generate_neutral_palette(
    seed: str,
) -> dict[int, str]:
    """
    Generate slightly tinted neutrals using the
    hue of the primary seed.

    Saturation remains deliberately low.
    """

    hue, _, _ = hex_to_hls(
        seed
    )

    palette = {}

    for tone in TONES:

        if tone == 0:
            palette[tone] = "#000000"
            continue

        if tone == 100:
            palette[tone] = "#FFFFFF"
            continue

        lightness = (
            tone / 100.0
        )

        # Subtle hue tint.
        if tone <= 20:
            saturation = 0.045

        elif tone <= 60:
            saturation = 0.035

        else:
            saturation = 0.025

        palette[tone] = hls_to_hex(
            hue,
            lightness,
            saturation,
        )

    return palette


# ==========================================================
# Status Colors
# ==========================================================

def generate_status_palette(
    mode: str,
) -> dict[str, str]:

    if mode == "light":

        return {
            "success": "#137333",
            "warning": "#9A6700",
            "error": "#B3261E",
            "info": "#1A73E8",
        }

    return {
        "success": "#81C995",
        "warning": "#F9AB00",
        "error": "#F2B8B5",
        "info": "#8AB4F8",
    }


# ==========================================================
# Light Semantic Palette
# ==========================================================

def generate_light_semantic_palette(
    brand: dict[int, str],
    neutral: dict[int, str],
    status: dict[str, str],
) -> dict[str, str]:

    primary = brand[40]

    primary_container = brand[90]

    background = neutral[99]

    surface = neutral[98]

    surface_variant = neutral[94]

    success = status["success"]
    warning = status["warning"]
    error = status["error"]
    info = status["info"]

    badge_background = error

    return {

        # ------------------------------------------
        # Primary
        # ------------------------------------------

        "primary":
            primary,

        "on_primary":
            choose_foreground_color(
                primary
            ),

        "primary_hover":
            brand[30],

        "primary_container":
            primary_container,

        "on_primary_container":
            choose_foreground_color(
                primary_container
            ),


        # ------------------------------------------
        # Background
        # ------------------------------------------

        "background":
            background,

        "on_background":
            neutral[10],


        # ------------------------------------------
        # Surfaces
        # ------------------------------------------

        "surface":
            surface,

        "on_surface":
            neutral[10],

        "surface_variant":
            surface_variant,

        "on_surface_variant":
            neutral[30],


        # ------------------------------------------
        # Text
        # ------------------------------------------

        "text_primary":
            neutral[10],

        "text_secondary":
            neutral[30],

        "text_disabled":
            neutral[50],


        # ------------------------------------------
        # Icons
        # ------------------------------------------

        "icon":
            neutral[20],

        "icon_secondary":
            neutral[40],


        # ------------------------------------------
        # Borders
        # ------------------------------------------

        "border":
            neutral[50],

        "border_subtle":
            neutral[90],


        # ------------------------------------------
        # Badge
        # ------------------------------------------

        "badge_background":
            badge_background,

        "badge_text":
            choose_foreground_color(
                badge_background
            ),


        # ------------------------------------------
        # Status
        # ------------------------------------------

        "success":
            success,

        "on_success":
            choose_foreground_color(
                success
            ),

        "warning":
            warning,

        "on_warning":
            choose_foreground_color(
                warning
            ),

        "error":
            error,

        "on_error":
            choose_foreground_color(
                error
            ),

        "info":
            info,

        "on_info":
            choose_foreground_color(
                info
            ),
    }


# ==========================================================
# Dark Semantic Palette
# ==========================================================

def generate_dark_semantic_palette(
    brand: dict[int, str],
    neutral: dict[int, str],
    status: dict[str, str],
) -> dict[str, str]:

    primary = brand[80]

    primary_container = brand[30]

    background = neutral[10]

    surface = neutral[15] if 15 in neutral else blend(
        neutral[10],
        neutral[20],
        0.5,
    )

    surface_variant = neutral[20]

    success = status["success"]
    warning = status["warning"]
    error = status["error"]
    info = status["info"]

    badge_background = error

    return {

        # ------------------------------------------
        # Primary
        # ------------------------------------------

        "primary":
            primary,

        "on_primary":
            choose_foreground_color(
                primary
            ),

        "primary_hover":
            brand[90],

        "primary_container":
            primary_container,

        "on_primary_container":
            choose_foreground_color(
                primary_container
            ),


        # ------------------------------------------
        # Background
        # ------------------------------------------

        "background":
            background,

        "on_background":
            neutral[95],


        # ------------------------------------------
        # Surfaces
        # ------------------------------------------

        "surface":
            surface,

        "on_surface":
            neutral[95],

        "surface_variant":
            surface_variant,

        "on_surface_variant":
            neutral[80],


        # ------------------------------------------
        # Text
        # ------------------------------------------

        "text_primary":
            neutral[95],

        "text_secondary":
            neutral[80],

        "text_disabled":
            neutral[60],


        # ------------------------------------------
        # Icons
        # ------------------------------------------

        "icon":
            neutral[90],

        "icon_secondary":
            neutral[70],


        # ------------------------------------------
        # Borders
        # ------------------------------------------

        "border":
            neutral[60],

        "border_subtle":
            neutral[30],


        # ------------------------------------------
        # Badge
        # ------------------------------------------

        "badge_background":
            badge_background,

        "badge_text":
            choose_foreground_color(
                badge_background
            ),


        # ------------------------------------------
        # Status
        # ------------------------------------------

        "success":
            success,

        "on_success":
            choose_foreground_color(
                success
            ),

        "warning":
            warning,

        "on_warning":
            choose_foreground_color(
                warning
            ),

        "error":
            error,

        "on_error":
            choose_foreground_color(
                error
            ),

        "info":
            info,

        "on_info":
            choose_foreground_color(
                info
            ),
    }


# ==========================================================
# WCAG Semantic Validation
# ==========================================================

def validate_semantic_palette(
    palette: dict[str, str],
) -> dict:
    """
    Validate actual semantic foreground/background
    relationships.
    """

    checks = {

        # ------------------------------------------
        # Normal Text
        # ------------------------------------------

        "background_text": (
            "on_background",
            "background",
            4.5,
        ),

        "primary_text": (
            "text_primary",
            "background",
            4.5,
        ),

        "secondary_text": (
            "text_secondary",
            "background",
            4.5,
        ),

        "surface_text": (
            "on_surface",
            "surface",
            4.5,
        ),

        "surface_variant_text": (
            "on_surface_variant",
            "surface_variant",
            4.5,
        ),


        # ------------------------------------------
        # Primary Components
        # ------------------------------------------

        "primary": (
            "on_primary",
            "primary",
            4.5,
        ),

        "primary_container": (
            "on_primary_container",
            "primary_container",
            4.5,
        ),


        # ------------------------------------------
        # Status Components
        # ------------------------------------------

        "success": (
            "on_success",
            "success",
            4.5,
        ),

        "warning": (
            "on_warning",
            "warning",
            4.5,
        ),

        "error": (
            "on_error",
            "error",
            4.5,
        ),

        "info": (
            "on_info",
            "info",
            4.5,
        ),

        "badge": (
            "badge_text",
            "badge_background",
            4.5,
        ),


        # ------------------------------------------
        # Non-text
        # ------------------------------------------

        "icon": (
            "icon",
            "surface",
            3.0,
        ),

        "icon_secondary": (
            "icon_secondary",
            "surface",
            3.0,
        ),

        "border": (
            "border",
            "background",
            3.0,
        ),
    }

    results = {}

    for name, (
        foreground_role,
        background_role,
        threshold,
    ) in checks.items():

        results[name] = contrast_result(
            palette[foreground_role],
            palette[background_role],
            threshold,
        )

    return results


# ==========================================================
# Overall Validation
# ==========================================================

def theme_passes_wcag(
    validation: dict,
) -> bool:
    """
    Return True when all configured required checks pass.
    """

    return all(
        result["pass"]
        for result in validation.values()
    )


# ==========================================================
# Public API
# ==========================================================

def generate_theme(
    seed: str | None = None,
    mode: str = "light",
) -> dict:
    """
    Generate a complete accessible theme.

    Parameters
    ----------
    seed:
        Optional primary seed color.

    mode:
        "light" or "dark"
    """

    if mode not in {
        "light",
        "dark",
    }:
        raise ValueError(
            "mode must be 'light' or 'dark'"
        )

    if seed is None:
        seed = random_seed_color()

    seed = seed.upper()

    brand = generate_brand_palette(
        seed
    )

    neutral = generate_neutral_palette(
        seed
    )

    status = generate_status_palette(
        mode
    )

    if mode == "light":

        semantic = (
            generate_light_semantic_palette(
                brand,
                neutral,
                status,
            )
        )

    else:

        semantic = (
            generate_dark_semantic_palette(
                brand,
                neutral,
                status,
            )
        )

    validation = validate_semantic_palette(
        semantic
    )

    return {
        "seed": seed,
        "mode": mode,

        "brand": brand,
        "neutral": neutral,
        "status": status,

        "semantic": semantic,

        "wcag": validation,

        "wcag_pass":
            theme_passes_wcag(
                validation
            ),
    }


# ==========================================================
# Generate Until Valid
# ==========================================================

def generate_accessible_theme(
    seed: str | None = None,
    mode: str | None = None,
    max_attempts: int = 100,
) -> dict:
    """
    Generate themes until all configured accessibility
    checks pass.

    When `seed` is supplied, the same seed is tested.

    When no seed is supplied, a new random seed can be
    selected for each attempt.
    """

    for _ in range(
        max_attempts
    ):

        selected_mode = (
            mode
            if mode is not None
            else random.choice(
                [
                    "light",
                    "dark",
                ]
            )
        )

        selected_seed = (
            seed
            if seed is not None
            else random_seed_color()
        )

        theme = generate_theme(
            seed=selected_seed,
            mode=selected_mode,
        )

        if theme["wcag_pass"]:
            return theme

    raise RuntimeError(
        "Unable to generate a fully valid theme "
        f"after {max_attempts} attempts."
    )


# ==========================================================
# Debug / Test
# ==========================================================

if __name__ == "__main__":

    theme = generate_accessible_theme(
        mode="light"
    )

    print("\n==============================")
    print("THEME")
    print("==============================")

    print(
        "Seed:",
        theme["seed"]
    )

    print(
        "Mode:",
        theme["mode"]
    )

    print(
        "WCAG Pass:",
        theme["wcag_pass"]
    )


    print("\n==============================")
    print("SEMANTIC COLORS")
    print("==============================")

    for role, color in (
        theme["semantic"].items()
    ):

        print(
            f"{role:24}",
            color
        )


    print("\n==============================")
    print("WCAG RESULTS")
    print("==============================")

    for name, result in (
        theme["wcag"].items()
    ):

        print(
            f"{name:24}",
            f"{result['ratio']:.2f}:1",
            "PASS"
            if result["pass"]
            else "FAIL"
        )