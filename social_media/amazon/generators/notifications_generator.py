from __future__ import annotations

import random

from social_media.amazon.generators.media_generator import (
    get_category_image,
)


# ==========================================================
# States
# ==========================================================

NOTIFICATION_STATES = [
    "inbox",
    "unread_only",
    "orders_only",
    "promotions",
    "all_read",
    "empty",
    "message_open",
    "bulk_select",
    "delivery_alert",
    "notification_settings",
]


# ==========================================================
# Tabs
# ==========================================================

TABS = [
    {
        "label": "All",
        "value": "all",
        "icon": "inbox",
    },
    {
        "label": "Orders",
        "value": "orders",
        "icon": "package_2",
    },
    {
        "label": "Deals",
        "value": "deals",
        "icon": "sell",
    },
    {
        "label": "Account",
        "value": "account",
        "icon": "person",
    },
]


# ==========================================================
# Notification Content
# ==========================================================

ORDER_MESSAGES = [
    {
        "title": "Your package has shipped",
        "body": (
            "Your order is on the way. "
            "Track the package for the latest delivery updates."
        ),
        "icon": "local_shipping",
    },
    {
        "title": "Your order was delivered",
        "body": (
            "Your package was delivered successfully. "
            "We hope you enjoy your purchase."
        ),
        "icon": "package_2",
    },
    {
        "title": "Delivery arriving tomorrow",
        "body": (
            "Your package is expected to arrive tomorrow."
        ),
        "icon": "schedule",
    },
    {
        "title": "Order update",
        "body": (
            "There has been an update to one of your recent orders."
        ),
        "icon": "info",
    },
]


DEAL_MESSAGES = [
    {
        "title": "A deal you may like",
        "body": (
            "A product related to your recent browsing "
            "is available at a lower price."
        ),
        "icon": "sell",
    },
    {
        "title": "Limited-time deal",
        "body": (
            "Save on selected products before the deal ends."
        ),
        "icon": "bolt",
    },
    {
        "title": "Price dropped",
        "body": (
            "An item from your wishlist recently dropped in price."
        ),
        "icon": "trending_down",
    },
]


ACCOUNT_MESSAGES = [
    {
        "title": "Account security update",
        "body": (
            "Your account settings were recently updated."
        ),
        "icon": "security",
    },
    {
        "title": "Payment method updated",
        "body": (
            "A payment method on your account was changed."
        ),
        "icon": "credit_card",
    },
    {
        "title": "Prime membership update",
        "body": (
            "There is an update regarding your Prime membership."
        ),
        "icon": "workspace_premium",
    },
]


# ==========================================================
# Notification
# ==========================================================

def generate_notification(
    category: str | None = None,
    force_unread: bool = False,
) -> dict:

    if category is None:

        category = random.choice(
            [
                "orders",
                "deals",
                "account",
            ]
        )

    if category == "orders":

        source = random.choice(
            ORDER_MESSAGES
        )

        product_category = random.choice(
            [
                "Electronics",
                "Fashion",
                "Home",
                "Books",
            ]
        )

        image = (
            get_category_image(
                product_category
            )
            if random.random() < 0.7
            else None
        )

    elif category == "deals":

        source = random.choice(
            DEAL_MESSAGES
        )

        product_category = random.choice(
            [
                "Electronics",
                "Fashion",
                "Home",
                "Books",
                "Grocery",
            ]
        )

        image = get_category_image(
            product_category
        )

    else:

        source = random.choice(
            ACCOUNT_MESSAGES
        )

        image = None


    return {

        "category":
            category,

        "title":
            source["title"],

        "body":
            source["body"],

        "icon":
            source["icon"],

        "image":
            image,

        "unread":
            (
                True
                if force_unread
                else random.random() < 0.45
            ),

        "selected":
            False,

        "timestamp":
            random.choice(
                [
                    "Just now",
                    "12 min ago",
                    "1 hr ago",
                    "3 hrs ago",
                    "Yesterday",
                    "2 days ago",
                    "Last week",
                ]
            ),

        "action_label":
            random.choice(
                [
                    "View details",
                    "Track package",
                    "View deal",
                    "Review update",
                ]
            ),
    }


# ==========================================================
# Settings
# ==========================================================

def generate_notification_settings() -> list[dict]:

    settings = [
        {
            "label": "Order updates",
            "description": (
                "Shipping, delivery, and return notifications."
            ),
            "icon": "package_2",
            "enabled": True,
        },
        {
            "label": "Deals and recommendations",
            "description": (
                "Price drops and personalized offers."
            ),
            "icon": "sell",
            "enabled": random.random() < 0.6,
        },
        {
            "label": "Account notifications",
            "description": (
                "Security and account-related updates."
            ),
            "icon": "security",
            "enabled": True,
        },
        {
            "label": "Prime updates",
            "description": (
                "Prime membership and benefit notifications."
            ),
            "icon": "workspace_premium",
            "enabled": random.random() < 0.7,
        },
    ]

    return settings


# ==========================================================
# Main Generator
# ==========================================================

def generate_notifications_data() -> dict:

    state = random.choice(
        NOTIFICATION_STATES
    )


    # ======================================================
    # Selected Tab
    # ======================================================

    if state == "orders_only":

        selected_tab = "orders"

    elif state == "promotions":

        selected_tab = "deals"

    else:

        selected_tab = "all"


    # ======================================================
    # Generate Notifications
    # ======================================================

    if state == "empty":

        notifications = []

    else:

        count = random.randint(
            6,
            14,
        )

        notifications = []

        for _ in range(count):

            if state == "orders_only":

                category = "orders"

            elif state == "promotions":

                category = "deals"

            else:

                category = None


            notification = generate_notification(
                category=category,
                force_unread=(
                    state == "unread_only"
                ),
            )

            notifications.append(
                notification
            )


    # ======================================================
    # All Read
    # ======================================================

    if state == "all_read":

        for notification in notifications:

            notification["unread"] = False


    # ======================================================
    # Bulk Select
    # ======================================================

    if state == "bulk_select":

        for notification in notifications:

            notification["selected"] = (
                random.random() < 0.45
            )


    # ======================================================
    # Delivery Alert
    # ======================================================

    if state == "delivery_alert":

        alert = generate_notification(
            category="orders",
            force_unread=True,
        )

        alert["title"] = (
            "Your package is arriving today"
        )

        alert["body"] = (
            "Your delivery is scheduled for today. "
            "You can track the driver for the latest status."
        )

        alert["icon"] = "local_shipping"

        notifications.insert(
            0,
            alert,
        )


    # ======================================================
    # Selected Message
    # ======================================================

    selected_message = (
        random.choice(
            notifications
        )
        if notifications
        else None
    )


    # ======================================================
    # Counters
    # ======================================================

    unread_count = sum(
        1
        for notification
        in notifications
        if notification["unread"]
    )

    selected_count = sum(
        1
        for notification
        in notifications
        if notification["selected"]
    )


    # ======================================================
    # Return
    # ======================================================

    return {

        "state":
            state,

        "tabs":
            TABS,

        "selected_tab":
            selected_tab,

        "notifications":
            notifications,

        "unread_count":
            unread_count,

        "selected_count":
            selected_count,

        "selected_message":
            selected_message,

        "show_message_dialog":
            (
                state == "message_open"
                and selected_message
                is not None
            ),

        "bulk_mode":
            state == "bulk_select",

        "show_settings":
            (
                state
                == "notification_settings"
            ),

        "settings":
            generate_notification_settings(),
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    data = generate_notifications_data()

    print(
        "\n=============================="
    )

    print(
        "AMAZON NOTIFICATIONS"
    )

    print(
        "=============================="
    )

    print(
        "State:",
        data["state"],
    )

    print(
        "Notifications:",
        len(
            data["notifications"]
        ),
    )

    print(
        "Unread:",
        data["unread_count"],
    )

    print(
        "Selected:",
        data["selected_count"],
    )