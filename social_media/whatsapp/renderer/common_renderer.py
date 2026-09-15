from __future__ import annotations

import json

from pathlib import Path

from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)

from PIL import (
    Image,
    ImageDraw,
)

from social_media.common.classes import (
    ANNOTATION_CLASSES,
    GLOBAL_CLASS_TO_ID,
    PROFILE_CLASS_TO_ID,
    get_profile_classes,
)

from social_media.common.viewport import (
    get_all_viewports,
    get_test_viewports,
    get_random_viewport,
    get_viewports_by_category,
    get_viewports_by_names,
    get_viewports_by_size_class,
    get_viewports_by_orientation,
)


# ==========================================================
# Project Paths
# ==========================================================

WHATSAPPROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)


TEMPLATE_DIR = (
    WHATSAPPROOT
    / "templates"
)


OUTPUT_ROOT = (
    WHATSAPPROOT
    / "output"
)

print(OUTPUT_ROOT)

# ==========================================================
# Default Annotation Profiles
# ==========================================================

DEFAULT_ANNOTATION_PROFILES = [
    "big_components",
    "components",
    "small_elements",
    "icons_only",

]


# ==========================================================
# Jinja
# ==========================================================

environment = Environment(

    loader=FileSystemLoader(
        TEMPLATE_DIR
    ),

    autoescape=select_autoescape(
        [
            "html",
            "xml",
        ]
    ),
)


# ==========================================================
# Text Classes
# ==========================================================

TEXT_CLASSES = {
    "text",
    "timestamp",
    "system_text",
}


# ==========================================================
# Viewport Resolver
# ==========================================================

def resolve_viewports(
    mode="selected",
    selected=None,
):

    selected = (
        selected
        or [
            "standard_iphone",
        ]
    )


    # ======================================================
    # All
    # ======================================================

    if mode == "all":

        return get_all_viewports()


    # ======================================================
    # Development / Test Set
    # ======================================================

    if mode == "test":

        return get_test_viewports()


    # ======================================================
    # Categories
    # ======================================================

    if mode in {
        "mobile",
        "mobile_landscape",
        "tablet",
        "foldable",
        "laptop",
        "desktop",
        "ultrawide",
    }:

        return get_viewports_by_category(
            mode
        )


    # ======================================================
    # Material Size Classes
    # ======================================================

    if mode in {
        "compact",
        "medium",
        "expanded",
    }:

        return get_viewports_by_size_class(
            mode
        )


    # ======================================================
    # Orientation
    # ======================================================

    if mode in {
        "portrait",
        "landscape",
    }:

        return get_viewports_by_orientation(
            mode
        )


    # ======================================================
    # Explicit Names
    # ======================================================

    if mode == "selected":

        return get_viewports_by_names(
            selected
        )


    # ======================================================
    # Random
    # ======================================================

    if mode == "random":

        return [
            get_random_viewport()
        ]


    raise ValueError(
        f"Unknown viewport mode: {mode}"
    )


# ==========================================================
# Visibility
# ==========================================================

async def is_actually_visible(
    element,
    min_visible_points=2,
):

    return await element.evaluate(
        """
        (el, minVisiblePoints) => {

            function hiddenByStyle(node) {

                let current = node;

                while (current) {

                    const style =
                        window.getComputedStyle(
                            current
                        );

                    if (
                        style.display === "none" ||
                        style.visibility === "hidden" ||
                        style.visibility === "collapse"
                    ) {
                        return true;
                    }

                    const opacity =
                        parseFloat(
                            style.opacity || "1"
                        );

                    if (opacity <= 0.01) {
                        return true;
                    }

                    current =
                        current.parentElement;
                }

                return false;
            }


            if (hiddenByStyle(el)) {
                return false;
            }


            const rect =
                el.getBoundingClientRect();


            if (
                rect.width <= 0 ||
                rect.height <= 0
            ) {
                return false;
            }


            const viewportWidth =
                window.innerWidth;

            const viewportHeight =
                window.innerHeight;


            const left =
                Math.max(
                    rect.left,
                    0
                );

            const top =
                Math.max(
                    rect.top,
                    0
                );

            const right =
                Math.min(
                    rect.right,
                    viewportWidth
                );

            const bottom =
                Math.min(
                    rect.bottom,
                    viewportHeight
                );


            if (
                right <= left ||
                bottom <= top
            ) {
                return false;
            }


            const width =
                right - left;

            const height =
                bottom - top;


            const points = [

                [
                    left + width * 0.50,
                    top + height * 0.50
                ],

                [
                    left + width * 0.25,
                    top + height * 0.25
                ],

                [
                    left + width * 0.75,
                    top + height * 0.25
                ],

                [
                    left + width * 0.25,
                    top + height * 0.75
                ],

                [
                    left + width * 0.75,
                    top + height * 0.75
                ],
            ];


            let visiblePoints = 0;


            for (
                const [x, y]
                of points
            ) {

                const topElement =
                    document.elementFromPoint(
                        x,
                        y
                    );


                if (
                    topElement === el ||
                    el.contains(
                        topElement
                    )
                ) {

                    visiblePoints += 1;
                }
            }


            return (
                visiblePoints >=
                minVisiblePoints
            );
        }
        """,
        min_visible_points,
    )


# ==========================================================
# Wait for Assets
# ==========================================================

async def wait_for_assets(
    page,
):

    await page.evaluate(
        """
        async () => {

            if (
                document.fonts &&
                document.fonts.ready
            ) {
                await document.fonts.ready;
            }


            const images =
                Array.from(
                    document.images
                );


            await Promise.all(

                images.map(

                    image => {

                        if (image.complete) {
                            return Promise.resolve();
                        }


                        return new Promise(
                            resolve => {

                                image.addEventListener(
                                    "load",
                                    resolve,
                                    {
                                        once: true
                                    }
                                );

                                image.addEventListener(
                                    "error",
                                    resolve,
                                    {
                                        once: true
                                    }
                                );
                            }
                        );
                    }
                )
            );
        }
        """
    )


    await page.wait_for_timeout(
        250
    )


# ==========================================================
# Clamp Bounding Box
# ==========================================================

def clamp_bbox(
    bbox,
    viewport_width,
    viewport_height,
):

    x1 = max(
        0.0,
        bbox["x"]
    )

    y1 = max(
        0.0,
        bbox["y"]
    )


    x2 = min(
        float(viewport_width),
        bbox["x"] + bbox["width"],
    )

    y2 = min(
        float(viewport_height),
        bbox["y"] + bbox["height"],
    )


    width = x2 - x1
    height = y2 - y1


    if (
        width <= 0
        or height <= 0
    ):
        return None


    return {
        "x": x1,
        "y": y1,
        "width": width,
        "height": height,
    }


# ==========================================================
# Extract ALL Annotations
#
# Important:
# This does NOT know anything about profiles.
# We extract everything only once.
# ==========================================================

async def extract_annotations(
    page,
    viewport_width,
    viewport_height,
    dpr,
):

    annotations = []


    elements = page.locator(
        "[data-class]"
    )


    count = (
        await elements.count()
    )


    for index in range(
        count
    ):

        element = elements.nth(
            index
        )


        class_name = (
            await element.get_attribute(
                "data-class"
            )
        )


        # --------------------------------------------------
        # Ignore unknown / unsupported annotation classes
        # --------------------------------------------------

        if (
            not class_name
            or class_name
            not in ANNOTATION_CLASSES
        ):
            continue


        # --------------------------------------------------
        # Visibility
        # --------------------------------------------------

        if not await is_actually_visible(
            element
        ):
            continue


        # --------------------------------------------------
        # DOM bbox
        # --------------------------------------------------

        bbox = (
            await element.bounding_box()
        )


        if not bbox:
            continue


        bbox_css = clamp_bbox(
            bbox,
            viewport_width,
            viewport_height,
        )


        if not bbox_css:
            continue


        # --------------------------------------------------
        # Global class ID
        #
        # Used only for global JSON identity.
        # YOLO will later use profile_class_id.
        # --------------------------------------------------

        global_class_id = (
            GLOBAL_CLASS_TO_ID.get(
                class_name
            )
        )


        if global_class_id is None:
            continue


        # --------------------------------------------------
        # Semantic metadata
        # --------------------------------------------------

        semantic = (
            await element.get_attribute(
                "data-semantic"
            )
        )


        if semantic:
            semantic = semantic.strip()


        # --------------------------------------------------
        # Convert CSS bbox to actual screenshot coordinates
        # --------------------------------------------------

        bbox_image = {

            "x":
                bbox_css["x"]
                * dpr,

            "y":
                bbox_css["y"]
                * dpr,

            "width":
                bbox_css["width"]
                * dpr,

            "height":
                bbox_css["height"]
                * dpr,
        }


        # --------------------------------------------------
        # Base annotation
        # --------------------------------------------------

        annotation = {

            "class":
                class_name,

            "global_class_id":
                global_class_id,

            "semantic":
                semantic,

            "bbox_css":
                bbox_css,

            "bbox_image":
                bbox_image,
        }


        # ==================================================
        # Text
        # ==================================================

        if class_name in TEXT_CLASSES:

            text = (
                await element.inner_text()
            )


            if text:

                annotation["text"] = (
                    text.strip()
                )


        # ==================================================
        # Emoji Metadata
        # ==================================================

        emoji_source = (
            await element.get_attribute(
                "data-emoji-source"
            )
        )


        if emoji_source:

            annotation[
                "emoji_source"
            ] = emoji_source


        # ==================================================
        # Image Source
        # ==================================================

        tag_name = (
            await element.evaluate(
                "(el) => el.tagName"
            )
        )


        if (
            tag_name
            and tag_name.lower()
            == "img"
        ):

            src = (
                await element.get_attribute(
                    "src"
                )
            )


            if src:

                if src.startswith(
                    "data:"
                ):

                    annotation["src"] = (
                        "embedded_asset"
                    )

                else:

                    annotation["src"] = (
                        src
                    )


        annotations.append(
            annotation
        )


    return annotations


# ==========================================================
# Filter Annotation Profile
# ==========================================================

def filter_annotations_by_profile(
    annotations,
    profile_name,
):

    # ------------------------------------------------------
    # Which classes belong to this profile?
    # ------------------------------------------------------

    allowed_classes = (
        get_profile_classes(
            profile_name
        )
    )


    # ------------------------------------------------------
    # Profile-specific YOLO class mapping
    # ------------------------------------------------------

    profile_class_map = (
        PROFILE_CLASS_TO_ID.get(
            profile_name
        )
    )


    if profile_class_map is None:

        raise ValueError(
            f"No PROFILE_CLASS_TO_ID "
            f"mapping found for "
            f"profile: {profile_name}"
        )


    filtered_annotations = []


    for annotation in annotations:

        class_name = (
            annotation["class"]
        )


        # Not part of this profile
        if (
            class_name
            not in allowed_classes
        ):
            continue


        # Should normally never happen,
        # but protects against class/profile mismatch.
        if (
            class_name
            not in profile_class_map
        ):
            continue


        profile_annotation = (
            annotation.copy()
        )


        profile_annotation[
            "profile"
        ] = profile_name


        profile_annotation[
            "profile_class_id"
        ] = (
            profile_class_map[
                class_name
            ]
        )


        filtered_annotations.append(
            profile_annotation
        )


    return filtered_annotations


# ==========================================================
# YOLO
#
# IMPORTANT:
# Uses profile_class_id, NOT global_class_id.
# ==========================================================

def save_yolo_labels(
    annotations,
    image_width,
    image_height,
    output_path,
):

    lines = []


    for annotation in annotations:

        bbox = (
            annotation[
                "bbox_image"
            ]
        )


        profile_class_id = (
            annotation.get(
                "profile_class_id"
            )
        )


        if profile_class_id is None:
            continue


        center_x = (
            bbox["x"]
            + bbox["width"] / 2
        )

        center_y = (
            bbox["y"]
            + bbox["height"] / 2
        )


        normalized_x = (
            center_x
            / image_width
        )

        normalized_y = (
            center_y
            / image_height
        )

        normalized_width = (
            bbox["width"]
            / image_width
        )

        normalized_height = (
            bbox["height"]
            / image_height
        )


        lines.append(

            f"{profile_class_id} "
            f"{normalized_x:.6f} "
            f"{normalized_y:.6f} "
            f"{normalized_width:.6f} "
            f"{normalized_height:.6f}"
        )


    output_path.write_text(
        "\n".join(
            lines
        ),
        encoding="utf-8",
    )


# ==========================================================
# Visualization
# ==========================================================

def draw_visualization(
    screenshot_path,
    annotations,
    output_path,
    dpr,
):

    image = Image.open(
        screenshot_path
    ).convert(
        "RGB"
    )


    draw = ImageDraw.Draw(
        image
    )


    for annotation in annotations:

        bbox = (
            annotation[
                "bbox_image"
            ]
        )


        x1 = bbox["x"]
        y1 = bbox["y"]


        x2 = (
            x1
            + bbox["width"]
        )

        y2 = (
            y1
            + bbox["height"]
        )


        draw.rectangle(

            [
                x1,
                y1,
                x2,
                y2,
            ],

            outline="red",

            width=max(
                1,
                round(
                    2 * dpr
                )
            ),
        )


        profile_class_id = (
            annotation.get(
                "profile_class_id",
                "?"
            )
        )


        label = (

            f"{profile_class_id} | "
            f"{annotation['class']} | "
            f"{annotation.get('semantic', '')}"
        )


        draw.text(

            (
                x1 + 2,
                max(
                    0,
                    y1 - 14 * dpr
                ),
            ),

            label,

            fill="red",
        )


    image.save(
        output_path
    )


# ==========================================================
# Render Single Page
# ==========================================================

async def render_page(
    browser,
    sample_index,
    page_type,
    template_name,
    context_key,
    page_data,
    system,
    theme,
    viewport,
    output_subdir=None,
    annotation_profiles=None,
):

    # ======================================================
    # Profiles
    # ======================================================

    annotation_profiles = (
        annotation_profiles
        or DEFAULT_ANNOTATION_PROFILES
    )


    width = viewport["width"]
    height = viewport["height"]


    dpr = viewport.get(
        "dpr",
        1
    )


    viewport_name = (
        viewport["name"]
    )


    viewport_category = (
        viewport.get(
            "category",
            "unknown"
        )
    )


    # ======================================================
    # Output Folder
    # ======================================================

    output_subdir = (
        output_subdir
        or page_type
    )


    output_dir = (
        OUTPUT_ROOT
        / output_subdir
    )


    # ------------------------------------------------------
    # Screenshot directory
    #
    # Screenshot is shared by all profiles.
    # ------------------------------------------------------

    image_dir = (
        output_dir
        / "images"
    )


    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )


    # ------------------------------------------------------
    # Profile directories
    # ------------------------------------------------------

    profile_directories = {}


    for profile_name in (
        annotation_profiles
    ):

        profile_root = (
            output_dir
            / profile_name
        )


        label_dir = (
            profile_root
            / "labels"
        )


        json_dir = (
            profile_root
            / "json"
        )


        visualization_dir = (
            profile_root
            / "visualization"
        )


        for directory in [

            label_dir,
            json_dir,
            visualization_dir,

        ]:

            directory.mkdir(
                parents=True,
                exist_ok=True,
            )


        profile_directories[
            profile_name
        ] = {

            "labels":
                label_dir,

            "json":
                json_dir,

            "visualization":
                visualization_dir,
        }


    # ======================================================
    # Template
    # ======================================================

    template = (
        environment.get_template(
            template_name
        )
    )


    context = {

        context_key:
            page_data,

        "system":
            system,

        "theme":
            theme,
    }


    html = template.render(
        **context
    )


    # ======================================================
    # Playwright Page
    # ======================================================

    page = await browser.new_page(

        viewport={

            "width":
                width,

            "height":
                height,
        },

        device_scale_factor=
            dpr,
    )


    try:

        await page.set_content(
            html,
            wait_until=
                "networkidle",
        )


        await wait_for_assets(
            page
        )


        # ==================================================
        # Naming
        # ==================================================

        base_name = (

            f"{page_type}_"
            f"{sample_index:06d}_"
            f"{viewport_name}"
        )


        screenshot_path = (
            image_dir
            / f"{base_name}.png"
        )


        # ==================================================
        # Screenshot
        # ==================================================

        await page.screenshot(

            path=str(
                screenshot_path
            ),

            full_page=False,
        )


        # ==================================================
        # Actual Screenshot Dimensions
        # ==================================================

        with Image.open(
            screenshot_path
        ) as screenshot:

            image_width = (
                screenshot.width
            )

            image_height = (
                screenshot.height
            )


        # ==================================================
        # Extract FULL Annotation Set ONCE
        # ==================================================

        all_annotations = (
            await extract_annotations(

                page=
                    page,

                viewport_width=
                    width,

                viewport_height=
                    height,

                dpr=
                    dpr,
            )
        )


        # ==================================================
        # Save Every Profile
        # ==================================================

        profile_results = {}


        for profile_name in (
            annotation_profiles
        ):

            # ----------------------------------------------
            # Filter
            # ----------------------------------------------

            annotations = (
                filter_annotations_by_profile(
                    all_annotations,
                    profile_name,
                )
            )


            directories = (
                profile_directories[
                    profile_name
                ]
            )


            label_path = (
                directories[
                    "labels"
                ]
                / f"{base_name}.txt"
            )


            json_path = (
                directories[
                    "json"
                ]
                / f"{base_name}.json"
            )


            visualization_path = (
                directories[
                    "visualization"
                ]
                / f"{base_name}.png"
            )


            # ==============================================
            # Metadata
            # ==============================================

            metadata = {

                "page_type":
                    page_type,

                "sample_index":
                    sample_index,

                "template":
                    template_name,

                # ------------------------------------------
                # Profile
                # ------------------------------------------

                "annotation_profile":
                    profile_name,

                "profile_class_map":
                    PROFILE_CLASS_TO_ID[
                        profile_name
                    ],

                # ------------------------------------------
                # Viewport
                # ------------------------------------------

                "viewport": {

                    "name":
                        viewport_name,

                    "category":
                        viewport_category,

                    "width_css":
                        width,

                    "height_css":
                        height,

                    "dpr":
                        dpr,

                    "image_width":
                        image_width,

                    "image_height":
                        image_height,
                },

                # ------------------------------------------
                # Theme
                # ------------------------------------------

                "theme": {

                    "mode":
                        getattr(
                            theme,
                            "mode",
                            None
                        ),
                },

                # ------------------------------------------
                # Annotation
                # ------------------------------------------

                "annotation_count":
                    len(
                        annotations
                    ),

                "annotations":
                    annotations,
            }


            # ==============================================
            # JSON
            # ==============================================

            json_path.write_text(

                json.dumps(
                    metadata,
                    indent=2,
                    ensure_ascii=False,
                ),

                encoding="utf-8",
            )


            # ==============================================
            # YOLO
            # ==============================================

            save_yolo_labels(

                annotations,
                image_width,
                image_height,
                label_path,
            )


            # ==============================================
            # Visualization
            # ==============================================

            draw_visualization(

                screenshot_path,
                annotations,
                visualization_path,
                dpr,
            )


            # ==============================================
            # Store profile result
            # ==============================================

            profile_results[
                profile_name
            ] = {

                "annotation_count":
                    len(
                        annotations
                    ),

                "labels":
                    label_path,

                "json":
                    json_path,

                "visualization":
                    visualization_path,
            }


            print(

                f"[OK] "
                f"{page_type} | "
                f"{viewport_name} | "
                f"{profile_name} | "
                f"{len(annotations)} annotations"
            )


        # ==================================================
        # Return
        # ==================================================

        return {

            "image":
                screenshot_path,

            "all_annotation_count":
                len(
                    all_annotations
                ),

            "profiles":
                profile_results,
        }


    finally:

        await page.close()