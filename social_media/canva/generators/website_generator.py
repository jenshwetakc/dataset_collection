from __future__ import annotations

import random

from faker import Faker

from social_media.canva.generators.media_generator import (
    get_random_avatar,
    get_random_background,
    get_random_photo,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

WEBSITE_STATES = [
    "editing",
    "mobile_preview",
    "publish_settings",
    "seo_settings",
    "published_success",
]


# ==========================================================
# Website Sections
# ==========================================================

SECTION_TYPES = [
    {
        "type": "hero",
        "icon": "web_asset",
        "label": "Hero",
    },
    {
        "type": "features",
        "icon": "grid_view",
        "label": "Features",
    },
    {
        "type": "gallery",
        "icon": "photo_library",
        "label": "Gallery",
    },
    {
        "type": "testimonial",
        "icon": "format_quote",
        "label": "Testimonials",
    },
    {
        "type": "contact",
        "icon": "mail",
        "label": "Contact",
    },
]


# ==========================================================
# Pages
# ==========================================================

def generate_pages() -> list[dict]:

    count = random.randint(
        2,
        5,
    )

    page_names = [
        "Home",
        "About",
        "Services",
        "Portfolio",
        "Contact",
    ]

    selected_index = random.randrange(
        count
    )

    return [
        {
            "name":
                page_names[index],

            "selected":
                index == selected_index,

            "published":
                random.random() > 0.20,
        }
        for index in range(count)
    ]


# ==========================================================
# Sections
# ==========================================================

def generate_sections() -> list[dict]:

    count = random.randint(
        4,
        7,
    )

    selected_index = random.randrange(
        count
    )

    sections = []

    for index in range(count):

        section_type = random.choice(
            SECTION_TYPES
        )

        sections.append(
            {
                **section_type,

                "selected":
                    index == selected_index,

                "visible":
                    random.random() > 0.08,
            }
        )

    return sections


# ==========================================================
# Features
# ==========================================================

def generate_features() -> list[dict]:

    return [
        {
            "title":
                random.choice(
                    [
                        "Simple workflow",
                        "Built for teams",
                        "Fast collaboration",
                        "Beautiful results",
                        "Easy publishing",
                    ]
                ),

            "description":
                fake.sentence(
                    nb_words=9
                ),

            "icon":
                random.choice(
                    [
                        "bolt",
                        "groups",
                        "auto_awesome",
                        "rocket_launch",
                        "verified",
                    ]
                ),
        }
        for _ in range(
            random.randint(
                3,
                4,
            )
        )
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_website_data(
    forced_state: str | None = None,
) -> dict:

    if forced_state is not None:

        if forced_state not in WEBSITE_STATES:

            raise ValueError(
                f"Unknown website state: "
                f"{forced_state}"
            )

        state = forced_state

    else:

        state = random.choice(
            WEBSITE_STATES
        )

    site_name = random.choice(
        [
            "Northstar Studio",
            "Nova Creative",
            "Luma Works",
            "Orbit Agency",
            "Bloom Studio",
        ]
    )

    domain_slug = (
        site_name
        .lower()
        .replace(
            " ",
            "-",
        )
    )

    return {

        "state":
            state,


        "document": {

            "name":
                f"{site_name} Website",

            "owner":
                fake.name(),

            "avatar":
                get_random_avatar(),
        },


        "site": {

            "name":
                site_name,

            "headline":
                random.choice(
                    [
                        "Ideas designed to move",
                        "Build something remarkable",
                        "Creative work that matters",
                        "Design your next chapter",
                        "Make your vision visible",
                    ]
                ),

            "subtitle":
                random.choice(
                    [
                        "We build thoughtful experiences for modern brands.",
                        "Strategy, design, and creativity in one place.",
                        "Helping ambitious teams turn ideas into experiences.",
                    ]
                ),

            "hero_image":
                (
                    get_random_background()
                    or get_random_photo()
                ),

            "cta":
                random.choice(
                    [
                        "Get started",
                        "View our work",
                        "Explore",
                        "Contact us",
                    ]
                ),
        },


        "pages":
            generate_pages(),


        "sections":
            generate_sections(),


        "features":
            generate_features(),


        "publish": {

            "domain":
                f"{domain_slug}.my.canva.site",

            "custom_domain":
                random.choice(
                    [
                        "",
                        f"www.{domain_slug}.com",
                    ]
                ),

            "resize_mobile":
                random.random() > 0.15,

            "navigation":
                random.random() > 0.25,

            "password":
                random.random() < 0.20,
        },


        "seo": {

            "title":
                f"{site_name} | Creative Studio",

            "description":
                fake.sentence(
                    nb_words=16
                ),

            "favicon":
                get_random_avatar(),

            "indexing":
                random.random() > 0.15,

            "social_preview":
                (
                    get_random_background()
                    or get_random_photo()
                ),
        },


        "published": {

            "url":
                f"https://{domain_slug}.my.canva.site",

            "time":
                random.choice(
                    [
                        "Just now",
                        "1 minute ago",
                        "3 minutes ago",
                    ]
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_website_data()
    )