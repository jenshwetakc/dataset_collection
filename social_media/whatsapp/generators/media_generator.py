import base64
import mimetypes
import random
from io import BytesIO
from PIL import Image

from pathlib import Path


# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[3]
)


# ==========================================================
# Asset Paths
# ==========================================================

ASSET_DIR = (
    PROJECT_ROOT
    / "assets"
)

print(ASSET_DIR)
NOTO_DIR = (
    ASSET_DIR
    / "noto-emoji"
)
print(NOTO_DIR)

TWEMOJI_DIR = (
    ASSET_DIR
    / "twemoji"
)


AVATAR_DIR = (
    ASSET_DIR
    / "avatars"
)


STICKER_DIR = (
    ASSET_DIR
    / "stickers"
)


GIF_DIR = (
    ASSET_DIR
    / "gifs"
)


CHAT_IMAGE_DIR = (
    ASSET_DIR
    / "photos"
)


# ==========================================================
# Supported Extensions
# ==========================================================

EMOJI_EXTENSIONS = {
    ".png",
    ".svg",
    ".webp",
}


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


GIF_EXTENSIONS = {
    ".gif",
    ".webp",
}


# ==========================================================
# Generic File Scanner
# ==========================================================

def scan_files(
    directory: Path,
    extensions,
):
    """
    Recursively scan a directory and return supported files.
    """

    if not directory.exists():

        print(
            f"[WARNING] Directory does not exist: "
            f"{directory}"
        )

        return []


    return [
        path

        for path
        in directory.rglob("*")

        if (
            path.is_file()
            and path.suffix.lower()
            in extensions
        )
    ]


# ==========================================================
# Convert File -> Data URI
# ==========================================================
def file_to_data_uri(
    path: Path,
):

    if path is None:
        return None

    if not path.exists():
        return None


    # ======================================================
    # SVG
    # ======================================================

    if path.suffix.lower() == ".svg":

        encoded = (
            base64.b64encode(
                path.read_bytes()
            )
            .decode("ascii")
        )

        return (
            "data:image/svg+xml;"
            f"base64,{encoded}"
        )


    # ======================================================
    # Detect actual image format
    # ======================================================

    raw_data = (
        path.read_bytes()
    )


    try:

        with Image.open(
            BytesIO(raw_data)
        ) as image:

            image_format = (
                image.format
            )

    except Exception as error:

        print(
            f"[IMAGE ERROR] "
            f"{path}: {error}"
        )

        return None


    # ======================================================
    # MIME mapping
    # ======================================================

    mime_map = {

        "JPEG":
            "image/jpeg",

        "PNG":
            "image/png",

        "WEBP":
            "image/webp",

        "GIF":
            "image/gif",

        "BMP":
            "image/bmp",
    }


    mime_type = (
        mime_map.get(
            image_format
        )
    )


    if mime_type is None:

        print(
            f"[WARNING] Unsupported format: "
            f"{image_format} | {path}"
        )

        return None


    # ======================================================
    # Encode
    # ======================================================

    encoded = (
        base64.b64encode(
            raw_data
        )
        .decode("ascii")
    )


    return (
        f"data:{mime_type};"
        f"base64,{encoded}"
    )

# ==========================================================
# Cached Asset Lists
# ==========================================================

_NOTO_EMOJIS = None

_TWEMOJIS = None

_AVATARS = None

_STICKERS = None

_GIFS = None

_CHAT_IMAGES = None


# ==========================================================
# Noto Emoji
# ==========================================================

def get_noto_emojis():

    global _NOTO_EMOJIS


    if _NOTO_EMOJIS is None:

        _NOTO_EMOJIS = (
            scan_files(
                NOTO_DIR,
                EMOJI_EXTENSIONS,
            )
        )


    return _NOTO_EMOJIS


# ==========================================================
# Twemoji
# ==========================================================

def get_twemoji_emojis():

    global _TWEMOJIS


    if _TWEMOJIS is None:

        _TWEMOJIS = (
            scan_files(
                TWEMOJI_DIR,
                EMOJI_EXTENSIONS,
            )
        )


    return _TWEMOJIS


# ==========================================================
# Avatars
# ==========================================================

def get_avatars():

    global _AVATARS


    if _AVATARS is None:

        _AVATARS = (
            scan_files(
                AVATAR_DIR,
                IMAGE_EXTENSIONS,
            )
        )


    return _AVATARS


# ==========================================================
# Stickers
# ==========================================================

def get_stickers():

    global _STICKERS


    if _STICKERS is None:

        _STICKERS = (
            scan_files(
                STICKER_DIR,
                IMAGE_EXTENSIONS,
            )
        )


    return _STICKERS


# ==========================================================
# GIFs
# ==========================================================

def get_gifs():

    global _GIFS


    if _GIFS is None:

        _GIFS = (
            scan_files(
                GIF_DIR,
                GIF_EXTENSIONS,
            )
        )


    return _GIFS


# ==========================================================
# Chat Images
# ==========================================================

def get_chat_images():

    global _CHAT_IMAGES


    if _CHAT_IMAGES is None:

        _CHAT_IMAGES = (
            scan_files(
                CHAT_IMAGE_DIR,
                IMAGE_EXTENSIONS,
            )
        )


    return _CHAT_IMAGES


# ==========================================================
# Random File
# ==========================================================

def get_random_file(
    files,
):
    """
    Return one random Path.
    """

    if not files:
        return None


    return random.choice(
        files
    )


# ==========================================================
# Random Data URI
# ==========================================================

def random_file_uri(
    files,
):
    """
    Pick one local asset and convert it
    to a browser-safe data URI.
    """

    selected = (
        get_random_file(
            files
        )
    )


    if selected is None:
        return None


    return file_to_data_uri(
        selected
    )


# ==========================================================
# Emoji
# ==========================================================

def get_random_emoji(
    source: str | None = None,
):
    """
    Return one random emoji.

    source:
        "noto"
        "twemoji"
        None -> random source
    """


    if source is None:

        source = random.choice(
            [
                "noto",
                "twemoji",
            ]
        )


    if source == "noto":

        files = (
            get_noto_emojis()
        )


    elif source == "twemoji":

        files = (
            get_twemoji_emojis()
        )


    else:

        raise ValueError(
            f"Unknown emoji source: "
            f"{source}"
        )


    selected = (
        get_random_file(
            files
        )
    )


    if selected is None:

        return {
            "source":
                source,

            "uri":
                None,

            "path":
                None,

            "filename":
                None,
        }


    return {

        "source":
            source,

        "uri":
            file_to_data_uri(
                selected
            ),

        # Keep useful metadata for JSON/debugging.
        "path":
            str(
                selected.relative_to(
                    ASSET_DIR
                )
            ),

        "filename":
            selected.name,
    }


# ==========================================================
# Avatar
# ==========================================================

def get_random_avatar():

    selected = (
        get_random_file(
            get_avatars()
        )
    )


    if selected is None:
        return None


    return file_to_data_uri(
        selected
    )


# ==========================================================
# Sticker
# ==========================================================

def get_random_sticker():

    selected = (
        get_random_file(
            get_stickers()
        )
    )


    if selected is None:
        return None


    return file_to_data_uri(
        selected
    )


# ==========================================================
# GIF
# ==========================================================

def get_random_gif():

    selected = (
        get_random_file(
            get_gifs()
        )
    )


    if selected is None:
        return None


    return file_to_data_uri(
        selected
    )


# ==========================================================
# Chat Image
# ==========================================================

def get_random_chat_image():

    selected = (
        get_random_file(
            get_chat_images()
        )
    )


    if selected is None:
        return None


    return file_to_data_uri(
        selected
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "ASSET DIRECTORIES"
    )

    print(
        "=============================="
    )


    print(
        "Noto exists:",
        NOTO_DIR.exists()
    )

    print(
        "Twemoji exists:",
        TWEMOJI_DIR.exists()
    )

    print(
        "Avatar exists:",
        AVATAR_DIR.exists()
    )

    print(
        "Sticker exists:",
        STICKER_DIR.exists()
    )

    print(
        "GIF exists:",
        GIF_DIR.exists()
    )

    print(
        "Chat image exists:",
        CHAT_IMAGE_DIR.exists()
    )


    print(
        "\n=============================="
    )

    print(
        "ASSET COUNTS"
    )

    print(
        "=============================="
    )


    print(
        "Noto:",
        len(
            get_noto_emojis()
        )
    )

    print(
        "Twemoji:",
        len(
            get_twemoji_emojis()
        )
    )

    print(
        "Avatars:",
        len(
            get_avatars()
        )
    )

    print(
        "Stickers:",
        len(
            get_stickers()
        )
    )

    print(
        "GIFs:",
        len(
            get_gifs()
        )
    )

    print(
        "Chat images:",
        len(
            get_chat_images()
        )
    )


    print(
        "\n=============================="
    )

    print(
        "TEST RANDOM EMOJI"
    )

    print(
        "=============================="
    )


    emoji = (
        get_random_emoji()
    )


    print(
        "Source:",
        emoji["source"]
    )

    print(
        "Path:",
        emoji["path"]
    )

    print(
        "Filename:",
        emoji["filename"]
    )

    print(
        "URI available:",
        emoji["uri"] is not None
    )


    print(
        "\n=============================="
    )

    print(
        "TEST AVATAR"
    )

    print(
        "=============================="
    )


    avatar = (
        get_random_avatar()
    )


    print(
        "Avatar loaded:",
        avatar is not None
    )



