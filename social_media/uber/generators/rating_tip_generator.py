from __future__ import annotations

import random

from faker import Faker

from social_media.uber.generators.media_generator import (
    get_random_driver_image,
    get_random_vehicle_image,
)


fake = Faker()


# ==========================================================
# Helpers
# ==========================================================

def generate_driver() -> dict:

    return {
        "name":
            fake.first_name(),

        "rating":
            round(
                random.uniform(
                    4.7,
                    5.0,
                ),
                2,
            ),

        "trips":
            random.randint(
                300,
                6200,
            ),

        "avatar":
            get_random_driver_image(),
    }


def generate_trip() -> dict:

    subtotal = round(
        random.uniform(
            8.0,
            55.0,
        ),
        2,
    )

    service_fee = round(
        random.uniform(
            0.8,
            4.5,
        ),
        2,
    )

    discount = random.choice(
        [
            0.0,
            0.0,
            round(
                random.uniform(
                    1.0,
                    8.0,
                ),
                2,
            ),
        ]
    )

    total = max(
        0.0,
        subtotal
        + service_fee
        - discount,
    )


    return {
        "ride_type":
            random.choice(
                [
                    "UberX",
                    "Comfort",
                    "Uber Green",
                    "UberXL",
                ]
            ),

        "duration":
            f"{random.randint(8, 48)} min",

        "distance":
            f"{random.uniform(2.0, 24.0):.1f} km",

        "pickup":
            f"{fake.street_name()}, {fake.city()}",

        "destination":
            f"{fake.street_name()}, {fake.city()}",

        "vehicle":
            random.choice(
                [
                    "Hyundai Sonata",
                    "Kia K5",
                    "Toyota Camry",
                    "Hyundai Ioniq",
                    "Kia Carnival",
                ]
            ),

        "vehicle_image":
            get_random_vehicle_image(),

        "subtotal":
            f"${subtotal:.2f}",

        "service_fee":
            f"${service_fee:.2f}",

        "discount":
            (
                f"-${discount:.2f}"
                if discount > 0
                else None
            ),

        "total":
            f"${total:.2f}",
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_rating_tip_data() -> dict:

    selected_rating = random.choice(
        [
            0,
            4,
            5,
            5,
        ]
    )

    tip_options = [
        {
            "label":
                "10%",

            "selected":
                False,
        },
        {
            "label":
                "15%",

            "selected":
                False,
        },
        {
            "label":
                "20%",

            "selected":
                False,
        },
    ]


    selected_tip_index = random.choice(
        [
            None,
            None,
            0,
            1,
            2,
        ]
    )


    if selected_tip_index is not None:

        tip_options[
            selected_tip_index
        ][
            "selected"
        ] = True


    return {

        "title":
            random.choice(
                [
                    "How was your ride?",
                    "Rate your trip",
                    "How did your trip go?",
                ]
            ),

        "subtitle":
            random.choice(
                [
                    "Your feedback helps improve the experience.",
                    "Let us know how your ride went.",
                    "Rate your driver and add an optional tip.",
                ]
            ),

        "driver":
            generate_driver(),

        "trip":
            generate_trip(),

        "selected_rating":
            selected_rating,

        "tip_options":
            tip_options,

        "custom_tip_placeholder":
            "Custom amount",

        "feedback_tags":
            random.sample(
                [
                    "Great driving",
                    "Friendly",
                    "Clean car",
                    "Smooth ride",
                    "Great conversation",
                    "Professional",
                ],
                k=random.randint(
                    3,
                    5,
                ),
            ),

        "show_receipt":
            random.choice(
                [
                    True,
                    True,
                    False,
                ]
            ),

        "primary_action":
            "Submit rating",

        "secondary_action":
            random.choice(
                [
                    "No thanks",
                    "Skip",
                    "Not now",
                ]
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(
        generate_rating_tip_data()
    )