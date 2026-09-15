import random

from faker import Faker

from social_media.whatsapp.generators.media_generator import (
    get_random_avatar,
    get_random_chat_image,
)


fake = Faker()


# ==========================================================
# Helpers
# ==========================================================

def generate_storage_values():

    total_gb = random.choice(
        [
            32.0,
            64.0,
            128.0,
            256.0,
        ]
    )

    used_gb = round(
        random.uniform(
            total_gb * 0.15,
            total_gb * 0.90,
        ),
        1,
    )

    free_gb = round(
        total_gb - used_gb,
        1,
    )

    used_percent = round(
        (
            used_gb
            / total_gb
        )
        * 100,
        1,
    )

    return {
        "used_gb":
            used_gb,

        "free_gb":
            free_gb,

        "total_gb":
            total_gb,

        "used_percent":
            used_percent,
    }


def generate_size_label(
    min_mb=50,
    max_mb=5000,
):

    value = random.uniform(
        min_mb,
        max_mb,
    )

    if value >= 1024:

        return (
            f"{value / 1024:.1f} GB"
        )

    return (
        f"{value:.0f} MB"
    )


def generate_media_count():

    return random.randint(
        10,
        900,
    )


# ==========================================================
# Media Preview
# ==========================================================

def generate_media_preview(
    min_items=3,
    max_items=6,
):

    count = random.randint(
        min_items,
        max_items,
    )

    items = []

    for _ in range(
        count
    ):

        media_type = random.choices(
            [
                "image",
                "video",
            ],
            weights=[
                0.78,
                0.22,
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
                        f"{random.randint(0, 8)}:"
                        f"{random.randint(0, 59):02d}"
                        if media_type == "video"
                        else None
                    ),
            }
        )

    return items


# ==========================================================
# Storage Category
# ==========================================================

def generate_storage_category(
    category_id,
    title,
):

    return {

        "id":
            category_id,

        "title":
            title,

        "size":
            generate_size_label(
                min_mb=300,
                max_mb=8000,
            ),

        "media_count":
            generate_media_count(),

        "media":
            generate_media_preview(
                min_items=3,
                max_items=5,
            ),
    }


# ==========================================================
# Chat Storage Item
# ==========================================================

def generate_chat_storage_item():

    chat_type = random.choices(
        [
            "person",
            "group",
        ],
        weights=[
            0.60,
            0.40,
        ],
        k=1,
    )[0]


    if chat_type == "group":

        name = random.choice(
            [
                fake.company(),
                fake.catch_phrase(),
                f"{fake.word().title()} Group",
            ]
        )

    else:

        name = fake.name()


    return {

        "name":
            name,

        "avatar":
            get_random_avatar(),

        "chat_type":
            chat_type,

        "size_mb":
            round(
                random.uniform(
                    10,
                    6000,
                ),
                1,
            ),

        "media_count":
            generate_media_count(),

        "message_count":
            random.randint(
                100,
                30000,
            ),
    }


# ==========================================================
# Sort Chats
# ==========================================================

def sort_chats_by_storage(
    chats,
):

    return sorted(
        chats,
        key=lambda item: item["size_mb"],
        reverse=True,
    )


# ==========================================================
# Format Chat Size
# ==========================================================

def format_chat_size(
    size_mb,
):

    if size_mb >= 1024:

        return (
            f"{size_mb / 1024:.1f} GB"
        )

    return (
        f"{size_mb:.0f} MB"
    )


# ==========================================================
# Storage Manager Page
# ==========================================================

def generate_storage_manager_page(
    min_chats=6,
    max_chats=14,
):

    storage = (
        generate_storage_values()
    )


    categories = [

        generate_storage_category(
            category_id="large_files",
            title="Larger than 5 MB",
        ),

        generate_storage_category(
            category_id="forwarded_many_times",
            title="Forwarded many times",
        ),
    ]


    # Optional third category for more diversity.
    if random.random() < 0.35:

        categories.append(
            generate_storage_category(
                category_id="recent_media",
                title="Recently received",
            )
        )


    chat_count = random.randint(
        min_chats,
        max_chats,
    )


    chats = [

        generate_chat_storage_item()

        for _ in range(
            chat_count
        )
    ]


    chats = (
        sort_chats_by_storage(
            chats
        )
    )


    # Add formatted value after sorting.
    for chat in chats:

        chat["size"] = (
            format_chat_size(
                chat["size_mb"]
            )
        )


    return {

        # --------------------------------------------------
        # Page
        # --------------------------------------------------

        "title":
            "Manage storage",

        # --------------------------------------------------
        # Device Storage
        # --------------------------------------------------

        "storage":
            storage,

        # --------------------------------------------------
        # Review Categories
        # --------------------------------------------------

        "categories":
            categories,

        "category_count":
            len(categories),

        # --------------------------------------------------
        # Chats
        # --------------------------------------------------

        "chats":
            chats,

        "chat_count":
            len(chats),

        # --------------------------------------------------
        # UI
        # --------------------------------------------------

        "show_search":
            True,

        "show_overflow":
            random.random() < 0.40,

        "show_free_space":
            True,
    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_storage_manager_page()
    )


    print(
        "\nSTORAGE MANAGER"
    )

    print(
        "Title:",
        page["title"]
    )

    print(
        "Used:",
        page["storage"]["used_gb"],
        "GB"
    )

    print(
        "Free:",
        page["storage"]["free_gb"],
        "GB"
    )

    print(
        "Total:",
        page["storage"]["total_gb"],
        "GB"
    )

    print(
        "Used percent:",
        page["storage"]["used_percent"]
    )

    print(
        "Categories:",
        page["category_count"]
    )

    print(
        "Chats:",
        page["chat_count"]
    )


    print(
        "\nCATEGORIES"
    )

    for category in page[
        "categories"
    ]:

        print(
            "-",
            category["title"],
            "|",
            category["size"],
            "|",
            category["media_count"],
            "items",
        )


    print(
        "\nTOP CHATS"
    )

    for chat in page[
        "chats"
    ][:5]:

        print(
            "-",
            chat["name"],
            "|",
            chat["size"],
            "| media:",
            chat["media_count"],
        )