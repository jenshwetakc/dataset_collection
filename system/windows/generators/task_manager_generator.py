from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

TASK_MANAGER_STATES = [
    "processes",
    "performance_cpu",
    "performance_memory",
    "performance_disk",
    "performance_gpu",
    "app_history",
    "startup_apps",
    "users",
    "details",
    "services",
    "end_task_dialog",
]


# ==========================================================
# Process Pool
# ==========================================================

PROCESS_POOL = [
    {
        "name": "File Explorer",
        "icon": "folder",
        "type": "Apps",
    },
    {
        "name": "Browser",
        "icon": "public",
        "type": "Apps",
    },
    {
        "name": "Settings",
        "icon": "settings",
        "type": "Apps",
    },
    {
        "name": "Terminal",
        "icon": "terminal",
        "type": "Apps",
    },
    {
        "name": "Photos",
        "icon": "photo_library",
        "type": "Apps",
    },
    {
        "name": "Desktop Window Manager",
        "icon": "window",
        "type": "Windows processes",
    },
    {
        "name": "Service Host",
        "icon": "memory",
        "type": "Background processes",
    },
    {
        "name": "Runtime Broker",
        "icon": "settings",
        "type": "Background processes",
    },
    {
        "name": "Windows Search",
        "icon": "search",
        "type": "Windows processes",
    },
]


# ==========================================================
# Startup Pool
# ==========================================================

STARTUP_POOL = [
    {
        "name": "Cloud Sync",
        "icon": "cloud",
        "publisher": "System",
    },
    {
        "name": "Chat",
        "icon": "chat",
        "publisher": "Microsoft",
    },
    {
        "name": "Music",
        "icon": "music_note",
        "publisher": "Media Apps",
    },
    {
        "name": "Terminal",
        "icon": "terminal",
        "publisher": "System",
    },
    {
        "name": "Security",
        "icon": "security",
        "publisher": "Windows",
    },
]


# ==========================================================
# Services
# ==========================================================

SERVICE_POOL = [
    {
        "name": "AudioSrv",
        "description": "Windows Audio",
    },
    {
        "name": "BITS",
        "description": "Background Intelligent Transfer Service",
    },
    {
        "name": "Dhcp",
        "description": "DHCP Client",
    },
    {
        "name": "Dnscache",
        "description": "DNS Client",
    },
    {
        "name": "EventLog",
        "description": "Windows Event Log",
    },
    {
        "name": "Spooler",
        "description": "Print Spooler",
    },
]


# ==========================================================
# Navigation
# ==========================================================

TASK_MANAGER_NAV = [
    {
        "id": "processes",
        "label": "Processes",
        "icon": "apps",
    },
    {
        "id": "performance",
        "label": "Performance",
        "icon": "monitoring",
    },
    {
        "id": "app_history",
        "label": "App history",
        "icon": "history",
    },
    {
        "id": "startup_apps",
        "label": "Startup apps",
        "icon": "rocket_launch",
    },
    {
        "id": "users",
        "label": "Users",
        "icon": "group",
    },
    {
        "id": "details",
        "label": "Details",
        "icon": "list",
    },
    {
        "id": "services",
        "label": "Services",
        "icon": "settings_suggest",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_processes() -> list[dict]:

    count = random.randint(
        6,
        len(PROCESS_POOL),
    )

    processes = []

    for process in random.sample(
        PROCESS_POOL,
        k=count,
    ):

        processes.append(
            {
                **process,

                "cpu":
                    round(
                        random.uniform(
                            0.0,
                            24.0,
                        ),
                        1,
                    ),

                "memory":
                    random.randint(
                        20,
                        1400,
                    ),

                "disk":
                    round(
                        random.uniform(
                            0.0,
                            8.0,
                        ),
                        1,
                    ),

                "network":
                    round(
                        random.uniform(
                            0.0,
                            4.0,
                        ),
                        1,
                    ),

                "selected":
                    False,
            }
        )

    return processes


def generate_performance_points(
    count: int = 36,
) -> list[int]:

    current = random.randint(
        15,
        75,
    )

    values = []

    for _ in range(count):

        current += random.randint(
            -12,
            12,
        )

        current = max(
            2,
            min(
                98,
                current,
            ),
        )

        values.append(
            current
        )

    return values


def generate_startup_apps() -> list[dict]:

    return [
        {
            **app,

            "status":
                random.choice(
                    [
                        "Enabled",
                        "Disabled",
                    ]
                ),

            "impact":
                random.choice(
                    [
                        "Low",
                        "Medium",
                        "High",
                        "Not measured",
                    ]
                ),
        }
        for app in STARTUP_POOL
    ]


def generate_services() -> list[dict]:

    return [
        {
            **service,

            "status":
                random.choice(
                    [
                        "Running",
                        "Stopped",
                    ]
                ),

            "pid":
                random.randint(
                    700,
                    12000,
                ),
        }
        for service in SERVICE_POOL
    ]


# ==========================================================
# Main Generator
# ==========================================================

def generate_task_manager_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            TASK_MANAGER_STATES
        )


    if state not in TASK_MANAGER_STATES:

        raise ValueError(
            f"Unknown Task Manager state: {state}"
        )


    processes = generate_processes()


    selected_process = None


    if state == "end_task_dialog":

        index = random.randrange(
            len(processes)
        )

        processes[
            index
        ]["selected"] = True

        selected_process = (
            processes[
                index
            ]
        )


    performance_type = None


    if state.startswith(
        "performance_"
    ):

        performance_type = (
            state.replace(
                "performance_",
                "",
            )
        )


    return {
        "state":
            state,

        "navigation":
            TASK_MANAGER_NAV,

        "processes":
            processes,

        "selected_process":
            selected_process,

        "performance_type":
            performance_type,

        "performance": {
            "cpu": {
                "label":
                    "CPU",

                "value":
                    random.randint(
                        12,
                        88,
                    ),

                "subtitle":
                    random.choice(
                        [
                            "3.40 GHz",
                            "4.10 GHz",
                            "2.80 GHz",
                        ]
                    ),

                "points":
                    generate_performance_points(),
            },

            "memory": {
                "label":
                    "Memory",

                "value":
                    random.randint(
                        30,
                        92,
                    ),

                "subtitle":
                    random.choice(
                        [
                            "10.8 / 16.0 GB",
                            "22.4 / 32.0 GB",
                            "6.7 / 8.0 GB",
                        ]
                    ),

                "points":
                    generate_performance_points(),
            },

            "disk": {
                "label":
                    "Disk 0",

                "value":
                    random.randint(
                        1,
                        100,
                    ),

                "subtitle":
                    "SSD",

                "points":
                    generate_performance_points(),
            },

            "gpu": {
                "label":
                    "GPU 0",

                "value":
                    random.randint(
                        3,
                        98,
                    ),

                "subtitle":
                    random.choice(
                        [
                            "NVIDIA GPU",
                            "Intel Graphics",
                            "AMD Graphics",
                        ]
                    ),

                "points":
                    generate_performance_points(),
            },
        },

        "startup_apps":
            generate_startup_apps(),

        "users": [
            {
                "name":
                    "User",

                "status":
                    "Active",

                "cpu":
                    random.randint(
                        2,
                        35,
                    ),

                "memory":
                    random.randint(
                        800,
                        6400,
                    ),
            },
            {
                "name":
                    "Guest",

                "status":
                    random.choice(
                        [
                            "Disconnected",
                            "Active",
                        ]
                    ),

                "cpu":
                    random.randint(
                        0,
                        8,
                    ),

                "memory":
                    random.randint(
                        120,
                        900,
                    ),
            },
        ],

        "services":
            generate_services(),
    }