import random

from faker import Faker

from social_media.whatsapp.generators.media_generator import (
    get_random_avatar,
    get_random_chat_image,
)


fake = Faker()


# ==========================================================
# Time
# ==========================================================

def generate_status_time():

    return random.choice(
        [
            "Just now",
            "1 min ago",
            "2 min ago",
            "5 min ago",
            "10 min ago",
            "Today, 09:42",
            "Today, 14:15",
            "Yesterday, 22:18",
        ]
    )


# ==========================================================
# Status Media
# ==========================================================

def generate_status_media():

    media_type = random.choices(
        [
            "image",
            "video",
        ],
        weights=[
            0.65,
            0.35,
        ],
        k=1,
    )[0]


    return {

        "type":
            media_type,

        # For now both image and simulated video
        # use a local image asset as the visual frame.
        "media":
            get_random_chat_image(),

        "video_muted":
            (
                random.random() < 0.25
                if media_type == "video"
                else False
            ),

        "video_paused":
            (
                random.random() < 0.12
                if media_type == "video"
                else False
            ),
    }


# ==========================================================
# Caption
# ==========================================================

def generate_caption():

    if random.random() < 0.55:

        return fake.sentence(
            nb_words=random.randint(
                3,
                10,
            )
        )

    return None


# ==========================================================
# Reactions
# ==========================================================

def generate_reactions():

    return random.sample(
        [
            "❤️",
            "😂",
            "😮",
            "😢",
            "🙏",
            "👏",
        ],
        k=random.randint(
            3,
            6,
        ),
    )


# ==========================================================
# Single Status Segment
# ==========================================================

def generate_status_segment():

    media = (
        generate_status_media()
    )


    return {

        "media_type":
            media["type"],

        "media":
            media["media"],

        "video_muted":
            media["video_muted"],

        "video_paused":
            media["video_paused"],

        "caption":
            generate_caption(),

        "time":
            generate_status_time(),
    }


# ==========================================================
# Contact / Status Owner
# ==========================================================

def generate_status_owner():

    return {

        "name":
            fake.name(),

        "avatar":
            get_random_avatar(),
    }


# ==========================================================
# Status Viewer
# ==========================================================

def generate_status_viewer_page(
    min_segments=1,
    max_segments=6,
):

    segment_count = random.randint(
        min_segments,
        max_segments,
    )


    segments = [

        generate_status_segment()

        for _ in range(
            segment_count
        )
    ]


    current_index = random.randint(
        0,
        segment_count - 1,
    )


    current_status = (
        segments[current_index]
    )


    # Progress of currently viewed status.
    current_progress = random.uniform(
        0.10,
        0.95,
    )


    reply_typed = (
        random.random() < 0.20
    )


    return {

        # --------------------------------------------------
        # Screen
        # --------------------------------------------------

        "page_type":
            "status_viewer",

        "owner":
            generate_status_owner(),

        # --------------------------------------------------
        # Stories / segments
        # --------------------------------------------------

        "segments":
            segments,

        "segment_count":
            segment_count,

        "current_index":
            current_index,

        "current":
            current_status,

        "current_progress":
            current_progress,

        # --------------------------------------------------
        # Controls
        # --------------------------------------------------

        "show_back_button":
            True,

        "show_overflow":
            True,

        "show_reaction_button":
            True,

        "show_reply":
            True,

        # --------------------------------------------------
        # Reaction panel
        # --------------------------------------------------

        "reactions":
            generate_reactions(),

        "reaction_panel_open":
            random.random() < 0.10,

        # --------------------------------------------------
        # Reply field
        # --------------------------------------------------

        "reply_placeholder":
            "Reply",

        "reply_text":
            (
                fake.sentence(
                    nb_words=random.randint(
                        2,
                        6,
                    )
                )
                if reply_typed
                else ""
            ),

        "reply_typed":
            reply_typed,

        # --------------------------------------------------
        # Misc state
        # --------------------------------------------------

        "liked":
            random.random() < 0.15,
    }


# ==========================================================
# Debug / Test
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_status_viewer_page()
    )


    print(
        "\nSTATUS VIEWER"
    )

    print(
        "Owner:",
        page["owner"]["name"]
    )

    print(
        "Segments:",
        page["segment_count"]
    )

    print(
        "Current:",
        page["current_index"]
    )

    print(
        "Media:",
        page["current"]["media_type"]
    )

    print(
        "Progress:",
        round(
            page["current_progress"],
            2,
        )
    )

    print(
        "Caption:",
        page["current"]["caption"]
    )

    print(
        "Reply typed:",
        page["reply_typed"]
    )