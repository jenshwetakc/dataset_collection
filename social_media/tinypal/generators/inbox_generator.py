from __future__ import annotations

import random
from copy import deepcopy


INBOX_STATES = (
    "all_activity",
    "unread_only",
    "reminders_only",
    "selection_mode",
    "empty_inbox",
    "notification_details",
    "preferences",
    "clear_dialog",
)


def generate_inbox_data(
    sample_index: int,
) -> dict:
    specifications = [
        (
            "Today", "09:40", "reminders", "schedule",
            "Your outing checklist is waiting",
            "Review the remaining items before your afternoon outing.",
            "Packing checklist", True,
        ),
        (
            "Today", "09:15", "family", "group",
            "Sam updated the afternoon plan",
            "The family walk is now listed for 4:00 PM.",
            "Family routines", True,
        ),
        (
            "Today", "08:50", "memories", "photo_library",
            "A new memory was added",
            "Alex shared a photo from your weekend together.",
            "Memories", True,
        ),
        (
            "Today", "08:30", "reminders", "menu_book",
            "Picture book time",
            "Your morning reading reminder is ready.",
            "Daily routine", False,
        ),
        (
            "Today", "08:10", "family", "checklist",
            "Morning checklist updated",
            "Sam marked two items as complete.",
            "Family checklist", False,
        ),
        (
            "Today", "07:45", "learning", "auto_stories",
            "A new play idea to explore",
            "Browse a simple activity for your next quiet afternoon.",
            "Learning library", True,
        ),
        (
            "Yesterday", "19:20", "memories", "favorite",
            "A favorite moment was saved",
            "Your family album has a new favorite.",
            "Memories", False,
        ),
        (
            "Yesterday", "18:00", "reminders", "inventory_2",
            "Prepare tomorrow’s bag",
            "Your packing reminder is ready to review.",
            "Packing checklist", True,
        ),
        (
            "Yesterday", "16:35", "family", "edit_calendar",
            "Weekend plan updated",
            "Alex added a family visit to the shared plan.",
            "Family routines", False,
        ),
        (
            "Yesterday", "14:10", "learning", "bookmark",
            "Your saved reading collection",
            "Revisit the articles you bookmarked this week.",
            "Learning library", False,
        ),
        (
            "Yesterday", "11:25", "family", "person_add",
            "Caregiver invitation accepted",
            "Alex is now included in your family workspace.",
            "Family members", True,
        ),
        (
            "Earlier", "Monday", "memories", "celebration",
            "A milestone was recorded",
            "A new favorite game has been added to your album.",
            "Memories", False,
        ),
        (
            "Earlier", "Monday", "reminders", "park",
            "Family walk reminder",
            "Your shared afternoon activity is ready to review.",
            "Daily routine", False,
        ),
        (
            "Earlier", "Sunday", "learning", "toys",
            "Explore your play collection",
            "Three saved activity ideas are waiting in your library.",
            "Learning library", False,
        ),
        (
            "Earlier", "Sunday", "family", "settings",
            "Family preferences updated",
            "Sam changed the shared reminder preferences.",
            "Family settings", False,
        ),
        (
            "Earlier", "Saturday", "memories", "photo_camera",
            "Your weekend album",
            "Look back at the moments your family shared.",
            "Memories", False,
        ),
    ]

    notifications = [
        {
            "id": f"notification_{index}",
            "group": group,
            "time": time,
            "category": category,
            "icon": item_icon,
            "title": title,
            "description": description,
            "source": source,
            "unread": unread,
            "selected": False,
        }
        for index, (
            group,
            time,
            category,
            item_icon,
            title,
            description,
            source,
            unread,
        ) in enumerate(specifications)
    ]

    # Vary some read statuses while keeping a useful unread subset.
    for notification in notifications[6:]:
        if random.random() < 0.2:
            notification["unread"] = True

    return {
        "sample_index": sample_index,
        "state": "all_activity",
        "popup_visible": False,
        "active_filter": "all",
        "selection_mode": False,
        "notifications": notifications,
        "groups": [],
        "total": 0,
        "unread_count": 0,
        "selected_count": 0,
        "visible_count": 0,
        "selected_notification": deepcopy(notifications[0]),
        "filters": [
            {"id": "all", "label": "All activity"},
            {"id": "unread", "label": "Unread"},
            {"id": "reminders", "label": "Reminders"},
            {"id": "family", "label": "Family"},
            {"id": "memories", "label": "Memories"},
            {"id": "learning", "label": "Learning"},
        ],
        "preferences": [
            {
                "id": "reminders",
                "title": "Routine reminders",
                "description": "Scheduled activities and packing reminders",
                "icon": "schedule",
                "enabled": True,
            },
            {
                "id": "family",
                "title": "Family updates",
                "description": "Shared plans and caregiver activity",
                "icon": "group",
                "enabled": True,
            },
            {
                "id": "memories",
                "title": "Memory updates",
                "description": "New photos and saved milestones",
                "icon": "photo_library",
                "enabled": True,
            },
            {
                "id": "learning",
                "title": "Learning suggestions",
                "description": "Articles and activity collections",
                "icon": "menu_book",
                "enabled": False,
            },
        ],
        "quick_links": [
            {
                "id": "routines",
                "label": "Family routines",
                "description": "Review your shared plan",
                "icon": "calendar_month",
            },
            {
                "id": "packing",
                "label": "Packing checklist",
                "description": "Prepare for your next outing",
                "icon": "checklist",
            },
            {
                "id": "memories",
                "label": "Family memories",
                "description": "Browse recent moments",
                "icon": "photo_library",
            },
        ],
        "navigation": [
            {"label": "Today", "icon": "today", "active": False},
            {"label": "Track", "icon": "monitoring", "active": False},
            {"label": "Learn", "icon": "menu_book", "active": False},
            {"label": "Family", "icon": "group", "active": True},
        ],
    }


def apply_inbox_state(
    base_data: dict,
    state: str,
) -> dict:
    if state not in INBOX_STATES:
        raise ValueError(f"Unknown inbox state: {state}")

    data = deepcopy(base_data)
    data["state"] = state
    data["popup_visible"] = state in {
        "notification_details",
        "preferences",
        "clear_dialog",
    }

    if state == "empty_inbox":
        data["notifications"] = []

    elif state == "unread_only":
        data["active_filter"] = "unread"

    elif state == "reminders_only":
        data["active_filter"] = "reminders"

    elif state == "selection_mode":
        data["selection_mode"] = True

        for index, notification in enumerate(data["notifications"]):
            notification["selected"] = index in {0, 1, 3}

    notifications = data["notifications"]

    data["total"] = len(notifications)
    data["unread_count"] = sum(
        notification["unread"]
        for notification in notifications
    )
    data["selected_count"] = sum(
        notification["selected"]
        for notification in notifications
    )

    active_filter = data["active_filter"]

    if active_filter == "unread":
        visible = [
            notification
            for notification in notifications
            if notification["unread"]
        ]
    elif active_filter == "all":
        visible = notifications
    else:
        visible = [
            notification
            for notification in notifications
            if notification["category"] == active_filter
        ]

    data["visible_count"] = len(visible)
    data["groups"] = []

    for group_name in ("Today", "Yesterday", "Earlier"):
        group_entries = [
            notification
            for notification in visible
            if notification["group"] == group_name
        ]

        if group_entries:
            data["groups"].append({
                "id": f"inbox_group_{len(data['groups'])}",
                "title": group_name,
                "entries": group_entries,
            })

    return data