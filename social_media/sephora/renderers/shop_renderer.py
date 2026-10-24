from __future__ import annotations

import asyncio
from pathlib import Path

from playwright.async_api import async_playwright
from tqdm import tqdm

from social_media.common.palette_generator import (
    generate_accessible_theme,
)

from social_media.common.dynamic_system_generator import (
    generate_system_data,
)

from social_media.sephora.generators.shop_generator import (
    SHOP_STATES,
    apply_shop_state,
    generate_shop_page,
)

from social_media.sephora.renderers.common_renderer import (
    render_page,
    resolve_viewports,
)


SEPHORA_ROOT = Path(__file__).resolve().parents[1]

TEMPLATE_DIR = SEPHORA_ROOT / "templates"
OUTPUT_ROOT = SEPHORA_ROOT / "output"


# ==========================================================
# Dataset configuration
# ==========================================================

NUM_SAMPLES = 2

VIEWPORT_MODE = "selected"

SELECTED_VIEWPORTS = [
    "small_mobile",
    "standard_iphone",
    "tablet_portrait",
    "laptop",
    "desktop_fhd",
]

ANNOTATION_PROFILES = [
    "big_components",
    "small_elements",
]

THEME_MODE = "random"

SYSTEM_STYLE = "random"
SYSTEM_ICON_DENSITY = "random"

# None respects the platform default.
# True places every system bar at the top.
SYSTEM_TOP_BAR = None

CAPTURE_FULL_PAGE = False
CAPTURE_VIEWPORTS = True

SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]

SAVE_VISUALIZATIONS = True

MIN_VISIBLE_RATIO = 0.20

SELECTED_STATES = list(SHOP_STATES)

# None uses the shared ASSETS_ROOT.
# Example:
MEDIA_DIR = Path("/Users/shwetakc/pythonProject3/assets/saphora")
# MEDIA_DIR = None


async def main() -> None:
    unknown_states = set(SELECTED_STATES) - set(SHOP_STATES)

    if unknown_states:
        raise ValueError(
            f"Unknown states: {sorted(unknown_states)}"
        )

    if THEME_MODE not in {"light", "dark", "random"}:
        raise ValueError(
            "THEME_MODE must be light, dark, or random."
        )

    viewports = resolve_viewports(
        mode=VIEWPORT_MODE,
        selected=SELECTED_VIEWPORTS,
    )

    total = (
        NUM_SAMPLES
        * len(viewports)
        * len(SELECTED_STATES)
    )

    failures = []

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True,
        )

        try:
            with tqdm(
                total=total,
                desc="Sephora shop",
                unit="render",
            ) as progress:
                for sample_index in range(NUM_SAMPLES):
                    base_data = generate_shop_page(
                        sample_index=sample_index,
                        media_dir=MEDIA_DIR,
                    )

                    theme = generate_accessible_theme(
                        mode=(
                            None
                            if THEME_MODE == "random"
                            else THEME_MODE
                        ),
                    )

                    for viewport in viewports:
                        system = generate_system_data(
                            style=SYSTEM_STYLE,
                            icon_density=SYSTEM_ICON_DENSITY,
                            viewport=viewport,
                            top_bar=SYSTEM_TOP_BAR,
                        )

                        for state in SELECTED_STATES:
                            page_data = apply_shop_state(
                                base_data,
                                state,
                            )

                            try:
                                await render_page(
                                    browser=browser,
                                    sample_index=sample_index,

                                    # Include state in filenames.
                                    page_type=f"shop_{state}",

                                    template_name="shop.html",
                                    context_key="sephora",
                                    page_data=page_data,
                                    system=system,
                                    theme=theme,
                                    viewport=viewport,
                                    template_dir=TEMPLATE_DIR,
                                    output_root=OUTPUT_ROOT,

                                    # All states use this directory.
                                    output_subdir="shop",

                                    annotation_profiles=ANNOTATION_PROFILES,
                                    min_visible_ratio=MIN_VISIBLE_RATIO,
                                    capture_full_page=CAPTURE_FULL_PAGE,
                                    capture_viewports=CAPTURE_VIEWPORTS,

                                    # Fixed popups need only one
                                    # viewport capture.
                                    scroll_percentages=(
                                        [0]
                                        if page_data["popup_visible"]
                                        else SCROLL_PERCENTAGES
                                    ),

                                    save_visualizations=SAVE_VISUALIZATIONS,
                                )

                            except Exception as exc:
                                failure = (
                                    f"sample={sample_index} "
                                    f"state={state} "
                                    f"viewport={viewport['name']} "
                                    f"error={exc!r}"
                                )

                                failures.append(failure)

                                tqdm.write(
                                    f"[SEPHORA FAILED] {failure}"
                                )

                            finally:
                                progress.update(1)

        finally:
            await browser.close()

    if failures:
        raise RuntimeError(
            f"{len(failures)} Sephora renders failed. "
            "See the failure messages above."
        )


if __name__ == "__main__":
    asyncio.run(main())