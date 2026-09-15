import random

from faker import Faker

from social_media.whatsapp.generators.media_generator import (
    get_random_avatar,
    get_random_chat_image,
)


fake = Faker()


# ==========================================================
# Call Duration
# ==========================================================

def generate_call_duration():

    minutes = random.randint(
        0,
        59,
    )

    seconds = random.randint(
        0,
        59,
    )

    return f"{minutes:02d}:{seconds:02d}"


# ==========================================================
# Participant
# ==========================================================

def generate_participant(
    is_self=False,
):

    video_enabled = (
        random.random() < 0.75
    )


    return {

        "name":
            (
                "You"
                if is_self
                else fake.name()
            ),

        "avatar":
            get_random_avatar(),

        "video_image":
            (
                get_random_chat_image()
                if video_enabled
                else None
            ),

        "video_enabled":
            video_enabled,

        "muted":
            random.random() < 0.35,

        "speaking":
            (
                random.random() < 0.30
                if not is_self
                else False
            ),

        "is_self":
            is_self,
    }


# ==========================================================
# Controls
# ==========================================================

def generate_controls():

    return {

        "microphone_enabled":
            random.random() < 0.80,

        "camera_enabled":
            random.random() < 0.80,

        "speaker_enabled":
            random.random() < 0.70,

        "flip_camera":
            True,

        "more":
            True,

        "end_call":
            True,
    }


# ==========================================================
# Single Video Call
# ==========================================================

def generate_single_video_call():

    remote = (
        generate_participant(
            is_self=False
        )
    )

    self_participant = (
        generate_participant(
            is_self=True
        )
    )


    return {

        "mode":
            "single",

        "call_type":
            "video",

        "status":
            random.choice(
                [
                    "connected",
                    "ringing",
                ]
            ),

        "duration":
            generate_call_duration(),

        "participants":
            [
                remote
            ],

        "self_participant":
            self_participant,

        "controls":
            generate_controls(),

        "title":
            remote["name"],
    }


# ==========================================================
# Group Video Call
# ==========================================================

def generate_group_video_call(
    min_participants=3,
    max_participants=9,
):

    participant_count = random.randint(
        min_participants,
        max_participants,
    )


    participants = [

        generate_participant(
            is_self=False
        )

        for _ in range(
            participant_count - 1
        )
    ]


    self_participant = (
        generate_participant(
            is_self=True
        )
    )


    return {

        "mode":
            "group",

        "call_type":
            "video",

        "status":
            "connected",

        "duration":
            generate_call_duration(),

        "participants":
            participants,

        "self_participant":
            self_participant,

        "participant_count":
            participant_count,

        "controls":
            generate_controls(),

        "title":
            f"{participant_count} participants",
    }


# ==========================================================
# Generic Entry Point
# ==========================================================

def generate_video_call_page(
    mode="single",
):

    if mode == "group":

        return (
            generate_group_video_call()
        )


    return (
        generate_single_video_call()
    )


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    print(
        "\nSINGLE CALL"
    )

    single = (
        generate_video_call_page(
            mode="single"
        )
    )

    print(
        single
    )


    print(
        "\nGROUP CALL"
    )

    group = (
        generate_video_call_page(
            mode="group"
        )
    )

    print(
        group
    )