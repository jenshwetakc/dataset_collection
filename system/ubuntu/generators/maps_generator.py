from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# States
# ==========================================================

MAPS_STATES = [

    "default_map",

    "search_open",

    "search_results",

    "place_selected",

    "route_planner",

    "route_results",

    "navigation_mode",

    "saved_places",

    "layers_menu",

    "location_permission",

    "offline_warning",

    "clear_route_dialog",
]


# ==========================================================
# Places
# ==========================================================

PLACE_NAMES = [

    "Central Library",

    "City Hall",

    "Coffee House",

    "University Campus",

    "Museum of Art",

    "Riverside Park",

    "Train Station",

    "Shopping Center",

    "Research Building",

    "Public Garden",

    "Community Center",

    "Science Museum",
]


# ==========================================================
# Categories
# ==========================================================

PLACE_CATEGORIES = [

    {
        "name":
            "Restaurants",

        "icon":
            "restaurant",
    },

    {
        "name":
            "Cafes",

        "icon":
            "local_cafe",
    },

    {
        "name":
            "Shopping",

        "icon":
            "shopping_bag",
    },

    {
        "name":
            "Hotels",

        "icon":
            "hotel",
    },

    {
        "name":
            "Parks",

        "icon":
            "park",
    },

    {
        "name":
            "Transit",

        "icon":
            "train",
    },
]


# ==========================================================
# Map Layers
# ==========================================================

MAP_LAYERS = [

    {
        "label":
            "Default",

        "icon":
            "map",

        "selected":
            False,
    },

    {
        "label":
            "Satellite",

        "icon":
            "satellite_alt",

        "selected":
            False,
    },

    {
        "label":
            "Transit",

        "icon":
            "directions_transit",

        "selected":
            False,
    },

    {
        "label":
            "Cycling",

        "icon":
            "directions_bike",

        "selected":
            False,
    },
]


# ==========================================================
# Route Modes
# ==========================================================

ROUTE_MODES = [

    {
        "name":
            "Driving",

        "icon":
            "directions_car",
    },

    {
        "name":
            "Walking",

        "icon":
            "directions_walk",
    },

    {
        "name":
            "Transit",

        "icon":
            "directions_transit",
    },

    {
        "name":
            "Cycling",

        "icon":
            "directions_bike",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_place(
    index: int,
) -> dict:

    name = random.choice(
        PLACE_NAMES
    )


    category = random.choice(
        [
            "Cafe",
            "Restaurant",
            "Park",
            "Museum",
            "University",
            "Shopping",
            "Transit",
        ]
    )


    return {

        "id":
            index,

        "name":
            name,

        "category":
            category,

        "address":
            fake.street_address(),

        "distance":
            round(
                random.uniform(
                    0.2,
                    8.5,
                ),
                1,
            ),

        "rating":
            round(
                random.uniform(
                    3.5,
                    5.0,
                ),
                1,
            ),

        "reviews":
            random.randint(
                20,
                3200,
            ),

        "open":
            random.random()
            < 0.80,

        "saved":
            random.random()
            < 0.22,

        "selected":
            False,

        "icon":
            random.choice(
                [
                    "location_on",
                    "restaurant",
                    "local_cafe",
                    "park",
                    "museum",
                    "school",
                ]
            ),

        "map_x":
            random.randint(
                16,
                86,
            ),

        "map_y":
            random.randint(
                15,
                82,
            ),
    }


def generate_places(
    minimum: int = 8,
    maximum: int = 16,
) -> list[dict]:

    return [

        generate_place(
            index
        )

        for index in range(
            random.randint(
                minimum,
                maximum,
            )
        )
    ]


# ==========================================================
# Route
# ==========================================================

def generate_route_steps() -> list[dict]:

    instructions = [

        "Head north on Main Street",

        "Turn right onto Central Avenue",

        "Continue straight for 800 m",

        "Turn left at the traffic lights",

        "Take the second exit at the roundabout",

        "Continue toward City Center",

        "Destination will be on your right",
    ]


    count = random.randint(
        4,
        7,
    )


    selected = instructions[
        :count
    ]


    return [

        {
            "instruction":
                text,

            "distance":
                random.choice(
                    [
                        "120 m",
                        "250 m",
                        "450 m",
                        "800 m",
                        "1.2 km",
                    ]
                ),

            "icon":
                random.choice(
                    [
                        "straight",
                        "turn_left",
                        "turn_right",
                        "roundabout_right",
                    ]
                ),
        }

        for text in selected
    ]


def generate_routes() -> list[dict]:

    routes = []


    for index in range(
        random.randint(
            2,
            3,
        )
    ):

        minutes = random.randint(
            12,
            48,
        )


        routes.append(
            {
                "id":
                    index,

                "time":
                    f"{minutes} min",

                "distance":
                    f"{random.uniform(2.4, 18.0):.1f} km",

                "description":
                    random.choice(
                        [
                            "Fastest route",
                            "Avoids highways",
                            "Less traffic",
                            "Via city center",
                        ]
                    ),

                "selected":
                    index == 0,
            }
        )


    return routes


# ==========================================================
# Saved Places
# ==========================================================

def generate_saved_places(
    places: list[dict],
) -> list[dict]:

    saved = [

        place

        for place
        in places

        if place[
            "saved"
        ]
    ]


    if len(
        saved
    ) < 3:

        saved = random.sample(
            places,
            k=min(
                4,
                len(
                    places
                ),
            ),
        )


    return saved


# ==========================================================
# Main Generator
# ==========================================================

def generate_maps_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            MAPS_STATES
        )


    if state not in MAPS_STATES:

        raise ValueError(
            f"Unknown Maps state: "
            f"{state}"
        )


    places = generate_places()


    selected_place = None


    if state in {
        "place_selected",
        "route_planner",
        "route_results",
        "navigation_mode",
    }:

        selected_place = random.choice(
            places
        )

        selected_place[
            "selected"
        ] = True


    # ======================================================
    # Search
    # ======================================================

    search_query = ""


    if state in {
        "search_open",
        "search_results",
    }:

        search_query = random.choice(
            [
                "coffee",
                "museum",
                "park",
                "university",
                "restaurant",
            ]
        )


    search_results = []


    if state == "search_results":

        search_results = random.sample(
            places,
            k=min(
                random.randint(
                    4,
                    7,
                ),
                len(
                    places
                ),
            ),
        )


    # ======================================================
    # Route
    # ======================================================

    route_mode = random.choice(
        ROUTE_MODES
    )


    origin = random.choice(
        [
            "Current location",
            "Home",
            "Central Station",
            "University",
        ]
    )


    destination = (
        selected_place[
            "name"
        ]
        if selected_place
        else random.choice(
            PLACE_NAMES
        )
    )


    # ======================================================
    # Layers
    # ======================================================

    layers = [

        dict(
            layer
        )

        for layer in MAP_LAYERS
    ]


    selected_layer = random.randrange(
        len(
            layers
        )
    )


    for index, layer in enumerate(
        layers
    ):

        layer[
            "selected"
        ] = (
            index
            == selected_layer
        )


    # ======================================================
    # Result
    # ======================================================

    return {

        "state":
            state,

        "places":
            places,

        "selected_place":
            selected_place,

        "categories":
            [
                dict(
                    entry
                )
                for entry
                in PLACE_CATEGORIES
            ],

        "search_query":
            search_query,

        "search_results":
            search_results,

        "saved_places":
            generate_saved_places(
                places
            ),

        "route_modes":
            [
                dict(
                    mode
                )
                for mode
                in ROUTE_MODES
            ],

        "route_mode":
            dict(
                route_mode
            ),

        "origin":
            origin,

        "destination":
            destination,

        "routes":
            generate_routes(),

        "route_steps":
            generate_route_steps(),

        "layers":
            layers,

        "zoom":
            random.randint(
                10,
                16,
            ),

        "current_x":
            random.randint(
                35,
                65,
            ),

        "current_y":
            random.randint(
                35,
                65,
            ),
    }