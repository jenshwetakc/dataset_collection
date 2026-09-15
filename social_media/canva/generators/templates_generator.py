from __future__ import annotations

import random

from faker import Faker

from social_media.canva.generators.media_generator import (
    get_random_template_image,
)


fake = Faker()


# ==========================================================
# Pools
# ==========================================================

SEARCH_TERMS = [
    "presentation",
    "instagram post",
    "marketing",
    "resume",
    "poster",
    "business proposal",
    "birthday invitation",
    "social media",
    "portfolio",
    "education",
    "travel",
    "food menu",
]


CATEGORIES = [
    "All",
    "Presentations",
    "Social media",
    "Video",
    "Print",
    "Documents",
    "Education",
    "Business",
    "Marketing",
]


STYLES = [
    "Minimalist",
    "Modern",
    "Elegant",
    "Bold",
    "Professional",
    "Creative",
    "Colorful",
    "Simple",
]


FORMATS = [
    "Presentation",
    "Instagram Post",
    "Poster",
    "Story",
    "Flyer",
    "Document",
    "Video",
    "Resume",
]


COLORS = [
    "Multicolor",
    "Blue",
    "Purple",
    "Green",
    "Orange",
    "Pink",
    "Red",
    "Neutral",
]


TEMPLATE_NAMES = [
    "Modern Business Proposal",
    "Minimal Marketing Presentation",
    "Creative Social Media Post",
    "Elegant Portfolio",
    "Bold Product Launch",
    "Weekly Planner",
    "Professional Pitch Deck",
    "Travel Story",
    "Restaurant Promotion",
    "Event Announcement",
    "Startup Presentation",
    "Brand Strategy",
    "Simple Resume",
    "Education Presentation",
    "Summer Campaign",
    "Modern Newsletter",
]


# ==========================================================
# Categories
# ==========================================================

def generate_categories() -> list[dict]:

    selected = random.choice(
        CATEGORIES
    )

    return [
        {
            "label":
                category,

            "selected":
                category == selected,
        }
        for category
        in CATEGORIES
    ]


# ==========================================================
# Filters
# ==========================================================

def generate_filter_group(
    values: list[str],
) -> list[dict]:

    selected_count = random.randint(
        0,
        min(
            2,
            len(values),
        ),
    )

    selected = set(
        random.sample(
            values,
            selected_count,
        )
    )

    return [
        {
            "label":
                value,

            "selected":
                value in selected,
        }
        for value
        in values
    ]


# ==========================================================
# Results
# ==========================================================

def generate_template_results(
    count: int | None = None,
) -> list[dict]:

    if count is None:

        count = random.randint(
            16,
            28,
        )

    results = []

    for index in range(
        count
    ):

        results.append(
            {
                "id":
                    index,

                "title":
                    random.choice(
                        TEMPLATE_NAMES
                    ),

                "author":
                    random.choice(
                        [
                            "Canva Creative Studio",
                            fake.company(),
                            fake.name(),
                            "Design Lab",
                            "Studio North",
                        ]
                    ),

                "format":
                    random.choice(
                        FORMATS
                    ),

                "style":
                    random.choice(
                        STYLES
                    ),

                "image":
                    get_random_template_image(),

                "premium":
                    random.random()
                    < 0.24,

                "new":
                    random.random()
                    < 0.10,

                "favorite":
                    random.random()
                    < 0.14,
            }
        )

    return results


# ==========================================================
# Featured
# ==========================================================

def generate_featured() -> list[dict]:

    count = random.randint(
        2,
        4,
    )

    return [
        {
            "title":
                random.choice(
                    [
                        "Trending presentation templates",
                        "Fresh social media ideas",
                        "Designs for your next campaign",
                        "Popular business templates",
                    ]
                ),

            "subtitle":
                random.choice(
                    [
                        "Start quickly with professionally designed layouts.",
                        "Explore popular designs picked for you.",
                        "Create something polished in minutes.",
                    ]
                ),

            "image":
                get_random_template_image(),
        }
        for _
        in range(
            count
        )
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_templates_data() -> dict:

    query = random.choice(
        SEARCH_TERMS
    )

    return {

        "query":
            query,

        "search": {
            "placeholder":
                "Search thousands of templates",
        },

        "result_title":
            random.choice(
                [
                    f"Templates for “{query}”",
                    f"Search results for “{query}”",
                    f"Explore {query} templates",
                ]
            ),

        "result_count":
            random.randint(
                240,
                7200,
            ),

        "categories":
            generate_categories(),

        "filters": {

            "style":
                generate_filter_group(
                    STYLES
                ),

            "format":
                generate_filter_group(
                    FORMATS
                ),

            "color":
                generate_filter_group(
                    COLORS
                ),
        },

        "sort":
            random.choice(
                [
                    "Recommended",
                    "Most popular",
                    "Newest",
                ]
            ),

        "featured":
            generate_featured(),

        "results":
            generate_template_results(),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_templates_data()
    )