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
# Screenshot / Scroll Configuration
# ==========================================================

DEFAULT_SCROLL_PERCENTAGES = [
    0,
    10,
    20,
    30,
    40,
    50,
    60,
    70,
    80,
    90,
    100,
]


DEFAULT_CAPTURE_FULL_PAGE = True

DEFAULT_CAPTURE_VIEWPORTS = True

# Controls whether annotated preview PNG files are generated.
# This can be overridden for each render_page() call.
DEFAULT_SAVE_VISUALIZATIONS = False

DEFAULT_MIN_SCROLL_DELTA = 100

DEFAULT_SCROLL_SETTLE_MS = 150


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
# Annotation Skip Check
# ==========================================================

async def should_skip_annotation(
    element,
) -> bool:
    """
    Return True when the element itself or any ancestor
    explicitly disables annotation extraction.

    Example
    -------

    <div data-annotation-skip="true">
        ...
    </div>

    Descendants remain visible in screenshots but do not
    produce annotations.

    This is especially useful for:

    - modal backgrounds
    - popup backgrounds
    - inactive application shells
    - decorative UI
    - intentionally ignored regions
    """

    return await element.evaluate(
        """
        (el) => {

            let current = el;

            while (current) {

                if (
                    current.getAttribute(
                        "data-annotation-skip"
                    ) === "true"
                ) {
                    return true;
                }

                current =
                    current.parentElement;
            }

            return false;
        }
        """
    )


# ==========================================================
# Viewport Visibility
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
# Full Document Visibility
# ==========================================================

async def is_document_element_visible(
    element,
) -> bool:

    """
    Visibility check used for full-page extraction.

    Unlike viewport visibility, this does NOT use
    document.elementFromPoint(), because elements may be
    outside the current viewport but still appear in a
    full-page screenshot.
    """

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


            if (
                rect.width <= 0 ||
                rect.height <= 0
            ) {
                return false;
            }


            return true;
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
# Document Metrics
# ==========================================================

async def get_document_metrics(
    page,
) -> dict:

    return await page.evaluate(
        """
        () => {

            const body =
                document.body;

            const root =
                document.documentElement;


            const width =
                Math.max(

                    body
                        ? body.scrollWidth
                        : 0,

                    body
                        ? body.offsetWidth
                        : 0,

                    root.scrollWidth,

                    root.offsetWidth,

                    root.clientWidth
                );


            const height =
                Math.max(

                    body
                        ? body.scrollHeight
                        : 0,

                    body
                        ? body.offsetHeight
                        : 0,

                    root.scrollHeight,

                    root.offsetHeight,

                    root.clientHeight
                );


            const viewportWidth =
                window.innerWidth;

            const viewportHeight =
                window.innerHeight;


            return {

                width:
                    width,

                height:
                    height,

                viewport_width:
                    viewportWidth,

                viewport_height:
                    viewportHeight,

                max_scroll_y:
                    Math.max(
                        0,
                        height
                        - viewportHeight
                    ),

                current_scroll_y:
                    window.scrollY,
            };
        }
        """
    )


# ==========================================================
# Scroll Information
# ==========================================================

async def get_scroll_information(
    page,
) -> dict:

    metrics = (
        await get_document_metrics(
            page
        )
    )

    return {

        "document_width":
            metrics[
                "width"
            ],

        "document_height":
            metrics[
                "height"
            ],

        "viewport_width":
            metrics[
                "viewport_width"
            ],

        "viewport_height":
            metrics[
                "viewport_height"
            ],

        "max_scroll_y":
            metrics[
                "max_scroll_y"
            ],

        "current_scroll_y":
            metrics[
                "current_scroll_y"
            ],
    }


# ==========================================================
# Scroll to Absolute Position
# ==========================================================

async def scroll_to_position(
    page,
    scroll_y: float,
    settle_ms: int = DEFAULT_SCROLL_SETTLE_MS,
) -> float:

    await page.evaluate(
        """
        (scrollY) => {

            window.scrollTo({
                top: scrollY,
                left: 0,
                behavior: "instant"
            });

        }
        """,
        scroll_y,
    )


    if settle_ms > 0:

        await page.wait_for_timeout(
            settle_ms
        )


    actual_scroll_y = (
        await page.evaluate(
            "() => window.scrollY"
        )
    )


    return float(
        actual_scroll_y
    )


# ==========================================================
# Scroll to Percentage
# ==========================================================

async def scroll_to_percentage(
    page,
    percentage: float,
    settle_ms: int = DEFAULT_SCROLL_SETTLE_MS,
) -> dict:

    percentage = max(
        0.0,
        min(
            100.0,
            float(
                percentage
            ),
        ),
    )


    info = (
        await get_scroll_information(
            page
        )
    )


    requested_scroll_y = (
        info[
            "max_scroll_y"
        ]
        * (
            percentage
            / 100.0
        )
    )


    actual_scroll_y = (
        await scroll_to_position(

            page,

            requested_scroll_y,

            settle_ms=
                settle_ms,
        )
    )


    current_info = (
        await get_scroll_information(
            page
        )
    )


    return {

        "percentage":
            percentage,

        "requested_scroll_y":
            requested_scroll_y,

        "scroll_y":
            actual_scroll_y,

        "max_scroll_y":
            current_info[
                "max_scroll_y"
            ],

        "document_width":
            current_info[
                "document_width"
            ],

        "document_height":
            current_info[
                "document_height"
            ],

        "viewport_width":
            current_info[
                "viewport_width"
            ],

        "viewport_height":
            current_info[
                "viewport_height"
            ],
    }


# ==========================================================
# Normalize Scroll Percentages
# ==========================================================

def normalize_scroll_percentages(
    percentages,
) -> list[float]:

    normalized = set()


    for percentage in percentages:

        value = float(
            percentage
        )


        if not (
            0.0
            <= value
            <= 100.0
        ):

            raise ValueError(
                "Scroll percentage must be between "
                f"0 and 100. Received: {percentage}"
            )


        normalized.add(
            value
        )


    return sorted(
        normalized
    )


# ==========================================================
# Check Duplicate Scroll Position
# ==========================================================

def should_capture_scroll_position(
    scroll_y: float,
    used_scroll_positions: list[float],
    min_scroll_delta: float,
) -> bool:

    if not used_scroll_positions:

        return True


    distances = [

        abs(
            scroll_y
            - previous_y
        )

        for previous_y
        in used_scroll_positions
    ]


    nearest_distance = min(
        distances
    )


    if nearest_distance <= 0.5:

        return False


    if (
        min_scroll_delta > 0
        and nearest_distance
        < min_scroll_delta
    ):

        return False


    return True


# ==========================================================
# Clamp Viewport Bounding Box
# ==========================================================

def clamp_bbox(
    bbox,
    viewport_width: int,
    viewport_height: int,
):

    x1 = max(
        0.0,
        bbox[
            "x"
        ],
    )


    y1 = max(
        0.0,
        bbox[
            "y"
        ],
    )


    x2 = min(

        float(
            viewport_width
        ),

        bbox[
            "x"
        ]
        + bbox[
            "width"
        ],
    )


    y2 = min(

        float(
            viewport_height
        ),

        bbox[
            "y"
        ]
        + bbox[
            "height"
        ],
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
# Clamp Full Document Bounding Box
# ==========================================================

def clamp_document_bbox(
    bbox,
    document_width: int,
    document_height: int,
):

    x1 = max(
        0.0,
        bbox[
            "x"
        ],
    )


    y1 = max(
        0.0,
        bbox[
            "y"
        ],
    )


    x2 = min(

        float(
            document_width
        ),

        bbox[
            "x"
        ]
        + bbox[
            "width"
        ],
    )


    y2 = min(

        float(
            document_height
        ),

        bbox[
            "y"
        ]
        + bbox[
            "height"
        ],
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
# Viewport Clipping Ancestors
# ==========================================================

async def get_clipping_ancestor_rects(
    element,
):

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
                    "auto"
                ].includes(
                    overflowX
                );


                const clipsY = [
                    "hidden",
                    "clip",
                    "scroll",
                    "auto"
                ].includes(
                    overflowY
                );


                if (
                    clipsX ||
                    clipsY
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
# Full Document Clipping Ancestors
# ==========================================================

async def get_document_clipping_ancestor_rects(
    element,
):

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
                    "auto"
                ].includes(
                    overflowX
                );


                const clipsY = [
                    "hidden",
                    "clip",
                    "scroll",
                    "auto"
                ].includes(
                    overflowY
                );


                if (
                    clipsX ||
                    clipsY
                ) {

                    const rect =
                        current.getBoundingClientRect();


                    rects.push({

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

    x1 = bbox[
        "x"
    ]

    y1 = bbox[
        "y"
    ]

    x2 = (
        x1
        + bbox[
            "width"
        ]
    )

    y2 = (
        y1
        + bbox[
            "height"
        ]
    )


    clip_x1 = (
        clip_rect[
            "x"
        ]
    )

    clip_y1 = (
        clip_rect[
            "y"
        ]
    )

    clip_x2 = (
        clip_x1
        + clip_rect[
            "width"
        ]
    )

    clip_y2 = (
        clip_y1
        + clip_rect[
            "height"
        ]
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
# Clip to All Ancestors
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
# Effective Viewport Occluders
# ==========================================================

async def get_effective_occluder_rects(
    element,
    viewport_width: int,
    viewport_height: int,
):

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

                if (
                    occluder === el
                ) {
                    continue;
                }


                if (
                    occluder.contains(
                        el
                    )
                ) {
                    continue;
                }


                const style =
                    window.getComputedStyle(
                        occluder
                    );


                if (
                    style.display === "none" ||
                    style.visibility === "hidden" ||
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


                const rect =
                    occluder.getBoundingClientRect();


                if (
                    rect.width <= 0 ||
                    rect.height <= 0
                ) {
                    continue;
                }


                if (
                    rect.right <= 0 ||
                    rect.bottom <= 0 ||
                    rect.left >= window.innerWidth ||
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

    bx1 = bbox[
        "x"
    ]

    by1 = bbox[
        "y"
    ]

    bx2 = (
        bx1
        + bbox[
            "width"
        ]
    )

    by2 = (
        by1
        + bbox[
            "height"
        ]
    )


    ox1 = occluder[
        "x"
    ]

    oy1 = occluder[
        "y"
    ]

    ox2 = (
        ox1
        + occluder[
            "width"
        ]
    )

    oy2 = (
        oy1
        + occluder[
            "height"
        ]
    )


    return not (

        bx2 <= ox1
        or bx1 >= ox2
        or by2 <= oy1
        or by1 >= oy2
    )


# ==========================================================
# Clip Against One Occluder
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


    bx1 = bbox[
        "x"
    ]

    by1 = bbox[
        "y"
    ]

    bx2 = (
        bx1
        + bbox[
            "width"
        ]
    )

    by2 = (
        by1
        + bbox[
            "height"
        ]
    )


    ox1 = occluder[
        "x"
    ]

    oy1 = occluder[
        "y"
    ]

    ox2 = (
        ox1
        + occluder[
            "width"
        ]
    )

    oy2 = (
        oy1
        + occluder[
            "height"
        ]
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


    ix1 = max(
        bx1,
        ox1,
    )

    iy1 = max(
        by1,
        oy1,
    )

    ix2 = min(
        bx2,
        ox2,
    )

    iy2 = min(
        by2,
        oy2,
    )


    if (
        ix2 <= ix1
        or iy2 <= iy1
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

            "x":
                bx1,

            "y":
                by1,

            "width":
                bbox[
                    "width"
                ],

            "height":
                new_height,
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

            "x":
                bx1,

            "y":
                new_y,

            "width":
                bbox[
                    "width"
                ],

            "height":
                new_height,
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

            "x":
                bx1,

            "y":
                by1,

            "width":
                new_width,

            "height":
                bbox[
                    "height"
                ],
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

            "x":
                new_x,

            "y":
                by1,

            "width":
                new_width,

            "height":
                bbox[
                    "height"
                ],
        }


    # Internal occlusion cannot be represented accurately
    # using one YOLO rectangle.
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
# Asset Source Helper
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
# Annotation Metadata
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
    # Emoji Metadata
    # ======================================================

    emoji_source = (
        await element.get_attribute(
            "data-emoji-source"
        )
    )


    if emoji_source:

        annotation[
            "emoji_source"
        ] = emoji_source


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
    viewport_width: int,
    viewport_height: int,
    dpr: float,
    min_visible_ratio: float = DEFAULT_MIN_VISIBLE_RATIO,
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


        # ==================================================
        # Explicit Annotation Exclusion
        # ==================================================

        if await should_skip_annotation(
            element
        ):

            continue


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
        # Viewport Visibility
        # ==================================================

        if not await is_actually_visible(
            element
        ):

            continue


        # ==================================================
        # BBox
        # ==================================================

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


        original_bbox_css = dict(
            bbox_css
        )


        # ==================================================
        # Ancestor Clipping
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
        # Occluder State
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


        if not is_occluder:

            effective_occluders = (
                await get_effective_occluder_rects(
                    element,
                    viewport_width,
                    viewport_height,
                )
            )


            if effective_occluders:

                previous_bbox = dict(
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
                    != previous_bbox
                )


        # ==================================================
        # Visible Ratio
        # ==================================================

        original_area = (

            original_bbox_css[
                "width"
            ]

            * original_bbox_css[
                "height"
            ]
        )


        visible_area = (

            bbox_css[
                "width"
            ]

            * bbox_css[
                "height"
            ]
        )


        if original_area <= 0:

            continue


        visible_ratio = (
            visible_area
            / original_area
        )


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
        # Class ID
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
                bbox_css[
                    "x"
                ]
                * dpr,

            "y":
                bbox_css[
                    "y"
                ]
                * dpr,

            "width":
                bbox_css[
                    "width"
                ]
                * dpr,

            "height":
                bbox_css[
                    "height"
                ]
                * dpr,
        }


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
                    4,
                ),

            "is_occluder":
                is_occluder,

            "ancestor_clipped":
                ancestor_clipped,

            "overlay_clipped":
                overlay_clipped,
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
    document_width: int,
    document_height: int,
    dpr: float,
    min_visible_ratio: float = DEFAULT_MIN_VISIBLE_RATIO,
):

    """
    Extract annotations using document coordinates.

    Differences from viewport extraction:

    - element does not need to be inside current viewport
    - no elementFromPoint requirement
    - coordinates contain window.scrollX / scrollY
    - clipping ancestors use document coordinates
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

        element = elements.nth(
            index
        )


        # ==================================================
        # Explicit Annotation Exclusion
        # ==================================================

        if await should_skip_annotation(
            element
        ):

            continue


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
        # Document Visibility
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

                bbox,

                document_width,
                document_height,
            )
        )


        if not bbox_css:

            continue


        original_bbox_css = dict(
            bbox_css
        )


        # ==================================================
        # Document Ancestor Clipping
        # ==================================================

        clipping_ancestors = (
            await get_document_clipping_ancestor_rects(
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
        # Visible Ratio
        # ==================================================

        original_area = (

            original_bbox_css[
                "width"
            ]

            * original_bbox_css[
                "height"
            ]
        )


        visible_area = (

            bbox_css[
                "width"
            ]

            * bbox_css[
                "height"
            ]
        )


        if original_area <= 0:

            continue


        visible_ratio = (
            visible_area
            / original_area
        )


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
        # Occluder Metadata
        # ==================================================

        is_occluder = (
            await element.get_attribute(
                "data-occluder"
            )
            == "true"
        )


        # ==================================================
        # Image Coordinates
        # ==================================================

        bbox_image = {

            "x":
                bbox_css[
                    "x"
                ]
                * dpr,

            "y":
                bbox_css[
                    "y"
                ]
                * dpr,

            "width":
                bbox_css[
                    "width"
                ]
                * dpr,

            "height":
                bbox_css[
                    "height"
                ]
                * dpr,
        }


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
                    4,
                ),

            "is_occluder":
                is_occluder,

            "ancestor_clipped":
                ancestor_clipped,

            "overlay_clipped":
                False,
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

    if (
        image_width <= 0
        or image_height <= 0
    ):

        raise ValueError(
            "Image dimensions must be positive."
        )


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
            bbox[
                "x"
            ]
            + bbox[
                "width"
            ]
            / 2
        )


        center_y = (
            bbox[
                "y"
            ]
            + bbox[
                "height"
            ]
            / 2
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
            bbox[
                "width"
            ]
            / image_width
        )


        normalized_height = (
            bbox[
                "height"
            ]
            / image_height
        )


        normalized_x = min(
            1.0,
            max(
                0.0,
                normalized_x,
            ),
        )


        normalized_y = min(
            1.0,
            max(
                0.0,
                normalized_y,
            ),
        )


        normalized_width = min(
            1.0,
            max(
                0.0,
                normalized_width,
            ),
        )


        normalized_height = min(
            1.0,
            max(
                0.0,
                normalized_height,
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
    screenshot_path: Path,
    annotations,
    output_path: Path,
    dpr: float,
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
            bbox[
                "x"
            ]
        )


        y1 = (
            bbox[
                "y"
            ]
        )


        x2 = (
            x1
            + bbox[
                "width"
            ]
        )


        y2 = (
            y1
            + bbox[
                "height"
            ]
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
                "?",
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
                1.0,
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
                    y1
                    - 14 * dpr,
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

            "wcag":
                theme.get(
                    "wcag"
                ),
        }


    return {

        "mode":
            getattr(
                theme,
                "mode",
                None,
            ),

        "seed":
            getattr(
                theme,
                "seed",
                None,
            ),

        "wcag_pass":
            getattr(
                theme,
                "wcag_pass",
                None,
            ),

        "wcag":
            getattr(
                theme,
                "wcag",
                None,
            ),
    }


# ==========================================================
# Create Profile Directories
# ==========================================================

def create_profile_directories(
    annotation_root: Path,
    annotation_profiles: list[str],
    save_visualizations: bool,
) -> dict:

    result = {}


    for profile_name in (
        annotation_profiles
    ):

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


        directories_to_create = [
            label_dir,
            json_dir,
        ]

        if save_visualizations:
            directories_to_create.append(
                visualization_dir
            )

        for directory in directories_to_create:

            directory.mkdir(
                parents=True,
                exist_ok=True,
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
                (
                    visualization_dir
                    if save_visualizations
                    else None
                ),
        }


    return result


# ==========================================================
# Create Output Directories
# ==========================================================

def create_output_directories(
    output_dir: Path,
    annotation_profiles: list[str],
    capture_full_page: bool,
    capture_viewports: bool,
    save_visualizations: bool,
) -> dict:

    result = {

        "full_page":
            None,

        "viewport":
            None,
    }


    # ======================================================
    # Full Page
    # ======================================================

    if capture_full_page:

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


        full_image_dir.mkdir(
            parents=True,
            exist_ok=True,
        )


        full_profiles = (
            create_profile_directories(

                full_annotation_root,

                annotation_profiles,

                save_visualizations,
            )
        )


        result[
            "full_page"
        ] = {

            "root":
                full_page_root,

            "images":
                full_image_dir,

            "annotations":
                full_annotation_root,

            "profiles":
                full_profiles,
        }


    # ======================================================
    # Viewport
    # ======================================================

    if capture_viewports:

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


        viewport_image_dir.mkdir(
            parents=True,
            exist_ok=True,
        )


        viewport_profiles = (
            create_profile_directories(

                viewport_annotation_root,

                annotation_profiles,

                save_visualizations,
            )
        )


        result[
            "viewport"
        ] = {

            "root":
                viewport_root,

            "images":
                viewport_image_dir,

            "annotations":
                viewport_annotation_root,

            "profiles":
                viewport_profiles,
        }


    return result


# ==========================================================
# Save Profile Outputs
# ==========================================================

def save_profile_outputs(
    *,
    all_annotations,
    profile_name: str,
    profile_directories: dict,
    base_name: str,
    screenshot_path: Path,
    image_width: int,
    image_height: int,
    dpr: float,
    base_metadata: dict,
    save_visualizations: bool,
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


    visualization_path = None


    metadata = {

        **base_metadata,

        "annotation_profile":
            profile_name,

        "profile_class_map":
            PROFILE_CLASS_TO_ID[
                profile_name
            ],

        "annotation_count":
            len(
                annotations
            ),

        "annotations":
            annotations,
    }


    json_path.write_text(

        json.dumps(
            metadata,
            indent=2,
            ensure_ascii=False,
        ),

        encoding="utf-8",
    )


    save_yolo_labels(

        annotations=
            annotations,

        image_width=
            image_width,

        image_height=
            image_height,

        output_path=
            label_path,
    )


    if save_visualizations:

        visualization_directory = (
            directories[
                "visualization"
            ]
        )

        if visualization_directory is None:

            raise RuntimeError(
                "Visualization directory was not created."
            )

        visualization_path = (
            visualization_directory
            / f"{base_name}.png"
        )

        draw_visualization(

            screenshot_path=
                screenshot_path,

            annotations=
                annotations,

            output_path=
                visualization_path,

            dpr=
                dpr,
        )


    return {

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

    capture_full_page: bool = DEFAULT_CAPTURE_FULL_PAGE,
    capture_viewports: bool = DEFAULT_CAPTURE_VIEWPORTS,

    scroll_percentages: list[int | float] | None = None,
    min_scroll_delta: int = DEFAULT_MIN_SCROLL_DELTA,
    scroll_settle_ms: int = DEFAULT_SCROLL_SETTLE_MS,
    save_visualizations: bool = DEFAULT_SAVE_VISUALIZATIONS,
):

    # ======================================================
    # Validate Capture Mode
    # ======================================================

    if (
        not capture_full_page
        and not capture_viewports
    ):

        raise ValueError(
            "At least one capture mode must be enabled."
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


    # ======================================================
    # Annotation Profiles
    # ======================================================

    if annotation_profiles is None:

        annotation_profiles = (
            DEFAULT_ANNOTATION_PROFILES.copy()
        )


    annotation_profiles = list(
        dict.fromkeys(
            annotation_profiles
        )
    )


    for profile_name in (
        annotation_profiles
    ):

        if (
            profile_name
            not in PROFILE_CLASS_TO_ID
        ):

            raise ValueError(
                f"Unknown annotation profile: "
                f"{profile_name}"
            )


    # ======================================================
    # Scroll Percentages
    # ======================================================

    if scroll_percentages is None:

        scroll_percentages = (
            DEFAULT_SCROLL_PERCENTAGES.copy()
        )


    scroll_percentages = (
        normalize_scroll_percentages(
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
            "unknown",
        )
    )


    viewport_orientation = (
        viewport.get(
            "orientation",
            (
                "landscape"
                if width > height
                else "portrait"
            ),
        )
    )


    viewport_size_class = (
        viewport.get(
            "size_class",
            "unknown",
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
    # Output Root
    # ======================================================

    output_subdir = (
        output_subdir
        or page_type
    )


    output_dir = (
        output_root
        / output_subdir
    )


    output_directories = (
        create_output_directories(

            output_dir=
                output_dir,

            annotation_profiles=
                annotation_profiles,

            capture_full_page=
                capture_full_page,

            capture_viewports=
                capture_viewports,

            save_visualizations=
                save_visualizations,
        )
    )


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


    html = (
        template.render(
            **context
        )
    )


    # ======================================================
    # Browser Page
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

        await scroll_to_position(

            page,

            0,

            settle_ms=
                scroll_settle_ms,
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


        # ==================================================
        # Naming
        # ==================================================

        page_base_name = (

            f"{page_type}_"
            f"{sample_index:06d}_"
            f"{theme_mode}_"
            f"{viewport_name}"
        )


        # ==================================================
        # Result
        # ==================================================

        result = {

            "page_type":
                page_type,

            "sample_index":
                sample_index,

            "theme_mode":
                theme_mode,

            "viewport":
                viewport_name,

            "document_width_css":
                document_width,

            "document_height_css":
                document_height,

            "full_page":
                None,

            "viewport_captures":
                [],
        }


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
        # Full Page
        # ==================================================

        if capture_full_page:

            await scroll_to_position(

                page,

                0,

                settle_ms=
                    scroll_settle_ms,
            )


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


            full_page_dirs = (
                output_directories[
                    "full_page"
                ]
            )


            full_page_name = (

                f"{page_base_name}_"
                f"full"
            )


            full_page_path = (

                full_page_dirs[
                    "images"
                ]
                / f"{full_page_name}.png"
            )


            await page.screenshot(

                path=str(
                    full_page_path
                ),

                full_page=True,
            )


            with Image.open(
                full_page_path
            ) as full_page_image:

                full_image_width = (
                    full_page_image.width
                )

                full_image_height = (
                    full_page_image.height
                )


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

                    min_visible_ratio=
                        min_visible_ratio,
                )
            )


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
                    {

                        **viewport_metadata,

                        "image_width":
                            full_image_width,

                        "image_height":
                            full_image_height,
                    },

                "document":
                    {

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
                    get_theme_metadata(
                        theme
                    ),

                "visibility":
                    {

                        "min_visible_ratio":
                            min_visible_ratio,

                        "document_clipping":
                            True,

                        "ancestor_clipping":
                            True,

                        "occlusion_clipping":
                            False,

                        "annotation_skip":
                            True,
                    },

                "global_annotation_count":
                    len(
                        full_annotations
                    ),
            }


            profile_results = {}


            for profile_name in (
                annotation_profiles
            ):

                profile_result = (
                    save_profile_outputs(

                        all_annotations=
                            full_annotations,

                        profile_name=
                            profile_name,

                        profile_directories=
                            full_page_dirs[
                                "profiles"
                            ],

                        base_name=
                            full_page_name,

                        screenshot_path=
                            full_page_path,

                        image_width=
                            full_image_width,

                        image_height=
                            full_image_height,

                        dpr=
                            dpr,

                        base_metadata=
                            full_base_metadata,

                        save_visualizations=
                            save_visualizations,
                    )
                )


                profile_results[
                    profile_name
                ] = profile_result


                print(

                    f"[FULL] "
                    f"{page_type} | "
                    f"{theme_mode} | "
                    f"{viewport_name} | "
                    f"{profile_name} | "
                    f"{profile_result['annotation_count']} "
                    f"annotations"
                )


            result[
                "full_page"
            ] = {

                "image":
                    full_page_path,

                "image_width":
                    full_image_width,

                "image_height":
                    full_image_height,

                "global_annotation_count":
                    len(
                        full_annotations
                    ),

                "profiles":
                    profile_results,
            }


        # ==================================================
        # Viewport Captures
        # ==================================================

        if capture_viewports:

            viewport_dirs = (
                output_directories[
                    "viewport"
                ]
            )


            used_scroll_positions = []


            for percentage in (
                scroll_percentages
            ):

                scroll_info = (
                    await scroll_to_percentage(

                        page,

                        percentage,

                        settle_ms=
                            scroll_settle_ms,
                    )
                )


                scroll_y = float(
                    scroll_info[
                        "scroll_y"
                    ]
                )


                if not should_capture_scroll_position(

                    scroll_y=
                        scroll_y,

                    used_scroll_positions=
                        used_scroll_positions,

                    min_scroll_delta=
                        min_scroll_delta,

                ):

                    print(

                        f"[SKIP] "
                        f"{page_type} | "
                        f"{theme_mode} | "
                        f"{viewport_name} | "
                        f"scroll={percentage:g}% | "
                        f"y={scroll_y:.0f}"
                    )

                    continue


                used_scroll_positions.append(
                    scroll_y
                )


                if float(
                    percentage
                ).is_integer():

                    scroll_label = (
                        f"{int(percentage):03d}"
                    )

                else:

                    scroll_label = (

                        str(
                            percentage
                        )
                        .replace(
                            ".",
                            "_",
                        )
                    )


                viewport_name_base = (

                    f"{page_base_name}_"
                    f"scroll_{scroll_label}"
                )


                screenshot_path = (

                    viewport_dirs[
                        "images"
                    ]

                    / f"{viewport_name_base}.png"
                )


                await page.screenshot(

                    path=str(
                        screenshot_path
                    ),

                    full_page=False,
                )


                with Image.open(
                    screenshot_path
                ) as screenshot:

                    image_width = (
                        screenshot.width
                    )

                    image_height = (
                        screenshot.height
                    )


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

                        min_visible_ratio=
                            min_visible_ratio,
                    )
                )


                viewport_base_metadata = {

                    "capture_type":
                        "viewport",

                    "page_type":
                        page_type,

                    "sample_index":
                        sample_index,

                    "template":
                        template_name,

                    "viewport":
                        {

                            **viewport_metadata,

                            "image_width":
                                image_width,

                            "image_height":
                                image_height,
                        },

                    "document":
                        {

                            "width_css":
                                scroll_info[
                                    "document_width"
                                ],

                            "height_css":
                                scroll_info[
                                    "document_height"
                                ],
                        },

                    "scroll":
                        {

                            "percentage":
                                percentage,

                            "requested_scroll_y_css":
                                scroll_info[
                                    "requested_scroll_y"
                                ],

                            "scroll_y_css":
                                scroll_y,

                            "max_scroll_y_css":
                                scroll_info[
                                    "max_scroll_y"
                                ],
                        },

                    "theme":
                        get_theme_metadata(
                            theme
                        ),

                    "visibility":
                        {

                            "min_visible_ratio":
                                min_visible_ratio,

                            "viewport_clipping":
                                True,

                            "ancestor_clipping":
                                True,

                            "occlusion_clipping":
                                True,

                            "annotation_skip":
                                True,
                        },

                    "global_annotation_count":
                        len(
                            annotations
                        ),
                }


                profile_results = {}


                for profile_name in (
                    annotation_profiles
                ):

                    profile_result = (
                        save_profile_outputs(

                            all_annotations=
                                annotations,

                            profile_name=
                                profile_name,

                            profile_directories=
                                viewport_dirs[
                                    "profiles"
                                ],

                            base_name=
                                viewport_name_base,

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

                            save_visualizations=
                                save_visualizations,
                        )
                    )


                    profile_results[
                        profile_name
                    ] = profile_result


                    print(

                        f"[VIEWPORT] "
                        f"{page_type} | "
                        f"{theme_mode} | "
                        f"{viewport_name} | "
                        f"scroll={percentage:g}% | "
                        f"y={scroll_y:.0f} | "
                        f"{profile_name} | "
                        f"{profile_result['annotation_count']} "
                        f"annotations"
                    )


                result[
                    "viewport_captures"
                ].append(
                    {

                        "image":
                            screenshot_path,

                        "scroll_percentage":
                            percentage,

                        "scroll_y_css":
                            scroll_y,

                        "image_width":
                            image_width,

                        "image_height":
                            image_height,

                        "global_annotation_count":
                            len(
                                annotations
                            ),

                        "profiles":
                            profile_results,
                    }
                )


        # ==================================================
        # Reset Scroll
        # ==================================================

        await scroll_to_position(
            page,
            0,
            settle_ms=0,
        )


        # ==================================================
        # Summary
        # ==================================================

        result[
            "viewport_capture_count"
        ] = len(
            result[
                "viewport_captures"
            ]
        )


        result[
            "captured_scroll_positions"
        ] = [

            {

                "percentage":
                    capture[
                        "scroll_percentage"
                    ],

                "scroll_y_css":
                    capture[
                        "scroll_y_css"
                    ],
            }

            for capture
            in result[
                "viewport_captures"
            ]
        ]


        return result


    finally:

        await page.close()
