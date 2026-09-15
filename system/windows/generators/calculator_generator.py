from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

CALCULATOR_STATES = [
    "standard",
    "scientific",
    "programmer",
    "history",
    "memory",
    "currency_converter",
    "unit_converter",
    "date_calculation",
    "division_by_zero",
    "calculation_result",
]


# ==========================================================
# Standard Keys
# ==========================================================

STANDARD_KEYS = [
    {
        "label": "%",
        "type": "function",
    },
    {
        "label": "CE",
        "type": "function",
    },
    {
        "label": "C",
        "type": "function",
    },
    {
        "label": "⌫",
        "type": "function",
        "icon": "backspace",
    },

    {
        "label": "1/x",
        "type": "function",
    },
    {
        "label": "x²",
        "type": "function",
    },
    {
        "label": "√x",
        "type": "function",
    },
    {
        "label": "÷",
        "type": "operator",
    },

    {
        "label": "7",
        "type": "number",
    },
    {
        "label": "8",
        "type": "number",
    },
    {
        "label": "9",
        "type": "number",
    },
    {
        "label": "×",
        "type": "operator",
    },

    {
        "label": "4",
        "type": "number",
    },
    {
        "label": "5",
        "type": "number",
    },
    {
        "label": "6",
        "type": "number",
    },
    {
        "label": "−",
        "type": "operator",
    },

    {
        "label": "1",
        "type": "number",
    },
    {
        "label": "2",
        "type": "number",
    },
    {
        "label": "3",
        "type": "number",
    },
    {
        "label": "+",
        "type": "operator",
    },

    {
        "label": "±",
        "type": "number",
    },
    {
        "label": "0",
        "type": "number",
    },
    {
        "label": ".",
        "type": "number",
    },
    {
        "label": "=",
        "type": "equals",
    },
]


# ==========================================================
# Scientific Keys
# ==========================================================

SCIENTIFIC_KEYS = [
    "2nd",
    "π",
    "e",
    "C",
    "⌫",
    "x²",
    "1/x",
    "|x|",
    "exp",
    "mod",
    "√x",
    "(",
    ")",
    "n!",
    "÷",
    "xʸ",
    "7",
    "8",
    "9",
    "×",
    "10ˣ",
    "4",
    "5",
    "6",
    "−",
    "log",
    "1",
    "2",
    "3",
    "+",
    "ln",
    "±",
    "0",
    ".",
    "=",
]


# ==========================================================
# Programmer Keys
# ==========================================================

PROGRAMMER_KEYS = [
    "HEX",
    "DEC",
    "OCT",
    "BIN",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "7",
    "8",
    "9",
    "÷",
    "4",
    "5",
    "6",
    "×",
    "1",
    "2",
    "3",
    "−",
    "0",
    "00",
    ".",
    "+",
    "AND",
    "OR",
    "XOR",
    "NOT",
    "LSH",
    "RSH",
    "C",
    "⌫",
    "=",
]


# ==========================================================
# History
# ==========================================================

HISTORY_POOL = [
    {
        "expression": "125 × 8",
        "result": "1,000",
    },
    {
        "expression": "1,024 ÷ 16",
        "result": "64",
    },
    {
        "expression": "45 + 72",
        "result": "117",
    },
    {
        "expression": "92 − 18",
        "result": "74",
    },
    {
        "expression": "12.5 × 4",
        "result": "50",
    },
    {
        "expression": "√144",
        "result": "12",
    },
]


# ==========================================================
# Memory
# ==========================================================

MEMORY_POOL = [
    "128",
    "256",
    "1,024",
    "3.141592",
    "42",
]


# ==========================================================
# Currency
# ==========================================================

CURRENCIES = [
    "USD",
    "KRW",
    "EUR",
    "JPY",
    "GBP",
]


# ==========================================================
# Units
# ==========================================================

UNIT_TYPES = {
    "Length": [
        "Meters",
        "Kilometers",
        "Miles",
        "Feet",
    ],
    "Weight": [
        "Kilograms",
        "Grams",
        "Pounds",
        "Ounces",
    ],
    "Temperature": [
        "Celsius",
        "Fahrenheit",
        "Kelvin",
    ],
}


# ==========================================================
# Helpers
# ==========================================================

def generate_expression() -> dict:

    left = random.randint(
        1,
        999,
    )

    right = random.randint(
        1,
        99,
    )

    operator = random.choice(
        [
            "+",
            "−",
            "×",
            "÷",
        ]
    )

    if operator == "+":

        result = left + right

    elif operator == "−":

        result = left - right

    elif operator == "×":

        result = left * right

    else:

        result = round(
            left / right,
            6,
        )


    return {
        "expression":
            f"{left} {operator} {right} =",

        "result":
            f"{result:,}",
    }


def generate_history() -> list[dict]:

    return random.sample(
        HISTORY_POOL,
        k=random.randint(
            3,
            len(HISTORY_POOL),
        ),
    )


def generate_memory() -> list[str]:

    return random.sample(
        MEMORY_POOL,
        k=random.randint(
            2,
            len(MEMORY_POOL),
        ),
    )


# ==========================================================
# Main Generator
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
            f"Unknown calculator state: {state}"
        )


    expression = generate_expression()


    if state == "division_by_zero":

        expression = {
            "expression":
                "25 ÷ 0 =",

            "result":
                "Cannot divide by zero",
        }


    if state == "standard":

        expression = {
            "expression":
                "",

            "result":
                "0",
        }


    if state == "calculation_result":

        expression = generate_expression()


    currency_from = random.choice(
        CURRENCIES
    )

    currency_to = random.choice(
        [
            item
            for item in CURRENCIES
            if item
            != currency_from
        ]
    )


    unit_type = random.choice(
        list(
            UNIT_TYPES.keys()
        )
    )

    units = UNIT_TYPES[
        unit_type
    ]

    unit_from = random.choice(
        units
    )

    unit_to = random.choice(
        [
            unit
            for unit in units
            if unit
            != unit_from
        ]
    )


    return {
        "state":
            state,

        "expression":
            expression["expression"],

        "display":
            expression["result"],

        "standard_keys":
            STANDARD_KEYS,

        "scientific_keys":
            SCIENTIFIC_KEYS,

        "programmer_keys":
            PROGRAMMER_KEYS,

        "history":
            generate_history(),

        "memory":
            generate_memory(),

        "currency": {
            "from":
                currency_from,

            "to":
                currency_to,

            "amount":
                random.randint(
                    10,
                    5000,
                ),

            "converted":
                round(
                    random.uniform(
                        100,
                        1500000,
                    ),
                    2,
                ),
        },

        "unit": {
            "type":
                unit_type,

            "from":
                unit_from,

            "to":
                unit_to,

            "value":
                random.randint(
                    1,
                    500,
                ),

            "converted":
                round(
                    random.uniform(
                        1,
                        1200,
                    ),
                    3,
                ),
        },

        "date": {
            "from":
                random.choice(
                    [
                        "09/05/2026",
                        "08/20/2026",
                        "07/12/2026",
                    ]
                ),

            "to":
                random.choice(
                    [
                        "10/18/2026",
                        "11/03/2026",
                        "12/01/2026",
                    ]
                ),

            "difference":
                random.randint(
                    12,
                    120,
                ),
        },
    }