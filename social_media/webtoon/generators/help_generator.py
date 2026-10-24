from __future__ import annotations

import random

from copy import deepcopy

from faker import Faker

from social_media.webtoon.generators.reader_generator import (
    generate_footer_data,
)


fake = Faker()

HELP_STATES = [
    "overview",
    "category_selected",
    "search_results",
    "search_empty",
    "answer_expanded",
    "helpful_selected",
    "sort_menu",
    "contact_dialog",
    "contact_validation",
    "request_sent",
]

TOPICS = [
    {
        "id": "getting_started",
        "title": "Getting started",
        "icon": "menu_book",
        "description": "Find your way around reading and subscriptions.",
        "questions": [
            "How can I start reading a series?",
            "Where can I find my subscriptions?",
            "How can I change the display theme?",
            "Where can I find my reading history?",
        ],
    },
    {
        "id": "accounts",
        "title": "Accounts and login",
        "icon": "person",
        "description": "Get help with your account and sign-in.",
        "questions": [
            "How can I recover access to my account?",
            "How can I change my email address?",
            "Where can I manage my profile?",
            "How can I sign out?",
        ],
    },
    {
        "id": "episodes",
        "title": "Coins and episodes",
        "icon": "paid",
        "description": "Explore episode access and purchase questions.",
        "questions": [
            "Where can I check my purchase history?",
            "How can I find an unlocked episode?",
            "Where can I check my Coin balance?",
            "How can I report a purchase issue?",
        ],
    },
    {
        "id": "troubleshooting",
        "title": "Troubleshooting",
        "icon": "build",
        "description": "Find help with loading and application issues.",
        "questions": [
            "What can I try when an episode does not load?",
            "How can I report an application error?",
            "Where can I check notification settings?",
            "How can I describe a connection issue?",
        ],
    },
]


def generate_help_data() -> dict:
    categories = deepcopy(TOPICS)

    article_id = 0

    for category in categories:
        articles = []

        for question in category.pop("questions"):
            articles.append(
                {
                    "id": f"article_{article_id}",
                    "title": question,
                    # Synthetic explanatory content for screenshot diversity.
                    "answer": fake.paragraph(nb_sentences=4),
                    "updated_days": random.randint(1, 90),
                    "views": random.randint(100, 20000),
                    "category": category["title"],
                    "category_id": category["id"],
                }
            )

            article_id += 1

        category["articles"] = articles

    data = {
        "categories": categories,
        "shortcuts": [
            {
                "title": "Getting started",
                "description": "Explore accounts, reading, and subscriptions.",
                "icon": "menu_book",
            },
            {
                "title": "CANVAS Creator Portal",
                "description": "Find resources for publishing your stories.",
                "icon": "draw",
            },
            {
                "title": "Get in touch",
                "description": "Send a request to the support team.",
                "icon": "mail",
            },
            {
                "title": "Feedback",
                "description": "Share suggestions for your reading experience.",
                "icon": "chat",
            },
        ],
        "contact_email": fake.email(),
        "request_reference": f"REQ-{random.randint(100000, 999999)}",
    }

    data.update(generate_footer_data())

    return data


def apply_help_state(content: dict, state: str) -> dict:
    if state not in HELP_STATES:
        raise ValueError(f"Unknown help state: {state}")

    data = dict(content)

    all_articles = [
        article
        for category in content["categories"]
        for article in category["articles"]
    ]

    selected_category = (
        content["categories"][1]
        if state == "category_selected"
        else None
    )

    is_search = state in {"search_results", "search_empty"}

    if state == "search_results":
        query = "account"
        results = [
            article
            for article in all_articles
            if "account" in article["title"].lower()
        ]
    elif state == "search_empty":
        query = fake.uuid4()[:12]
        results = []
    else:
        query = ""
        results = []

    data.update(
        {
            "state": state,
            "popup": state in {
                "contact_dialog",
                "contact_validation",
                "request_sent",
            },
            "query": query,
            "is_search": is_search,
            "search_results": results,
            "selected_category": selected_category,
            "visible_categories": (
                [selected_category]
                if selected_category
                else content["categories"]
            ),
            "expanded_article_id": (
                all_articles[0]["id"]
                if state in {"answer_expanded", "helpful_selected"}
                else None
            ),
            "helpful_selected": state == "helpful_selected",
            "sort_menu_open": state == "sort_menu",
            "sort_label": "Most popular",
            "validation_error": state == "contact_validation",
            "request_sent": state == "request_sent",
        }
    )

    return data