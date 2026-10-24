from __future__ import annotations

import random

from faker import Faker

from social_media.common.media_generator import (
    ASSETS_ROOT,
    get_random_image,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

GOOGLE_SLIDES_STATES = [
    "editing_title_slide",
    "editing_content_slide",
    "theme_panel_open",
    "insert_menu_open",
    "speaker_notes_open",
    "present_mode",
    "share_dialog_open",
]


# ==========================================================
# Constants
# ==========================================================

PRESENTATION_TITLES = [
    "Quarterly Product Strategy",
    "Design Systems Review",
    "Research Findings",
    "Sustainable Growth Plan",
    "Customer Journey Workshop",
    "AI Product Roadmap",
    "Market Opportunity Analysis",
    "Team Planning Session",
]

ACCENT_COLORS = [
    "#1A73E8",
    "#9334E6",
    "#E37400",
    "#0F9D58",
    "#D93025",
    "#00838F",
]

SLIDE_BACKGROUNDS = [
    "#FFFFFF",
    "#F8F9FA",
    "#E8F0FE",
    "#FCE8E6",
    "#E6F4EA",
    "#FFF7E0",
]

AVATAR_COLORS = [
    "#1A73E8",
    "#9334E6",
    "#E37400",
    "#0F9D58",
    "#D93025",
]

THEME_NAMES = [
    "Simple Light",
    "Focus",
    "Material",
    "Gradient",
    "Gallery",
]


# ==========================================================
# Helpers
# ==========================================================

def get_initials(
    name: str,
) -> str:
    words = [
        word
        for word in name.split()
        if word
    ]

    if not words:
        return "U"

    return "".join(
        word[0].upper()
        for word in words[:2]
    )


def get_slide_image() -> str | None:
    directories = [
        ASSETS_ROOT / "photos",
        ASSETS_ROOT / "images",
        ASSETS_ROOT,
    ]

    for directory in directories:
        if directory.exists():
            image = get_random_image(directory)

            if image is not None:
                return image

    return None


def generate_collaborators() -> list[dict]:
    collaborators = []

    for index in range(
        random.randint(2, 5)
    ):
        name = fake.name()

        collaborators.append(
            {
                "id": f"person_{index}",
                "name": name,
                "initials": get_initials(name),
                "color": random.choice(
                    AVATAR_COLORS
                ),
                "active": index == 0,
            }
        )

    return collaborators


def generate_bullets() -> list[str]:
    return [
        fake.sentence(
            nb_words=random.randint(5, 10),
        ).rstrip(".")
        for _ in range(
            random.randint(3, 5)
        )
    ]


def generate_chart_data() -> list[dict]:
    return [
        {
            "label": label,
            "value": random.randint(25, 95),
            "color": random.choice(
                ACCENT_COLORS
            ),
        }
        for label in [
            "Q1",
            "Q2",
            "Q3",
            "Q4",
        ]
    ]


# ==========================================================
# Slide Factories
# ==========================================================

def generate_title_slide(
    title: str,
    accent_color: str,
) -> dict:
    subtitle = (
        f"{fake.catch_phrase()} · "
        f"{fake.month_name()} "
        f"{random.randint(2025, 2027)}"
    )

    return {
        "id": "slide_1",
        "number": 1,
        "layout": "title",
        "title": title,
        "subtitle": subtitle,
        "background": random.choice(
            SLIDE_BACKGROUNDS
        ),
        "accent_color": accent_color,
        "notes": (
            "Welcome the audience and introduce the "
            "purpose of this presentation."
        ),
    }


def generate_agenda_slide(
    number: int,
    accent_color: str,
) -> dict:
    return {
        "id": f"slide_{number}",
        "number": number,
        "layout": "agenda",
        "title": "Today’s agenda",
        "background": "#FFFFFF",
        "accent_color": accent_color,
        "agenda_items": [
            "Context and opportunity",
            "Key insights",
            "Proposed direction",
            "Next steps",
        ],
        "notes": (
            "Briefly walk through the presentation flow "
            "before moving into the details."
        ),
    }


def generate_content_slide(
    number: int,
    accent_color: str,
) -> dict:
    return {
        "id": f"slide_{number}",
        "number": number,
        "layout": "content",
        "title": fake.sentence(
            nb_words=random.randint(3, 6),
        ).rstrip("."),
        "background": "#FFFFFF",
        "accent_color": accent_color,
        "bullets": generate_bullets(),
        "notes": fake.paragraph(
            nb_sentences=2,
        ),
    }


def generate_image_slide(
    number: int,
    accent_color: str,
) -> dict:
    return {
        "id": f"slide_{number}",
        "number": number,
        "layout": "image",
        "title": fake.sentence(
            nb_words=random.randint(3, 6),
        ).rstrip("."),
        "caption": fake.sentence(
            nb_words=random.randint(8, 13),
        ),
        "background": "#FFFFFF",
        "accent_color": accent_color,
        "image_src": get_slide_image(),
        "notes": (
            "Use this visual to connect the discussion "
            "to a concrete example."
        ),
    }


def generate_chart_slide(
    number: int,
    accent_color: str,
) -> dict:
    return {
        "id": f"slide_{number}",
        "number": number,
        "layout": "chart",
        "title": random.choice(
            [
                "Momentum is building",
                "The opportunity is measurable",
                "Growth is concentrated",
                "Customer demand is accelerating",
            ]
        ),
        "background": "#FFFFFF",
        "accent_color": accent_color,
        "chart_data": generate_chart_data(),
        "insight": (
            f"+{random.randint(18, 64)}% "
            "compared with the previous period"
        ),
        "notes": fake.paragraph(
            nb_sentences=2,
        ),
    }


def generate_quote_slide(
    number: int,
    accent_color: str,
) -> dict:
    return {
        "id": f"slide_{number}",
        "number": number,
        "layout": "quote",
        "title": "What we heard",
        "background": random.choice(
            SLIDE_BACKGROUNDS
        ),
        "accent_color": accent_color,
        "quote": fake.sentence(
            nb_words=random.randint(12, 20),
        ),
        "speaker": fake.name(),
        "speaker_role": fake.job(),
        "notes": (
            "Read the quote and connect it to the "
            "product decision."
        ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_google_slides_data(
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:
    """
    Generate one synthetic Google Slides editor page.
    """

    del viewport

    state = state or random.choice(
        GOOGLE_SLIDES_STATES
    )

    if state not in GOOGLE_SLIDES_STATES:
        raise ValueError(
            f"Unsupported Google Slides state: {state}. "
            f"Expected one of: "
            f"{GOOGLE_SLIDES_STATES}"
        )

    accent_color = random.choice(
        ACCENT_COLORS
    )

    presentation_title = random.choice(
        PRESENTATION_TITLES
    )

    slides = [
        generate_title_slide(
            title=presentation_title,
            accent_color=accent_color,
        ),
        generate_agenda_slide(
            number=2,
            accent_color=accent_color,
        ),
        generate_content_slide(
            number=3,
            accent_color=accent_color,
        ),
        generate_image_slide(
            number=4,
            accent_color=accent_color,
        ),
        generate_chart_slide(
            number=5,
            accent_color=accent_color,
        ),
        generate_quote_slide(
            number=6,
            accent_color=accent_color,
        ),
    ]

    selected_slide_number = {
        "editing_title_slide": 1,
        "editing_content_slide": 3,
        "theme_panel_open": 4,
        "insert_menu_open": 3,
        "speaker_notes_open": 5,
        "present_mode": 1,
        "share_dialog_open": 3,
    }[state]

    selected_slide = next(
        slide
        for slide in slides
        if slide["number"]
        == selected_slide_number
    )

    collaborators = generate_collaborators()

    return {
        "app_name": "Google Slides",
        "state": state,
        "presentation": {
            "title": presentation_title,
            "folder_name": random.choice(
                [
                    "Work",
                    "Research",
                    "Product planning",
                    "Team presentations",
                ]
            ),
            "accent_color": accent_color,
            "saved_text": random.choice(
                [
                    "Saved to Drive",
                    "All changes saved",
                    "Last edit was seconds ago",
                ]
            ),
        },
        "slides": slides,
        "selected_slide": selected_slide,
        "selected_slide_number": selected_slide_number,
        "collaborators": collaborators,
        "toolbar_menus": [
            "File",
            "Edit",
            "View",
            "Insert",
            "Format",
            "Slide",
            "Arrange",
            "Tools",
            "Extensions",
            "Help",
        ],
        "toolbar_icons": [
            "↶",
            "↷",
            "⎙",
            "⎘",
            "⌕",
            "⌖",
            "T",
            "▣",
            "◯",
        ],
        "zoom_text": random.choice(
            [
                "75%",
                "90%",
                "100%",
                "125%",
            ]
        ),
        "selection": {
            "visible": state in [
                "editing_content_slide",
                "insert_menu_open",
            ],
            "type": random.choice(
                [
                    "text_box",
                    "image",
                    "chart",
                ]
            ),
        },
        "theme_panel": {
            "visible": state == "theme_panel_open",
            "themes": [
                {
                    "name": name,
                    "background": random.choice(
                        SLIDE_BACKGROUNDS
                    ),
                    "accent": (
                        accent_color
                        if index == 0
                        else random.choice(
                            ACCENT_COLORS
                        )
                    ),
                    "selected": index == 0,
                }
                for index, name
                in enumerate(THEME_NAMES)
            ],
        },
        "insert_menu": {
            "visible": state == "insert_menu_open",
            "menu_entries": [
                {
                    "label": "Image",
                    "symbol": "▣",
                },
                {
                    "label": "Text box",
                    "symbol": "T",
                },
                {
                    "label": "Shape",
                    "symbol": "◇",
                },
                {
                    "label": "Chart",
                    "symbol": "▥",
                },
                {
                    "label": "Table",
                    "symbol": "▦",
                },
                {
                    "label": "Video",
                    "symbol": "▶",
                },
            ],
        },
        "speaker_notes": {
            "visible": state == "speaker_notes_open",
            "text": selected_slide["notes"],
        },
        "share_dialog": {
            "visible": state == "share_dialog_open",
            "link_access": random.choice(
                [
                    "Restricted",
                    "Anyone with the link",
                ]
            ),
            "permission": random.choice(
                [
                    "Viewer",
                    "Commenter",
                    "Editor",
                ]
            ),
            "suggested_people": [
                {
                    "name": fake.name(),
                    "email": fake.email(),
                }
                for _ in range(2)
            ],
        },
        "present_mode": {
            "visible": state == "present_mode",
            "show_controls": True,
        },
    }