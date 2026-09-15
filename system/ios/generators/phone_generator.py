from __future__ import annotations

import random

from faker import Faker

from system.ios.generators.icon_generator import (
    get_icon,
    get_lucide_icon,
)


fake = Faker()


# ==========================================================
# States
# ==========================================================

PHONE_STATES = [

    "recents",

    "favorites",

    "keypad",

    "voicemail",

    "contact_detail",

    "active_call",

    "incoming_call",

    "add_contact_sheet",
]


PHONE_STATE_WEIGHTS = [

    24,

    12,

    14,

    12,

    12,

    10,

    10,

    6,
]


# ==========================================================
# Icon Resolver
# ==========================================================

def resolve_icon(
    semantic: str,
    fallback: str | None = None,
) -> str | None:

    icon = get_icon(
        semantic
    )

    if icon is None and fallback:

        icon = get_lucide_icon(
            fallback
        )

    return icon


# ==========================================================
# Contact
# ==========================================================

def generate_contact(
    index: int,
) -> dict:

    name = fake.name()

    initials = "".join(
        part[0]
        for part in name.split()[:2]
    ).upper()


    return {

        "id":
            f"contact_{index}",

        "name":
            name,

        "initials":
            initials,

        "phone":
            fake.numerify(
                "010-####-####"
            ),

        "location":
            random.choice([
                "mobile",
                "home",
                "work",
            ]),

        "favorite":
            random.random() < 0.35,

        "missed":
            random.random() < 0.28,

        "incoming":
            random.random() < 0.50,

        "time":
            random.choice([
                "9:41 AM",
                "10:08 AM",
                "11:27 AM",
                "1:05 PM",
                "3:18 PM",
                "Yesterday",
                "Friday",
            ]),

        "duration":
            random.choice([
                "1 min",
                "3 min",
                "6 min",
                "12 min",
            ]),
    }


# ==========================================================
# Contacts
# ==========================================================

def generate_contacts(
    count: int = 9,
) -> list[dict]:

    return [

        generate_contact(
            index
        )

        for index
        in range(
            count
        )
    ]


# ==========================================================
# Voicemail
# ==========================================================

def generate_voicemails(
    contacts: list[dict],
) -> list[dict]:

    items = []


    for index, contact in enumerate(
        contacts[:6]
    ):

        items.append({

            "id":
                f"voicemail_{index}",

            "name":
                contact["name"],

            "phone":
                contact["phone"],

            "time":
                contact["time"],

            "duration":
                random.choice([
                    "0:18",
                    "0:32",
                    "1:04",
                    "2:11",
                ]),

            "unread":
                random.random() < 0.45,
        })


    return items


# ==========================================================
# Keypad
# ==========================================================

def generate_keypad() -> list[dict]:

    return [

        {
            "digit": "1",
            "letters": "",
        },

        {
            "digit": "2",
            "letters": "ABC",
        },

        {
            "digit": "3",
            "letters": "DEF",
        },

        {
            "digit": "4",
            "letters": "GHI",
        },

        {
            "digit": "5",
            "letters": "JKL",
        },

        {
            "digit": "6",
            "letters": "MNO",
        },

        {
            "digit": "7",
            "letters": "PQRS",
        },

        {
            "digit": "8",
            "letters": "TUV",
        },

        {
            "digit": "9",
            "letters": "WXYZ",
        },

        {
            "digit": "*",
            "letters": "",
        },

        {
            "digit": "0",
            "letters": "+",
        },

        {
            "digit": "#",
            "letters": "",
        },
    ]


# ==========================================================
# Active Call
# ==========================================================

def generate_call_data(
    contact: dict,
) -> dict:

    return {

        "contact":
            contact,

        "duration":
            random.choice([
                "00:18",
                "01:24",
                "03:42",
                "12:05",
            ]),

        "muted":
            random.random() < 0.15,

        "speaker":
            random.random() < 0.22,

        "video_available":
            random.random() < 0.65,
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_phone_data(
    *,
    viewport: dict | None = None,
    state: str | None = None,
) -> dict:

    # ======================================================
    # State
    # ======================================================

    if state is None:

        state = random.choices(

            PHONE_STATES,

            weights=
                PHONE_STATE_WEIGHTS,

            k=1,

        )[0]


    if state not in PHONE_STATES:

        raise ValueError(
            f"Unknown Phone state: {state}"
        )


    # ======================================================
    # Device
    # ======================================================

    category = (

        viewport.get(
            "category",
            ""
        )

        if viewport
        else ""
    )


    device_family = (

        "ipad"

        if category == "tablet"

        else "iphone"
    )


    # ======================================================
    # Contacts
    # ======================================================

    contacts = generate_contacts()


    favorite_contacts = [

        contact

        for contact
        in contacts

        if contact["favorite"]
    ]


    if not favorite_contacts:

        favorite_contacts = contacts[:3]


    active_contact = random.choice(
        contacts
    )


    # ======================================================
    # Overlay States
    # ======================================================

    is_overlay_state = (
        state
        in {
            "add_contact_sheet",
        }
    )


    # ======================================================
    # Data
    # ======================================================

    return {

        "state":
            state,

        "device_family":
            device_family,

        "is_overlay_state":
            is_overlay_state,

        "title":
            "Phone",


        # --------------------------------------------------
        # Contacts
        # --------------------------------------------------

        "contacts":
            contacts,

        "favorites":
            favorite_contacts,

        "active_contact":
            active_contact,


        # --------------------------------------------------
        # Keypad
        # --------------------------------------------------

        "keypad":
            generate_keypad(),

        "dialed_number":
            random.choice([
                "",
                "01012345678",
                "021234567",
            ]),


        # --------------------------------------------------
        # Voicemail
        # --------------------------------------------------

        "voicemails":
            generate_voicemails(
                contacts
            ),


        # --------------------------------------------------
        # Call
        # --------------------------------------------------

        "call":
            generate_call_data(
                active_contact
            ),


        # --------------------------------------------------
        # Icons
        # --------------------------------------------------

        "icons": {

            "phone":
                resolve_icon(
                    "phone"
                ),

            "phone_call":
                resolve_icon(
                    "phone_call",
                    "phone-call",
                ),

            "phone_off":
                resolve_icon(
                    "phone_off",
                    "phone-off",
                ),

            "back":
                resolve_icon(
                    "back",
                    "chevron-left",
                ),

            "info":
                resolve_icon(
                    "info"
                ),

            "search":
                resolve_icon(
                    "search"
                ),

            "star":
                get_lucide_icon(
                    "star"
                ),

            "clock":
                get_lucide_icon(
                    "clock-3"
                ),

            "users":
                get_lucide_icon(
                    "users"
                ),

            "keypad":
                get_lucide_icon(
                    "grid-3x3"
                ),

            "voicemail":
                get_lucide_icon(
                    "audio-lines"
                ),

            "mic":
                get_lucide_icon(
                    "mic"
                ),

            "mic_off":
                get_lucide_icon(
                    "mic-off"
                ),

            "speaker":
                get_lucide_icon(
                    "volume-2"
                ),

            "video":
                get_lucide_icon(
                    "video"
                ),

            "plus":
                get_lucide_icon(
                    "plus"
                ),

            "contacts":
                get_lucide_icon(
                    "contact"
                ),

            "delete":
                get_lucide_icon(
                    "delete"
                ),

            "message":
                resolve_icon(
                    "message",
                    "message-circle",
                ),

            "mail":
                resolve_icon(
                    "mail"
                ),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint


    for state in PHONE_STATES:

        print(
            "\n"
            "=========================================="
        )

        print(
            state
        )

        print(
            "=========================================="
        )

        pprint(

            generate_phone_data(
                state=
                    state
            ),

            sort_dicts=False,
        )