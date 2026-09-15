from __future__ import annotations

import random

from faker import Faker

from social_media.canva.generators.media_generator import (
    get_random_avatar,
    get_random_design_thumbnail,
    get_random_template_image,
)


fake = Faker()


# ==========================================================
# Static Pools
# ==========================================================

NAVIGATION_ITEMS = [
    {
        "label": "Home",
        "icon": "home",
    },
    {
        "label": "Projects",
        "icon": "folder",
    },
    {
        "label": "Templates",
        "icon": "dashboard",
    },
    {
        "label": "Brand",
        "icon": "diamond",
    },
]


DESIGN_TYPES = [
    {
        "label": "Presentation",
        "icon": "present_to_all",
    },
    {
        "label": "Social media",
        "icon": "share",
    },
    {
        "label": "Video",
        "icon": "movie",
    },
    {
        "label": "Print",
        "icon": "print",
    },
    {
        "label": "Website",
        "icon": "language",
    },
    {
        "label": "Photo",
        "icon": "photo",
    },
    {
        "label": "Whiteboard",
        "icon": "dashboard_customize",
    },
]


TEMPLATE_CATEGORIES = [
    "For you",
    "Presentations",
    "Social media",
    "Videos",
    "Documents",
    "Education",
    "Marketing",
    "Business",
]


TEMPLATE_TITLES = [
    "Minimal Business Presentation",
    "Modern Project Proposal",
    "Summer Social Media Post",
    "Product Launch Presentation",
    "Creative Portfolio",
    "Weekly Planner",
    "Marketing Strategy",
    "Instagram Story",
    "Event Invitation",
    "Travel Presentation",
    "Resume",
    "Class Presentation",
    "Pitch Deck",
    "Brand Guidelines",
    "Restaurant Menu",
    "Photo Collage",
    "YouTube Thumbnail",
    "Newsletter",
]


PROJECT_TYPES = [
    "Presentation",
    "Instagram Post",
    "Document",
    "Video",
    "Poster",
    "Logo",
    "Website",
    "Story",
]


# ==========================================================
# Navigation
# ==========================================================

def generate_navigation() -> list[dict]:

    active_index = random.randrange(
        len(
            NAVIGATION_ITEMS
        )
    )

    items = []

    for index, item in enumerate(
        NAVIGATION_ITEMS
    ):

        items.append(
            {
                **item,
                "active":
                    index
                    == active_index,
            }
        )

    return items


# ==========================================================
# Design Type Shortcuts
# ==========================================================

def generate_design_types() -> list[dict]:

    count = random.randint(
        5,
        len(
            DESIGN_TYPES
        ),
    )

    return [
        dict(item)
        for item in random.sample(
            DESIGN_TYPES,
            count,
        )
    ]


# ==========================================================
# Template Categories
# ==========================================================

def generate_template_categories() -> list[dict]:

    selected = random.choice(
        TEMPLATE_CATEGORIES
    )

    return [
        {
            "label": category,
            "selected":
                category
                == selected,
        }
        for category in TEMPLATE_CATEGORIES
    ]


# ==========================================================
# Templates
# ==========================================================

def generate_templates(
    count: int | None = None,
) -> list[dict]:

    if count is None:

        count = random.randint(
            8,
            14,
        )

    templates = []

    for index in range(
        count
    ):

        title = random.choice(
            TEMPLATE_TITLES
        )

        templates.append(
            {
                "id":
                    index,

                "title":
                    title,

                "subtitle":
                    random.choice(
                        [
                            "Presentation",
                            "Social post",
                            "Document",
                            "Video",
                            "Poster",
                            "Story",
                        ]
                    ),

                "image":
                    get_random_template_image(),

                "premium":
                    random.random()
                    < 0.20,

                "favorite":
                    random.random()
                    < 0.15,

                "new":
                    random.random()
                    < 0.12,
            }
        )

    return templates


# ==========================================================
# Recent Projects
# ==========================================================

def generate_recent_projects(
    count: int | None = None,
) -> list[dict]:

    if count is None:

        count = random.randint(
            5,
            10,
        )

    projects = []

    for index in range(
        count
    ):

        project_type = random.choice(
            PROJECT_TYPES
        )

        projects.append(
            {
                "id":
                    index,

                "title":
                    random.choice(
                        [
                            fake.catch_phrase(),
                            fake.company(),
                            fake.bs().title(),
                            f"{fake.word().title()} Project",
                            f"{fake.month_name()} Campaign",
                        ]
                    ),

                "type":
                    project_type,

                "image":
                    get_random_design_thumbnail(),

                "edited":
                    random.choice(
                        [
                            "Just now",
                            "5 minutes ago",
                            "Yesterday",
                            "2 days ago",
                            "Last week",
                        ]
                    ),

                "shared":
                    random.random()
                    < 0.35,
            }
        )

    return projects


# ==========================================================
# Suggested Search
# ==========================================================

def generate_search_placeholder() -> str:

    return random.choice(
        [
            "What will you design today?",
            "Search your content or Canva's",
            "Search templates and projects",
            "Try 'presentation'",
            "Search designs, templates and more",
        ]
    )


# ==========================================================
# Main Generator
# ==========================================================

def generate_home_data() -> dict:

    first_name = fake.first_name()

    return {

        "app_name":
            "Canva",

        "user": {

            "name":
                fake.name(),

            "first_name":
                first_name,

            "avatar":
                get_random_avatar(),

            "team":
                random.choice(
                    [
                        "Personal",
                        "Design team",
                        "Marketing team",
                        "My workspace",
                    ]
                ),
        },


        "navigation":
            generate_navigation(),


        "search": {

            "placeholder":
                generate_search_placeholder(),

            "query":
                "",
        },


        "hero": {

            "eyebrow":
                random.choice(
                    [
                        "Create anything",
                        "Start designing",
                        "Bring your ideas to life",
                    ]
                ),

            "title":
                random.choice(
                    [
                        f"What will you design today, "
                        f"{first_name}?",

                        "What will you create today?",

                        "Design anything you can imagine",

                        "Start creating something amazing",
                    ]
                ),
        },


        "design_types":
            generate_design_types(),


        "template_section": {

            "title":
                random.choice(
                    [
                        "Templates for you",
                        "Explore templates",
                        "Recommended templates",
                        "You might want to try...",
                    ]
                ),

            "categories":
                generate_template_categories(),

            "items":
                generate_templates(),
        },


        "recent_section": {

            "title":
                random.choice(
                    [
                        "Recent designs",
                        "Your recent projects",
                        "Continue designing",
                    ]
                ),

            "items":
                generate_recent_projects(),
        },


        "actions": {

            "create_text":
                "Create a design",

            "upload_text":
                "Upload",
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_home_data()
    )