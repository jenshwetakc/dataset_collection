from __future__ import annotations

import random

from faker import Faker


fake = Faker()


CLASSROOM_STATES = [
    "dashboard_grid",
    "class_stream",
    "classwork",
    "people",
    "assignment_detail",
    "search_results",
    "create_class_dialog",
    "join_class_dialog",
]


CLASS_COLORS = [
    "#6b5cb8",
    "#1976d2",
    "#00897b",
    "#c0582c",
    "#9c3d75",
    "#4f6f3b",
]


SUBJECTS = [
    "Machine Learning",
    "Human-Computer Interaction",
    "Software Engineering",
    "Data Structures",
    "Computer Vision",
    "Natural Language Processing",
    "Web Programming",
]


def initials(
    name: str,
) -> str:

    return "".join(
        word[0].upper()
        for word in name.split()[:2]
    )


def generate_assignment(
    index: int,
) -> dict:

    assignment_type = random.choice(
        [
            "Assignment",
            "Quiz assignment",
            "Material",
            "Question",
        ]
    )

    return {
        "id":
            f"assignment_{index:03d}",

        "title":
            fake.sentence(
                nb_words=random.randint(3, 7),
            ).rstrip("."),

        "type":
            assignment_type,

        "due":
            random.choice(
                [
                    "Due today",
                    "Due tomorrow",
                    "Due Friday",
                    "Due Oct 4",
                    "No due date",
                ]
            ),

        "points":
            random.choice(
                [10, 20, 50, 100],
            ),

        "description":
            fake.paragraph(
                nb_sentences=3,
            ),

        "submitted":
            random.randint(4, 26),

        "total_students":
            random.randint(20, 34),
    }


def generate_course(
    index: int,
) -> dict:

    teacher = fake.name()

    return {
        "id":
            f"course_{index:03d}",

        "name":
            random.choice(
                SUBJECTS
            ),

        "section":
            f"Section {random.randint(1, 4)}",

        "room":
            f"Room {random.randint(101, 542)}",

        "teacher":
            teacher,

        "teacher_initials":
            initials(teacher),

        "color":
            random.choice(
                CLASS_COLORS
            ),

        "code":
            fake.bothify(
                text="???-####",
            ).lower(),
    }


def generate_person(
    index: int,
) -> dict:

    name = fake.name()

    return {
        "id":
            f"person_{index:03d}",

        "name":
            name,

        "email":
            fake.email(),

        "initials":
            initials(name),

        "color":
            random.choice(
                CLASS_COLORS
            ),
    }


def generate_classroom_page(
    state: str | None = None,
) -> dict:

    state = (
        state
        or random.choice(
            CLASSROOM_STATES
        )
    )

    courses = [
        generate_course(index)
        for index in range(
            random.randint(5, 8)
        )
    ]

    selected_course = random.choice(
        courses
    )

    assignments = [
        generate_assignment(index)
        for index in range(
            random.randint(5, 9)
        )
    ]

    selected_assignment = random.choice(
        assignments
    )

    teachers = [
        generate_person(index)
        for index in range(2)
    ]

    students = [
        generate_person(index + 10)
        for index in range(
            random.randint(12, 22)
        )
    ]

    announcements = [
        {
            "id":
                f"announcement_{index:03d}",

            "author":
                selected_course["teacher"],

            "initials":
                selected_course[
                    "teacher_initials"
                ],

            "color":
                selected_course["color"],

            "text":
                fake.paragraph(
                    nb_sentences=2,
                ),

            "time":
                random.choice(
                    [
                        "Posted today",
                        "Posted yesterday",
                        "Posted Sep 24",
                    ]
                ),
        }
        for index in range(
            random.randint(2, 5)
        )
    ]

    search_query = random.choice(
        [
            selected_course["name"],
            fake.word(),
            "assignment",
            "project",
        ]
    )

    return {
        "app_name":
            "Google Classroom",

        "state":
            state,

        "courses":
            courses,

        "selected_course":
            selected_course,

        "assignments":
            assignments,

        "selected_assignment":
            selected_assignment,

        "teachers":
            teachers,

        "students":
            students,

        "announcements":
            announcements,

        "search_query":
            search_query,
    }