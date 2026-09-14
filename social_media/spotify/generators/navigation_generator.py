from __future__ import annotations


def generate_navigation(
    selected: str = "home",
) -> dict:

    return {

        "selected":
            selected,

        "items": [

            {
                "name":
                    "Home",

                "semantic":
                    "home",

                "icon":
                    "home",
            },

            {
                "name":
                    "Search",

                "semantic":
                    "search",

                "icon":
                    "search",
            },

            {
                "name":
                    "Your Library",

                "semantic":
                    "library",

                "icon":
                    "library_music",
            },
        ],
    }