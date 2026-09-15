from __future__ import annotations

import random

from faker import Faker

from social_media.canva.generators.media_generator import (
    get_random_avatar,
    get_random_design_thumbnail,
)


fake = Faker()


# ==========================================================
# Pools
# ==========================================================

PROJECT_TYPES = [
    "Presentation",
    "Instagram Post",
    "Poster",
    "Document",
    "Video",
    "Logo",
    "Whiteboard",
    "Website",
    "Story",
    "Flyer",
]


FOLDER_NAMES = [
    "Marketing",
    "Brand Assets",
    "Social Media",
    "Client Work",
    "Presentations",
    "Campaigns",
    "Templates",
    "Personal",
    "Research",
    "Archive",
]


FILTERS = [
    "All",
    "Owned by me",
    "Shared with me",
    "Starred",
]


SORT_OPTIONS = [
    "Last modified",
    "Name",
    "Created date",
]


# ==========================================================
# Folders
# ==========================================================

def generate_folders(
    count: int | None = None,
) -> list[dict]:

    if count is None:
        count = random.randint(
            4,
            7,
        )

    names = random.sample(
        FOLDER_NAMES,
        k=min(
            count,
            len(FOLDER_NAMES),
        ),
    )

    return [
        {
            "id":
                index,

            "name":
                name,

            "item_count":
                random.randint(
                    3,
                    48,
                ),

            "shared":
                random.random()
                < 0.30,
        }
        for index, name
        in enumerate(
            names
        )
    ]


# ==========================================================
# Project Items
# ==========================================================

def generate_projects(
    count: int | None = None,
) -> list[dict]:

    if count is None:
        count = random.randint(
            10,
            18,
        )

    projects = []

    for index in range(
        count
    ):

        owner_name = (
            fake.name()
            if random.random() < 0.30
            else "You"
        )

        projects.append(
            {
                "id":
                    index,

                "title":
                    random.choice(
                        [
                            fake.catch_phrase(),
                            f"{fake.word().title()} Campaign",
                            f"{fake.company()} Proposal",
                            f"{fake.month_name()} Content Plan",
                            "Untitled design",
                        ]
                    ),

                "type":
                    random.choice(
                        PROJECT_TYPES
                    ),

                "thumbnail":
                    get_random_design_thumbnail(),

                "owner":
                    owner_name,

                "avatar":
                    (
                        get_random_avatar()
                        if owner_name != "You"
                        else None
                    ),

                "modified":
                    random.choice(
                        [
                            "Just now",
                            "12 minutes ago",
                            "Yesterday",
                            "2 days ago",
                            "Last week",
                            "Aug 21",
                        ]
                    ),

                "shared":
                    random.random()
                    < 0.35,

                "starred":
                    random.random()
                    < 0.15,
            }
        )

    return projects


# ==========================================================
# Main Generator
# ==========================================================

def generate_projects_data() -> dict:

    selected_filter = random.choice(
        FILTERS
    )

    return {

        "title":
            random.choice(
                [
                    "Projects",
                    "Your projects",
                    "Designs and folders",
                ]
            ),

        "subtitle":
            random.choice(
                [
                    "Everything you've created in one place.",
                    "Browse and manage your designs.",
                    "Keep your work organized.",
                ]
            ),

        "search": {
            "placeholder":
                random.choice(
                    [
                        "Search projects",
                        "Search designs and folders",
                        "Find your content",
                    ]
                ),
        },

        "filters": [
            {
                "label":
                    label,

                "selected":
                    label
                    == selected_filter,
            }
            for label
            in FILTERS
        ],

        "sort": {
            "selected":
                random.choice(
                    SORT_OPTIONS
                ),

            "options":
                SORT_OPTIONS,
        },

        "view_mode":
            random.choice(
                [
                    "grid",
                    "list",
                ]
            ),

        "folders":
            generate_folders(),

        "projects":
            generate_projects(),

        "actions": {
            "new_folder":
                "New folder",

            "create_design":
                "Create design",
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_projects_data()
    )