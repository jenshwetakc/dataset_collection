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
    TEXT_CLASSES,
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
# Default Annotation Profiles
# ==========================================================

DEFAULT_ANNOTATION_PROFILES = [
    "big_components",
    "components",
    "small_elements",
    "icons_only",
]


# ==========================================================
# Visibility Configuration
# ==========================================================

DEFAULT_MIN_VISIBLE_RATIO = 0.20


# ==========================================================
# Jinja Environment
# ==========================================================

def create_template_environment(
    template_dir: Path,
) -> Environment:

    template_dir = Path(
        template_dir
    )

    if not template_dir.exists():

        raise FileNotFoundError(
            f"Template directory does not exist: "
            f"{template_dir}"
        )

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
# Viewport Resolver
# ==========================================================

def resolve_viewports(
    mode: str = "selected",
    selected: list[str] | None = None,
):

    selected = (
        selected
        or [
            "standard_iphone",
        ]
    )

    if mode == "all":

        return get_all_viewports()

    if mode == "test":

        return get_test_viewports()

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

    if mode in {
        "compact",
        "medium",
        "expanded",
    }:

        return get_viewports_by_size_class(
            mode
        )

    if mode in {
        "portrait",
        "landscape",
    }:

        return get_viewports_by_orientation(
            mode
        )

    if mode == "selected":

        return get_viewports_by_names(
            selected
        )

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
    min_visible_points: int = 2,
) -> bool:

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
    viewport_width: int,
    viewport_height: int,
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
        "x": x1,
        "y": y1,
        "width": width,
        "height": height,
    }


# ==========================================================
# Clipping Ancestors
# ==========================================================

async def get_clipping_ancestor_rects(
    element,
):
    """
    Return ancestor rectangles that clip the child element.

    Handles:
    - overflow: hidden
    - overflow: clip
    - overflow: scroll
    - overflow: auto
    """

    return await element.evaluate(
        """
        (el) => {

            const rects = [];

            let current =
                el.parentElement;


            while (current) {

                const style =
                    window.getComputedStyle(
                        current
                    );


                const overflowX =
                    style.overflowX;

                const overflowY =
                    style.overflowY;


                const clipsX = [
                    "hidden",
                    "clip",
                    "scroll",
                    "auto",
                ].includes(
                    overflowX
                );


                const clipsY = [
                    "hidden",
                    "clip",
                    "scroll",
                    "auto",
                ].includes(
                    overflowY
                );


                if (
                    clipsX
                    || clipsY
                ) {

                    const rect =
                        current.getBoundingClientRect();


                    rects.push({

                        x:
                            rect.left,

                        y:
                            rect.top,

                        width:
                            rect.width,

                        height:
                            rect.height,

                        clips_x:
                            clipsX,

                        clips_y:
                            clipsY,
                    });
                }


                current =
                    current.parentElement;
            }


            return rects;
        }
        """
    )


# ==========================================================
# Clip BBox to One Ancestor
# ==========================================================

def clip_bbox_to_ancestor(
    bbox,
    clip_rect,
):

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


    clip_x1 = (
        clip_rect["x"]
    )

    clip_y1 = (
        clip_rect["y"]
    )

    clip_x2 = (
        clip_x1
        + clip_rect["width"]
    )

    clip_y2 = (
        clip_y1
        + clip_rect["height"]
    )


    if clip_rect.get(
        "clips_x",
        False,
    ):

        x1 = max(
            x1,
            clip_x1,
        )

        x2 = min(
            x2,
            clip_x2,
        )


    if clip_rect.get(
        "clips_y",
        False,
    ):

        y1 = max(
            y1,
            clip_y1,
        )

        y2 = min(
            y2,
            clip_y2,
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
        "x": x1,
        "y": y1,
        "width": width,
        "height": height,
    }


# ==========================================================
# Clip BBox to All Ancestors
# ==========================================================

def clip_bbox_to_ancestors(
    bbox,
    clipping_ancestors,
):

    visible_bbox = dict(
        bbox
    )


    for clip_rect in (
        clipping_ancestors
    ):

        visible_bbox = (
            clip_bbox_to_ancestor(
                visible_bbox,
                clip_rect,
            )
        )


        if visible_bbox is None:

            return None


    return visible_bbox


# ==========================================================
# Collect Occluders
# ==========================================================

async def get_occluder_rects(
    page,
    viewport_width: int,
    viewport_height: int,
):

    occluders = []

    elements = page.locator(
        '[data-occluder="true"]'
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


        if not await is_actually_visible(
            element,
            min_visible_points=1,
        ):

            continue


        bbox = (
            await element.bounding_box()
        )


        if not bbox:

            continue


        bbox = clamp_bbox(
            bbox,
            viewport_width,
            viewport_height,
        )


        if not bbox:

            continue


        occluders.append(
            bbox
        )


    return occluders




# ==========================================================
# Get Effective Occluders for One Element
# ==========================================================

async def get_effective_occluder_rects(
    element,
    viewport_width: int,
    viewport_height: int,
):
    """
    Return overlay occluders that can actually cover the
    target element.

    Important rules:

    1. An occluder must NOT occlude itself.
    2. An occluder must NOT occlude its own descendants.
    3. Hidden occluders are ignored.
    4. Occluders outside the viewport are ignored.
    """

    rects = await element.evaluate(
        """
        (el) => {

            const result = [];

            const occluders =
                document.querySelectorAll(
                    '[data-occluder="true"]'
                );


            for (
                const occluder
                of occluders
            ) {

                // ==========================================
                // Do not let an overlay hide itself
                // ==========================================

                if (
                    occluder === el
                ) {
                    continue;
                }


                // ==========================================
                // CRITICAL:
                //
                // If the target element belongs to the
                // occluder, it must remain visible.
                //
                // Example:
                //
                // navigation_bar
                // ├── navigation_item
                // │   ├── icon
                // │   └── text
                //
                // The navigation bar must not hide those.
                // ==========================================

                if (
                    occluder.contains(el)
                ) {
                    continue;
                }


                const style =
                    window.getComputedStyle(
                        occluder
                    );


                // ==========================================
                // Style visibility
                // ==========================================

                if (
                    style.display === "none"
                    ||
                    style.visibility === "hidden"
                    ||
                    style.visibility === "collapse"
                ) {
                    continue;
                }


                const opacity =
                    parseFloat(
                        style.opacity || "1"
                    );


                if (
                    opacity <= 0.01
                ) {
                    continue;
                }


                // ==========================================
                // Geometry
                // ==========================================

                const rect =
                    occluder.getBoundingClientRect();


                if (
                    rect.width <= 0
                    ||
                    rect.height <= 0
                ) {
                    continue;
                }


                // ==========================================
                // Ignore completely off-screen occluders
                // ==========================================

                if (
                    rect.right <= 0
                    ||
                    rect.bottom <= 0
                    ||
                    rect.left >= window.innerWidth
                    ||
                    rect.top >= window.innerHeight
                ) {
                    continue;
                }


                result.push({

                    x:
                        rect.left,

                    y:
                        rect.top,

                    width:
                        rect.width,

                    height:
                        rect.height,
                });
            }


            return result;
        }
        """
    )


    clipped_rects = []


    for rect in rects:

        clipped = clamp_bbox(
            rect,
            viewport_width,
            viewport_height,
        )


        if clipped:

            clipped_rects.append(
                clipped
            )


    return clipped_rects

# ==========================================================
# Rectangle Intersection
# ==========================================================

def rects_overlap(
    bbox,
    occluder,
) -> bool:

    bx1 = bbox["x"]
    by1 = bbox["y"]

    bx2 = (
        bx1
        + bbox["width"]
    )

    by2 = (
        by1
        + bbox["height"]
    )


    ox1 = occluder["x"]
    oy1 = occluder["y"]

    ox2 = (
        ox1
        + occluder["width"]
    )

    oy2 = (
        oy1
        + occluder["height"]
    )


    return not (

        bx2 <= ox1
        or bx1 >= ox2
        or by2 <= oy1
        or by1 >= oy2
    )


# ==========================================================
# Clip One Bounding Box Against One Occluder
# ==========================================================

def clip_bbox_against_occluder(
    bbox,
    occluder,
):

    if not rects_overlap(
        bbox,
        occluder,
    ):

        return bbox


    bx1 = bbox["x"]
    by1 = bbox["y"]

    bx2 = (
        bx1
        + bbox["width"]
    )

    by2 = (
        by1
        + bbox["height"]
    )


    ox1 = occluder["x"]
    oy1 = occluder["y"]

    ox2 = (
        ox1
        + occluder["width"]
    )

    oy2 = (
        oy1
        + occluder["height"]
    )


    # ======================================================
    # Fully Covered
    # ======================================================

    if (
        ox1 <= bx1
        and oy1 <= by1
        and ox2 >= bx2
        and oy2 >= by2
    ):

        return None


    # ======================================================
    # Intersection
    # ======================================================

    ix1 = max(
        bx1,
        ox1
    )

    iy1 = max(
        by1,
        oy1
    )

    ix2 = min(
        bx2,
        ox2
    )

    iy2 = min(
        by2,
        oy2
    )


    intersection_width = (
        ix2 - ix1
    )

    intersection_height = (
        iy2 - iy1
    )


    if (
        intersection_width <= 0
        or intersection_height <= 0
    ):

        return bbox


    # ======================================================
    # Bottom Edge Covered
    # ======================================================

    if (
        iy2 >= by2
        and iy1 > by1
    ):

        new_height = (
            iy1 - by1
        )

        if new_height <= 0:

            return None


        return {
            "x": bx1,
            "y": by1,
            "width": bbox["width"],
            "height": new_height,
        }


    # ======================================================
    # Top Edge Covered
    # ======================================================

    if (
        iy1 <= by1
        and iy2 < by2
    ):

        new_y = (
            iy2
        )

        new_height = (
            by2 - new_y
        )


        if new_height <= 0:

            return None


        return {
            "x": bx1,
            "y": new_y,
            "width": bbox["width"],
            "height": new_height,
        }


    # ======================================================
    # Right Edge Covered
    # ======================================================

    if (
        ix2 >= bx2
        and ix1 > bx1
    ):

        new_width = (
            ix1 - bx1
        )


        if new_width <= 0:

            return None


        return {
            "x": bx1,
            "y": by1,
            "width": new_width,
            "height": bbox["height"],
        }


    # ======================================================
    # Left Edge Covered
    # ======================================================

    if (
        ix1 <= bx1
        and ix2 < bx2
    ):

        new_x = (
            ix2
        )

        new_width = (
            bx2 - new_x
        )


        if new_width <= 0:

            return None


        return {
            "x": new_x,
            "y": by1,
            "width": new_width,
            "height": bbox["height"],
        }


    # ======================================================
    # Complex/Internal Occlusion
    #
    # Cannot represent disconnected visible regions using
    # one YOLO rectangle, so retain bbox.
    # ======================================================

    return bbox


# ==========================================================
# Clip Against All Occluders
# ==========================================================

def clip_bbox_against_occluders(
    bbox,
    occluders,
):

    visible_bbox = dict(
        bbox
    )


    for occluder in occluders:

        visible_bbox = (
            clip_bbox_against_occluder(
                visible_bbox,
                occluder,
            )
        )


        if visible_bbox is None:

            return None


    return visible_bbox


# ==========================================================
# Extract All Annotations
# ==========================================================

# ==========================================================
# Extract All Annotations
# ==========================================================

async def extract_annotations(
    page,
    viewport_width: int,
    viewport_height: int,
    dpr: float,
    min_visible_ratio: float = DEFAULT_MIN_VISIBLE_RATIO,
):

    annotations = []


    # ======================================================
    # Get All Annotated Elements
    # ======================================================

    elements = page.locator(
        "[data-class]"
    )


    count = (
        await elements.count()
    )


    # ======================================================
    # Process Every Annotated Element
    # ======================================================

    for index in range(
        count
    ):

        element = elements.nth(
            index
        )


        # ==================================================
        # Class
        # ==================================================

        class_name = (
            await element.get_attribute(
                "data-class"
            )
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
        # DOM Bounding Box
        # ==================================================

        bbox = (
            await element.bounding_box()
        )


        if not bbox:

            continue


        # ==================================================
        # Clamp Bounding Box to Viewport
        # ==================================================

        bbox_css = clamp_bbox(
            bbox,
            viewport_width,
            viewport_height,
        )


        if not bbox_css:

            continue


        # ==================================================
        # Baseline BBox
        #
        # This is the viewport-visible bbox BEFORE:
        #
        # - ancestor clipping
        # - overlay clipping
        #
        # We use it to calculate visible_ratio.
        # ==================================================

        original_bbox_css = dict(
            bbox_css
        )


        # ==================================================
        # Clip Against Ancestor Containers
        #
        # Example:
        #
        # card
        # └── rotated image extending outside card
        #
        # If card has overflow:hidden, clip image to card.
        # ==================================================

        clipping_ancestors = (
            await get_clipping_ancestor_rects(
                element
            )
        )


        ancestor_clipped = False


        if clipping_ancestors:

            clipped_bbox = (
                clip_bbox_to_ancestors(
                    bbox_css,
                    clipping_ancestors,
                )
            )


            if not clipped_bbox:

                continue


            ancestor_clipped = (
                clipped_bbox
                != bbox_css
            )


            bbox_css = (
                clipped_bbox
            )


        # ==================================================
        # Is Target Itself an Occluder?
        # ==================================================

        is_occluder = (
            await element.get_attribute(
                "data-occluder"
            )
            == "true"
        )


        # ==================================================
        # Overlay Clipping
        # ==================================================

        overlay_clipped = False


        # An overlay itself does not need to be clipped by
        # other overlay logic here.
        if not is_occluder:

            # ==============================================
            # IMPORTANT:
            #
            # Calculate occluders specifically for this
            # element.
            #
            # Parent overlays are excluded automatically.
            # ==============================================

            effective_occluders = (
                await get_effective_occluder_rects(
                    element,
                    viewport_width,
                    viewport_height,
                )
            )


            if effective_occluders:

                before_overlay_bbox = dict(
                    bbox_css
                )


                bbox_css = (
                    clip_bbox_against_occluders(
                        bbox_css,
                        effective_occluders,
                    )
                )


                if not bbox_css:

                    continue


                overlay_clipped = (
                    bbox_css
                    != before_overlay_bbox
                )


        # ==================================================
        # Visible Ratio
        # ==================================================

        original_area = (
            original_bbox_css["width"]
            *
            original_bbox_css["height"]
        )


        visible_area = (
            bbox_css["width"]
            *
            bbox_css["height"]
        )


        if original_area <= 0:

            continue


        visible_ratio = (
            visible_area
            /
            original_area
        )


        # Numerical protection
        visible_ratio = min(
            1.0,
            max(
                0.0,
                visible_ratio,
            ),
        )


        if (
            visible_ratio
            < min_visible_ratio
        ):

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
        # Semantic Metadata
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
        # Screenshot Coordinates
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
        # Base Annotation
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

            "visible_ratio":
                round(
                    visible_ratio,
                    4
                ),

            "is_occluder":
                is_occluder,

            "ancestor_clipped":
                ancestor_clipped,

            "overlay_clipped":
                overlay_clipped,
        }


        # ==================================================
        # Text Metadata
        # ==================================================

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
        # Image Metadata
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

                    annotation[
                        "src"
                    ] = (
                        "embedded_asset"
                    )

                else:

                    annotation[
                        "src"
                    ] = src


        # ==================================================
        # Save Annotation
        # ==================================================

        annotations.append(
            annotation
        )


    return annotations

# ==========================================================
# Filter Annotation Profile
# ==========================================================

def filter_annotations_by_profile(
    annotations,
    profile_name: str,
):

    allowed_classes = (
        get_profile_classes(
            profile_name
        )
    )


    profile_class_map = (
        PROFILE_CLASS_TO_ID.get(
            profile_name
        )
    )


    if profile_class_map is None:

        raise ValueError(
            f"No PROFILE_CLASS_TO_ID "
            f"mapping found for profile: "
            f"{profile_name}"
        )


    filtered_annotations = []


    for annotation in annotations:

        class_name = (
            annotation[
                "class"
            ]
        )


        if (
            class_name
            not in allowed_classes
        ):

            continue


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
# Save YOLO Labels
# ==========================================================

def save_yolo_labels(
    annotations,
    image_width: int,
    image_height: int,
    output_path: Path,
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
    screenshot_path: Path,
    annotations,
    output_path: Path,
    dpr: float,
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


        semantic = (
            annotation.get(
                "semantic"
            )
            or ""
        )


        visible_ratio = (
            annotation.get(
                "visible_ratio",
                1.0
            )
        )


        label = (

            f"{profile_class_id} | "
            f"{annotation['class']} | "
            f"{semantic} | "
            f"{visible_ratio:.2f}"
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
# Theme Metadata Helper
# ==========================================================

def get_theme_metadata(
    theme,
) -> dict:

    if isinstance(
        theme,
        dict
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
        }


    return {

        "mode":
            getattr(
                theme,
                "mode",
                None
            ),

        "seed":
            getattr(
                theme,
                "seed",
                None
            ),

        "wcag_pass":
            getattr(
                theme,
                "wcag_pass",
                None
            ),
    }


# ==========================================================
# Render Single Page
# ==========================================================

async def render_page(
    browser,
    sample_index: int,
    page_type: str,
    template_name: str,
    context_key: str,
    page_data: dict,
    system: dict,
    theme: dict,
    viewport: dict,
    template_dir: Path,
    output_root: Path,
    output_subdir: str | None = None,
    annotation_profiles: list[str] | None = None,
    min_visible_ratio: float = DEFAULT_MIN_VISIBLE_RATIO,
):

    template_dir = Path(
        template_dir
    )

    output_root = Path(
        output_root
    )


    annotation_profiles = (
        annotation_profiles
        or DEFAULT_ANNOTATION_PROFILES
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
            1,
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
            "orientation"
        )
    )


    viewport_size_class = (
        viewport.get(
            "size_class"
        )
    )


    # ======================================================
    # Theme Mode
    # ======================================================

    if isinstance(
        theme,
        dict
    ):

        theme_mode = (
            theme.get(
                "mode",
                "unknown",
            )
        )

    else:

        theme_mode = (
            getattr(
                theme,
                "mode",
                "unknown",
            )
        )


    # ======================================================
    # Output Paths
    # ======================================================

    output_subdir = (
        output_subdir
        or page_type
    )


    output_dir = (
        output_root
        / output_subdir
    )


    image_dir = (
        output_dir
        / "images"
    )


    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )


    # ======================================================
    # Profile Directories
    # ======================================================

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

    environment = (
        create_template_environment(
            template_dir
        )
    )


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

        "viewport":
            viewport,
    }


    html = template.render(
        **context
    )


    # ======================================================
    # Browser
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

        # ==================================================
        # Load
        # ==================================================

        await page.set_content(
            html,
            wait_until="networkidle",
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
            f"{theme_mode}_"
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
        # Actual Image Dimensions
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
        # Extract Once
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

                min_visible_ratio=
                    min_visible_ratio,
            )
        )


        # ==================================================
        # Profile Outputs
        # ==================================================

        profile_results = {}


        for profile_name in (
            annotation_profiles
        ):

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

                "annotation_profile":
                    profile_name,

                "profile_class_map":
                    PROFILE_CLASS_TO_ID[
                        profile_name
                    ],

                "viewport": {

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

                    "image_width":
                        image_width,

                    "image_height":
                        image_height,
                },

                "theme":
                    get_theme_metadata(
                        theme
                    ),

                "visibility": {

                    "min_visible_ratio":
                        min_visible_ratio,

                    "viewport_clipping":
                        True,

                    "ancestor_clipping":
                        True,

                    "occlusion_clipping":
                        True,
                },

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
            # Result
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
                f"{theme_mode} | "
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

            "theme_mode":
                theme_mode,

            "all_annotation_count":
                len(
                    all_annotations
                ),

            "profiles":
                profile_results,
        }


    finally:

        await page.close()