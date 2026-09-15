from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# Prompt Ideas
# ==========================================================

IMAGE_PROMPTS = [
    (
        "A futuristic research laboratory with large glass "
        "windows, soft morning light, and minimal architecture"
    ),
    (
        "A cozy reading room filled with books and warm natural "
        "light, photographed in a cinematic style"
    ),
    (
        "An abstract visualization of artificial intelligence "
        "with flowing geometric shapes and glowing particles"
    ),
    (
        "A modern mobile application workspace displayed on a "
        "clean desk with soft studio lighting"
    ),
    (
        "A peaceful mountain village surrounded by clouds at "
        "sunrise, realistic landscape photography"
    ),
    (
        "A colorful isometric illustration of a machine learning "
        "pipeline with connected components"
    ),
]


# ==========================================================
# Image Styles
# ==========================================================

IMAGE_STYLES = [
    "Natural",
    "Vivid",
    "Cinematic",
    "Illustration",
    "Minimal",
    "Photorealistic",
]


# ==========================================================
# Aspect Ratios
# ==========================================================

ASPECT_RATIOS = [
    {
        "id": "square",
        "label": "Square",
        "ratio": "1:1",
    },
    {
        "id": "landscape",
        "label": "Landscape",
        "ratio": "16:9",
    },
    {
        "id": "portrait",
        "label": "Portrait",
        "ratio": "4:5",
    },
]


# ==========================================================
# Visual Variants
# ==========================================================

GRADIENT_VARIANTS = [
    "variant-a",
    "variant-b",
    "variant-c",
    "variant-d",
    "variant-e",
    "variant-f",
    "variant-g",
    "variant-h",
]


# ==========================================================
# History
# ==========================================================

def generate_history() -> list[dict]:

    groups = []

    history_titles = [
        "Generate landscape images",
        "UI illustration ideas",
        "Research diagram",
        "Image editing prompt",
        "Presentation visuals",
        "Abstract background",
        "Design concept",
        "Product mockup",
    ]

    for group_index, label in enumerate(
        [
            "Today",
            "Yesterday",
            "Previous 7 days",
        ]
    ):

        count = random.randint(
            2,
            4,
        )

        items = []

        for item_index in range(
            count
        ):

            items.append({

                "title":
                    random.choice(
                        history_titles
                    ),

                "active":
                    (
                        group_index == 0
                        and item_index == 0
                    ),
            })

        groups.append({

            "label":
                label,

            "items":
                items,
        })

    return groups


# ==========================================================
# Generated Image
# ==========================================================

def generate_image_item(
    index: int,
) -> dict:

    complete = (
        random.random()
        > 0.18
    )

    if complete:

        progress = 100

    else:

        progress = random.randint(
            20,
            88,
        )

    return {

        "id":
            f"generated_image_{index}",

        "variant":
            random.choice(
                GRADIENT_VARIANTS
            ),

        "complete":
            complete,

        "progress":
            progress,

        "selected":
            False,

        "favorite":
            random.random()
            < 0.12,
    }


# ==========================================================
# Suggestions
# ==========================================================

def generate_follow_up_suggestions() -> list[str]:

    suggestions = [
        "Make it more realistic",
        "Use warmer lighting",
        "Create a portrait version",
        "Add more detail",
        "Make the background simpler",
        "Try a cinematic style",
        "Create another variation",
        "Use softer colors",
    ]

    return random.sample(
        suggestions,
        k=random.randint(
            3,
            5,
        ),
    )


# ==========================================================
# Main Generator
# ==========================================================

def generate_image_generation_data() -> dict:

    image_count = random.choice([
        2,
        4,
    ])

    images = [

        generate_image_item(
            index
        )

        for index in range(
            image_count
        )
    ]

    completed_images = [
        image
        for image in images
        if image["complete"]
    ]

    if completed_images:

        selected_image = random.choice(
            completed_images
        )

        selected_image["selected"] = True

    prompt = random.choice(
        IMAGE_PROMPTS
    )

    user_name = fake.first_name()

    return {

        "page_variant":
            "image_generation",

        "model": {

            "name":
                random.choice([
                    "ChatGPT",
                    "GPT-5",
                    "GPT-5 Thinking",
                ]),
        },

        "user": {

            "name":
                user_name,

            "initials":
                user_name[:1].upper(),
        },

        "history_sections":
            generate_history(),

        "prompt":
            prompt,

        "style":
            random.choice(
                IMAGE_STYLES
            ),

        "aspect_ratio":
            random.choice(
                ASPECT_RATIOS
            ),

        "generation_status":
            random.choice([
                "Generated",
                "Creating variations",
                "Image ready",
            ]),

        "images":
            images,

        "suggestions":
            generate_follow_up_suggestions(),

        "composer": {

            "placeholder":
                random.choice([
                    "Describe changes",
                    "Ask for another image",
                    "Message ChatGPT",
                ]),
        },
    }


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    import pprint

    pprint.pp(
        generate_image_generation_data()
    )