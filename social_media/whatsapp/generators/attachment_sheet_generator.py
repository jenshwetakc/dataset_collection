import random

from social_media.whatsapp.generators.media_generator import (
    get_random_chat_image,
)


# ==========================================================
# Attachment Actions
# ==========================================================

ATTACHMENT_ACTIONS = [

    {
        "id": "document",
        "label": "Document",
        "icon": "description",
        "semantic": "attachment_document",
    },

    {
        "id": "camera",
        "label": "Camera",
        "icon": "photo_camera",
        "semantic": "attachment_camera",
    },

    {
        "id": "gallery",
        "label": "Gallery",
        "icon": "image",
        "semantic": "attachment_gallery",
    },

    {
        "id": "audio",
        "label": "Audio",
        "icon": "headphones",
        "semantic": "attachment_audio",
    },

    {
        "id": "location",
        "label": "Location",
        "icon": "location_on",
        "semantic": "attachment_location",
    },

    {
        "id": "contact",
        "label": "Contact",
        "icon": "person",
        "semantic": "attachment_contact",
    },

    {
        "id": "poll",
        "label": "Poll",
        "icon": "poll",
        "semantic": "attachment_poll",
    },

    {
        "id": "event",
        "label": "Event",
        "icon": "calendar_month",
        "semantic": "attachment_event",
    },
]


# ==========================================================
# Recent Media
# ==========================================================

def generate_recent_media(
    min_items=4,
    max_items=12,
):

    item_count = random.randint(
        min_items,
        max_items,
    )


    items = []

    for _ in range(
        item_count
    ):

        media_type = random.choices(
            [
                "image",
                "video",
            ],
            weights=[
                0.80,
                0.20,
            ],
            k=1,
        )[0]


        items.append(
            {

                "type":
                    media_type,

                "image":
                    get_random_chat_image(),

                "duration":
                    (
                        f"{random.randint(0, 5)}:"
                        f"{random.randint(0, 59):02d}"
                        if media_type == "video"
                        else None
                    ),

                "selected":
                    random.random() < 0.10,
            }
        )


    return items


# ==========================================================
# Attachment Sheet
# ==========================================================

def generate_attachment_sheet_page():

    # ------------------------------------------------------
    # Some states may show all actions.
    # Others can hide less common actions.
    # ------------------------------------------------------

    action_count = random.choice(
        [
            6,
            7,
            8,
        ]
    )


    actions = [
        dict(action)
        for action in ATTACHMENT_ACTIONS[
            :action_count
        ]
    ]


    # ------------------------------------------------------
    # Random state
    # ------------------------------------------------------

    show_recent_media = (
        random.random() < 0.70
    )


    recent_media = (
        generate_recent_media()
        if show_recent_media
        else []
    )


    return {

        "title":
            "Attach",

        "actions":
            actions,

        "action_count":
            len(actions),

        "show_recent_media":
            show_recent_media,

        "recent_media":
            recent_media,

        "recent_media_count":
            len(recent_media),

        # --------------------------------------------------
        # Sheet state
        # --------------------------------------------------

        "show_handle":
            True,

        "show_close":
            random.random() < 0.35,

        # --------------------------------------------------
        # Background conversation simulation
        # --------------------------------------------------

        "background": {

            "show":
                True,

            "contact_name":
                "Chat",

            "message":
                random.choice(
                    [
                        "Type a message",
                        "Photo",
                        "Document",
                    ]
                ),
        },
    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_attachment_sheet_page()
    )


    print(
        "\nATTACHMENT SHEET"
    )

    print(
        "Actions:",
        page["action_count"]
    )

    print(
        "Recent media:",
        page["recent_media_count"]
    )

    print(
        "Show close:",
        page["show_close"]
    )


    print(
        "\nACTIONS"
    )

    for action in page["actions"]:

        print(
            action["label"],
            action["icon"]
        )


    print(
        "\nRECENT MEDIA"
    )

    for media in page[
        "recent_media"
    ][:3]:

        print(
            media["type"],
            media["image"] is not None
        )