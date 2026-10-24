from __future__ import annotations

import random
from copy import deepcopy

from faker import Faker

fake = Faker()

REGISTRATION_STATES = [
    "overview",
    "sold_out",
    "empty_questions",
    "ticket_dialog",
    "paid_ticket_dialog",
    "validation_errors",
    "question_dialog",
    "preview_dialog",
    "delete_question_dialog",
]


def generate_registration_data(
    sample_index: int = 0,
) -> dict:
    tickets = []

    for index, name in enumerate([
        "General Admission",
        "Early Bird",
        "Community Ticket",
    ]):
        capacity = random.randint(30, 100)
        sold = random.randint(0, capacity - 1)
        price = random.choice([0, 10, 15, 25])

        tickets.append({
            "id": f"ticket_{sample_index}_{index}",
            "name": name,
            "description": random.choice([
                "Join us for the full event.",
                "A ticket for our community.",
                "Includes all event sessions.",
            ]),
            "capacity": capacity,
            "sold": sold,
            "price": price,
            "price_label": (
                "Free"
                if price == 0
                else f"${price:.2f}"
            ),
            "payment_type": (
                "Free"
                if price == 0
                else "Paid"
            ),
            "require_approval": (
                random.random() < 0.3
            ),
            "status": "Available",
        })

    questions = [
        {
            "id": f"question_{sample_index}_0",
            "title": "What would you like to learn?",
            "type": "Text",
            "required": True,
            "options": [],
        },
        {
            "id": f"question_{sample_index}_1",
            "title": "How did you hear about this event?",
            "type": "Multiple Choice",
            "required": False,
            "options": [
                "A friend",
                "Social media",
                "Community newsletter",
            ],
        },
        {
            "id": f"question_{sample_index}_2",
            "title": "Do you have any dietary preferences?",
            "type": "Text",
            "required": False,
            "options": [],
        },
    ]

    return {
        "state": "overview",
        "popup_visible": False,
        "event_title": random.choice([
            "Creative Community Night",
            "Builders & Ideas",
            "Weekend Workshop",
        ]),
        "tickets": tickets,
        "questions": questions,
        "selected_question": deepcopy(
            questions[1]
        ),
        "ticket_form": {
            "name": "Community Ticket",
            "description": "Join our next gathering.",
            "payment_type": "Free",
            "price": "15.00",
            "currency": "USD",
            "capacity": "60",
            "require_approval": False,
        },
        "question_form": {
            "title": "Which session interests you?",
            "type": "Multiple Choice",
            "required": True,
            "options": [
                "Design",
                "Technology",
                "Community",
            ],
        },
        "errors": {},
        "preview_name": fake.name(),
        "preview_email": fake.safe_email(),
    }


def apply_registration_state(
    page_data: dict,
    state: str,
) -> dict:
    if state not in REGISTRATION_STATES:
        raise ValueError(
            f"Unknown Registration state: {state}"
        )

    data = deepcopy(page_data)

    data["state"] = state
    data["popup_visible"] = state in {
        "ticket_dialog",
        "paid_ticket_dialog",
        "validation_errors",
        "question_dialog",
        "preview_dialog",
        "delete_question_dialog",
    }
    data["errors"] = {}

    if state == "sold_out":
        for ticket in data["tickets"]:
            ticket["sold"] = ticket["capacity"]
            ticket["status"] = "Sold Out"

    elif state == "empty_questions":
        data["questions"] = []

    elif state == "paid_ticket_dialog":
        data["ticket_form"].update({
            "name": "Workshop Pass",
            "payment_type": "Paid",
            "require_approval": True,
        })

    elif state == "validation_errors":
        data["ticket_form"].update({
            "name": "",
            "payment_type": "Paid",
            "price": "-5",
            "capacity": "0",
        })

        data["errors"] = {
            "name": "Enter a ticket name.",
            "price": "Enter a positive price.",
            "capacity": "Capacity must be at least 1.",
        }

    return data