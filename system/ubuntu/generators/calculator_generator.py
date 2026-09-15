from __future__ import annotations

import math
import random


# ==========================================================
# States
# ==========================================================

CALCULATOR_STATES = [

    "basic",

    "result",

    "expression",

    "error",

    "history_open",

    "scientific",

    "programmer",

    "memory_open",

    "unit_conversion",

    "angle_menu",

    "function_menu",

    "clear_confirmation",
]


# ==========================================================
# Basic Keys
# ==========================================================

BASIC_KEYS = [

    {
        "label": "%",
        "semantic": "percent",
        "type": "function",
    },

    {
        "label": "CE",
        "semantic": "clear_entry",
        "type": "function",
    },

    {
        "label": "C",
        "semantic": "clear",
        "type": "function",
    },

    {
        "label": "⌫",
        "semantic": "backspace",
        "type": "icon",
        "icon": "backspace",
    },

    {
        "label": "1/x",
        "semantic": "reciprocal",
        "type": "function",
    },

    {
        "label": "x²",
        "semantic": "square",
        "type": "function",
    },

    {
        "label": "√x",
        "semantic": "square_root",
        "type": "function",
    },

    {
        "label": "÷",
        "semantic": "divide",
        "type": "operator",
    },

    {
        "label": "7",
        "semantic": "digit_7",
        "type": "number",
    },

    {
        "label": "8",
        "semantic": "digit_8",
        "type": "number",
    },

    {
        "label": "9",
        "semantic": "digit_9",
        "type": "number",
    },

    {
        "label": "×",
        "semantic": "multiply",
        "type": "operator",
    },

    {
        "label": "4",
        "semantic": "digit_4",
        "type": "number",
    },

    {
        "label": "5",
        "semantic": "digit_5",
        "type": "number",
    },

    {
        "label": "6",
        "semantic": "digit_6",
        "type": "number",
    },

    {
        "label": "−",
        "semantic": "subtract",
        "type": "operator",
    },

    {
        "label": "1",
        "semantic": "digit_1",
        "type": "number",
    },

    {
        "label": "2",
        "semantic": "digit_2",
        "type": "number",
    },

    {
        "label": "3",
        "semantic": "digit_3",
        "type": "number",
    },

    {
        "label": "+",
        "semantic": "add",
        "type": "operator",
    },

    {
        "label": "±",
        "semantic": "sign",
        "type": "function",
    },

    {
        "label": "0",
        "semantic": "digit_0",
        "type": "number",
    },

    {
        "label": ".",
        "semantic": "decimal",
        "type": "number",
    },

    {
        "label": "=",
        "semantic": "equals",
        "type": "equals",
    },
]


# ==========================================================
# Scientific Keys
# ==========================================================

SCIENTIFIC_KEYS = [

    {
        "label": "sin",
        "semantic": "sin",
    },

    {
        "label": "cos",
        "semantic": "cos",
    },

    {
        "label": "tan",
        "semantic": "tan",
    },

    {
        "label": "π",
        "semantic": "pi",
    },

    {
        "label": "e",
        "semantic": "euler",
    },

    {
        "label": "ln",
        "semantic": "ln",
    },

    {
        "label": "log",
        "semantic": "log",
    },

    {
        "label": "xʸ",
        "semantic": "power",
    },

    {
        "label": "10ˣ",
        "semantic": "ten_power",
    },

    {
        "label": "n!",
        "semantic": "factorial",
    },

    {
        "label": "|x|",
        "semantic": "absolute",
    },

    {
        "label": "mod",
        "semantic": "modulo",
    },
]


# ==========================================================
# Programmer Keys
# ==========================================================

PROGRAMMER_BASES = [

    {
        "name": "HEX",
        "value": "FF2A",
    },

    {
        "name": "DEC",
        "value": "65322",
    },

    {
        "name": "OCT",
        "value": "177452",
    },

    {
        "name": "BIN",
        "value": "1111111100101010",
    },
]


PROGRAMMER_EXTRA_KEYS = [

    {
        "label": "A",
        "semantic": "hex_a",
    },

    {
        "label": "B",
        "semantic": "hex_b",
    },

    {
        "label": "C",
        "semantic": "hex_c",
    },

    {
        "label": "D",
        "semantic": "hex_d",
    },

    {
        "label": "E",
        "semantic": "hex_e",
    },

    {
        "label": "F",
        "semantic": "hex_f",
    },

    {
        "label": "AND",
        "semantic": "bit_and",
    },

    {
        "label": "OR",
        "semantic": "bit_or",
    },

    {
        "label": "XOR",
        "semantic": "bit_xor",
    },

    {
        "label": "NOT",
        "semantic": "bit_not",
    },
]


# ==========================================================
# Memory
# ==========================================================

MEMORY_VALUES = [
    12.5,
    42,
    156,
    3.14159,
    1024,
    -18.4,
]


# ==========================================================
# Units
# ==========================================================

UNIT_GROUPS = [

    {
        "name": "Length",
        "icon": "straighten",
        "from_unit": "Meters",
        "to_unit": "Feet",
        "factor": 3.28084,
    },

    {
        "name": "Temperature",
        "icon": "device_thermostat",
        "from_unit": "Celsius",
        "to_unit": "Fahrenheit",
        "factor": None,
    },

    {
        "name": "Mass",
        "icon": "scale",
        "from_unit": "Kilograms",
        "to_unit": "Pounds",
        "factor": 2.20462,
    },

    {
        "name": "Volume",
        "icon": "water_drop",
        "from_unit": "Liters",
        "to_unit": "Gallons",
        "factor": 0.264172,
    },
]


# ==========================================================
# History
# ==========================================================

def generate_history() -> list[dict]:

    expressions = [

        ("24 × 6", "144"),

        ("144 ÷ 12", "12"),

        ("57 + 28", "85"),

        ("200 − 74", "126"),

        ("12²", "144"),

        ("√144", "12"),

        ("8 × 9 + 12", "84"),

        ("125 ÷ 5", "25"),
    ]

    count = random.randint(
        3,
        7,
    )

    selected = random.sample(
        expressions,
        k=min(
            count,
            len(
                expressions
            ),
        ),
    )

    return [

        {
            "expression":
                expression,

            "result":
                result,
        }

        for expression, result
        in selected
    ]


# ==========================================================
# Display
# ==========================================================

def generate_display(
    state: str,
) -> tuple[str, str]:

    if state == "error":

        return (
            "1 ÷ 0",
            "Cannot divide by zero",
        )


    if state == "result":

        first = random.randint(
            10,
            99,
        )

        second = random.randint(
            2,
            12,
        )

        result = (
            first
            * second
        )

        return (
            f"{first} × {second}",
            str(
                result
            ),
        )


    if state == "expression":

        return (
            "12 + 8 × 4 − 6",
            "38",
        )


    if state == "scientific":

        return (
            "sin(45)",
            "0.70710678",
        )


    if state == "programmer":

        return (
            "DEC",
            "65322",
        )


    return (
        "",
        str(
            random.randint(
                0,
                999,
            )
        ),
    )


# ==========================================================
# Main
# ==========================================================

def generate_calculator_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            CALCULATOR_STATES
        )


    if state not in CALCULATOR_STATES:

        raise ValueError(
            f"Unknown calculator state: "
            f"{state}"
        )


    expression, display_value = (
        generate_display(
            state
        )
    )


    # ======================================================
    # Mode
    # ======================================================

    if state == "scientific":

        mode = "scientific"

    elif state == "programmer":

        mode = "programmer"

    else:

        mode = "basic"


    # ======================================================
    # Conversion
    # ======================================================

    conversion = random.choice(
        UNIT_GROUPS
    )

    from_value = round(
        random.uniform(
            1,
            50,
        ),
        2,
    )


    if conversion[
        "name"
    ] == "Temperature":

        to_value = round(
            (
                from_value
                * 9
                / 5
            )
            + 32,
            2,
        )

    else:

        to_value = round(
            from_value
            * conversion[
                "factor"
            ],
            2,
        )


    # ======================================================
    # Angle
    # ======================================================

    angle_mode = random.choice(
        [
            "Degrees",
            "Radians",
            "Gradians",
        ]
    )


    # ======================================================
    # Functions
    # ======================================================

    function_entries = [

        {
            "label":
                "Trigonometry",

            "icon":
                "functions",
        },

        {
            "label":
                "Constants",

            "icon":
                "calculate",
        },

        {
            "label":
                "Logarithms",

            "icon":
                "query_stats",
        },

        {
            "label":
                "Combinatorics",

            "icon":
                "account_tree",
        },
    ]


    return {

        "state":
            state,

        "mode":
            mode,

        "expression":
            expression,

        "display_value":
            display_value,

        "basic_keys":
            [
                dict(
                    key
                )
                for key
                in BASIC_KEYS
            ],

        "scientific_keys":
            [
                dict(
                    key
                )
                for key
                in SCIENTIFIC_KEYS
            ],

        "programmer_bases":
            [
                dict(
                    base
                )
                for base
                in PROGRAMMER_BASES
            ],

        "programmer_keys":
            [
                dict(
                    key
                )
                for key
                in PROGRAMMER_EXTRA_KEYS
            ],

        "history_entries":
            generate_history(),

        "memory_entries":
            [
                {
                    "value":
                        value,
                }
                for value
                in random.sample(
                    MEMORY_VALUES,
                    k=random.randint(
                        2,
                        5,
                    ),
                )
            ],

        "conversion":
            dict(
                conversion
            ),

        "from_value":
            from_value,

        "to_value":
            to_value,

        "angle_mode":
            angle_mode,

        "function_entries":
            function_entries,

        "memory_active":
            random.random()
            < 0.55,
    }