from __future__ import annotations

import inspect

from pathlib import Path
from typing import Any


# ==========================================================
# Shared Renderer
#
# Adjust this import if your shared all_common.py file
# is located elsewhere.
# ==========================================================

from social_media.common.all_common import (
    render_page as shared_render_page,
)


# ==========================================================
# WEBTOON Paths
# ==========================================================

WEBTOON_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

TEMPLATE_DIR = WEBTOON_ROOT / "templates"

OUTPUT_ROOT = WEBTOON_ROOT / "output"


# ==========================================================
# Defaults
# ==========================================================

DEFAULT_ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]

DEFAULT_SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]


# ==========================================================
# App-Specific Renderer
# ==========================================================

async def render_webtoon_page(
    browser,
    sample_index: int,
    page_type: str,
    template_name: str,
    context_key: str,
    page_data: dict[str, Any],
    system: dict[str, Any],
    theme: dict[str, Any],
    viewport: dict[str, Any],
    output_subdir: str | None = "home",
    annotation_profiles: list[str] | None = None,
    min_visible_ratio: float = 0.20,
    capture_full_page: bool = False,
    capture_viewports: bool = True,
    scroll_percentages: list[int | float] | None = None,
    save_visualizations: bool = True,
    *,
    template_dir: str | Path | None = None,
    output_root: str | Path | None = None,
):
    """
    Render a WEBTOON page through the shared renderer.

    Paths default to this application's templates and output
    directories. Optional explicit paths are accepted for
    compatibility with earlier versions of home_renderer.py.
    """

    resolved_template_dir = (
        Path(template_dir)
        if template_dir is not None
        else TEMPLATE_DIR
    )

    resolved_output_root = (
        Path(output_root)
        if output_root is not None
        else OUTPUT_ROOT
    )

    if not resolved_template_dir.is_dir():
        raise FileNotFoundError(
            "WEBTOON template directory does not exist: "
            f"{resolved_template_dir}"
        )

    template_path = (
        resolved_template_dir
        / template_name
    )

    if not template_path.is_file():
        raise FileNotFoundError(
            "WEBTOON template does not exist: "
            f"{template_path}"
        )

    if not capture_full_page and not capture_viewports:
        raise ValueError(
            "Enable capture_full_page or capture_viewports."
        )

    profiles = (
        list(annotation_profiles)
        if annotation_profiles is not None
        else DEFAULT_ANNOTATION_PROFILES.copy()
    )

    scroll_positions = (
        list(scroll_percentages)
        if scroll_percentages is not None
        else DEFAULT_SCROLL_PERCENTAGES.copy()
    )

    # Popup states capture only the initial position.
    if page_data.get("popup", False):
        scroll_positions = [0]

    kwargs = {
        "browser": browser,
        "sample_index": sample_index,
        "page_type": page_type,
        "template_name": template_name,
        "context_key": context_key,
        "page_data": page_data,
        "system": system,
        "theme": theme,
        "viewport": viewport,
        "template_dir": resolved_template_dir,
        "output_root": resolved_output_root,
        "output_subdir": output_subdir,
        "annotation_profiles": profiles,
        "min_visible_ratio": min_visible_ratio,
        "capture_full_page": capture_full_page,
        "capture_viewports": capture_viewports,
        "scroll_percentages": scroll_positions,
        "save_visualizations": save_visualizations,
    }

    # Validate before calling the shared renderer so that
    # interface mismatches identify the actual source file.
    signature = inspect.signature(
        shared_render_page
    )

    try:
        signature.bind(**kwargs)

    except TypeError as error:
        source_file = inspect.getsourcefile(
            shared_render_page
        )

        raise TypeError(
            "The shared renderer does not expose the expected "
            "generic render_page interface. "
            f"Source: {source_file}. "
            f"Signature: {signature}. "
            f"Details: {error}"
        ) from error

    resolved_output_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    return await shared_render_page(
        **kwargs
    )


# ==========================================================
# Compatibility Alias
#
# Existing home_renderer.py imports render_page.
# New runners may import render_webtoon_page instead.
# ==========================================================

render_page = render_webtoon_page