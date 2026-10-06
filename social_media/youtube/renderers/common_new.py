from __future__ import annotations

from pathlib import Path


from social_media.common.all_common import (
    DEFAULT_CAPTURE_FULL_PAGE,
    DEFAULT_CAPTURE_VIEWPORTS,
    DEFAULT_MIN_SCROLL_DELTA,
    DEFAULT_MIN_VISIBLE_RATIO,
    DEFAULT_SCROLL_SETTLE_MS,
    render_page as common_render_page,
)


# ==========================================================
# YouTube Paths
# ==========================================================

YOUTUBE_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

TEMPLATE_DIR = (
    YOUTUBE_ROOT
    / "templates"
)

OUTPUT_ROOT = (
    YOUTUBE_ROOT
    / "output"
)


# ==========================================================
# YouTube Theme Adapter
# ==========================================================

def prepare_youtube_theme(
    theme: dict,
) -> dict:
    """
    Convert the generated global theme into the structure
    expected by existing YouTube templates.

    YouTube templates use:

        {{ theme.background }}
        {{ theme.surface }}
        {{ theme.text_primary }}
        {{ theme.text_secondary }}
        {{ theme.border }}

    while the palette generator may store these colors under:

        theme["semantic"]

    We merge semantic values onto the top level while keeping
    metadata such as mode, seed, wcag_pass, etc.

    This transformation is YouTube-only and does not affect
    any other application.
    """

    if not isinstance(
        theme,
        dict,
    ):
        return theme


    semantic = (
        theme.get(
            "semantic",
            {},
        )
    )


    if not isinstance(
        semantic,
        dict,
    ):
        semantic = {}


    return {
        **theme,
        **semantic,
    }


# ==========================================================
# YouTube Render Wrapper
# ==========================================================

async def render_youtube_page(
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

    min_visible_ratio: float =
        DEFAULT_MIN_VISIBLE_RATIO,

    capture_full_page: bool =
        DEFAULT_CAPTURE_FULL_PAGE,

    capture_viewports: bool =
        DEFAULT_CAPTURE_VIEWPORTS,

    scroll_percentages: list[int | float] | None = None,

    min_scroll_delta: int =
        DEFAULT_MIN_SCROLL_DELTA,

    scroll_settle_ms: int =
        DEFAULT_SCROLL_SETTLE_MS,
):
    """
    YouTube-specific wrapper around the shared renderer.

    Important:
    YouTube theme normalization happens here so that the
    global renderer remains unchanged for other applications.
    """


    # ======================================================
    # Prepare YouTube Theme
    # ======================================================

    youtube_theme = (
        prepare_youtube_theme(
            theme
        )
    )


    # ======================================================
    # Render
    # ======================================================

    return await common_render_page(

        browser=
            browser,

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

        # --------------------------------------------------
        # YouTube-specific theme.
        # Other applications are unaffected.
        # --------------------------------------------------
        theme=
            youtube_theme,

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

        min_visible_ratio=
            min_visible_ratio,

        capture_full_page=
            capture_full_page,

        capture_viewports=
            capture_viewports,

        scroll_percentages=
            scroll_percentages,

        min_scroll_delta=
            min_scroll_delta,

        scroll_settle_ms=
            scroll_settle_ms,
    )


# ==========================================================
# Debug
# ==========================================================

if __name__ == "__main__":

    print(
        "\n=============================="
    )

    print(
        "YOUTUBE RENDERER"
    )

    print(
        "=============================="
    )

    print(
        "YouTube root:",
        YOUTUBE_ROOT,
    )

    print(
        "Template directory:",
        TEMPLATE_DIR,
    )

    print(
        "Template exists:",
        TEMPLATE_DIR.exists(),
    )

    print(
        "Output root:",
        OUTPUT_ROOT,
    )