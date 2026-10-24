from __future__ import annotations
import random
from datetime import datetime, timedelta
from faker import Faker

DRIVE_STATES = ["my_drive_grid","my_drive_list","folder_open","search_results",
                "file_preview","shared_with_me","starred","trash","new_menu",
                "upload_dialog","file_context_menu"]

KINDS = [("document","📄","#4285f4",".docx"),("spreadsheet","📊","#0f9d58",".xlsx"),
         ("presentation","▣","#f4b400",".pptx"),("pdf","PDF","#db4437",".pdf"),
         ("image","▧","#7e57c2",".png"),("video","▶","#e8710a",".mp4")]

def generate_drive_page(state: str | None = None, seed: int | None = None) -> dict:
    state = state or random.choice(DRIVE_STATES)
    if state not in DRIVE_STATES:
        raise ValueError(f"Unknown state: {state}")
    seed = seed if seed is not None else random.randint(0, 2**31 - 1)
    random.seed(seed); fake = Faker(); fake.seed_instance(seed)

    files = []
    for index in range(random.randint(14, 26)):
        kind, symbol, color, extension = random.choice(KINDS)
        files.append({
            "id": f"file_{index}", "kind": kind, "symbol": symbol, "color": color,
            "name": fake.catch_phrase().replace(" ", "_").lower() + extension,
            "owner": fake.name(), "shared": random.random() < .35,
            "starred": random.random() < .25,
            "modified": (datetime.now() - timedelta(days=random.randint(0, 120))).strftime("%b %d, %Y"),
            "size": f"{random.randint(10, 900)} {random.choice(['KB', 'MB'])}",
            "thumb": random.choice(["#d2e3fc","#ceead6","#fce8e6","#fef7e0"]),
        })

    folders = [{"id": f"folder_{i}", "name": name, "shared": random.random() < .3}
               for i, name in enumerate(random.sample(
                   ["Research","Coursework","Project assets","Team documents",
                    "Travel plans","Design drafts"], k=5))]

    selected = random.choice(files)
    query = random.choice(["research", "proposal", "meeting", "project"])

    return {
        "state": state, "seed": seed,
        "title": {"folder_open": folders[0]["name"], "search_results": f"Search results for “{query}”",
                  "file_preview": selected["name"], "shared_with_me": "Shared with me",
                  "starred": "Starred", "trash": "Trash"}.get(state, "My Drive"),
        "view_mode": "list" if state == "my_drive_list" else "grid",
        "files": files, "folders": folders, "selected_file": selected, "search_query": query,
        "navigation": [("my_drive","My Drive","▰"),("computers","Computers","▣"),
                       ("shared","Shared with me","♟"),("recent","Recent","◷"),
                       ("starred","Starred","☆"),("trash","Trash","♲")],
        "new_menu": ["New folder","File upload","Folder upload","Google Docs","Google Sheets","Google Slides"],
        "context_menu": ["Open with","Share","Get link","Rename","Download","Move to trash"],
        "upload": {"file_name": selected["name"], "progress": random.randint(15, 92)},
    }