from __future__ import annotations

from pathlib import Path

from social_media.common.cc import (
    render_page as common_render_page,
)


# ==========================================================
# Spotify Paths
# ==========================================================

SPOTIFY_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)


TEMPLATE_DIR = (
    SPOTIFY_ROOT
    / "templates"
)


OUTPUT_ROOT = (
    SPOTIFY_ROOT
    / "output"
)


# ==========================================================
# Spotify Render Wrapper
# ==========================================================

async def render_spotify_page(
    browser,
    sample_index: int,
    page_type: str,
    template_name: str,
    context_key: str,
    page_data: dict,
    system: dict,
    theme: dict,
    viewport: dict,
    output_subdir: str | None = None,
    annotation_profiles: list[str] | None = None,
):
    """
    Spotify-specific wrapper around the common renderer.

    This supplies only Spotify paths.

    All bbox extraction, annotation filtering, JSON,
    YOLO and visualization logic remains in the common
    renderer.
    """

    return await common_render_page(

        browser=browser,

        sample_index=
            sample_index,

        page_type=
            page_type,

        template_name=
            template_name,

        context_key=
            context_key,

        page_data=
            page_data,

        system=
            system,

        theme=
            theme,

        viewport=
            viewport,

        template_dir=
            TEMPLATE_DIR,

        output_root=
            OUTPUT_ROOT,

        output_subdir=
            output_subdir,

        annotation_profiles=
            annotation_profiles,
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "SPOTIFY RENDERER"
    )

    print(
        "=============================="
    )

    print(
        "Spotify root:",
        SPOTIFY_ROOT
    )

    print(
        "Template directory:",
        TEMPLATE_DIR
    )

    print(
        "Template exists:",
        TEMPLATE_DIR.exists()
    )

    print(
        "Output root:",
        OUTPUT_ROOT
    )