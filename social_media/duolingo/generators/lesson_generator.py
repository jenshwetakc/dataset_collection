from __future__ import annotations

import random

from faker import Faker

from social_media.duolingo.generators.media_generator import (
    get_random_character,
    get_random_illustration,
)


fake = Faker()


# ==========================================================
# Exercise Types
# ==========================================================

EXERCISE_TYPES = [
    "translation",
    "multiple_choice",
    "listening",
    "sentence_order",
    "image_choice",
]


# ==========================================================
# Exercise States
# ==========================================================

EXERCISE_STATES = [
    "unanswered",
    "selected",
    "correct",
    "incorrect",
]


# ==========================================================
# Translation Questions
# ==========================================================

TRANSLATION_QUESTIONS = [
    {
        "prompt":
            "Translate this sentence",

        "question":
            "La mujer bebe agua.",

        "answers": [
            "The woman drinks water.",
            "The woman buys water.",
            "The man drinks water.",
            "The woman drinks coffee.",
        ],

        "correct_index":
            0,
    },
    {
        "prompt":
            "Translate this sentence",

        "question":
            "Yo tengo una hermana.",

        "answers": [
            "I have a sister.",
            "I have a brother.",
            "She has a sister.",
            "I see my sister.",
        ],

        "correct_index":
            0,
    },
    {
        "prompt":
            "Translate this sentence",

        "question":
            "Ellos viven en Madrid.",

        "answers": [
            "They live in Madrid.",
            "We visit Madrid.",
            "They work in Madrid.",
            "He lives in Madrid.",
        ],

        "correct_index":
            0,
    },
]


# ==========================================================
# Multiple Choice Questions
# ==========================================================

MULTIPLE_CHOICE_QUESTIONS = [
    {
        "prompt":
            "Choose the correct meaning",

        "question":
            "biblioteca",

        "answers": [
            "library",
            "school",
            "book",
            "office",
        ],

        "correct_index":
            0,
    },
    {
        "prompt":
            "Choose the correct translation",

        "question":
            "Good morning",

        "answers": [
            "Buenos días",
            "Buenas noches",
            "Gracias",
            "Hasta luego",
        ],

        "correct_index":
            0,
    },
    {
        "prompt":
            "Select the best answer",

        "question":
            "¿Cómo estás?",

        "answers": [
            "Estoy bien.",
            "Me llamo Ana.",
            "Tengo veinte años.",
            "Vivo en Corea.",
        ],

        "correct_index":
            0,
    },
]


# ==========================================================
# Listening Questions
# ==========================================================

LISTENING_QUESTIONS = [
    {
        "prompt":
            "What do you hear?",

        "question":
            "Audio exercise",

        "answers": [
            "Necesito ayuda.",
            "Necesito agua.",
            "Quiero estudiar.",
            "Tengo hambre.",
        ],

        "correct_index":
            0,
    },
    {
        "prompt":
            "Listen and select",

        "question":
            "Audio exercise",

        "answers": [
            "Vamos al mercado.",
            "Vamos a casa.",
            "Vamos a comer.",
            "Vamos mañana.",
        ],

        "correct_index":
            0,
    },
]


# ==========================================================
# Sentence Order Questions
# ==========================================================

SENTENCE_ORDER_QUESTIONS = [
    {
        "prompt":
            "Build the sentence",

        "question":
            "I want to eat an apple.",

        "tokens": [
            "quiero",
            "comer",
            "una",
            "manzana",
        ],
    },
    {
        "prompt":
            "Build the sentence",

        "question":
            "We are going to school.",

        "tokens": [
            "vamos",
            "a",
            "la",
            "escuela",
        ],
    },
    {
        "prompt":
            "Build the sentence",

        "question":
            "She has a new book.",

        "tokens": [
            "ella",
            "tiene",
            "un",
            "libro",
            "nuevo",
        ],
    },
]


# ==========================================================
# Image Choice Words
# ==========================================================

IMAGE_CHOICE_WORDS = [
    "apple",
    "house",
    "dog",
    "book",
    "coffee",
    "train",
]


# ==========================================================
# Standard Answer Generator
# ==========================================================

def generate_standard_answers(
    source: dict,
    state: str,
) -> list[dict]:

    selected_index = None

    if state == "selected":

        selected_index = random.randrange(
            len(
                source["answers"]
            )
        )

    elif state == "correct":

        selected_index = (
            source["correct_index"]
        )

    elif state == "incorrect":

        incorrect_indices = [
            index
            for index
            in range(
                len(
                    source["answers"]
                )
            )
            if index
            != source[
                "correct_index"
            ]
        ]

        selected_index = random.choice(
            incorrect_indices
        )


    answers = []


    for index, text in enumerate(
        source["answers"]
    ):

        selected = (
            index
            == selected_index
        )

        correct = (
            index
            == source[
                "correct_index"
            ]
        )

        if (
            state == "correct"
            and selected
        ):

            answer_state = "correct"

        elif (
            state == "incorrect"
            and selected
        ):

            answer_state = "incorrect"

        elif selected:

            answer_state = "selected"

        else:

            answer_state = "default"


        answers.append(
            {
                "id":
                    f"answer_{index + 1}",

                "text":
                    text,

                "selected":
                    selected,

                "correct":
                    correct,

                "state":
                    answer_state,

                "shortcut":
                    str(
                        index + 1
                    ),
            }
        )


    return answers


# ==========================================================
# Sentence Token Generator
# ==========================================================

def generate_sentence_tokens(
    source: dict,
    state: str,
) -> dict:

    tokens = list(
        source["tokens"]
    )

    shuffled = list(
        tokens
    )

    random.shuffle(
        shuffled
    )


    selected_count = 0

    if state == "selected":

        selected_count = random.randint(
            1,
            max(
                1,
                len(tokens) - 1,
            )
        )

    elif state in {
        "correct",
        "incorrect",
    }:

        selected_count = len(
            tokens
        )


    if state == "correct":

        selected_tokens = list(
            tokens
        )

    elif state == "incorrect":

        selected_tokens = list(
            shuffled
        )

        if (
            selected_tokens
            == tokens
        ):

            selected_tokens.reverse()

    else:

        selected_tokens = (
            shuffled[
                :selected_count
            ]
        )


    available_tokens = list(
        shuffled
    )

    for token in selected_tokens:

        if token in available_tokens:

            available_tokens.remove(
                token
            )


    return {
        "selected_tokens":
            selected_tokens,

        "available_tokens":
            available_tokens,
    }


# ==========================================================
# Image Choice Generator
# ==========================================================

def generate_image_answers(
    state: str,
) -> tuple[list[dict], int]:

    words = random.sample(
        IMAGE_CHOICE_WORDS,
        k=4,
    )

    correct_index = random.randrange(
        len(words)
    )

    selected_index = None

    if state == "selected":

        selected_index = random.randrange(
            len(words)
        )

    elif state == "correct":

        selected_index = correct_index

    elif state == "incorrect":

        choices = [
            index
            for index
            in range(
                len(words)
            )
            if index != correct_index
        ]

        selected_index = random.choice(
            choices
        )


    answers = []


    for index, word in enumerate(
        words
    ):

        selected = (
            index
            == selected_index
        )


        if (
            state == "correct"
            and selected
        ):

            answer_state = "correct"

        elif (
            state == "incorrect"
            and selected
        ):

            answer_state = "incorrect"

        elif selected:

            answer_state = "selected"

        else:

            answer_state = "default"


        answers.append(
            {
                "id":
                    f"image_answer_{index + 1}",

                "label":
                    word.title(),

                "image":
                    get_random_illustration(),

                "state":
                    answer_state,

                "selected":
                    selected,

                "correct":
                    index
                    == correct_index,
            }
        )


    return (
        answers,
        correct_index,
    )


# ==========================================================
# Feedback
# ==========================================================

def generate_feedback(
    state: str,
) -> dict:

    if state == "correct":

        return {
            "visible":
                True,

            "type":
                "correct",

            "title":
                random.choice(
                    [
                        "Excellent!",
                        "Great job!",
                        "Correct!",
                        "Nice work!",
                    ]
                ),

            "message":
                random.choice(
                    [
                        "You're making great progress.",
                        "Keep it going!",
                        "That was the right answer.",
                    ]
                ),

            "icon":
                "check_circle",
        }


    if state == "incorrect":

        return {
            "visible":
                True,

            "type":
                "incorrect",

            "title":
                random.choice(
                    [
                        "Not quite",
                        "Incorrect",
                        "Try again",
                    ]
                ),

            "message":
                random.choice(
                    [
                        "Review the answer and keep practicing.",
                        "Don't worry, you'll get the next one.",
                        "Check the translation carefully.",
                    ]
                ),

            "icon":
                "cancel",
        }


    return {
        "visible":
            False,

        "type":
            None,

        "title":
            None,

        "message":
            None,

        "icon":
            None,
    }


# ==========================================================
# Generate Lesson
# ==========================================================

def generate_lesson_data() -> dict:

    exercise_type = random.choice(
        EXERCISE_TYPES
    )

    state = random.choices(
        EXERCISE_STATES,
        weights=[
            35,
            25,
            22,
            18,
        ],
        k=1,
    )[0]


    current_question = random.randint(
        1,
        9,
    )

    total_questions = random.randint(
        max(
            current_question + 1,
            10,
        ),
        15,
    )


    progress = (
        current_question
        / total_questions
    )


    data = {
        "exercise_type":
            exercise_type,

        "state":
            state,

        "current_question":
            current_question,

        "total_questions":
            total_questions,

        "progress":
            progress,

        "hearts":
            random.randint(
                1,
                5,
            ),

        "xp":
            random.choice(
                [
                    10,
                    15,
                    20,
                    25,
                ]
            ),

        "character":
            get_random_character(),

        "feedback":
            generate_feedback(
                state
            ),

        "answer_button": {
            "label":
                (
                    "CONTINUE"
                    if state
                    in {
                        "correct",
                        "incorrect",
                    }
                    else "CHECK"
                ),

            "enabled":
                state
                != "unanswered",
        },
    }


    # ======================================================
    # Translation
    # ======================================================

    if exercise_type == "translation":

        source = random.choice(
            TRANSLATION_QUESTIONS
        )

        data.update(
            {
                "prompt":
                    source["prompt"],

                "question":
                    source["question"],

                "answers":
                    generate_standard_answers(
                        source,
                        state,
                    ),
            }
        )


    # ======================================================
    # Multiple Choice
    # ======================================================

    elif exercise_type == "multiple_choice":

        source = random.choice(
            MULTIPLE_CHOICE_QUESTIONS
        )

        data.update(
            {
                "prompt":
                    source["prompt"],

                "question":
                    source["question"],

                "answers":
                    generate_standard_answers(
                        source,
                        state,
                    ),
            }
        )


    # ======================================================
    # Listening
    # ======================================================

    elif exercise_type == "listening":

        source = random.choice(
            LISTENING_QUESTIONS
        )

        data.update(
            {
                "prompt":
                    source["prompt"],

                "question":
                    source["question"],

                "answers":
                    generate_standard_answers(
                        source,
                        state,
                    ),

                "audio_speed":
                    random.choice(
                        [
                            "normal",
                            "slow",
                        ]
                    ),
            }
        )


    # ======================================================
    # Sentence Order
    # ======================================================

    elif exercise_type == "sentence_order":

        source = random.choice(
            SENTENCE_ORDER_QUESTIONS
        )

        token_data = (
            generate_sentence_tokens(
                source,
                state,
            )
        )

        data.update(
            {
                "prompt":
                    source["prompt"],

                "question":
                    source["question"],

                **token_data,
            }
        )


    # ======================================================
    # Image Choice
    # ======================================================

    else:

        answers, correct_index = (
            generate_image_answers(
                state
            )
        )

        data.update(
            {
                "prompt":
                    "Which one of these is...",

                "question":
                    answers[
                        correct_index
                    ][
                        "label"
                    ],

                "answers":
                    answers,
            }
        )


    return data