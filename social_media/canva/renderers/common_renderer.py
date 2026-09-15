from __future__ import annotations

from pathlib import Path

# from social_media.common.common_renderer import (
#     DEFAULT_CAPTURE_FULL_PAGE,
#     DEFAULT_CAPTURE_VIEWPORTS,
#     DEFAULT_MIN_SCROLL_DELTA,
#     DEFAULT_MIN_VISIBLE_RATIO,
#     DEFAULT_SCROLL_SETTLE_MS,
#     render_page as common_render_page,
# )
from social_media.common.cc import (
    DEFAULT_CAPTURE_FULL_PAGE,
    DEFAULT_CAPTURE_VIEWPORTS,
    DEFAULT_MIN_SCROLL_DELTA,
    DEFAULT_MIN_VISIBLE_RATIO,
    DEFAULT_SCROLL_SETTLE_MS,
    render_page as common_render_page,
)


# ==========================================================
# Canva Paths
# ==========================================================

CANVA_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

TEMPLATE_DIR = (
    CANVA_ROOT
    / "templates"
)

OUTPUT_ROOT = (
    CANVA_ROOT
    / "output"
)


# ==========================================================
# Canva Render Wrapper
# ==========================================================

async def render_canva_page(
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
    Canva-specific wrapper around the common renderer.

    All screenshot capture, scrolling, annotation extraction,
    visibility handling, YOLO export, JSON export, and
    visualization logic remain inside:

        social_media.common.common_renderer
    """

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
        "CANVA RENDERER"
    )

    print(
        "=============================="
    )

    print(
        "Canva root:",
        CANVA_ROOT,
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