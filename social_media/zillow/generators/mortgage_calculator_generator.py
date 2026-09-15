from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

LOAN_PROGRAMS = [
    {
        "name": "30-year fixed",
        "years": 30,
    },
    {
        "name": "15-year fixed",
        "years": 15,
    },
    {
        "name": "20-year fixed",
        "years": 20,
    },
    {
        "name": "5/1 ARM",
        "years": 30,
    },
]


CALCULATOR_CARDS = [
    {
        "title": "Affordability calculator",
        "description": (
            "Estimate how much home may fit "
            "comfortably within your budget."
        ),
        "icon": "account_balance_wallet",
        "semantic": "affordability_calculator",
    },
    {
        "title": "Down payment calculator",
        "description": (
            "Estimate the cash you may need "
            "for your home purchase."
        ),
        "icon": "payments",
        "semantic": "down_payment_calculator",
    },
    {
        "title": "Closing cost calculator",
        "description": (
            "Explore possible fees associated "
            "with purchasing a home."
        ),
        "icon": "receipt_long",
        "semantic": "closing_cost_calculator",
    },
    {
        "title": "Loan comparison",
        "description": (
            "Compare loan terms and monthly "
            "payment scenarios."
        ),
        "icon": "compare_arrows",
        "semantic": "loan_comparison",
    },
]


# ==========================================================
# Mortgage Formula
# ==========================================================

def calculate_principal_and_interest(
    principal: float,
    annual_rate: float,
    years: int,
) -> float:

    months = (
        years
        * 12
    )

    monthly_rate = (
        annual_rate
        / 100
        / 12
    )

    if monthly_rate <= 0:

        return (
            principal
            / months
        )

    factor = (
        (1 + monthly_rate)
        ** months
    )

    return (
        principal
        * monthly_rate
        * factor
        / (
            factor - 1
        )
    )


# ==========================================================
# Formatting
# ==========================================================

def currency(
    value: float,
) -> str:

    return (
        "$"
        f"{round(value):,}"
    )


def percentage_text(
    value: float,
) -> str:

    return (
        f"{value:.2f}%"
    )


# ==========================================================
# Amortization Samples
# ==========================================================

def generate_amortization_points(
    loan_amount: float,
    annual_rate: float,
    years: int,
) -> list[dict]:

    payment = (
        calculate_principal_and_interest(
            loan_amount,
            annual_rate,
            years,
        )
    )

    monthly_rate = (
        annual_rate
        / 100
        / 12
    )

    remaining = (
        loan_amount
    )

    months = (
        years
        * 12
    )

    checkpoints = [
        0.0,
        0.20,
        0.40,
        0.60,
        0.80,
        1.0,
    ]

    results = []

    previous_month = 0

    for checkpoint in checkpoints:

        target_month = round(
            months
            * checkpoint
        )

        for _ in range(
            previous_month,
            target_month,
        ):

            interest = (
                remaining
                * monthly_rate
            )

            principal_payment = (
                payment
                - interest
            )

            remaining = max(
                0,
                remaining
                - principal_payment,
            )

        previous_month = (
            target_month
        )

        results.append(
            {
                "label": (
                    "Start"
                    if target_month == 0
                    else (
                        f"Year "
                        f"{round(target_month / 12)}"
                    )
                ),
                "month": target_month,
                "remaining": round(
                    remaining
                ),
                "remaining_text": currency(
                    remaining
                ),
                "paid_ratio": round(
                    checkpoint
                    * 100,
                    1,
                ),
            }
        )

    return results


# ==========================================================
# Main Generator
# ==========================================================

def generate_mortgage_calculator_data() -> dict:

    home_price = random.randrange(
        260_000,
        1_600_000,
        5_000,
    )

    down_payment_percent = (
        random.choice(
            [
                5,
                10,
                15,
                20,
                25,
            ]
        )
    )

    down_payment = round(
        home_price
        * down_payment_percent
        / 100
    )

    loan_amount = (
        home_price
        - down_payment
    )

    loan_program = (
        random.choice(
            LOAN_PROGRAMS
        )
    )

    interest_rate = round(
        random.uniform(
            4.75,
            7.80,
        ),
        2,
    )

    principal_interest = (
        calculate_principal_and_interest(
            loan_amount,
            interest_rate,
            loan_program[
                "years"
            ],
        )
    )

    property_tax = (
        home_price
        * random.uniform(
            0.008,
            0.018,
        )
        / 12
    )

    insurance = random.randint(
        80,
        260,
    )

    hoa = (
        random.randint(
            0,
            550,
        )
        if random.random() < 0.45
        else 0
    )

    mortgage_insurance = (
        loan_amount
        * random.uniform(
            0.003,
            0.009,
        )
        / 12
        if down_payment_percent < 20
        else 0
    )

    total_payment = (
        principal_interest
        + property_tax
        + insurance
        + hoa
        + mortgage_insurance
    )

    annual_income = random.randrange(
        70_000,
        320_000,
        5_000,
    )

    monthly_debt = random.randrange(
        0,
        2400,
        50,
    )

    affordability = round(
        annual_income
        * random.uniform(
            3.1,
            4.7,
        )
    )

    breakdown = [
        {
            "label": "Principal & interest",
            "value": principal_interest,
            "value_text": currency(
                principal_interest
            ),
            "percent": round(
                principal_interest
                / total_payment
                * 100
            ),
            "icon": "account_balance",
        },
        {
            "label": "Property taxes",
            "value": property_tax,
            "value_text": currency(
                property_tax
            ),
            "percent": round(
                property_tax
                / total_payment
                * 100
            ),
            "icon": "location_city",
        },
        {
            "label": "Home insurance",
            "value": insurance,
            "value_text": currency(
                insurance
            ),
            "percent": round(
                insurance
                / total_payment
                * 100
            ),
            "icon": "shield",
        },
    ]

    if mortgage_insurance > 0:

        breakdown.append(
            {
                "label": "Mortgage insurance",
                "value": mortgage_insurance,
                "value_text": currency(
                    mortgage_insurance
                ),
                "percent": round(
                    mortgage_insurance
                    / total_payment
                    * 100
                ),
                "icon": "verified_user",
            }
        )

    if hoa > 0:

        breakdown.append(
            {
                "label": "HOA dues",
                "value": hoa,
                "value_text": currency(
                    hoa
                ),
                "percent": round(
                    hoa
                    / total_payment
                    * 100
                ),
                "icon": "apartment",
            }
        )

    return {

        "brand": {
            "name": "Zillow",
            "short_name": "Z",
        },


        "calculator": {

            "home_price":
                home_price,

            "home_price_text":
                currency(
                    home_price
                ),

            "down_payment":
                down_payment,

            "down_payment_text":
                currency(
                    down_payment
                ),

            "down_payment_percent":
                down_payment_percent,

            "loan_amount":
                loan_amount,

            "loan_amount_text":
                currency(
                    loan_amount
                ),

            "loan_program":
                loan_program[
                    "name"
                ],

            "loan_years":
                loan_program[
                    "years"
                ],

            "interest_rate":
                interest_rate,

            "interest_rate_text":
                percentage_text(
                    interest_rate
                ),

            "zipcode":
                fake.postcode(),
        },


        "payment": {

            "monthly_total":
                total_payment,

            "monthly_total_text":
                (
                    currency(
                        total_payment
                    )
                    + "/mo"
                ),

            "breakdown":
                breakdown,
        },


        "affordability": {

            "annual_income":
                annual_income,

            "annual_income_text":
                currency(
                    annual_income
                ),

            "monthly_debt":
                monthly_debt,

            "monthly_debt_text":
                (
                    currency(
                        monthly_debt
                    )
                    + "/mo"
                ),

            "estimated_home_price":
                affordability,

            "estimated_home_price_text":
                currency(
                    affordability
                ),

            "dti":
                random.randint(
                    26,
                    42,
                ),
        },


        "amortization":
            generate_amortization_points(
                loan_amount,
                interest_rate,
                loan_program[
                    "years"
                ],
            ),


        "calculator_cards":
            CALCULATOR_CARDS,


        "mobile_navigation": [

            {
                "label": "Home",
                "icon": "home",
                "active": False,
            },

            {
                "label": "Search",
                "icon": "search",
                "active": False,
            },

            {
                "label": "Loans",
                "icon": "payments",
                "active": True,
            },

            {
                "label": "Saved",
                "icon": "favorite",
                "active": False,
            },

            {
                "label": "Profile",
                "icon": "person",
                "active": False,
            },
        ],
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = (
        generate_mortgage_calculator_data()
    )

    print(
        "Home price:",
        data[
            "calculator"
        ][
            "home_price_text"
        ],
    )

    print(
        "Payment:",
        data[
            "payment"
        ][
            "monthly_total_text"
        ],
    )