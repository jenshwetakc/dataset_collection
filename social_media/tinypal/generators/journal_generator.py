from __future__ import annotations

import random
from copy import deepcopy


JOURNAL_STATES = (
    "all_notes",
    "pinned_only",
    "handover_notes",
    "selection_mode",
    "empty_journal",
    "note_details",
    "add_note",
    "delete_dialog",
)


def generate_journal_data(sample_index: int) -> dict:
    specifications = [
        (
            "Afternoon handover", "handover", "assignment",
            "The outing bag is beside the door. The picture book "
            "and spare outfit are already packed.",
            ["Check the outing bag", "Bring the water bottle"],
        ),
        (
            "Favorite play ideas", "play", "toys",
            "Building a small tower and sorting wooden blocks "
            "were the favorite activities this week.",
            ["Wooden blocks", "Stacking cups"],
        ),
        (
            "Weekend family visit", "plans", "event",
            "Bring the shared photo album and the blue blanket. "
            "We will confirm the departure time together.",
            ["Photo album", "Blue blanket"],
        ),
        (
            "Reading basket", "play", "menu_book",
            "The animal picture book is in the living room basket. "
            "Keep the smaller books nearby for quiet time.",
            [],
        ),
        (
            "Morning handover", "handover", "wb_sunny",
            "The spare clothes are in the front pocket of the bag. "
            "The afternoon plan is on the routines page.",
            ["Check spare clothes"],
        ),
        (
            "Things to restock", "home", "inventory_2",
            "Review the family supplies before the next shopping trip.",
            ["Wipes", "Storage bags", "Laundry detergent"],
        ),
        (
            "A moment to remember", "memories", "favorite",
            "Everyone joined in with the new game today. "
            "Add the photos to the family album later.",
            ["Choose two photos"],
        ),
        (
            "Rainy afternoon ideas", "play", "umbrella",
            "Keep a few indoor activities ready: drawing, "
            "picture books, and a simple sorting game.",
            ["Drawing paper", "Crayons"],
        ),
        (
            "Next outing", "plans", "park",
            "Choose a meeting point and review the packing list "
            "before leaving home.",
            ["Choose meeting point", "Review packing list"],
        ),
        (
            "Evening handover", "handover", "bedtime",
            "The story basket is ready. The favorite blanket "
            "is folded beside the sofa.",
            [],
        ),
        (
            "Family photo collection", "memories", "photo_library",
            "Collect everyone’s favorite weekend photos in one album.",
            ["Ask Sam for photos", "Add album title"],
        ),
        (
            "Organize the play shelf", "home", "shelves",
            "Group books and toys into small baskets so that "
            "they are easier to find.",
            ["Book basket", "Toy basket"],
        ),
    ]

    notes = []

    for index, (title, category, item_icon, body, tasks) in enumerate(
        specifications
    ):
        notes.append({
            "id": f"journal_note_{index}",
            "title": title,
            "category": category,
            "icon": item_icon,
            "body": body,
            "author": random.choice(["You", "Sam", "Alex"]),
            "updated": ["Today", "Yesterday", "This week"][index % 3],
            "pinned": index in {0, 1, 2},
            "selected": False,
            "tasks": [
                {
                    "id": f"journal_task_{index}_{task_index}",
                    "title": task,
                    "done": task_index == 0 and index % 2 == 0,
                }
                for task_index, task in enumerate(tasks)
            ],
        })

    return {
        "sample_index": sample_index,
        "state": "all_notes",
        "popup_visible": False,
        "selection_mode": False,
        "active_filter": "all",
        "notes": notes,
        "visible_notes": [],
        "selected_note": deepcopy(notes[0]),
        "total": 0,
        "pinned_count": 0,
        "selected_count": 0,
        "task_count": 0,
        "filters": [
            {"id": "all", "label": "All notes"},
            {"id": "pinned", "label": "Pinned"},
            {"id": "handover", "label": "Handover"},
            {"id": "play", "label": "Play"},
            {"id": "plans", "label": "Plans"},
            {"id": "home", "label": "Home"},
            {"id": "memories", "label": "Memories"},
        ],
        "categories": [
            {"id": "handover", "label": "Handover"},
            {"id": "play", "label": "Play"},
            {"id": "plans", "label": "Plans"},
            {"id": "home", "label": "Home"},
            {"id": "memories", "label": "Memories"},
        ],
        "form": {
            "title": "",
            "body": "",
            "category": "handover",
            "pinned": True,
        },
        "activity": [
            {
                "id": "activity_0",
                "icon": "edit_note",
                "title": "Sam updated a handover note",
                "time": "10 minutes ago",
            },
            {
                "id": "activity_1",
                "icon": "push_pin",
                "title": "You pinned the weekend plan",
                "time": "40 minutes ago",
            },
            {
                "id": "activity_2",
                "icon": "add",
                "title": "Alex added a play idea",
                "time": "Yesterday",
            },
            {
                "id": "activity_3",
                "icon": "checklist",
                "title": "Sam completed a packing task",
                "time": "Yesterday",
            },
        ],
        "navigation": [
            {"label": "Today", "icon": "today", "active": False},
            {"label": "Track", "icon": "monitoring", "active": False},
            {"label": "Learn", "icon": "menu_book", "active": False},
            {"label": "Family", "icon": "group", "active": True},
        ],
    }


def apply_journal_state(base_data: dict, state: str) -> dict:
    if state not in JOURNAL_STATES:
        raise ValueError(f"Unknown journal state: {state}")

    data = deepcopy(base_data)
    data["state"] = state
    data["popup_visible"] = state in {
        "note_details",
        "add_note",
        "delete_dialog",
    }

    if state == "empty_journal":
        data["notes"] = []
        data["activity"] = []

    elif state == "pinned_only":
        data["active_filter"] = "pinned"

    elif state == "handover_notes":
        data["active_filter"] = "handover"

    elif state == "selection_mode":
        data["selection_mode"] = True

        for index, note in enumerate(data["notes"]):
            note["selected"] = index in {0, 2, 4}

    notes = data["notes"]
    active_filter = data["active_filter"]

    if active_filter == "pinned":
        visible = [note for note in notes if note["pinned"]]
    elif active_filter == "all":
        visible = notes
    else:
        visible = [
            note for note in notes
            if note["category"] == active_filter
        ]

    data["visible_notes"] = visible
    data["total"] = len(notes)
    data["pinned_count"] = sum(note["pinned"] for note in notes)
    data["selected_count"] = sum(note["selected"] for note in notes)
    data["task_count"] = sum(
        not task["done"]
        for note in notes
        for task in note["tasks"]
    )

    return data