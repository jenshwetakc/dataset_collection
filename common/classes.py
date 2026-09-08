# social_media/common/classes.py

from __future__ import annotations


# ==========================================================
# All Supported Annotation Classes
# ==========================================================

ANNOTATION_CLASSES = {

    # ------------------------------------------------------
    # Small / Atomic GUI Elements
    # ------------------------------------------------------

    "icon",
    "system_icon",

    "button",

    "avatar",
    "image",
    "video",

    "input_field",
    "search_bar",

    "tab",
    "badge",

    "timestamp",
    "system_text",
    "text",

    "navigation_item",
    "selection_indicator",

    "progress_bar",

    # ------------------------------------------------------
    # Composite / Structural GUI Elements
    # ------------------------------------------------------

    "message_bubble",

    "card",
    "list_item",

    "app_bar",
    "navigation_bar",

    "bottom_sheet",
    "dialog",

    "toolbar",
    "section",

    "media_item",
    "status_bar",

    "switch",

    "map",

    "emoji",

    "checkbox",
    "chip",
    "slider",
    "logo",

}


# ==========================================================
# Global Class IDs
#
# These IDs are stable across the entire project.
#
# They are useful for:
#
# - JSON annotations
# - debugging
# - metadata
# - unified/full datasets
#
# IMPORTANT:
# Keep these stable once dataset generation begins.
# ==========================================================

GLOBAL_CLASS_TO_ID = {

    # ------------------------------------------------------
    # Small / Atomic
    # ------------------------------------------------------

    "icon": 0,
    "system_icon": 1,

    "button": 2,

    "avatar": 3,
    "image": 4,
    "video": 5,

    "input_field": 6,
    "search_bar": 7,

    "tab": 8,
    "badge": 9,

    "timestamp": 10,
    "system_text": 11,
    "text": 12,

    "navigation_item": 13,
    "selection_indicator": 14,

    "progress_bar": 15,

    # ------------------------------------------------------
    # Structural / Composite
    # ------------------------------------------------------

    "message_bubble": 16,

    "card": 17,
    "list_item": 18,

    "app_bar": 19,
    "navigation_bar": 20,

    "bottom_sheet": 21,
    "dialog": 22,

    "toolbar": 23,
    "section": 24,

    "media_item": 25,
    "status_bar": 26,

    "switch": 27,
    "map": 28,
    "emoji": 29,
    "checkbox": 30,
    "chip":31,
    "slider":32,
    "logo":33,
}


# ==========================================================
# Backward Compatibility
#
# Existing renderer code may still import CLASS_TO_ID.
# ==========================================================

CLASS_TO_ID = GLOBAL_CLASS_TO_ID


# ==========================================================
# Reverse Global Map
# ==========================================================

GLOBAL_ID_TO_CLASS = {
    class_id: class_name
    for class_name, class_id
    in GLOBAL_CLASS_TO_ID.items()
}


# ==========================================================
# Annotation Class Groups
# ==========================================================


# ==========================================================
# Big Components
#
# Large structural regions that usually occupy substantial
# parts of the interface.
#
# Intentionally excludes:
#
# - list_item
# - toolbar
# - section
# - media_item
# - tab
# - navigation_item
#
# These tend to be too fine-grained for the big-component
# dataset.
# ==========================================================

BIG_COMPONENT_CLASSES = {
    "section",
    "card",

    "app_bar",
    "navigation_bar",

    "bottom_sheet",
    "dialog",

    "image",
    "video",
    "map",

}


# ==========================================================
# Components
#
# Broader structural GUI component dataset.
# ==========================================================

COMPONENT_CLASSES = {

    "message_bubble",

    "card",
    "list_item",

    "app_bar",
    "navigation_bar",

    "bottom_sheet",
    "dialog",

    "toolbar",
    "section",

    "media_item",

    "image",
    "video",

    "status_bar",
}


# ==========================================================
# Small / Atomic Elements
#
# IMPORTANT:
#
# image/video are intentionally NOT included here.
#
# They belong to structural/component profiles because they
# frequently occupy large visual regions.
#
# Generic text is also intentionally excluded because a
# small-elements object detection dataset would otherwise
# become dominated by text boxes.
# ==========================================================

# ==========================================================
# Small / Atomic Elements
# ==========================================================

SMALL_ELEMENT_CLASSES = {
    "icon",
    "system_icon",

    "button",
    "avatar",

    "input_field",
    "search_bar",

    "badge",

    "progress_bar",
    "slider",

    "selection_indicator",
    "tab",
    "switch",

    "emoji",
    "checkbox",
    "chip",
    "logo",
}

# ==========================================================
# Icon Classes
# ==========================================================

ICON_CLASSES = {
    "icon",
    "system_icon",
}


# ==========================================================
# Text Classes
#
# Used primarily by renderer visibility/text logic.
# ==========================================================

TEXT_CLASSES = {
    "text",
    "system_text",
    "timestamp",
}


# ==========================================================
# Annotation Profiles
# ==========================================================

ANNOTATION_PROFILES = {

    # ------------------------------------------------------
    # Everything
    # ------------------------------------------------------

    "full": {
        "include": set(
            ANNOTATION_CLASSES
        ),
    },


    # ------------------------------------------------------
    # Large Structural Components
    # ------------------------------------------------------

    "big_components": {
        "include": set(
            BIG_COMPONENT_CLASSES
        ),
    },


    # ------------------------------------------------------
    # All Structural Components
    # ------------------------------------------------------

    "components": {
        "include": set(
            COMPONENT_CLASSES
        ),
    },


    # ------------------------------------------------------
    # Small / Atomic Elements
    # ------------------------------------------------------

    "small_elements": {
        "include": set(
            SMALL_ELEMENT_CLASSES
        ),
    },


    # ------------------------------------------------------
    # Icons Only
    #
    # icon + system_icon are intentionally merged into one
    # YOLO class.
    # ------------------------------------------------------

    "icons_only": {
        "include": set(
            ICON_CLASSES
        ),
    },
}


# ==========================================================
# Profile-Specific YOLO Class Maps
#
# IMPORTANT:
#
# Each profile should use a compact/dense class ID range
# beginning from 0.
#
# Different semantic classes MAY intentionally share the
# same profile ID.
#
# Example:
#
# icons_only:
#     icon        -> 0
#     system_icon -> 0
#
# This means the training task is "detect generic icons".
# ==========================================================

PROFILE_CLASS_TO_ID = {


    # ======================================================
    # Big Components
    # ======================================================

    "big_components": {

        "section": 0,

        "card": 1,

        "app_bar": 2,
        "navigation_bar": 3,

        "bottom_sheet": 4,
        "dialog": 5,

        "image": 6,
        "video": 7,
        "map":8,
    },


    # ======================================================
    # Components
    # ======================================================

    "components": {

        "message_bubble": 0,

        "card": 1,
        "list_item": 2,

        "app_bar": 3,
        "navigation_bar": 4,

        "bottom_sheet": 5,
        "dialog": 6,

        "toolbar": 7,
        "section": 8,

        "media_item": 9,

        "image": 10,
        "video": 11,

        "status_bar": 12,
    },


    # ======================================================
    # Small Elements
    #
    # timestamp + system_text are intentionally merged.
    # ======================================================

    "small_elements": {
        # Merged into the generic "icon" class.
        "icon": 0,
        "system_icon": 0,

        "button": 1,
        "avatar": 2,

        "input_field": 3,
        "search_bar": 4,

        "badge": 5,

        # Merged into the generic "progress_bar" class.
        "progress_bar": 6,
        "slider": 6,

        "selection_indicator": 7,
        "tab": 8,
        "switch": 9,

        "emoji": 10,
        "checkbox": 11,
        "chip": 12,
        "logo": 13,
    },


    # ======================================================
    # Icons Only
    #
    # Both icon types become one generic YOLO class.
    # ======================================================

    "icons_only": {

        "icon": 0,
        "system_icon": 0,
    },
}


# ==========================================================
# Full Profile
#
# Preserve the stable global IDs exactly.
# ==========================================================

PROFILE_CLASS_TO_ID["full"] = dict(
    GLOBAL_CLASS_TO_ID
)


# ==========================================================
# Canonical Profile ID Names
#
# Required when multiple semantic classes share one profile
# ID.
#
# Example:
#
# icons_only:
#
#     icon        -> 0
#     system_icon -> 0
#
# YOLO data.yaml still needs ONE name for class 0.
#
# We therefore explicitly define the canonical class name.
# ==========================================================

PROFILE_ID_TO_NAME = {


    # ======================================================
    # Big Components
    # ======================================================

    "big_components": {

        0: "section",

        1: "card",

        2: "app_bar",
        3: "navigation_bar",

        4: "bottom_sheet",
        5: "dialog",

        6: "image",
        7: "video",
        8:"map"
    },


    # ======================================================
    # Components
    # ======================================================

    "components": {

        0: "message_bubble",

        1: "card",
        2: "list_item",

        3: "app_bar",
        4: "navigation_bar",

        5: "bottom_sheet",
        6: "dialog",

        7: "toolbar",
        8: "section",

        9: "media_item",

        10: "image",
        11: "video",

        12: "status_bar",
    },


    # ======================================================
    # Small Elements
    # ======================================================

    "small_elements": {
    0: "icon",
    1: "button",
    2: "avatar",
    3: "input_field",
    4: "search_bar",
    5: "badge",
    6: "progress_bar",
    7: "selection_indicator",
    8: "tab",
    9: "switch",
    10: "emoji",
    11: "checkbox",
    12: "chip",
    13: "logo",
    },


    # ======================================================
    # Icons Only
    # ======================================================

    "icons_only": {
        0: "icon",
    },


    # ======================================================
    # Full
    # ======================================================

    "full": {
        class_id: class_name
        for class_name, class_id
        in GLOBAL_CLASS_TO_ID.items()
    },
}


# ==========================================================
# Helper:
# Get Classes Enabled by a Profile
# ==========================================================

def get_profile_classes(
    profile_name: str,
) -> set[str]:

    if profile_name not in ANNOTATION_PROFILES:

        raise ValueError(
            f"Unknown annotation profile: "
            f"{profile_name}. "
            f"Available profiles: "
            f"{sorted(ANNOTATION_PROFILES.keys())}"
        )

    profile = (
        ANNOTATION_PROFILES[
            profile_name
        ]
    )

    include = set(
        profile.get(
            "include",
            ANNOTATION_CLASSES,
        )
    )

    exclude = set(
        profile.get(
            "exclude",
            set(),
        )
    )

    return (
        include
        - exclude
    )


# ==========================================================
# Helper:
# Check Whether a Class is Enabled
# ==========================================================

def class_in_profile(
    profile_name: str,
    class_name: str,
) -> bool:

    return (
        class_name
        in get_profile_classes(
            profile_name
        )
    )


# ==========================================================
# Helper:
# Get Profile-Specific Class ID
# ==========================================================

def get_profile_class_id(
    profile_name: str,
    class_name: str,
) -> int | None:

    profile_map = (
        PROFILE_CLASS_TO_ID.get(
            profile_name
        )
    )

    if profile_map is None:

        raise ValueError(
            f"No class map for profile: "
            f"{profile_name}"
        )

    return profile_map.get(
        class_name
    )


# ==========================================================
# Helper:
# Get Global Class ID
# ==========================================================

def get_global_class_id(
    class_name: str,
) -> int | None:

    return (
        GLOBAL_CLASS_TO_ID.get(
            class_name
        )
    )


# ==========================================================
# Helper:
# Get Canonical YOLO Names
#
# Returns:
#
# [
#     "icon",
#     "system_icon",
#     "button",
#     ...
# ]
#
# IDs are guaranteed to correspond to list indices.
# ==========================================================

def get_profile_names(
    profile_name: str,
) -> list[str]:

    id_to_name = (
        PROFILE_ID_TO_NAME.get(
            profile_name
        )
    )

    if id_to_name is None:

        raise ValueError(
            f"No canonical name map for profile: "
            f"{profile_name}"
        )

    if not id_to_name:

        return []

    max_id = max(
        id_to_name.keys()
    )

    names = [
        None
    ] * (
        max_id + 1
    )

    for (
        class_id,
        class_name,
    ) in id_to_name.items():

        names[class_id] = (
            class_name
        )

    missing_ids = [
        index
        for index, name
        in enumerate(names)
        if name is None
    ]

    if missing_ids:

        raise ValueError(
            f"Profile '{profile_name}' "
            f"contains missing YOLO IDs: "
            f"{missing_ids}"
        )

    return names


# ==========================================================
# Helper:
# Get Profile Class Count
# ==========================================================

def get_profile_class_count(
    profile_name: str,
) -> int:

    return len(
        get_profile_names(
            profile_name
        )
    )


# ==========================================================
# Helper:
# Get Available Profiles
# ==========================================================

def get_annotation_profile_names() -> list[str]:

    return list(
        ANNOTATION_PROFILES.keys()
    )


# ==========================================================
# Validation:
# Global Classes
# ==========================================================

def validate_global_classes() -> None:

    # ------------------------------------------------------
    # Ensure annotation set and global map agree
    # ------------------------------------------------------

    annotation_classes = set(
        ANNOTATION_CLASSES
    )

    global_classes = set(
        GLOBAL_CLASS_TO_ID.keys()
    )

    missing_global_ids = (
        annotation_classes
        - global_classes
    )

    extra_global_ids = (
        global_classes
        - annotation_classes
    )

    if missing_global_ids:

        raise ValueError(
            "Classes missing from "
            "GLOBAL_CLASS_TO_ID: "
            f"{sorted(missing_global_ids)}"
        )

    if extra_global_ids:

        raise ValueError(
            "GLOBAL_CLASS_TO_ID contains "
            "unknown classes: "
            f"{sorted(extra_global_ids)}"
        )


    # ------------------------------------------------------
    # IDs must be unique
    # ------------------------------------------------------

    ids = list(
        GLOBAL_CLASS_TO_ID.values()
    )

    if len(ids) != len(set(ids)):

        raise ValueError(
            "GLOBAL_CLASS_TO_ID contains "
            "duplicate IDs."
        )


    # ------------------------------------------------------
    # Global IDs should be contiguous
    # ------------------------------------------------------

    expected_ids = list(
        range(
            len(
                GLOBAL_CLASS_TO_ID
            )
        )
    )

    actual_ids = sorted(
        ids
    )

    if actual_ids != expected_ids:

        raise ValueError(
            "GLOBAL_CLASS_TO_ID must use "
            "contiguous IDs starting at 0. "
            f"Expected {expected_ids}, "
            f"got {actual_ids}."
        )


# ==========================================================
# Validation:
# Annotation Profiles
# ==========================================================

def validate_annotation_profiles() -> None:

    for (
        profile_name,
        profile,
    ) in ANNOTATION_PROFILES.items():

        include = set(
            profile.get(
                "include",
                set(),
            )
        )

        exclude = set(
            profile.get(
                "exclude",
                set(),
            )
        )

        unknown_include = (
            include
            - ANNOTATION_CLASSES
        )

        unknown_exclude = (
            exclude
            - ANNOTATION_CLASSES
        )

        if unknown_include:

            raise ValueError(
                f"Profile '{profile_name}' "
                f"includes unknown classes: "
                f"{sorted(unknown_include)}"
            )

        if unknown_exclude:

            raise ValueError(
                f"Profile '{profile_name}' "
                f"excludes unknown classes: "
                f"{sorted(unknown_exclude)}"
            )


# ==========================================================
# Validation:
# Profile Class Maps
# ==========================================================

def validate_profile_class_maps() -> None:

    for profile_name in ANNOTATION_PROFILES:

        if profile_name not in PROFILE_CLASS_TO_ID:

            raise ValueError(
                f"Profile '{profile_name}' "
                f"has no PROFILE_CLASS_TO_ID map."
            )

        if profile_name not in PROFILE_ID_TO_NAME:

            raise ValueError(
                f"Profile '{profile_name}' "
                f"has no PROFILE_ID_TO_NAME map."
            )

        enabled_classes = (
            get_profile_classes(
                profile_name
            )
        )

        profile_map = (
            PROFILE_CLASS_TO_ID[
                profile_name
            ]
        )

        mapped_classes = set(
            profile_map.keys()
        )


        # --------------------------------------------------
        # Every enabled class must have a profile ID.
        # --------------------------------------------------

        missing = (
            enabled_classes
            - mapped_classes
        )

        if missing:

            raise ValueError(
                f"Profile '{profile_name}' "
                f"is missing class mappings for: "
                f"{sorted(missing)}"
            )


        # --------------------------------------------------
        # Profile map should not contain disabled classes.
        # --------------------------------------------------

        extra = (
            mapped_classes
            - enabled_classes
        )

        if extra:

            raise ValueError(
                f"Profile '{profile_name}' "
                f"maps classes that are not enabled: "
                f"{sorted(extra)}"
            )


        # --------------------------------------------------
        # Check canonical ID names
        # --------------------------------------------------

        canonical_map = (
            PROFILE_ID_TO_NAME[
                profile_name
            ]
        )

        used_ids = set(
            profile_map.values()
        )

        canonical_ids = set(
            canonical_map.keys()
        )

        if used_ids != canonical_ids:

            raise ValueError(
                f"Profile '{profile_name}' "
                f"YOLO IDs do not match canonical "
                f"name IDs. "
                f"Used IDs={sorted(used_ids)}, "
                f"canonical IDs="
                f"{sorted(canonical_ids)}"
            )


        # --------------------------------------------------
        # Profile IDs must be contiguous from 0.
        # --------------------------------------------------

        expected_ids = set(
            range(
                max(used_ids) + 1
            )
        )

        if used_ids != expected_ids:

            raise ValueError(
                f"Profile '{profile_name}' "
                f"must use contiguous IDs from 0. "
                f"Found: "
                f"{sorted(used_ids)}"
            )


# ==========================================================
# Validate Everything
# ==========================================================

def validate_classes_config() -> None:

    validate_global_classes()

    validate_annotation_profiles()

    validate_profile_class_maps()


# ==========================================================
# Automatic Validation
#
# Fail immediately at import time if the configuration is
# internally inconsistent.
# ==========================================================

validate_classes_config()


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n"
        "=========================================="
    )

    print(
        "ANNOTATION CLASS CONFIGURATION"
    )

    print(
        "=========================================="
    )


    print(
        "\nGlobal classes:"
    )

    for (
        class_name,
        class_id,
    ) in GLOBAL_CLASS_TO_ID.items():

        print(
            f"{class_id:>2}  "
            f"{class_name}"
        )


    print(
        "\n"
        "=========================================="
    )

    print(
        "PROFILES"
    )

    print(
        "=========================================="
    )


    for profile_name in (
        ANNOTATION_PROFILES
    ):

        print(
            "\n"
            "------------------------------------------"
        )

        print(
            f"Profile: "
            f"{profile_name}"
        )

        print(
            f"Classes: "
            f"{sorted(get_profile_classes(profile_name))}"
        )

        print(
            "YOLO map:"
        )

        for (
            class_name,
            class_id,
        ) in (
            PROFILE_CLASS_TO_ID[
                profile_name
            ].items()
        ):

            print(
                f"  "
                f"{class_name:<22}"
                f" -> "
                f"{class_id}"
            )

        print(
            f"YOLO names: "
            f"{get_profile_names(profile_name)}"
        )

        print(
            f"YOLO nc: "
            f"{get_profile_class_count(profile_name)}"
        )



