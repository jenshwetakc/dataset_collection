from __future__ import annotations

import random

from social_media.booking.generators.media_generator import (
    get_random_hotel_image,
)


# ==========================================================
# States
# ==========================================================

CHECKOUT_STATES = [
    "guest_details",
    "payment",
    "login_prompt",
    "validation_error",
    "confirmation",
    "mobile_summary_open",
]


HOTEL_NAMES = [
    "Grand Central Hotel",
    "Riverside Boutique Hotel",
    "Urban Stay Suites",
    "The Metropolitan",
    "Royal Garden Hotel",
    "Harbor View Residence",
]


ROOM_NAMES = [
    "Standard Double Room",
    "Deluxe King Room",
    "Superior Twin Room",
    "Family Suite",
]


PAYMENT_METHODS = [
    {
        "label": "Credit or debit card",
        "icon": "credit_card",
    },
    {
        "label": "Pay at property",
        "icon": "hotel",
    },
    {
        "label": "Digital wallet",
        "icon": "account_balance_wallet",
    },
]


COUNTRIES = [
    "South Korea",
    "Japan",
    "United States",
    "United Kingdom",
    "France",
    "Germany",
]


# ==========================================================
# Price Summary
# ==========================================================

def generate_price_summary() -> dict:

    nights = random.randint(
        2,
        5,
    )

    nightly_price = random.randint(
        80,
        240,
    )

    room_total = (
        nights
        * nightly_price
    )

    tax = round(
        room_total
        * random.uniform(
            0.07,
            0.14,
        )
    )

    discount = (
        random.randint(
            15,
            60,
        )
        if random.random() < 0.55
        else 0
    )

    total = (
        room_total
        + tax
        - discount
    )

    return {
        "nights":
            nights,

        "nightly_price":
            nightly_price,

        "room_total":
            room_total,

        "tax":
            tax,

        "discount":
            discount,

        "total":
            total,

        "currency":
            random.choice(
                [
                    "US$",
                    "€",
                    "₩",
                ]
            ),
    }


# ==========================================================
# Guest Data
# ==========================================================

def generate_guest_data(
    *,
    with_error: bool = False,
) -> dict:

    return {
        "first_name":
            (
                ""
                if with_error
                else random.choice(
                    [
                        "Alex",
                        "Emma",
                        "Daniel",
                        "Mina",
                        "Sophie",
                        "Lucas",
                    ]
                )
            ),

        "last_name":
            random.choice(
                [
                    "Kim",
                    "Park",
                    "Smith",
                    "Lee",
                    "Martin",
                    "Brown",
                ]
            ),

        "email":
            (
                "invalid-email"
                if with_error
                else random.choice(
                    [
                        "guest@example.com",
                        "traveler@example.com",
                        "booking.user@example.com",
                    ]
                )
            ),

        "phone":
            random.choice(
                [
                    "+82 10 1234 5678",
                    "+1 202 555 0148",
                    "+44 7700 900123",
                ]
            ),

        "country":
            random.choice(
                COUNTRIES
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_booking_checkout_data() -> dict:

    state = random.choice(
        CHECKOUT_STATES
    )

    validation_error = (
        state == "validation_error"
    )

    payment_state = (
        state == "payment"
    )

    confirmation_state = (
        state == "confirmation"
    )

    login_prompt = (
        state == "login_prompt"
    )

    mobile_summary_open = (
        state == "mobile_summary_open"
    )

    price = (
        generate_price_summary()
    )

    payment_methods = (
        PAYMENT_METHODS.copy()
    )

    selected_payment = (
        random.choice(
            payment_methods
        )[
            "label"
        ]
    )

    return {

        # ------------------------------------------
        # State
        # ------------------------------------------

        "state":
            state,

        "validation_error":
            validation_error,

        "payment_state":
            payment_state,

        "confirmation_state":
            confirmation_state,

        "login_prompt":
            login_prompt,

        "mobile_summary_open":
            mobile_summary_open,

        # ------------------------------------------
        # Reservation
        # ------------------------------------------

        "hotel_name":
            random.choice(
                HOTEL_NAMES
            ),

        "room_name":
            random.choice(
                ROOM_NAMES
            ),

        "hotel_image":
            get_random_hotel_image(),

        "city":
            random.choice(
                [
                    "Seoul",
                    "Tokyo",
                    "Paris",
                    "London",
                    "Bangkok",
                ]
            ),

        "check_in":
            "Sep 18",

        "check_out":
            "Sep 21",

        "guests":
            random.choice(
                [
                    "2 adults",
                    "1 adult",
                    "2 adults · 1 child",
                ]
            ),

        # ------------------------------------------
        # Guest
        # ------------------------------------------

        "guest":
            generate_guest_data(
                with_error=
                    validation_error
            ),

        # ------------------------------------------
        # Payment
        # ------------------------------------------

        "payment_methods":
            payment_methods,

        "selected_payment":
            selected_payment,

        # ------------------------------------------
        # Pricing
        # ------------------------------------------

        "price":
            price,

        # ------------------------------------------
        # Confirmation
        # ------------------------------------------

        "confirmation_number":
            (
                f"BK{random.randint(100000, 999999)}"
            ),

        "confirmation_message":
            (
                "Your booking is confirmed. "
                "A confirmation has been sent to your email."
            ),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_booking_checkout_data()
    )

    print(
        "\n=============================="
    )

    print(
        "BOOKING CHECKOUT"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Hotel:",
        data["hotel_name"],
    )

    print(
        "Total:",
        data["price"]["total"],
    )