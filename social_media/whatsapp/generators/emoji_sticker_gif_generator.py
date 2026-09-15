import random

from social_media.whatsapp.generators.media_generator import (
    get_random_emoji,
    get_random_sticker,
    get_random_gif,
)


# ==========================================================
# Constants
# ==========================================================

EMOJI_CATEGORIES = [
    {
        "id": "recent",
        "label": "Recent",
        "icon": "history",
    },
    {
        "id": "smileys",
        "label": "Smileys",
        "icon": "sentiment_satisfied",
    },
    {
        "id": "people",
        "label": "People",
        "icon": "person",
    },
    {
        "id": "animals",
        "label": "Animals",
        "icon": "pets",
    },
    {
        "id": "food",
        "label": "Food",
        "icon": "restaurant",
    },
    {
        "id": "travel",
        "label": "Travel",
        "icon": "flight",
    },
    {
        "id": "activities",
        "label": "Activities",
        "icon": "sports_soccer",
    },
    {
        "id": "objects",
        "label": "Objects",
        "icon": "lightbulb",
    },
    {
        "id": "symbols",
        "label": "Symbols",
        "icon": "favorite",
    },
]


PICKER_TABS = [
    {
        "id": "emoji",
        "label": "Emoji",
        "icon": "sentiment_satisfied",
    },
    {
        "id": "gifs",
        "label": "GIFs",
        "icon": "gif_box",
    },
    {
        "id": "stickers",
        "label": "Stickers",
        "icon": "sticky_note_2",
    },
]


# ==========================================================
# Emoji Items
# ==========================================================

def generate_emoji_items(
    min_items=30,
    max_items=80,
):

    item_count = random.randint(
        min_items,
        max_items,
    )

    items = []

    for _ in range(item_count):

        emoji = get_random_emoji()

        if not emoji:
            continue

        items.append(
            {
                "uri":
                    emoji["uri"],

                "source":
                    emoji.get(
                        "source"
                    ),

                "filename":
                    emoji.get(
                        "filename"
                    ),

                "path":
                    emoji.get(
                        "path"
                    ),
            }
        )

    return items


# ==========================================================
# Sticker Items
# ==========================================================

def generate_sticker_items(
    min_items=12,
    max_items=30,
):

    item_count = random.randint(
        min_items,
        max_items,
    )

    items = []

    for _ in range(item_count):

        sticker = get_random_sticker()

        if not sticker:
            continue

        # Current media_generator may return
        # either a URI string or a richer dict.
        if isinstance(sticker, dict):

            items.append(
                {
                    "uri":
                        sticker.get("uri"),

                    "path":
                        sticker.get("path"),

                    "filename":
                        sticker.get(
                            "filename"
                        ),
                }
            )

        else:

            items.append(
                {
                    "uri":
                        sticker,

                    "path":
                        None,

                    "filename":
                        None,
                }
            )

    return items


# ==========================================================
# GIF Items
# ==========================================================

def generate_gif_items(
    min_items=8,
    max_items=20,
):

    item_count = random.randint(
        min_items,
        max_items,
    )

    items = []

    for _ in range(item_count):

        gif = get_random_gif()

        if not gif:
            continue

        if isinstance(gif, dict):

            uri = gif.get("uri")
            path = gif.get("path")
            filename = gif.get(
                "filename"
            )

        else:

            uri = gif
            path = None
            filename = None


        items.append(
            {
                "uri":
                    uri,

                "path":
                    path,

                "filename":
                    filename,

                "duration":
                    f"{random.randint(1, 8)}."
                    f"{random.randint(0, 9)}s",

                "favorite":
                    random.random() < 0.12,
            }
        )

    return items


# ==========================================================
# Search State
# ==========================================================

def generate_search_state():

    search_active = (
        random.random() < 0.25
    )

    if not search_active:

        return {
            "active":
                False,

            "query":
                "",
        }


    return {

        "active":
            True,

        "query":
            random.choice(
                [
                    "happy",
                    "love",
                    "funny",
                    "wow",
                    "party",
                    "hello",
                    "thanks",
                ]
            ),
    }


# ==========================================================
# Picker Page
# ==========================================================

def generate_emoji_sticker_gif_page():

    active_tab = random.choices(
        [
            "emoji",
            "gifs",
            "stickers",
        ],
        weights=[
            0.55,
            0.20,
            0.25,
        ],
        k=1,
    )[0]


    selected_category = random.choice(
        EMOJI_CATEGORIES
    )["id"]


    search = (
        generate_search_state()
    )


    emojis = (
        generate_emoji_items()
    )


    stickers = (
        generate_sticker_items()
    )


    gifs = (
        generate_gif_items()
    )


    return {

        # --------------------------------------------------
        # Page
        # --------------------------------------------------

        "title":
            "Emoji, GIFs and stickers",

        "active_tab":
            active_tab,

        # --------------------------------------------------
        # Main Tabs
        # --------------------------------------------------

        "tabs":
            PICKER_TABS,

        # --------------------------------------------------
        # Search
        # --------------------------------------------------

        "search":
            search,

        "search_placeholder":
            "Search",

        # --------------------------------------------------
        # Emoji
        # --------------------------------------------------

        "emoji_categories":
            EMOJI_CATEGORIES,

        "selected_category":
            selected_category,

        "emojis":
            emojis,

        "emoji_count":
            len(emojis),

        # --------------------------------------------------
        # Stickers
        # --------------------------------------------------

        "stickers":
            stickers,

        "sticker_count":
            len(stickers),

        # --------------------------------------------------
        # GIFs
        # --------------------------------------------------

        "gifs":
            gifs,

        "gif_count":
            len(gifs),

        # --------------------------------------------------
        # UI State
        # --------------------------------------------------

        "show_backspace":
            active_tab == "emoji",

        "show_favorites":
            active_tab in {
                "gifs",
                "stickers",
            },

        "show_recent":
            True,

        # --------------------------------------------------
        # Background chat
        # --------------------------------------------------

        "background": {

            "show":
                True,

            "composer_text":
                "",

            "keyboard_open":
                True,
        },
    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_emoji_sticker_gif_page()
    )


    print(
        "\nEMOJI / STICKER / GIF PICKER"
    )

    print(
        "Active tab:",
        page["active_tab"]
    )

    print(
        "Search active:",
        page["search"]["active"]
    )

    print(
        "Search query:",
        page["search"]["query"]
    )

    print(
        "Category:",
        page["selected_category"]
    )

    print(
        "Emoji:",
        page["emoji_count"]
    )

    print(
        "Stickers:",
        page["sticker_count"]
    )

    print(
        "GIFs:",
        page["gif_count"]
    )