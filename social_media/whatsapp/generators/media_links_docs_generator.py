import random

from faker import Faker

from social_media.whatsapp.generators.media_generator import (
    get_random_chat_image,
)


fake = Faker()


# ==========================================================
# Helpers
# ==========================================================

def generate_time_label():

    return random.choice(
        [
            "Today",
            "Yesterday",
            "Monday",
            "Tuesday",
            "Friday",
            fake.date(
                pattern="%b %d"
            ),
        ]
    )


def generate_file_size():

    value = random.uniform(
        0.2,
        25.0,
    )

    return f"{value:.1f} MB"


def generate_document_type():

    return random.choice(
        [
            "PDF",
            "DOCX",
            "PPTX",
            "XLSX",
            "TXT",
            "ZIP",
        ]
    )


def generate_document_name(
    file_type,
):

    base = random.choice(
        [
            "report",
            "project",
            "presentation",
            "meeting_notes",
            "research_paper",
            "assignment",
            "proposal",
            "budget",
            "schedule",
            "document",
        ]
    )

    return (
        f"{base}_{random.randint(1, 999)}"
        f".{file_type.lower()}"
    )


# ==========================================================
# Media Item
# ==========================================================

def generate_media_item():

    media_type = random.choices(
        [
            "image",
            "video",
        ],
        weights=[
            0.80,
            0.20,
        ],
        k=1,
    )[0]


    return {

        "type":
            media_type,

        "image":
            get_random_chat_image(),

        "date":
            generate_time_label(),

        "duration":
            (
                f"{random.randint(0, 9)}:"
                f"{random.randint(0, 59):02d}"
                if media_type == "video"
                else None
            ),
    }


# ==========================================================
# Link Item
# ==========================================================

def generate_link_item():

    has_preview = (
        random.random() < 0.75
    )


    domain = random.choice(
        [
            "github.com",
            "youtube.com",
            "medium.com",
            "arxiv.org",
            "google.com",
            "wikipedia.org",
            "stackoverflow.com",
            "example.com",
        ]
    )


    return {

        "title":
            fake.sentence(
                nb_words=random.randint(
                    4,
                    9,
                )
            ),

        "domain":
            domain,

        "url_text":
            f"https://{domain}/"
            f"{fake.slug()}",

        "preview_image":
            (
                get_random_chat_image()
                if has_preview
                else None
            ),

        "time":
            generate_time_label(),

        "sender":
            fake.name(),
    }


# ==========================================================
# Document Item
# ==========================================================

def generate_document_item():

    file_type = (
        generate_document_type()
    )


    return {

        "name":
            generate_document_name(
                file_type
            ),

        "file_type":
            file_type,

        "size":
            generate_file_size(),

        "time":
            generate_time_label(),

        "sender":
            fake.name(),
    }


# ==========================================================
# Page Generator
# ==========================================================

def generate_media_links_docs_page(
    min_media=9,
    max_media=24,
    min_links=4,
    max_links=10,
    min_docs=4,
    max_docs=10,
):

    active_tab = random.choice(
        [
            "media",
            "links",
            "docs",
        ]
    )


    media_count = random.randint(
        min_media,
        max_media,
    )

    link_count = random.randint(
        min_links,
        max_links,
    )

    doc_count = random.randint(
        min_docs,
        max_docs,
    )


    media = [

        generate_media_item()

        for _ in range(
            media_count
        )
    ]


    links = [

        generate_link_item()

        for _ in range(
            link_count
        )
    ]


    documents = [

        generate_document_item()

        for _ in range(
            doc_count
        )
    ]


    return {

        "title":
            "Media, links and docs",

        "active_tab":
            active_tab,

        "tabs":
            [
                {
                    "id":
                        "media",

                    "label":
                        "Media",

                    "count":
                        media_count,
                },
                {
                    "id":
                        "links",

                    "label":
                        "Links",

                    "count":
                        link_count,
                },
                {
                    "id":
                        "docs",

                    "label":
                        "Docs",

                    "count":
                        doc_count,
                },
            ],

        "media":
            media,

        "links":
            links,

        "documents":
            documents,

        "media_count":
            media_count,

        "link_count":
            link_count,

        "document_count":
            doc_count,
    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    page = (
        generate_media_links_docs_page()
    )


    print(
        "\nMEDIA / LINKS / DOCS PAGE"
    )

    print(
        "Active tab:",
        page["active_tab"]
    )

    print(
        "Media:",
        page["media_count"]
    )

    print(
        "Links:",
        page["link_count"]
    )

    print(
        "Documents:",
        page["document_count"]
    )


    print(
        "\nMEDIA SAMPLE:"
    )

    for item in page["media"][:3]:

        print(
            item
        )


    print(
        "\nLINK SAMPLE:"
    )

    for item in page["links"][:2]:

        print(
            item
        )


    print(
        "\nDOCUMENT SAMPLE:"
    )

    for item in page["documents"][:2]:

        print(
            item
        )