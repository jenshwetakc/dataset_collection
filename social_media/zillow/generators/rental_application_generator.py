from __future__ import annotations

import random

from faker import Faker

from social_media.zillow.generators.media_generator import (
    get_random_agent_image,
    get_random_property_image,
)


fake = Faker()


# ==========================================================
# Constants
# ==========================================================

APPLICATION_STEPS = [
    {
        "label": "Profile",
        "icon": "person",
        "semantic": "profile",
    },
    {
        "label": "Income",
        "icon": "payments",
        "semantic": "income",
    },
    {
        "label": "Rental history",
        "icon": "home_work",
        "semantic": "rental_history",
    },
    {
        "label": "Documents",
        "icon": "description",
        "semantic": "documents",
    },
    {
        "label": "Review",
        "icon": "fact_check",
        "semantic": "review",
    },
]


DOCUMENT_TYPES = [
    {
        "label": "Government ID",
        "icon": "badge",
        "semantic": "government_id",
    },
    {
        "label": "Proof of income",
        "icon": "payments",
        "semantic": "proof_of_income",
    },
    {
        "label": "Bank statement",
        "icon": "account_balance",
        "semantic": "bank_statement",
    },
    {
        "label": "Employment letter",
        "icon": "business_center",
        "semantic": "employment_letter",
    },
]


EMPLOYMENT_TYPES = [
    "Full-time",
    "Part-time",
    "Self-employed",
    "Contract",
]


LEASE_TERMS = [
    "12 months",
    "18 months",
    "24 months",
]


# ==========================================================
# Formatting
# ==========================================================

def format_currency(
    value: int,
) -> str:

    return f"${value:,}"


# ==========================================================
# Application Steps
# ==========================================================

def generate_steps() -> list[dict]:

    current_index = random.randint(
        1,
        3,
    )

    result = []

    for index, step in enumerate(
        APPLICATION_STEPS
    ):

        value = dict(
            step
        )

        value[
            "completed"
        ] = (
            index
            < current_index
        )

        value[
            "active"
        ] = (
            index
            == current_index
        )

        value[
            "locked"
        ] = (
            index
            > current_index
        )

        result.append(
            value
        )

    return result


# ==========================================================
# Documents
# ==========================================================

def generate_documents() -> list[dict]:

    documents = []

    for item in DOCUMENT_TYPES:

        status = random.choice(
            [
                "uploaded",
                "uploaded",
                "missing",
                "review",
            ]
        )

        documents.append(
            {
                **item,

                "status":
                    status,

                "filename":
                    (
                        fake.file_name(
                            extension=random.choice(
                                [
                                    "pdf",
                                    "jpg",
                                    "png",
                                ]
                            )
                        )
                        if status != "missing"
                        else None
                    ),

                "size":
                    (
                        f"{random.randint(200, 2400)} KB"
                        if status != "missing"
                        else None
                    ),
            }
        )

    return documents


# ==========================================================
# Rental History
# ==========================================================

def generate_rental_history() -> list[dict]:

    history = []

    for index in range(
        random.randint(
            1,
            3,
        )
    ):

        history.append(
            {
                "address":
                    fake.street_address(),

                "city":
                    fake.city(),

                "state":
                    fake.state_abbr(),

                "monthly_rent":
                    random.randrange(
                        900,
                        3600,
                        50,
                    ),

                "monthly_rent_text":
                    "",

                "years":
                    random.randint(
                        1,
                        5,
                    ),

                "landlord":
                    fake.name(),

                "landlord_phone":
                    fake.phone_number(),
            }
        )

    for item in history:

        item[
            "monthly_rent_text"
        ] = format_currency(
            item[
                "monthly_rent"
            ]
        )

    return history


# ==========================================================
# Co-applicants
# ==========================================================

def generate_coapplicants() -> list[dict]:

    result = []

    count = random.choice(
        [
            0,
            1,
            1,
            2,
        ]
    )

    for index in range(
        count
    ):

        name = fake.name()

        result.append(
            {
                "name":
                    name,

                "initial":
                    name[
                        :1
                    ].upper(),

                "avatar":
                    get_random_agent_image(),

                "email":
                    fake.email(),

                "status":
                    random.choice(
                        [
                            "Completed",
                            "In progress",
                            "Invited",
                        ]
                    ),
            }
        )

    return result


# ==========================================================
# Main Generator
# ==========================================================

def generate_rental_application_data() -> dict:

    monthly_rent = random.randrange(
        1200,
        4800,
        50,
    )

    deposit = random.choice(
        [
            monthly_rent,
            round(
                monthly_rent
                * 1.5
            ),
            random.randrange(
                800,
                3000,
                50,
            ),
        ]
    )

    monthly_income = random.randrange(
        3500,
        14000,
        250,
    )

    application_fee = random.choice(
        [
            25,
            30,
            35,
            40,
            50,
        ]
    )

    first_name = fake.first_name()
    last_name = fake.last_name()

    employment_type = random.choice(
        EMPLOYMENT_TYPES
    )

    steps = generate_steps()

    completed_steps = sum(
        step[
            "completed"
        ]
        for step in steps
    )

    progress_percent = round(
        completed_steps
        /
        max(
            1,
            len(
                steps
            )
            - 1
        )
        *
        100
    )

    return {

        "brand": {
            "name": "Zillow",
            "short_name": "Z",
        },


        "property": {

            "image":
                get_random_property_image(),

            "address":
                fake.street_address(),

            "city":
                fake.city(),

            "state":
                fake.state_abbr(),

            "zipcode":
                fake.postcode(),

            "monthly_rent":
                monthly_rent,

            "monthly_rent_text":
                (
                    f"{format_currency(monthly_rent)}/mo"
                ),

            "deposit":
                deposit,

            "deposit_text":
                format_currency(
                    deposit
                ),

            "bedrooms":
                random.randint(
                    1,
                    4,
                ),

            "bathrooms":
                random.choice(
                    [
                        1,
                        1.5,
                        2,
                        2.5,
                        3,
                    ]
                ),

            "sqft":
                random.randint(
                    550,
                    2200,
                ),

            "available_date":
                fake.date_between(
                    start_date="+7d",
                    end_date="+60d",
                ).strftime(
                    "%b %d, %Y"
                ),
        },


        "application": {

            "steps":
                steps,

            "progress_percent":
                progress_percent,

            "application_fee":
                application_fee,

            "application_fee_text":
                format_currency(
                    application_fee
                ),

            "lease_term":
                random.choice(
                    LEASE_TERMS
                ),

            "move_in_date":
                fake.date_between(
                    start_date="+14d",
                    end_date="+90d",
                ).strftime(
                    "%b %d, %Y"
                ),
        },


        "applicant": {

            "first_name":
                first_name,

            "last_name":
                last_name,

            "full_name":
                f"{first_name} {last_name}",

            "email":
                fake.email(),

            "phone":
                fake.phone_number(),

            "birth_date":
                fake.date_of_birth(
                    minimum_age=21,
                    maximum_age=55,
                ).strftime(
                    "%m/%d/%Y"
                ),

            "current_address":
                fake.street_address(),

            "city":
                fake.city(),

            "state":
                fake.state_abbr(),

            "zipcode":
                fake.postcode(),
        },


        "employment": {

            "type":
                employment_type,

            "employer":
                (
                    fake.company()
                    if employment_type
                    != "Self-employed"
                    else "Self-employed"
                ),

            "job_title":
                fake.job(),

            "monthly_income":
                monthly_income,

            "monthly_income_text":
                format_currency(
                    monthly_income
                ),

            "start_date":
                fake.date_between(
                    start_date="-8y",
                    end_date="-6m",
                ).strftime(
                    "%b %Y"
                ),

            "manager":
                fake.name(),

            "manager_phone":
                fake.phone_number(),
        },


        "rental_history":
            generate_rental_history(),


        "documents":
            generate_documents(),


        "coapplicants":
            generate_coapplicants(),


        "screening": {

            "credit_check":
                True,

            "background_check":
                True,

            "income_verification":
                random.random()
                < 0.8,

            "identity_verification":
                random.random()
                < 0.9,
        },


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
                "label": "Rentals",
                "icon": "apartment",
                "active": True,
            },

            {
                "label": "Messages",
                "icon": "chat",
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

    data = generate_rental_application_data()

    print(
        "Property:",
        data[
            "property"
        ][
            "address"
        ],
    )

    print(
        "Rent:",
        data[
            "property"
        ][
            "monthly_rent_text"
        ],
    )

    print(
        "Progress:",
        data[
            "application"
        ][
            "progress_percent"
        ],
    )