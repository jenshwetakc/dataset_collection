
import random


# ==========================================================
# Viewport Configuration
# ==========================================================

VIEWPORTS = [

    # ======================================================
    # Mobile Portrait
    # ======================================================

    {
        "name": "small_mobile",
        "category": "mobile",
        "orientation": "portrait",
        "size_class": "compact",
        "width": 320,
        "height": 568,
        "dpr": 2,
    },

    {
        "name": "standard_android",
        "category": "mobile",
        "orientation": "portrait",
        "size_class": "compact",
        "width": 360,
        "height": 800,
        "dpr": 3,
    },

    {
        "name": "standard_iphone",
        "category": "mobile",
        "orientation": "portrait",
        "size_class": "compact",
        "width": 390,
        "height": 844,
        "dpr": 3,
    },

    {
        "name": "large_mobile",
        "category": "mobile",
        "orientation": "portrait",
        "size_class": "compact",
        "width": 430,
        "height": 932,
        "dpr": 3,
    },

    # ======================================================
    # Mobile Landscape
    # ======================================================

    {
        "name": "mobile_landscape",
        "category": "mobile_landscape",
        "orientation": "landscape",
        "size_class": "expanded",
        "width": 844,
        "height": 390,
        "dpr": 3,
    },

    # ======================================================
    # Tablet
    # ======================================================

    {
        "name": "tablet_portrait",
        "category": "tablet",
        "orientation": "portrait",
        "size_class": "medium",
        "width": 768,
        "height": 1024,
        "dpr": 3,
    },

    {
        "name": "large_tablet_portrait",
        "category": "tablet",
        "orientation": "portrait",
        "size_class": "medium",
        "width": 820,
        "height": 1180,
        "dpr": 2,
    },

    {
        "name": "tablet_landscape",
        "category": "tablet",
        "orientation": "landscape",
        "size_class": "expanded",
        "width": 1024,
        "height": 768,
        "dpr": 2,
    },

    # ======================================================
    # Foldable
    # ======================================================

    {
        "name": "foldable",
        "category": "foldable",
        "orientation": "portrait",
        "size_class": "expanded",
        "width": 884,
        "height": 1104,
        "dpr": 2,
    },

    # ======================================================
    # Laptop
    # ======================================================

    {
        "name": "small_laptop",
        "category": "laptop",
        "orientation": "landscape",
        "size_class": "expanded",
        "width": 1280,
        "height": 720,
        "dpr": 2,
    },

    {
        "name": "laptop",
        "category": "laptop",
        "orientation": "landscape",
        "size_class": "expanded",
        "width": 1366,
        "height": 768,
        "dpr": 2,
    },

    {
        "name": "large_laptop",
        "category": "laptop",
        "orientation": "landscape",
        "size_class": "expanded",
        "width": 1440,
        "height": 900,
        "dpr": 2,
    },

    # ======================================================
    # Desktop
    # ======================================================

    {
        "name": "desktop_fhd",
        "category": "desktop",
        "orientation": "landscape",
        "size_class": "expanded",
        "width": 1920,
        "height": 1080,
        "dpr": 2,
    },

    {
        "name": "desktop_qhd",
        "category": "desktop",
        "orientation": "landscape",
        "size_class": "expanded",
        "width": 2560,
        "height": 1440,
        "dpr": 2,
    },

    {
        "name": "desktop_4k",
        "category": "desktop",
        "orientation": "landscape",
        "size_class": "expanded",
        "width": 3840,
        "height": 2160,
        "dpr": 2,
    },

    # ======================================================
    # Ultrawide
    # ======================================================

    {
        "name": "ultrawide",
        "category": "ultrawide",
        "orientation": "landscape",
        "size_class": "expanded",
        "width": 3440,
        "height": 1440,
        "dpr": 2,
    },
]


# ==========================================================
# Development / Test Subset
# ==========================================================

ALL_VIEWPORT_NAMES = [
    "small_mobile",
    "standard_android",
    "standard_iphone",
    "large_mobile",
    "mobile_landscape",
    "tablet_portrait",
    "large_tablet_portrait",
    "tablet_landscape",
    "foldable",
    "small_laptop",
    "laptop",
    "large_laptop",
    "desktop_fhd",
    "desktop_qhd",
    "desktop_4k",
    "ultrawide",
]


# ==========================================================
# Helpers
# ==========================================================

def get_all_viewports():
    """
    Return a copy of all configured viewports.
    """
    return VIEWPORTS.copy()


def get_test_viewports():
    """
    Return the reduced viewport set used during development.
    """
    return get_viewports_by_names(TEST_VIEWPORTS)


def get_viewports_by_category(category: str):
    """
    Return all viewports belonging to a category.

    Examples:
        mobile
        mobile_landscape
        tablet
        foldable
        laptop
        desktop
        ultrawide
    """

    result = [
        viewport
        for viewport in VIEWPORTS
        if viewport["category"] == category
    ]

    if not result:
        valid_categories = sorted({
            viewport["category"]
            for viewport in VIEWPORTS
        })

        raise ValueError(
            f"Unknown viewport category: {category}. "
            f"Available categories: {valid_categories}"
        )

    return result


def get_viewports_by_size_class(size_class: str):
    """
    Return viewports belonging to a Material-style size class.

    Supported:
        compact
        medium
        expanded
    """

    result = [
        viewport
        for viewport in VIEWPORTS
        if viewport["size_class"] == size_class
    ]

    if not result:
        valid_size_classes = sorted({
            viewport["size_class"]
            for viewport in VIEWPORTS
        })

        raise ValueError(
            f"Unknown size class: {size_class}. "
            f"Available size classes: {valid_size_classes}"
        )

    return result


def get_viewports_by_orientation(orientation: str):
    """
    Return portrait or landscape viewports.
    """

    result = [
        viewport
        for viewport in VIEWPORTS
        if viewport["orientation"] == orientation
    ]

    if not result:
        raise ValueError(
            f"Unknown orientation: {orientation}. "
            f"Expected 'portrait' or 'landscape'."
        )

    return result


def get_viewports_by_names(names):
    """
    Return viewports matching the supplied names.
    """

    selected = [
        viewport
        for viewport in VIEWPORTS
        if viewport["name"] in names
    ]

    found_names = {
        viewport["name"]
        for viewport in selected
    }

    missing = set(names) - found_names

    if missing:
        available = [
            viewport["name"]
            for viewport in VIEWPORTS
        ]

        raise ValueError(
            f"Unknown viewport names: {sorted(missing)}. "
            f"Available viewports: {available}"
        )

    # Preserve the order supplied by `names`
    lookup = {
        viewport["name"]: viewport
        for viewport in selected
    }

    return [
        lookup[name]
        for name in names
    ]


def get_viewport(name: str):
    """
    Return one viewport by name.
    """

    for viewport in VIEWPORTS:
        if viewport["name"] == name:
            return viewport.copy()

    available = [
        viewport["name"]
        for viewport in VIEWPORTS
    ]

    raise ValueError(
        f"Unknown viewport name: {name}. "
        f"Available viewports: {available}"
    )


def get_random_viewport():
    """
    Return one completely random viewport.
    """
    return random.choice(VIEWPORTS).copy()


def get_random_viewport_by_category(category: str):
    """
    Return one random viewport from the specified category.
    """

    candidates = get_viewports_by_category(category)

    return random.choice(candidates).copy()

TEST_VIEWPORTS = [
    "standard_iphone",
    "tablet_portrait",
    "laptop",
    "desktop_fhd",
]