from __future__ import annotations

from pathlib import Path

from social_media.common.all_common import (
    render_page,
    resolve_viewports,
)


SEPHORA_ROOT = Path(__file__).resolve().parents[1]

TEMPLATE_DIR = SEPHORA_ROOT / "templates"
OUTPUT_ROOT = SEPHORA_ROOT / "output"


async def render_uptodate_page(
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
    capture_full_page: bool = False,
    capture_viewports: bool = True,
    scroll_percentages: list[int | float] | None = None,
    min_visible_ratio: float = 0.20,
    save_visualizations: bool = True,
):
    return await render_page(
        browser=browser,
        sample_index=sample_index,
        page_type=page_type,
        template_name=template_name,
        context_key=context_key,
        page_data=page_data,
        system=system,
        theme=theme,
        viewport=viewport,
        template_dir=TEMPLATE_DIR,
        output_root=OUTPUT_ROOT,
        output_subdir=output_subdir,
        annotation_profiles=annotation_profiles,
        capture_full_page=capture_full_page,
        capture_viewports=capture_viewports,
        scroll_percentages=scroll_percentages,
        min_visible_ratio=min_visible_ratio,
        save_visualizations=save_visualizations,
    )