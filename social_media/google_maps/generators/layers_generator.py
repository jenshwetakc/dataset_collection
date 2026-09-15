from __future__ import annotations

import random

from social_media.google_maps.generators.home_generator import (
    generate_buildings,
    generate_map_labels,
    generate_markers,
    generate_parks,
    generate_roads,
    generate_water,
)


# ==========================================================
# Map Types
# ==========================================================

MAP_TYPES = [
    {
        "key": "default",
        "label": "Default",
        "icon": "map",
    },
    {
        "key": "satellite",
        "label": "Satellite",
        "icon": "satellite_alt",
    },
    {
        "key": "terrain",
        "label": "Terrain",
        "icon": "terrain",
    },
]


# ==========================================================
# Map Details
# ==========================================================

MAP_DETAILS = [
    {
        "key": "traffic",
        "label": "Traffic",
        "icon": "traffic",
    },
    {
        "key": "transit",
        "label": "Transit",
        "icon": "train",
    },
    {
        "key": "bicycling",
        "label": "Bicycling",
        "icon": "directions_bike",
    },
    {
        "key": "street_view",
        "label": "Street View",
        "icon": "streetview",
    },
    {
        "key": "air_quality",
        "label": "Air quality",
        "icon": "air",
    },
]


# ==========================================================
# Map Preview
# ==========================================================

def generate_map_preview(
    map_type: str,
) -> dict:

    return {
        "type":
            map_type,

        "roads":
            random.randint(
                3,
                7,
            ),

        "blocks":
            random.randint(
                4,
                10,
            ),

        "has_water":
            random.random()
            < 0.45,

        "has_park":
            random.random()
            < 0.55,
    }


# ==========================================================
# Layers Data
# ==========================================================

def generate_layers_data() -> dict:

    selected_type = random.choice(
        MAP_TYPES
    )

    map_types = [
        {
            **item,
            "selected":
                item["key"]
                == selected_type["key"],

            "preview":
                generate_map_preview(
                    item["key"]
                ),
        }
        for item in MAP_TYPES
    ]

    details = []

    for item in MAP_DETAILS:

        enabled_probability = {
            "traffic": 0.55,
            "transit": 0.25,
            "bicycling": 0.20,
            "street_view": 0.35,
            "air_quality": 0.18,
        }.get(
            item["key"],
            0.25,
        )

        details.append(
            {
                **item,
                "enabled":
                    random.random()
                    < enabled_probability,
            }
        )

    return {

        "map_types":
            map_types,

        "selected_map_type":
            selected_type["key"],

        "details":
            details,

        "map": {
            "roads":
                generate_roads(
                    count=random.randint(
                        18,
                        30,
                    )
                ),

            "buildings":
                generate_buildings(
                    count=random.randint(
                        30,
                        50,
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
                        15,
                    )
                ),

            "markers":
                generate_markers(
                    count=random.randint(
                        5,
                        10,
                    )
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_layers_data()

    print(
        "\n=============================="
    )

    print(
        "LAYERS UI"
    )

    print(
        "=============================="
    )

    print(
        "Selected type:",
        data[
            "selected_map_type"
        ],
    )

    print(
        "Enabled details:",
        [
            item["key"]
            for item
            in data["details"]
            if item["enabled"]
        ],
    )