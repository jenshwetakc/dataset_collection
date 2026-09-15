from __future__ import annotations

import random

from faker import Faker

from system.ios.generators.icon_generator import (
    get_icon,
    get_lucide_icon,
)

from system.ios.generators.media_generators import (
    get_random_photo,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

PHOTOS_STATES = [

    "library",

    "album_open",

    "selection_mode",

    "search_active",

    "photo_viewer",

    "share_sheet",

    "delete_confirmation",

    "empty_library",
]


PHOTOS_STATE_WEIGHTS = [

    26,

    14,

    12,

    12,

    14,

    10,

    6,

    6,
]


# ==========================================================
# Icon Resolver
# ==========================================================

def resolve_icon(
    semantic: str,
    fallback: str | None = None,
) -> str | None:

    icon = get_icon(
        semantic
    )

    if (
        icon is None
        and fallback
    ):

        icon = get_lucide_icon(
            fallback
        )

    return icon


# ==========================================================
# Photo
# ==========================================================

def generate_photo(
    index: int,
) -> dict:

    image = get_random_photo()


    return {

        "id":
            f"photo_{index}",

        "image":
            image,

        "title":
            random.choice([
                "Recent Photo",
                "Weekend",
                "Trip",
                "Morning",
                "City",
                "Memories",
            ]),

        "date":
            random.choice([
                "Today",
                "Yesterday",
                "September 3",
                "September 1",
                "August 29",
                "August 24",
            ]),

        "time":
            random.choice([
                "9:41 AM",
                "10:18 AM",
                "1:32 PM",
                "4:05 PM",
                "6:42 PM",
                "8:17 PM",
            ]),

        "favorite":
            random.random() < 0.18,

        "selected":
            False,

        "location":
            random.choice([
                "Seoul",
                "Campus",
                "Home",
                "Downtown",
                "Park",
                "Cafe",
            ]),
    }


# ==========================================================
# Photo Collection
# ==========================================================

def generate_photos(
    count: int = 24,
) -> list[dict]:

    return [

        generate_photo(
            index
        )

        for index
        in range(
            count
        )
    ]


# ==========================================================
# Albums
# ==========================================================

def generate_albums(
    photos: list[dict],
) -> list[dict]:

    definitions = [

        (
            "Recents",
            "clock-3",
        ),

        (
            "Favorites",
            "heart",
        ),

        (
            "People",
            "users",
        ),

        (
            "Places",
            "map-pin",
        ),

        (
            "Screenshots",
            "monitor",
        ),

        (
            "Videos",
            "video",
        ),
    ]


    albums = []


    for index, (
        title,
        icon_name,
    ) in enumerate(
        definitions
    ):

        cover = (

            photos[
                index
                % len(
                    photos
                )
            ]["image"]

            if photos
            else None
        )


        albums.append({

            "id":
                title
                .lower()
                .replace(
                    " ",
                    "_"
                ),

            "title":
                title,

            "count":
                random.randint(
                    8,
                    180,
                ),

            "cover":
                cover,

            "icon":
                get_lucide_icon(
                    icon_name
                ),
        })


    return albums


# ==========================================================
# Search
# ==========================================================

def generate_search_data(
    photos: list[dict],
) -> dict:

    query = random.choice([

        "Seoul",

        "summer",

        "people",

        "screenshots",

        "trip",

        "park",
    ])


    count = min(
        len(
            photos
        ),
        random.randint(
            6,
            12,
        ),
    )


    return {

        "query":
            query,

        "results":
            random.sample(
                photos,
                k=count,
            )
            if photos
            else [],
    }


# ==========================================================
# Selection
# ==========================================================

def apply_selection(
    photos: list[dict],
) -> list[dict]:

    if not photos:

        return photos


    selection_count = min(
        len(
            photos
        ),
        random.randint(
            2,
            6,
        ),
    )


    selected_indices = set(

        random.sample(

            range(
                len(
                    photos
                )
            ),

            k=
                selection_count,
        )
    )


    result = []


    for index, photo in enumerate(
        photos
    ):

        copied = {
            **photo
        }


        copied[
            "selected"
        ] = (
            index
            in selected_indices
        )


        result.append(
            copied
        )


    return result


# ==========================================================
# Share Sheet
# ==========================================================

def generate_share_sheet() -> dict:

    return {

        "title":
            "Share Photo",

        "people": [

            {
                "name":
                    fake.first_name(),

                "icon":
                    get_lucide_icon(
                        "user"
                    ),
            }

            for _ in range(
                4
            )
        ],

        "apps": [

            {
                "id":
                    "messages",

                "title":
                    "Messages",

                "icon":
                    resolve_icon(
                        "message",
                        "message-circle",
                    ),

                "style":
                    "green",
            },

            {
                "id":
                    "mail",

                "title":
                    "Mail",

                "icon":
                    resolve_icon(
                        "mail",
                        "mail",
                    ),

                "style":
                    "blue",
            },

            {
                "id":
                    "notes",

                "title":
                    "Notes",

                "icon":
                    get_lucide_icon(
                        "notebook"
                    ),

                "style":
                    "yellow",
            },

            {
                "id":
                    "files",

                "title":
                    "Files",

                "icon":
                    resolve_icon(
                        "folder",
                        "folder",
                    ),

                "style":
                    "blue",
            },
        ],

        "actions": [

            {
                "id":
                    "copy",

                "title":
                    "Copy Photo",

                "icon":
                    get_lucide_icon(
                        "copy"
                    ),
            },

            {
                "id":
                    "save_files",

                "title":
                    "Save to Files",

                "icon":
                    get_lucide_icon(
                        "folder-down"
                    ),
            },

            {
                "id":
                    "assign_contact",

                "title":
                    "Assign to Contact",

                "icon":
                    get_lucide_icon(
                        "contact"
                    ),
            },

            {
                "id":
                    "wallpaper",

                "title":
                    "Use as Wallpaper",

                "icon":
                    get_lucide_icon(
                        "image"
                    ),
            },
        ],
    }


# ==========================================================
# Delete Confirmation
# ==========================================================

def generate_delete_confirmation() -> dict:

    return {

        "title":
            "Delete This Photo?",

        "message":
            (
                "This photo will be deleted from "
                "iCloud Photos on all your devices."
            ),

        "cancel":
            "Cancel",

        "confirm":
            "Delete Photo",
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_photos_data(
    *,
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:

    # ======================================================
    # Resolve State
    # ======================================================

    if state is None:

        state = random.choices(

            PHOTOS_STATES,

            weights=
                PHOTOS_STATE_WEIGHTS,

            k=1,

        )[0]


    if state not in PHOTOS_STATES:

        raise ValueError(
            f"Unknown Photos state: {state}"
        )


    # ======================================================
    # Device
    # ======================================================

    category = (

        viewport.get(
            "category",
            ""
        )

        if viewport
        else ""
    )


    device_family = (

        "ipad"

        if category == "tablet"

        else "iphone"
    )


    # ======================================================
    # Photos
    # ======================================================

    photos = (

        []

        if state == "empty_library"

        else generate_photos(
            count=
                random.randint(
                    20,
                    32,
                )
        )
    )


    if state == "selection_mode":

        photos = apply_selection(
            photos
        )


    # ======================================================
    # Active Photo
    # ======================================================

    active_photo = (

        random.choice(
            photos
        )

        if photos
        else None
    )


    # ======================================================
    # Album
    # ======================================================

    albums = generate_albums(
        photos
    )


    active_album = (

        random.choice(
            albums
        )

        if albums
        else None
    )


    album_photos = (

        random.sample(

            photos,

            k=
                min(
                    len(
                        photos
                    ),
                    random.randint(
                        8,
                        18,
                    ),
                ),
        )

        if photos
        else []
    )


    # ======================================================
    # Popup State
    # ======================================================

    is_overlay_state = (
        state
        in {
            "share_sheet",
            "delete_confirmation",
        }
    )


    # ======================================================
    # Data
    # ======================================================

    return {

        "state":
            state,

        "device_family":
            device_family,

        "is_overlay_state":
            is_overlay_state,


        # --------------------------------------------------
        # Page
        # --------------------------------------------------

        "title":
            "Photos",


        # --------------------------------------------------
        # Content
        # --------------------------------------------------

        "photos":
            photos,

        "albums":
            albums,

        "active_album":
            active_album,

        "album_photos":
            album_photos,

        "active_photo":
            active_photo,


        # --------------------------------------------------
        # Search
        # --------------------------------------------------

        "search":
            generate_search_data(
                photos
            ),


        # --------------------------------------------------
        # Share
        # --------------------------------------------------

        "share_sheet":
            generate_share_sheet(),


        # --------------------------------------------------
        # Delete
        # --------------------------------------------------

        "delete_confirmation":
            generate_delete_confirmation(),


        # --------------------------------------------------
        # Icons
        # --------------------------------------------------

        "icons": {

            "search":
                resolve_icon(
                    "search"
                ),

            "select":
                resolve_icon(
                    "check"
                ),

            "back":
                resolve_icon(
                    "back",
                    "chevron-left",
                ),

            "more":
                resolve_icon(
                    "more",
                    "ellipsis",
                ),

            "share":
                resolve_icon(
                    "share",
                    "share",
                ),

            "trash":
                get_lucide_icon(
                    "trash-2"
                ),

            "favorite":
                get_lucide_icon(
                    "heart"
                ),

            "check":
                resolve_icon(
                    "check"
                ),

            "close":
                resolve_icon(
                    "close"
                ),

            "photos":
                resolve_icon(
                    "image",
                    "image"
                ),

            "albums":
                get_lucide_icon(
                    "layout-grid"
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint


    for state in PHOTOS_STATES:

        print(
            "\n"
            "=========================================="
        )

        print(
            state
        )

        print(
            "=========================================="
        )

        pprint(

            generate_photos_data(
                state=
                    state
            ),

            sort_dicts=False,
        )