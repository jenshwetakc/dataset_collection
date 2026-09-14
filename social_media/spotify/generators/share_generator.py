from __future__ import annotations

import random
import re

from social_media.spotify.generators.media_generator import (
    get_random_album_cover,
    get_random_playlist_cover,
    get_random_podcast_cover,
)

from social_media.spotify.generators.navigation_generator import (
    generate_navigation,
)


# ==========================================================
# Data Pools
# ==========================================================

TRACK_TITLES = [
    "Midnight Drive",
    "Golden Hour",
    "Northern Lights",
    "After Midnight",
    "Slow Motion",
    "Daydream",
    "Open Roads",
    "Blue Horizon",
    "Quiet Places",
    "Summer Rain",
    "Parallel Lines",
    "Falling Stars",
]

ARTIST_NAMES = [
    "Maya Chen",
    "Leo Hart",
    "Aria Stone",
    "Noah Reed",
    "Luna Park",
    "River Lane",
    "Nova Lights",
    "Daniel Grey",
    "Hana Lee",
    "Elena Cruz",
]

ALBUM_NAMES = [
    "Northern Lights",
    "After Midnight",
    "Fragments",
    "Blue Horizon",
    "City Dreams",
    "Parallel Lines",
    "Quiet Places",
    "Open Roads",
    "New Beginnings",
]

PLAYLIST_NAMES = [
    "Late Night Mix",
    "Study Sessions",
    "Road Trip",
    "Weekend Vibes",
    "Morning Energy",
    "Chill Collection",
    "Workout Rotation",
    "Daily Favorites",
    "Focus Mode",
    "Summer Memories",
]

SHOW_NAMES = [
    "Tech Today",
    "Creative Minds",
    "Science Explained",
    "Inside Innovation",
    "Developer Radio",
    "Future Thinking",
    "Design Stories",
]

SHARE_ACTION_POOL = [
    {"label": "Copy link", "icon": "link"},
    {"label": "Messages", "icon": "chat"},
    {"label": "Email", "icon": "mail"},
    {"label": "More", "icon": "share"},
    {"label": "QR code", "icon": "qr_code"},
    {"label": "Bluetooth", "icon": "bluetooth"},
    {"label": "Nearby", "icon": "near_me"},
]


# ==========================================================
# Helpers
# ==========================================================

def slugify(text: str) -> str:
    return re.sub(
        r"[^a-z0-9]+",
        "-",
        text.lower(),
    ).strip("-")


def generate_background_track() -> dict:
    return {
        "title": random.choice(TRACK_TITLES),
        "artist": random.choice(ARTIST_NAMES),
        "image": get_random_album_cover(),
        "duration": f"{random.randint(2, 5)}:{random.randint(0, 59):02d}",
        "liked": random.random() < 0.25,
    }


def generate_entity() -> dict:
    entity_type = random.choice(
        [
            "track",
            "album",
            "playlist",
            "episode",
        ]
    )

    if entity_type == "track":
        title = random.choice(TRACK_TITLES)
        subtitle = random.choice(ARTIST_NAMES)
        meta = random.choice(ALBUM_NAMES)
        image = get_random_album_cover()
        share_title = "Share track"
        url_prefix = "track"

    elif entity_type == "album":
        title = random.choice(ALBUM_NAMES)
        subtitle = random.choice(ARTIST_NAMES)
        meta = "Album"
        image = get_random_album_cover()
        share_title = "Share album"
        url_prefix = "album"

    elif entity_type == "playlist":
        title = random.choice(PLAYLIST_NAMES)
        subtitle = "Spotify"
        meta = f"Playlist • {random.randint(18, 120)} songs"
        image = (
            get_random_playlist_cover()
            or get_random_album_cover()
        )
        share_title = "Share playlist"
        url_prefix = "playlist"

    else:
        title = random.choice(
            [
                "How AI Is Changing Creative Work",
                "The Future of Personal Computing",
                "Designing for Millions of Users",
                "What Comes After Smartphones?",
                "How Developers Learn Faster",
            ]
        )
        subtitle = random.choice(SHOW_NAMES)
        meta = "Podcast episode"
        image = (
            get_random_podcast_cover()
            or get_random_album_cover()
        )
        share_title = "Share episode"
        url_prefix = "episode"

    share_url = (
        f"https://open.spotify.com/{url_prefix}/"
        f"{slugify(title)[:24]}-{random.randint(1000, 9999)}"
    )

    return {
        "type": entity_type,
        "title": title,
        "subtitle": subtitle,
        "meta": meta,
        "image": image,
        "share_title": share_title,
        "share_url": share_url,
    }


# ==========================================================
# Page Generator
# ==========================================================

def generate_share_page() -> dict:
    entity = generate_entity()

    selected_actions = random.sample(
        SHARE_ACTION_POOL,
        k=4,
    )

    return {
        "navigation": generate_navigation(
            selected="home"
        ),
        "entity": entity,
        "dialog_title": "Share",
        "actions": selected_actions,
        "copy_button_label": "Copy link",
        "background": {
            "title": "Now Playing",
            "subtitle": "Share music with friends",
            "tracks": [
                generate_background_track()
                for _ in range(random.randint(6, 10))
            ],
        },
    }