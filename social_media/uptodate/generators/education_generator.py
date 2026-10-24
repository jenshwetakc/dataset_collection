from __future__ import annotations

import random
from copy import deepcopy


EDUCATION_STATES = [
    "library",
    "search_results",
    "document_reader",
    "reading_checklist",
    "language_dialog",
    "print_dialog",
    "share_dialog",
    "share_error",
]


DOCUMENT_TOPICS = [
    ("Preparing for a healthcare visit", "General health"),
    ("Keeping a personal health record", "General health"),
    ("Understanding your visit summary", "General health"),
    ("Questions to discuss at your next visit", "General health"),
    ("Organizing your medication list", "Medicines"),
    ("Reading medication information", "Medicines"),
    ("Preparing questions about prescriptions", "Medicines"),
    ("Keeping track of routine appointments", "Preventive care"),
    ("Understanding screening information", "Preventive care"),
    ("Preparing for a routine checkup", "Preventive care"),
    ("Recording your sleep routine", "Daily wellbeing"),
    ("Keeping a daily activity journal", "Daily wellbeing"),
    ("Preparing a nutrition discussion", "Daily wellbeing"),
    ("Understanding laboratory report headings", "Tests and procedures"),
    ("Preparing questions about a planned test", "Tests and procedures"),
    ("Organizing documents before a procedure", "Tests and procedures"),
    ("Planning a follow-up conversation", "Follow-up care"),
    ("Keeping track of questions after a visit", "Follow-up care"),
    ("Sharing visit information with a caregiver", "Follow-up care"),
    ("Finding your care team's contact details", "Follow-up care"),
]


def generate_education_data(
    *,
    sample_index: int,
) -> dict:
    documents = []

    for index, (title, category) in enumerate(DOCUMENT_TOPICS):
        documents.append({
            "id": f"education_{index}",
            "title": title,
            "category": category,
            "level": "The Basics" if index % 3 else "Beyond the Basics",
            "minutes": random.choice([3, 4, 5, 6, 8]),
            "pages": random.choice([2, 3, 4]),
            "saved": index % 4 == 0,
            "updated": random.choice([
                "September 2026",
                "August 2026",
                "July 2026",
            ]),
        })

    selected_document = deepcopy(documents[0])

    selected_document["sections"] = [
        {
            "id": "overview",
            "title": "About this guide",
            "paragraphs": [
                (
                    "This sample guide shows how a patient education "
                    "document can be presented in a reading workspace."
                ),
                (
                    "The document contains an overview, a preparation "
                    "checklist, space for questions, and related resources."
                ),
            ],
        },
        {
            "id": "preparation",
            "title": "Organizing information",
            "paragraphs": [
                (
                    "A preparation list can help organize the information "
                    "you want to discuss during a healthcare visit."
                ),
                (
                    "Use the sample checklist below to see how selected "
                    "and unselected items appear in the interface."
                ),
            ],
        },
        {
            "id": "questions",
            "title": "Questions and notes",
            "paragraphs": [
                (
                    "Write down the topics you would like to discuss. "
                    "This demonstration provides a notes field and "
                    "related document links."
                ),
            ],
        },
        {
            "id": "followup",
            "title": "Keeping your documents together",
            "paragraphs": [
                (
                    "The workspace lets you save a document, prepare a "
                    "printout, or open a sharing form."
                ),
                (
                    "These controls represent synthetic interface states "
                    "for screenshot generation."
                ),
            ],
        },
    ]

    categories = list(dict.fromkeys(
        category
        for _, category in DOCUMENT_TOPICS
    ))

    return {
        "sample_index": sample_index,
        "state": "library",
        "popup_visible": False,
        "reader_visible": False,
        "checklist_expanded": False,
        "query": "",
        "active_category": "All topics",
        "active_level": "All reading levels",
        "documents": documents,
        "total_count": len(documents),
        "saved_count": sum(item["saved"] for item in documents),
        "categories": ["All topics", *categories],
        "category_counts": {
            category: sum(
                item["category"] == category
                for item in documents
            )
            for category in categories
        },
        "document": selected_document,
        "active_section": "overview",
        "language": "English",
        "languages": [
            "English",
            "Español",
            "Français",
            "한국어",
            "中文",
            "العربية",
        ],
        "checklist": [
            {
                "id": "questions",
                "label": "List the questions you want to discuss",
                "checked": True,
            },
            {
                "id": "records",
                "label": "Organize documents you want to bring",
                "checked": True,
            },
            {
                "id": "contacts",
                "label": "Check your care team's contact information",
                "checked": False,
            },
            {
                "id": "notes",
                "label": "Prepare space for visit notes",
                "checked": False,
            },
        ],
        "notes": "",
        "recent_documents": deepcopy(documents[4:9]),
        "related_documents": deepcopy(documents[1:4]),
        "print_options": [
            {
                "id": "article",
                "label": "Document text",
                "checked": True,
            },
            {
                "id": "checklist",
                "label": "Preparation checklist",
                "checked": True,
            },
            {
                "id": "notes",
                "label": "My notes",
                "checked": False,
            },
            {
                "id": "related",
                "label": "Related resource list",
                "checked": False,
            },
        ],
        "print_size": "Standard",
        "share_email": "",
        "share_message": (
            "Here is the education document we discussed."
        ),
        "share_include_checklist": True,
        "errors": {},
    }


def apply_education_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in EDUCATION_STATES:
        raise ValueError(
            f"Unknown education state: {state}"
        )

    data = deepcopy(base_data)
    data["state"] = state

    data["popup_visible"] = state in {
        "language_dialog",
        "print_dialog",
        "share_dialog",
        "share_error",
    }

    data["reader_visible"] = state not in {
        "library",
        "search_results",
    }

    if state == "search_results":
        data["query"] = "Preparing"

        data["documents"] = [
            document
            for document in data["documents"]
            if "prepar" in document["title"].lower()
        ]

    elif state == "reading_checklist":
        data["checklist_expanded"] = True
        data["active_section"] = "preparation"
        data["notes"] = "Bring my questions and recent visit documents."

    elif state == "share_error":
        data["share_email"] = "reader.example.com"
        data["errors"] = {
            "email": "Enter an email address in the format name@example.com."
        }

    return data