# social_media/youtube/renderers/common_renderer.py

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


# ==========================================================
# Annotation Classes / Profiles
# ==========================================================

from social_media.common.classes import (
    ANNOTATION_CLASSES,
    ANNOTATION_PROFILES,

    TEXT_CLASSES,

    GLOBAL_CLASS_TO_ID,

    get_profile_classes,
    get_profile_class_id,
    get_profile_names,
)


# ==========================================================
# Viewports
# ==========================================================

from social_media.common.viewport import (
    get_all_viewports,
    get_random_viewport,

    get_viewports_by_category,
    get_viewports_by_names,

    get_viewports_by_size_class,
    get_viewports_by_orientation,
)


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
# Default Scroll Positions
# ==========================================================

DEFAULT_SCROLL_PERCENTAGES = [
    0,
    25,
    50,
    75,
    100,
]


# ==========================================================
# Viewport Resolver
# ==========================================================

def resolve_viewports(
    mode="selected",
    selected=None,
    category=None,
    size_class=None,
    orientation=None,
):

    """
    Resolve viewport configurations.

    Supported modes:

        all
        selected
        random
        category
        size_class
        orientation

    Category shorthand is also supported:

        mobile
        mobile_landscape
        tablet
        foldable
        laptop
        desktop
        ultrawide
    """

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
    # Selected Names
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


    # ======================================================
    # Category
    # ======================================================

    if mode == "category":

        if not category:

            raise ValueError(
                "category must be provided "
                "when mode='category'."
            )

        return get_viewports_by_category(
            category
        )


    # ======================================================
    # Size Class
    # ======================================================

    if mode == "size_class":

        if not size_class:

            raise ValueError(
                "size_class must be provided "
                "when mode='size_class'."
            )

        return get_viewports_by_size_class(
            size_class
        )


    # ======================================================
    # Orientation
    # ======================================================

    if mode == "orientation":

        if not orientation:

            raise ValueError(
                "orientation must be provided "
                "when mode='orientation'."
            )

        return get_viewports_by_orientation(
            orientation
        )


    # ======================================================
    # Category Shorthand
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


    raise ValueError(
        f"Unknown viewport mode: {mode}"
    )


# ==========================================================
# Annotation Profile Resolver
# ==========================================================

def resolve_annotation_profiles(
    profiles=None,
):

    """
    Validate and return annotation profile names.
    """

    if profiles is None:

        profiles = (
            DEFAULT_ANNOTATION_PROFILES.copy()
        )


    # Remove duplicates while preserving order.

    profiles = list(
        dict.fromkeys(
            profiles
        )
    )


    unknown_profiles = [

        profile_name

        for profile_name
        in profiles

        if profile_name
        not in ANNOTATION_PROFILES
    ]


    if unknown_profiles:

        raise ValueError(
            "Unknown annotation profiles: "
            f"{unknown_profiles}. "
            "Available profiles: "
            f"{sorted(ANNOTATION_PROFILES.keys())}"
        )


    return profiles


# ==========================================================
# Jinja Environment
# ==========================================================

def create_environment(
    template_dir: Path,
) -> Environment:

    return Environment(

        loader=FileSystemLoader(
            str(template_dir)
        ),

        autoescape=select_autoescape(
            [
                "html",
                "xml",
            ]
        ),
    )


# ==========================================================
# Output Directory Helper
# ==========================================================

def make_directories(
    *directories: Path,
):

    for directory in directories:

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )


# ==========================================================
# Profile Directory Helper
# ==========================================================

def create_profile_directories(
    annotation_root: Path,
    annotation_profiles,
):

    """
    Create:

    annotations/
        big_components/
            labels/
            json/
            visualization/

        components/
            ...

        small_elements/
            ...

        icons_only/
            ...
    """

    result = {}


    for profile_name in annotation_profiles:

        profile_root = (
            annotation_root
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


        make_directories(

            label_dir,

            json_dir,

            visualization_dir,
        )


        result[
            profile_name
        ] = {

            "root":
                profile_root,

            "labels":
                label_dir,

            "json":
                json_dir,

            "visualization":
                visualization_dir,
        }


    return result


# ==========================================================
# Visibility - Current Viewport
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
# Visibility - Full Document
# ==========================================================

async def is_document_element_visible(
    element,
):

    return await element.evaluate(
        """
        (el) => {

            let current = el;

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
                    return false;
                }


                const opacity =
                    parseFloat(
                        style.opacity || "1"
                    );


                if (opacity <= 0.01) {
                    return false;
                }


                current =
                    current.parentElement;
            }


            const rect =
                el.getBoundingClientRect();


            return (
                rect.width > 0 &&
                rect.height > 0
            );
        }
        """
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


            const videos =
                Array.from(
                    document.querySelectorAll(
                        "video"
                    )
                );


            await Promise.all(

                videos.map(

                    video => {

                        if (
                            video.readyState >= 1
                        ) {
                            return Promise.resolve();
                        }


                        return new Promise(
                            resolve => {

                                video.addEventListener(
                                    "loadedmetadata",
                                    resolve,
                                    {
                                        once: true
                                    }
                                );

                                video.addEventListener(
                                    "error",
                                    resolve,
                                    {
                                        once: true
                                    }
                                );


                                setTimeout(
                                    resolve,
                                    1000
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
# Clamp Viewport Bounding Box
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

        float(
            viewport_width
        ),

        bbox["x"]
        + bbox["width"],
    )


    y2 = min(

        float(
            viewport_height
        ),

        bbox["y"]
        + bbox["height"],
    )


    width = (
        x2 - x1
    )

    height = (
        y2 - y1
    )


    if (
        width <= 0
        or height <= 0
    ):

        return None


    return {

        "x":
            x1,

        "y":
            y1,

        "width":
            width,

        "height":
            height,
    }


# ==========================================================
# Clamp Full-Document Bounding Box
# ==========================================================

def clamp_document_bbox(
    bbox,
    document_width,
    document_height,
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

        float(
            document_width
        ),

        bbox["x"]
        + bbox["width"],
    )


    y2 = min(

        float(
            document_height
        ),

        bbox["y"]
        + bbox["height"],
    )


    width = (
        x2 - x1
    )

    height = (
        y2 - y1
    )


    if (
        width <= 0
        or height <= 0
    ):

        return None


    return {

        "x":
            x1,

        "y":
            y1,

        "width":
            width,

        "height":
            height,
    }


# ==========================================================
# Asset Metadata Helper
# ==========================================================

def normalize_asset_source(
    src,
):

    if not src:

        return None


    if src.startswith(
        "data:"
    ):

        return "embedded_asset"


    if src.startswith(
        "blob:"
    ):

        return "blob_asset"


    return src


# ==========================================================
# Annotation Metadata Helper
# ==========================================================

async def add_annotation_metadata(
    element,
    annotation,
    class_name,
):

    # ======================================================
    # Text
    # ======================================================

    if class_name in TEXT_CLASSES:

        text = (
            await element.inner_text()
        )


        if text:

            text = (
                text.strip()
            )


            if text:

                annotation[
                    "text"
                ] = text


    # ======================================================
    # Tag
    # ======================================================

    tag_name = (
        await element.evaluate(
            "(el) => el.tagName"
        )
    )


    if tag_name:

        tag_name = (
            tag_name.lower()
        )


    # ======================================================
    # Image
    # ======================================================

    if tag_name == "img":

        src = (
            await element.get_attribute(
                "src"
            )
        )


        normalized_src = (
            normalize_asset_source(
                src
            )
        )


        if normalized_src:

            annotation[
                "src"
            ] = normalized_src


    # ======================================================
    # Video
    # ======================================================

    elif tag_name == "video":

        src = (
            await element.get_attribute(
                "src"
            )
        )


        poster = (
            await element.get_attribute(
                "poster"
            )
        )


        normalized_src = (
            normalize_asset_source(
                src
            )
        )


        normalized_poster = (
            normalize_asset_source(
                poster
            )
        )


        if normalized_src:

            annotation[
                "src"
            ] = normalized_src


        if normalized_poster:

            annotation[
                "poster"
            ] = normalized_poster


    return annotation


# ==========================================================
# Extract Viewport Annotations
# ==========================================================

async def extract_annotations(
    page,
    viewport_width,
    viewport_height,
    dpr,
):

    """
    Extract ALL supported annotations visible in the current
    viewport.

    IMPORTANT:

    This extraction is profile-independent.

    Profile filtering happens AFTER extraction so that the
    browser DOM is only inspected once.
    """

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

        element = (
            elements.nth(
                index
            )
        )


        # ==================================================
        # Class
        # ==================================================

        class_name = (
            await element.get_attribute(
                "data-class"
            )
        )


        if class_name:

            class_name = (
                class_name.strip()
            )


        if (
            not class_name
            or class_name
            not in ANNOTATION_CLASSES
        ):

            continue


        # ==================================================
        # Visibility
        # ==================================================

        if not await is_actually_visible(
            element
        ):

            continue


        # ==================================================
        # Bounding Box
        # ==================================================

        bbox = (
            await element.bounding_box()
        )


        if not bbox:

            continue


        bbox_css = clamp_bbox(

            bbox=

                bbox,

            viewport_width=
                viewport_width,

            viewport_height=
                viewport_height,
        )


        if not bbox_css:

            continue


        # ==================================================
        # Global Class ID
        # ==================================================

        global_class_id = (
            GLOBAL_CLASS_TO_ID.get(
                class_name
            )
        )


        if global_class_id is None:

            continue


        # ==================================================
        # Semantic
        # ==================================================

        semantic = (
            await element.get_attribute(
                "data-semantic"
            )
        )


        if semantic:

            semantic = (
                semantic.strip()
            )


        # ==================================================
        # Image Coordinates
        # ==================================================

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


        # ==================================================
        # Global Annotation
        # ==================================================

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


        annotation = (
            await add_annotation_metadata(

                element=
                    element,

                annotation=
                    annotation,

                class_name=
                    class_name,
            )
        )


        annotations.append(
            annotation
        )


    return annotations


# ==========================================================
# Extract Full Page Annotations
# ==========================================================

async def extract_full_page_annotations(
    page,
    document_width,
    document_height,
    dpr,
):

    """
    Extract ALL supported annotations in the complete
    document.

    Coordinates are document coordinates.

    Like viewport extraction, this is profile-independent.
    """

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

        element = (
            elements.nth(
                index
            )
        )


        # ==================================================
        # Class
        # ==================================================

        class_name = (
            await element.get_attribute(
                "data-class"
            )
        )


        if class_name:

            class_name = (
                class_name.strip()
            )


        if (
            not class_name
            or class_name
            not in ANNOTATION_CLASSES
        ):

            continue


        # ==================================================
        # Basic Document Visibility
        # ==================================================

        if not await is_document_element_visible(
            element
        ):

            continue


        # ==================================================
        # Document Bounding Box
        # ==================================================

        bbox = (
            await element.evaluate(
                """
                (el) => {

                    const rect =
                        el.getBoundingClientRect();

                    return {

                        x:
                            rect.left
                            + window.scrollX,

                        y:
                            rect.top
                            + window.scrollY,

                        width:
                            rect.width,

                        height:
                            rect.height,
                    };
                }
                """
            )
        )


        bbox_css = (
            clamp_document_bbox(

                bbox=

                    bbox,

                document_width=
                    document_width,

                document_height=
                    document_height,
            )
        )


        if not bbox_css:

            continue


        # ==================================================
        # Global Class ID
        # ==================================================

        global_class_id = (
            GLOBAL_CLASS_TO_ID.get(
                class_name
            )
        )


        if global_class_id is None:

            continue


        # ==================================================
        # Semantic
        # ==================================================

        semantic = (
            await element.get_attribute(
                "data-semantic"
            )
        )


        if semantic:

            semantic = (
                semantic.strip()
            )


        # ==================================================
        # Image Coordinates
        # ==================================================

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


        # ==================================================
        # Global Annotation
        # ==================================================

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


        annotation = (
            await add_annotation_metadata(

                element=
                    element,

                annotation=
                    annotation,

                class_name=
                    class_name,
            )
        )


        annotations.append(
            annotation
        )


    return annotations


# ==========================================================
# Build Profile-Specific Annotations
# ==========================================================

def build_profile_annotations(
    annotations,
    profile_name,
):

    """
    Convert global annotations into one profile.

    Keeps:

        class
        global_class_id

    Adds:

        profile_class_id
        profile_class_name

    This is especially important for merged classes.

    Example:

        system_text
            global_class_id = 11

        small_elements
            profile_class_id = 7
            profile_class_name = timestamp
    """

    allowed_classes = (
        get_profile_classes(
            profile_name
        )
    )


    profile_names = (
        get_profile_names(
            profile_name
        )
    )


    result = []


    for annotation in annotations:

        class_name = (
            annotation[
                "class"
            ]
        )


        if class_name not in allowed_classes:

            continue


        profile_class_id = (
            get_profile_class_id(

                profile_name=
                    profile_name,

                class_name=
                    class_name,
            )
        )


        if profile_class_id is None:

            continue


        profile_class_name = (
            profile_names[
                profile_class_id
            ]
        )


        profile_annotation = {

            **annotation,

            "profile_class_id":
                profile_class_id,

            "profile_class_name":
                profile_class_name,
        }


        result.append(
            profile_annotation
        )


    return result


# ==========================================================
# YOLO
# ==========================================================

def save_yolo_labels(
    annotations,
    image_width,
    image_height,
    output_path,
):

    """
    Save profile-specific annotations.

    annotations MUST already contain:

        profile_class_id
    """

    lines = []


    if (
        image_width <= 0
        or image_height <= 0
    ):

        raise ValueError(
            "Image dimensions must be positive."
        )


    for annotation in annotations:

        profile_class_id = (
            annotation.get(
                "profile_class_id"
            )
        )


        if profile_class_id is None:

            continue


        bbox = (
            annotation[
                "bbox_image"
            ]
        )


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


        # ==================================================
        # Safety Clamp
        # ==================================================

        normalized_x = min(
            1.0,
            max(
                0.0,
                normalized_x
            ),
        )


        normalized_y = min(
            1.0,
            max(
                0.0,
                normalized_y
            ),
        )


        normalized_width = min(
            1.0,
            max(
                0.0,
                normalized_width
            ),
        )


        normalized_height = min(
            1.0,
            max(
                0.0,
                normalized_height
            ),
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

    image = (
        Image.open(
            screenshot_path
        )
        .convert(
            "RGB"
        )
    )


    draw = (
        ImageDraw.Draw(
            image
        )
    )


    for annotation in annotations:

        bbox = (
            annotation[
                "bbox_image"
            ]
        )


        x1 = (
            bbox["x"]
        )

        y1 = (
            bbox["y"]
        )


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


        semantic = (
            annotation.get(
                "semantic"
            )
        )


        profile_class_name = (
            annotation.get(
                "profile_class_name"
            )
        )


        original_class_name = (
            annotation.get(
                "class"
            )
        )


        # ==================================================
        # Label
        # ==================================================

        if (
            profile_class_name
            and
            profile_class_name
            != original_class_name
        ):

            base_label = (

                f"{original_class_name}"
                f"→"
                f"{profile_class_name}"
            )

        else:

            base_label = (
                original_class_name
            )


        if semantic:

            label = (

                f"{base_label}"
                f" | "
                f"{semantic}"
            )

        else:

            label = (
                base_label
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
# Theme Metadata
# ==========================================================

def build_theme_metadata(
    theme,
):

    return {

        "mode":
            theme.get(
                "mode"
            ),

        "seed":
            theme.get(
                "seed"
            ),

        "wcag_pass":
            theme.get(
                "wcag_pass"
            ),

        "wcag":
            theme.get(
                "wcag"
            ),
    }


# ==========================================================
# Document Metrics
# ==========================================================

async def get_document_metrics(
    page,
):

    return await page.evaluate(
        """
        () => {

            const body =
                document.body;

            const html =
                document.documentElement;


            const width = Math.max(

                body
                    ? body.scrollWidth
                    : 0,

                body
                    ? body.offsetWidth
                    : 0,

                html.scrollWidth,

                html.offsetWidth,

                html.clientWidth
            );


            const height = Math.max(

                body
                    ? body.scrollHeight
                    : 0,

                body
                    ? body.offsetHeight
                    : 0,

                html.scrollHeight,

                html.offsetHeight,

                html.clientHeight
            );


            return {

                width:
                    width,

                height:
                    height,

                viewport_width:
                    window.innerWidth,

                viewport_height:
                    window.innerHeight,

                max_scroll_y:
                    Math.max(
                        0,
                        height
                        - window.innerHeight
                    ),
            };
        }
        """
    )


# ==========================================================
# Save JSON
# ==========================================================

def save_json(
    path,
    data,
):

    path.write_text(

        json.dumps(

            data,

            indent=2,

            ensure_ascii=False,
        ),

        encoding="utf-8",
    )


# ==========================================================
# Build Profile Metadata
# ==========================================================

def build_profile_metadata(
    *,
    base_metadata,
    profile_name,
    annotations,
):

    """
    Add profile-specific class information to capture metadata.
    """

    class_names = (
        get_profile_names(
            profile_name
        )
    )


    return {

        **base_metadata,

        "annotation_profile":
            profile_name,

        "num_classes":
            len(
                class_names
            ),

        "class_names":
            class_names,

        "annotation_count":
            len(
                annotations
            ),

        "annotations":
            annotations,
    }


# ==========================================================
# Save Profile Outputs
# ==========================================================

def save_profile_outputs(
    *,
    annotations,
    profile_name,
    profile_directories,
    base_name,
    screenshot_path,
    image_width,
    image_height,
    dpr,
    base_metadata,
):

    """
    Save:

        YOLO
        JSON
        visualization

    for ONE annotation profile.

    The screenshot itself is shared across all profiles.
    """

    profile_annotations = (
        build_profile_annotations(

            annotations=
                annotations,

            profile_name=
                profile_name,
        )
    )


    profile_dirs = (
        profile_directories[
            profile_name
        ]
    )


    # ======================================================
    # Paths
    # ======================================================

    label_path = (

        profile_dirs[
            "labels"
        ]

        / f"{base_name}.txt"
    )


    json_path = (

        profile_dirs[
            "json"
        ]

        / f"{base_name}.json"
    )


    visualization_path = (

        profile_dirs[
            "visualization"
        ]

        / f"{base_name}.png"
    )


    # ======================================================
    # YOLO
    # ======================================================

    save_yolo_labels(

        annotations=
            profile_annotations,

        image_width=
            image_width,

        image_height=
            image_height,

        output_path=
            label_path,
    )


    # ======================================================
    # JSON
    # ======================================================

    metadata = (
        build_profile_metadata(

            base_metadata=
                base_metadata,

            profile_name=
                profile_name,

            annotations=
                profile_annotations,
        )
    )


    save_json(
        json_path,
        metadata,
    )


    # ======================================================
    # Visualization
    # ======================================================

    draw_visualization(

        screenshot_path=
            screenshot_path,

        annotations=
            profile_annotations,

        output_path=
            visualization_path,

        dpr=
            dpr,
    )


    return {

        "profile":
            profile_name,

        "annotation_count":
            len(
                profile_annotations
            ),

        "labels":
            label_path,

        "json":
            json_path,

        "visualization":
            visualization_path,
    }


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
    template_dir,
    output_root,
    output_subdir=None,

    scroll_percentages=None,

    save_full_page=True,
    save_viewports=True,

    annotation_profiles=None,
):

    # ======================================================
    # Annotation Profiles
    # ======================================================

    annotation_profiles = (
        resolve_annotation_profiles(
            annotation_profiles
        )
    )


    # ======================================================
    # Scroll Configuration
    # ======================================================

    if scroll_percentages is None:

        scroll_percentages = (
            DEFAULT_SCROLL_PERCENTAGES.copy()
        )


    scroll_percentages = [

        int(
            percentage
        )

        for percentage
        in scroll_percentages
    ]


    for percentage in scroll_percentages:

        if not (
            0 <= percentage <= 100
        ):

            raise ValueError(
                "Scroll percentage must be "
                "between 0 and 100. "
                f"Received: {percentage}"
            )


    # Remove duplicate requested percentages.

    scroll_percentages = list(
        dict.fromkeys(
            scroll_percentages
        )
    )


    # ======================================================
    # Viewport
    # ======================================================

    width = (
        viewport[
            "width"
        ]
    )


    height = (
        viewport[
            "height"
        ]
    )


    dpr = (
        viewport.get(
            "dpr",
            1
        )
    )


    viewport_name = (
        viewport[
            "name"
        ]
    )


    viewport_category = (
        viewport.get(
            "category",
            "unknown"
        )
    )


    viewport_orientation = (
        viewport.get(
            "orientation",
            (
                "landscape"
                if width > height
                else "portrait"
            )
        )
    )


    viewport_size_class = (
        viewport.get(
            "size_class",
            "unknown"
        )
    )


    # ======================================================
    # Paths
    # ======================================================

    template_dir = Path(
        template_dir
    )


    output_root = Path(
        output_root
    )


    output_subdir = (
        output_subdir
        or page_type
    )


    output_dir = (

        output_root
        / output_subdir
    )


    # ======================================================
    # Full Page
    # ======================================================

    full_page_root = (

        output_dir
        / "full_page"
    )


    full_image_dir = (

        full_page_root
        / "images"
    )


    full_annotation_root = (

        full_page_root
        / "annotations"
    )


    full_profile_directories = {}


    if save_full_page:

        make_directories(
            full_image_dir
        )


        full_profile_directories = (
            create_profile_directories(

                annotation_root=
                    full_annotation_root,

                annotation_profiles=
                    annotation_profiles,
            )
        )


    # ======================================================
    # Viewport
    # ======================================================

    viewport_root = (

        output_dir
        / "viewport"
    )


    viewport_image_dir = (

        viewport_root
        / "images"
    )


    viewport_annotation_root = (

        viewport_root
        / "annotations"
    )


    viewport_profile_directories = {}


    if save_viewports:

        make_directories(
            viewport_image_dir
        )


        viewport_profile_directories = (
            create_profile_directories(

                annotation_root=
                    viewport_annotation_root,

                annotation_profiles=
                    annotation_profiles,
            )
        )


    # ======================================================
    # Jinja
    # ======================================================

    environment = (
        create_environment(
            template_dir
        )
    )


    template = (
        environment.get_template(
            template_name
        )
    )


    # ======================================================
    # Theme
    # ======================================================

    if (
        "semantic"
        not in theme
    ):

        raise ValueError(
            "Theme must contain "
            "'semantic' colors."
        )


    semantic_theme = (
        theme[
            "semantic"
        ]
    )


    # ======================================================
    # Template Context
    # ======================================================

    context = {

        context_key:
            page_data,

        "system":
            system,

        "theme":
            semantic_theme,

        "theme_meta":
            theme,
    }


    html = (
        template.render(
            **context
        )
    )


    # ======================================================
    # Playwright Page
    # ======================================================

    page = (
        await browser.new_page(

            viewport={

                "width":
                    width,

                "height":
                    height,
            },

            device_scale_factor=
                dpr,
        )
    )


    # ======================================================
    # Results
    # ======================================================

    results = {

        "full_page":
            None,

        "viewports":
            [],
    }


    try:

        # ==================================================
        # Load
        # ==================================================

        await page.set_content(

            html,

            wait_until=
                "networkidle",
        )


        await wait_for_assets(
            page
        )


        # ==================================================
        # Reset Scroll
        # ==================================================

        await page.evaluate(
            """
            () => {
                window.scrollTo(
                    0,
                    0
                );
            }
            """
        )


        await page.wait_for_timeout(
            100
        )


        # ==================================================
        # Document Metrics
        # ==================================================

        document_metrics = (
            await get_document_metrics(
                page
            )
        )


        document_width = (
            document_metrics[
                "width"
            ]
        )


        document_height = (
            document_metrics[
                "height"
            ]
        )


        max_scroll_y = (
            document_metrics[
                "max_scroll_y"
            ]
        )


        # ==================================================
        # Shared Base Name
        # ==================================================

        shared_base_name = (

            f"{page_type}_"
            f"{sample_index:06d}_"
            f"{viewport_name}"
        )


        # ==================================================
        # Shared Viewport Metadata
        # ==================================================

        viewport_metadata = {

            "name":
                viewport_name,

            "category":
                viewport_category,

            "orientation":
                viewport_orientation,

            "size_class":
                viewport_size_class,

            "width_css":
                width,

            "height_css":
                height,

            "dpr":
                dpr,
        }


        # ==================================================
        # FULL PAGE CAPTURE
        # ==================================================

        if save_full_page:

            # ==============================================
            # Reset Scroll
            # ==============================================

            await page.evaluate(
                """
                () => {
                    window.scrollTo(
                        0,
                        0
                    );
                }
                """
            )


            await page.wait_for_timeout(
                100
            )


            # ==============================================
            # Name
            # ==============================================

            full_base_name = (
                f"{shared_base_name}_full"
            )


            full_screenshot_path = (

                full_image_dir

                / f"{full_base_name}.png"
            )


            # ==============================================
            # Screenshot ONCE
            # ==============================================

            await page.screenshot(

                path=str(
                    full_screenshot_path
                ),

                full_page=True,
            )


            # ==============================================
            # Actual Dimensions
            # ==============================================

            with Image.open(
                full_screenshot_path
            ) as screenshot:

                full_image_width = (
                    screenshot.width
                )

                full_image_height = (
                    screenshot.height
                )


            # ==============================================
            # Extract ALL Annotations ONCE
            # ==============================================

            full_annotations = (
                await extract_full_page_annotations(

                    page=
                        page,

                    document_width=
                        document_width,

                    document_height=
                        document_height,

                    dpr=
                        dpr,
                )
            )


            # ==============================================
            # Shared Metadata
            # ==============================================

            full_base_metadata = {

                "capture_type":
                    "full_page",

                "page_type":
                    page_type,

                "sample_index":
                    sample_index,

                "template":
                    template_name,


                "viewport":
                    viewport_metadata,


                "document": {

                    "width_css":
                        document_width,

                    "height_css":
                        document_height,

                    "image_width":
                        full_image_width,

                    "image_height":
                        full_image_height,
                },


                "theme":
                    build_theme_metadata(
                        theme
                    ),
            }


            # ==============================================
            # Save Every Annotation Profile
            # ==============================================

            profile_results = {}


            for profile_name in (
                annotation_profiles
            ):

                profile_result = (
                    save_profile_outputs(

                        annotations=
                            full_annotations,

                        profile_name=
                            profile_name,

                        profile_directories=
                            full_profile_directories,

                        base_name=
                            full_base_name,

                        screenshot_path=
                            full_screenshot_path,

                        image_width=
                            full_image_width,

                        image_height=
                            full_image_height,

                        dpr=
                            dpr,

                        base_metadata=
                            full_base_metadata,
                    )
                )


                profile_results[
                    profile_name
                ] = profile_result


            # ==============================================
            # Log
            # ==============================================

            profile_count_text = (
                " | ".join(

                    f"{profile_name}="
                    f"{profile_results[profile_name]['annotation_count']}"

                    for profile_name
                    in annotation_profiles
                )
            )


            print(

                f"[FULL] "
                f"{page_type} | "
                f"{viewport_name} | "
                f"{theme.get('mode')} | "
                f"global={len(full_annotations)} | "
                f"{profile_count_text} | "
                f"{full_image_width}x"
                f"{full_image_height}"
            )


            # ==============================================
            # Result
            # ==============================================

            results[
                "full_page"
            ] = {

                "image":
                    full_screenshot_path,

                "global_annotation_count":
                    len(
                        full_annotations
                    ),

                "profiles":
                    profile_results,
            }


        # ==================================================
        # VIEWPORT / SCROLL CAPTURES
        # ==================================================

        if save_viewports:

            seen_scroll_positions = set()


            for scroll_percent in (
                scroll_percentages
            ):

                # ==========================================
                # Requested Scroll
                # ==========================================

                requested_scroll_y = (

                    max_scroll_y
                    * scroll_percent
                    / 100.0
                )


                # ==========================================
                # Scroll
                # ==========================================

                await page.evaluate(

                    """
                    (scrollY) => {

                        window.scrollTo(
                            0,
                            scrollY
                        );
                    }
                    """,

                    requested_scroll_y,
                )


                await page.wait_for_timeout(
                    150
                )


                # ==========================================
                # Actual Scroll
                # ==========================================

                actual_scroll_y = (
                    await page.evaluate(
                        """
                        () => window.scrollY
                        """
                    )
                )


                actual_scroll_y = (
                    round(
                        actual_scroll_y
                    )
                )


                # ==========================================
                # Avoid Duplicate Captures
                # ==========================================

                if (
                    actual_scroll_y
                    in seen_scroll_positions
                ):

                    continue


                seen_scroll_positions.add(
                    actual_scroll_y
                )


                # ==========================================
                # Name
                # ==========================================

                viewport_base_name = (

                    f"{shared_base_name}_"
                    f"scroll_"
                    f"{scroll_percent:03d}"
                )


                screenshot_path = (

                    viewport_image_dir

                    / f"{viewport_base_name}.png"
                )


                # ==========================================
                # Screenshot ONCE
                # ==========================================

                await page.screenshot(

                    path=str(
                        screenshot_path
                    ),

                    full_page=False,
                )


                # ==========================================
                # Actual Screenshot Dimensions
                # ==========================================

                with Image.open(
                    screenshot_path
                ) as screenshot:

                    image_width = (
                        screenshot.width
                    )

                    image_height = (
                        screenshot.height
                    )


                # ==========================================
                # Extract ALL Viewport Annotations ONCE
                # ==========================================

                annotations = (
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


                # ==========================================
                # Shared Metadata
                # ==========================================

                viewport_base_metadata = {

                    "capture_type":
                        "viewport",

                    "page_type":
                        page_type,

                    "sample_index":
                        sample_index,

                    "template":
                        template_name,


                    "viewport": {

                        **viewport_metadata,

                        "image_width":
                            image_width,

                        "image_height":
                            image_height,
                    },


                    "document": {

                        "width_css":
                            document_width,

                        "height_css":
                            document_height,
                    },


                    "scroll": {

                        "requested_percent":
                            scroll_percent,

                        "requested_y_css":
                            requested_scroll_y,

                        "actual_y_css":
                            actual_scroll_y,

                        "max_scroll_y_css":
                            max_scroll_y,
                    },


                    "theme":
                        build_theme_metadata(
                            theme
                        ),
                }


                # ==========================================
                # Save Every Annotation Profile
                # ==========================================

                profile_results = {}


                for profile_name in (
                    annotation_profiles
                ):

                    profile_result = (
                        save_profile_outputs(

                            annotations=
                                annotations,

                            profile_name=
                                profile_name,

                            profile_directories=
                                viewport_profile_directories,

                            base_name=
                                viewport_base_name,

                            screenshot_path=
                                screenshot_path,

                            image_width=
                                image_width,

                            image_height=
                                image_height,

                            dpr=
                                dpr,

                            base_metadata=
                                viewport_base_metadata,
                        )
                    )


                    profile_results[
                        profile_name
                    ] = profile_result


                # ==========================================
                # Log
                # ==========================================

                profile_count_text = (
                    " | ".join(

                        f"{profile_name}="
                        f"{profile_results[profile_name]['annotation_count']}"

                        for profile_name
                        in annotation_profiles
                    )
                )


                print(

                    f"[VIEWPORT] "
                    f"{page_type} | "
                    f"{viewport_name} | "
                    f"scroll={scroll_percent}% | "
                    f"y={actual_scroll_y} | "
                    f"{theme.get('mode')} | "
                    f"global={len(annotations)} | "
                    f"{profile_count_text}"
                )


                # ==========================================
                # Results
                # ==========================================

                results[
                    "viewports"
                ].append(
                    {

                        "scroll_percent":
                            scroll_percent,

                        "scroll_y":
                            actual_scroll_y,

                        "image":
                            screenshot_path,

                        "global_annotation_count":
                            len(
                                annotations
                            ),

                        "profiles":
                            profile_results,
                    }
                )


        return results


    finally:

        await page.close()