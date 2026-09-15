from __future__ import annotations

import random

from faker import Faker

from social_media.google_maps.generators.home_generator import (
    generate_buildings,
    generate_map_labels,
    generate_parks,
    generate_roads,
    generate_water,
)

from social_media.google_maps.generators.media_generator import (
    get_random_avatar,
)


fake = Faker()


# ==========================================================
# Sharing Durations
# ==========================================================

SHARING_DURATIONS = [
    {
        "key": "15_minutes",
        "label": "15 minutes",
    },
    {
        "key": "1_hour",
        "label": "1 hour",
    },
    {
        "key": "8_hours",
        "label": "8 hours",
    },
    {
        "key": "until_off",
        "label": "Until you turn this off",
    },
]


# ==========================================================
# Sharing Methods
# ==========================================================

SHARING_METHODS = [
    {
        "key": "people",
        "label": "People",
        "icon": "group",
    },
    {
        "key": "link",
        "label": "Link",
        "icon": "link",
    },
]


# ==========================================================
# Generate Contact
# ==========================================================

def generate_contact(
    index: int,
) -> dict:

    name = fake.name()

    selected = (
        random.random()
        < 0.38
    )

    return {
        "id":
            index,

        "name":
            name,

        "first_name":
            name.split()[0],

        "avatar":
            get_random_avatar(),

        "selected":
            selected,

        "subtitle":
            random.choice(
                [
                    "Google Maps",
                    "Recent contact",
                    "Frequently contacted",
                    "Shared with you before",
                    fake.email(),
                ]
            ),

        "online":
            random.random()
            < 0.58,
    }


# ==========================================================
# Generate Existing Share
# ==========================================================

def generate_existing_share(
    index: int,
) -> dict:

    return {
        "id":
            index,

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),

        "remaining":
            random.choice(
                [
                    "12 min remaining",
                    "37 min remaining",
                    "1 hr remaining",
                    "4 hr remaining",
                    "Until turned off",
                ]
            ),

        "distance":
            random.choice(
                [
                    "0.4 mi away",
                    "1.2 mi away",
                    "2.8 mi away",
                    "5.1 mi away",
                ]
            ),
    }


# ==========================================================
# Map Person Markers
# ==========================================================

def generate_person_markers(
    count: int,
) -> list[dict]:

    markers = []

    for index in range(
        count
    ):

        markers.append(
            {
                "id":
                    index,

                "x":
                    random.randint(
                        10,
                        90,
                    ),

                "y":
                    random.randint(
                        18,
                        82,
                    ),

                "avatar":
                    get_random_avatar(),

                "label":
                    fake.first_name(),
            }
        )

    return markers


# ==========================================================
# Location Sharing Data
# ==========================================================

def generate_location_sharing_data() -> dict:

    selected_duration = random.choice(
        SHARING_DURATIONS
    )

    selected_method = random.choice(
        SHARING_METHODS
    )

    contacts = [
        generate_contact(
            index
        )
        for index
        in range(
            random.randint(
                7,
                12,
            )
        )
    ]

    # Always ensure at least one selected contact.
    if not any(
        contact["selected"]
        for contact
        in contacts
    ):

        random.choice(
            contacts
        )["selected"] = True

    existing_shares = [
        generate_existing_share(
            index
        )
        for index
        in range(
            random.randint(
                1,
                4,
            )
        )
    ]

    person_markers = (
        generate_person_markers(
            count=random.randint(
                3,
                6,
            )
        )
    )

    durations = [
        {
            **duration,
            "selected":
                duration["key"]
                == selected_duration["key"],
        }
        for duration
        in SHARING_DURATIONS
    ]

    methods = [
        {
            **method,
            "selected":
                method["key"]
                == selected_method["key"],
        }
        for method
        in SHARING_METHODS
    ]

    return {

        "title":
            "Location sharing",

        "sharing_enabled":
            random.random()
            < 0.35,

        "durations":
            durations,

        "selected_duration":
            selected_duration["key"],

        "methods":
            methods,

        "selected_method":
            selected_method["key"],

        "contacts":
            contacts,

        "selected_count":
            sum(
                1
                for contact
                in contacts
                if contact["selected"]
            ),

        "existing_shares":
            existing_shares,

        "map": {
            "roads":
                generate_roads(
                    count=random.randint(
                        18,
                        28,
                    )
                ),

            "buildings":
                generate_buildings(
                    count=random.randint(
                        28,
                        48,
                    )
                ),

            "parks":
                generate_parks(),

            "water":
                generate_water(),

            "labels":
                generate_map_labels(
                    count=random.randint(
                        8,
                        14,
                    )
                ),

            "people":
                person_markers,

            "current_location":
                {
                    "x":
                        random.randint(
                            42,
                            58,
                        ),

                    "y":
                        random.randint(
                            42,
                            62,
                        ),
                },
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_location_sharing_data()
    )

    print(
        "\n=============================="
    )

    print(
        "LOCATION SHARING"
    )

    print(
        "=============================="
    )

    print(
        "Contacts:",
        len(
            data["contacts"]
        ),
    )

    print(
        "Selected:",
        data["selected_count"],
    )

    print(
        "Duration:",
        data["selected_duration"],
    )