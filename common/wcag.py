"""
==========================================================
WCAG Color Utilities
==========================================================

Utilities for:

- Hex/RGB conversion
- Relative luminance
- Contrast ratio
- WCAG contrast checks
"""

from typing import Tuple


# ==========================================================
# WCAG Thresholds
# ==========================================================

TEXT_THRESHOLD = 4.5
LARGE_TEXT_THRESHOLD = 3.0
NON_TEXT_THRESHOLD = 3.0


# ==========================================================
# Color Conversion
# ==========================================================

def hex_to_rgb(
    hex_color: str,
) -> Tuple[int, int, int]:
    """
    Convert hex color to RGB.

    Example
    -------
    "#2563EB" -> (37, 99, 235)
    """

    hex_color = hex_color.strip().lstrip("#")

    if len(hex_color) != 6:
        raise ValueError(
            f"Invalid hex color: {hex_color}"
        )

    try:
        return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )

    except ValueError as exc:
        raise ValueError(
            f"Invalid hex color: {hex_color}"
        ) from exc


def rgb_to_hex(
    rgb: Tuple[int, int, int],
) -> str:
    """
    Convert RGB tuple to hex.

    Example
    -------
    (37, 99, 235) -> "#2563EB"
    """

    r, g, b = rgb

    if not all(
        0 <= channel <= 255
        for channel in (r, g, b)
    ):
        raise ValueError(
            f"RGB values must be between 0 and 255: {rgb}"
        )

    return "#{:02X}{:02X}{:02X}".format(
        r,
        g,
        b,
    )


# ==========================================================
# Relative Luminance
# ==========================================================

def relative_luminance(
    rgb: Tuple[int, int, int],
) -> float:
    """
    Calculate relative luminance.

    Uses the current sRGB threshold 0.04045.
    """

    def transform(
        channel: int,
    ) -> float:

        value = channel / 255.0

        if value <= 0.04045:
            return value / 12.92

        return (
            (value + 0.055) / 1.055
        ) ** 2.4

    r = transform(rgb[0])
    g = transform(rgb[1])
    b = transform(rgb[2])

    return (
        0.2126 * r
        + 0.7152 * g
        + 0.0722 * b
    )


# ==========================================================
# Contrast Ratio
# ==========================================================

def contrast_ratio(
    foreground: str,
    background: str,
) -> float:
    """
    Calculate contrast ratio.

    Range:
        1.0 -> identical colors
        21.0 -> black against white
    """

    foreground_luminance = relative_luminance(
        hex_to_rgb(foreground)
    )

    background_luminance = relative_luminance(
        hex_to_rgb(background)
    )

    lighter = max(
        foreground_luminance,
        background_luminance,
    )

    darker = min(
        foreground_luminance,
        background_luminance,
    )

    return (
        lighter + 0.05
    ) / (
        darker + 0.05
    )


# ==========================================================
# WCAG Validation
# ==========================================================

def meets_text_contrast(
    foreground: str,
    background: str,
    large_text: bool = False,
) -> bool:
    """
    Check text contrast.

    Normal text:
        >= 4.5:1

    Large text:
        >= 3.0:1
    """

    threshold = (
        LARGE_TEXT_THRESHOLD
        if large_text
        else TEXT_THRESHOLD
    )

    return (
        contrast_ratio(
            foreground,
            background,
        )
        >= threshold
    )


def meets_non_text_contrast(
    foreground: str,
    background: str,
) -> bool:
    """
    Check meaningful icons, controls,
    boundaries and graphical objects.

    Required target:
        >= 3.0:1
    """

    return (
        contrast_ratio(
            foreground,
            background,
        )
        >= NON_TEXT_THRESHOLD
    )


# Backward-compatible alias
def meets_icon_contrast(
    foreground: str,
    background: str,
) -> bool:

    return meets_non_text_contrast(
        foreground,
        background,
    )


# ==========================================================
# Generic Validation
# ==========================================================

def validate_contrast(
    foreground: str,
    background: str,
    minimum_ratio: float,
) -> bool:
    """
    Generic contrast validator.
    """

    return (
        contrast_ratio(
            foreground,
            background,
        )
        >= minimum_ratio
    )


# ==========================================================
# Detailed Validation
# ==========================================================

def contrast_result(
    foreground: str,
    background: str,
    minimum_ratio: float,
) -> dict:
    """
    Return detailed validation information.
    """

    ratio = contrast_ratio(
        foreground,
        background,
    )

    return {
        "foreground": foreground,
        "background": background,
        "ratio": round(ratio, 3),
        "minimum_ratio": minimum_ratio,
        "pass": ratio >= minimum_ratio,
    }