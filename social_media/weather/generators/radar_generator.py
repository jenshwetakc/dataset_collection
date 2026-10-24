from __future__ import annotations

import random

from copy import deepcopy


RADAR_STATES = [
    "precipitation",
    "satellite",
    "temperature",
    "storm_tracking",
    "playing",
    "layers_dialog",
    "location_search",
]

LAYERS = [
    {
        "key": "precipitation",
        "label": "Precipitation",
        "icon": "rainy",
        "description": "Rain and snow intensity",
    },
    {
        "key": "satellite",
        "label": "Satellite",
        "icon": "satellite_alt",
        "description": "Synthetic cloud coverage",
    },
    {
        "key": "temperature",
        "label": "Temperature",
        "icon": "thermostat",
        "description": "Surface temperature",
    },
]

CITIES = [
    {"name": "Seoul", "x": 47, "y": 31},
    {"name": "Incheon", "x": 29, "y": 38},
    {"name": "Suwon", "x": 48, "y": 55},
    {"name": "Chuncheon", "x": 74, "y": 24},
    {"name": "Wonju", "x": 76, "y": 54},
    {"name": "Daejeon", "x": 54, "y": 81},
]


def generate_radar_data(
    *,
    sample_index: int,
) -> dict:
    cities = deepcopy(CITIES)

    for city in cities:
        city["temperature"] = f"{random.randint(12, 28)}°"

    return {
        "sample_index": sample_index,
        "location": "Seoul, South Korea",
        "cities": cities,
        "layers": deepcopy(LAYERS),
        "show_city_labels": random.choice([True, False]),
        "show_storm_tracks": False,
        "opacity": random.choice([60, 75, 90]),
        "frames": [
            "14:00",
            "14:10",
            "14:20",
            "14:30",
            "14:40",
            "14:50",
        ],
        "search_query": "Seo",
        "search_results": [
            {
                "name": "Seoul",
                "region": "South Korea",
            },
            {
                "name": "Seongnam",
                "region": "Gyeonggi, South Korea",
            },
            {
                "name": "Seosan",
                "region": "South Chungcheong, South Korea",
            },
        ],
        "cells": [
            {
                "id": index,
                "x": random.randint(10, 86),
                "y": random.randint(10, 85),
                "rx": random.randint(7, 15),
                "ry": random.randint(5, 11),
                "rotation": random.randint(-55, 55),
                "intensity": random.choice([
                    "light",
                    "moderate",
                    "heavy",
                ]),
            }
            for index in range(random.randint(7, 11))
        ],
        "storms": [
            {
                "id": 0,
                "name": "Cell A",
                "x": 38,
                "y": 44,
                "direction": "Northeast",
                "speed": "28 km/h",
                "arrival": "Approximately 20 minutes",
            },
            {
                "id": 1,
                "name": "Cell B",
                "x": 67,
                "y": 65,
                "direction": "East",
                "speed": "34 km/h",
                "arrival": "Approximately 35 minutes",
            },
        ],
    }


def apply_radar_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in RADAR_STATES:
        raise ValueError(
            f"Unknown radar state: {state!r}"
        )

    data = deepcopy(base_data)

    layer = (
        state
        if state in {
            "precipitation",
            "satellite",
            "temperature",
        }
        else "precipitation"
    )

    data.update({
        "state": state,
        "active_layer": layer,
        "active_layer_label": next(
            item["label"]
            for item in data["layers"]
            if item["key"] == layer
        ),
        "popup_visible": state in {
            "layers_dialog",
            "location_search",
        },
        "popup_type": (
            state
            if state in {
                "layers_dialog",
                "location_search",
            }
            else None
        ),
        "playing": state == "playing",
        "frame_index": 3 if state == "playing" else 5,
        "show_storm_tracks": state == "storm_tracking",
    })

    if state == "temperature":
        data["show_city_labels"] = True

    data["frame_time"] = data["frames"][
        data["frame_index"]
    ]

    data["timeline_percent"] = round(
        data["frame_index"]
        / (len(data["frames"]) - 1)
        * 100
    )

    if layer == "satellite":
        legend = [
            {"label": "Thin cloud", "color": "#AAB4BF"},
            {"label": "Cloud", "color": "#D8DFE5"},
            {"label": "Dense cloud", "color": "#FFFFFF"},
        ]

    elif layer == "temperature":
        legend = [
            {"label": "Cool", "color": "#4179C6"},
            {"label": "Mild", "color": "#E4CD67"},
            {"label": "Warm", "color": "#D46D52"},
        ]

    else:
        legend = [
            {"label": "Light", "color": "#4EAF76"},
            {"label": "Moderate", "color": "#E7C653"},
            {"label": "Heavy", "color": "#D75B55"},
        ]

    data["legend"] = legend

    return data