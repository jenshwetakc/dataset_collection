from __future__ import annotations

from android.renderers.common_renderer import (
    render_android_page,
)


# ==========================================================
# Settings Renderer
# ==========================================================

async def render_settings_page(
    browser,
    sample_index: int,
    settings: dict,
    system: dict,
    theme: dict,
    viewport: dict,

    annotation_profiles:
        list[str] | None = None,

    capture_full_page: bool = True,

    capture_viewports: bool = True,

    scroll_percentages:
        list[int | float] | None = None,

    min_scroll_delta: int = 80,
):

    return await render_android_page(

        browser=
            browser,

        sample_index=
            sample_index,

        page_type=
            "settings",

        template_name=
            "settings.html",

        context_key=
            "settings",

        page_data=
            settings,

        system=
            system,

        theme=
            theme,

        viewport=
            viewport,

        output_subdir=
            "settings",

        annotation_profiles=
            annotation_profiles,

        capture_full_page=
            False,

        capture_viewports=
            capture_viewports,

        scroll_percentages=
            scroll_percentages,

        min_scroll_delta=
            min_scroll_delta,
    )