from __future__ import annotations

import random

from faker import Faker


fake = Faker()


# ==========================================================
# States
# ==========================================================

SYSTEM_MONITOR_STATES = [

    "processes",

    "process_selected",

    "process_search",

    "high_cpu",

    "resources",

    "memory_pressure",

    "disk_usage",

    "network_activity",

    "details_menu",

    "kill_process_dialog",

    "force_stop_dialog",
]


# ==========================================================
# Process Names
# ==========================================================

PROCESS_NAMES = [

    "firefox",

    "gnome-shell",

    "nautilus",

    "python3",

    "code",

    "Xorg",

    "NetworkManager",

    "systemd",

    "pipewire",

    "pulseaudio",

    "tracker-miner",

    "bash",

    "terminal",

    "snap-store",

    "dbus-daemon",

    "packagekitd",

    "evolution",

    "chromium",

    "docker",

    "containerd",
]


# ==========================================================
# Process Icons
# ==========================================================

PROCESS_ICONS = {

    "firefox":
        "language",

    "gnome-shell":
        "desktop_windows",

    "nautilus":
        "folder",

    "python3":
        "code",

    "code":
        "data_object",

    "Xorg":
        "monitor",

    "NetworkManager":
        "wifi",

    "systemd":
        "settings",

    "pipewire":
        "graphic_eq",

    "pulseaudio":
        "volume_up",

    "tracker-miner":
        "search",

    "bash":
        "terminal",

    "terminal":
        "terminal",

    "snap-store":
        "shopping_bag",

    "dbus-daemon":
        "hub",

    "packagekitd":
        "package_2",

    "evolution":
        "mail",

    "chromium":
        "public",

    "docker":
        "deployed_code",

    "containerd":
        "deployed_code",
}


# ==========================================================
# Process States
# ==========================================================

PROCESS_STATES = [

    "Running",

    "Sleeping",

    "Waiting",

    "Idle",
]


# ==========================================================
# Storage Devices
# ==========================================================

STORAGE_DEVICES = [

    {
        "name":
            "Ubuntu",

        "mount":
            "/",

        "size_gb":
            256,
    },

    {
        "name":
            "Home",

        "mount":
            "/home",

        "size_gb":
            512,
    },

    {
        "name":
            "Backup",

        "mount":
            "/media/backup",

        "size_gb":
            1000,
    },
]


# ==========================================================
# Helpers
# ==========================================================

def generate_process(
    index: int,
) -> dict:

    name = random.choice(
        PROCESS_NAMES
    )

    cpu = round(
        random.uniform(
            0.0,
            24.0,
        ),
        1,
    )

    memory = round(
        random.uniform(
            20,
            1800,
        ),
        1,
    )

    return {

        "id":
            index,

        "pid":
            random.randint(
                400,
                30000,
            ),

        "name":
            name,

        "icon":
            PROCESS_ICONS.get(
                name,
                "memory",
            ),

        "user":
            random.choice(
                [
                    "user",
                    "root",
                    fake.user_name(),
                ]
            ),

        "cpu":
            cpu,

        "memory":
            memory,

        "state":
            random.choice(
                PROCESS_STATES
            ),

        "selected":
            False,
    }


# ==========================================================
# Processes
# ==========================================================

def generate_processes(
    minimum: int = 12,
    maximum: int = 22,
) -> list[dict]:

    count = random.randint(
        minimum,
        maximum,
    )

    return [

        generate_process(
            index
        )

        for index in range(
            count
        )
    ]


# ==========================================================
# Disk Entries
# ==========================================================

def generate_disks() -> list[dict]:

    entries = []

    for index, device in enumerate(
        STORAGE_DEVICES
    ):

        total = device[
            "size_gb"
        ]

        used = round(
            total
            * random.uniform(
                0.18,
                0.92,
            ),
            1,
        )

        percent = int(
            (
                used
                / total
            )
            * 100
        )

        entries.append(
            {
                "id":
                    index,

                "name":
                    device[
                        "name"
                    ],

                "mount":
                    device[
                        "mount"
                    ],

                "total":
                    total,

                "used":
                    used,

                "available":
                    round(
                        total
                        - used,
                        1,
                    ),

                "percent":
                    percent,
            }
        )

    return entries


# ==========================================================
# Resource Values
# ==========================================================

def generate_resource_values(
    state: str,
) -> dict:

    if state == "high_cpu":

        cpu = random.randint(
            78,
            98,
        )

    else:

        cpu = random.randint(
            8,
            72,
        )


    if state == "memory_pressure":

        memory = random.randint(
            82,
            97,
        )

    else:

        memory = random.randint(
            22,
            76,
        )


    swap = random.randint(
        0,
        48,
    )


    disk = random.randint(
        18,
        86,
    )


    return {

        "cpu_percent":
            cpu,

        "memory_percent":
            memory,

        "swap_percent":
            swap,

        "disk_percent":
            disk,

        "cpu_cores":
            [
                random.randint(
                    2,
                    98,
                )

                for _ in range(
                    random.choice(
                        [
                            4,
                            6,
                            8,
                        ]
                    )
                )
            ],

        "memory_used":
            round(
                random.uniform(
                    3.0,
                    14.0,
                ),
                1,
            ),

        "memory_total":
            16.0,

        "swap_used":
            round(
                random.uniform(
                    0.0,
                    2.0,
                ),
                1,
            ),

        "swap_total":
            4.0,

        "network_down":
            round(
                random.uniform(
                    0.2,
                    86.0,
                ),
                1,
            ),

        "network_up":
            round(
                random.uniform(
                    0.1,
                    24.0,
                ),
                1,
            ),
    }


# ==========================================================
# Main Generator
# ==========================================================

def generate_system_monitor_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            SYSTEM_MONITOR_STATES
        )


    if state not in SYSTEM_MONITOR_STATES:

        raise ValueError(
            f"Unknown System Monitor state: "
            f"{state}"
        )


    # ======================================================
    # Processes
    # ======================================================

    processes = generate_processes()

    selected_process = None


    if state in {
        "process_selected",
        "details_menu",
        "kill_process_dialog",
        "force_stop_dialog",
    }:

        selected_process = random.choice(
            processes
        )

        selected_process[
            "selected"
        ] = True


    # ======================================================
    # High CPU
    # ======================================================

    if state == "high_cpu":

        heavy_process = random.choice(
            processes
        )

        heavy_process[
            "cpu"
        ] = round(
            random.uniform(
                75.0,
                98.0,
            ),
            1,
        )


    # ======================================================
    # Search
    # ======================================================

    search_query = ""

    displayed_processes = processes


    if state == "process_search":

        search_query = random.choice(
            [
                "python",
                "firefox",
                "system",
                "terminal",
                "network",
            ]
        )

        displayed_processes = [

            process

            for process in processes

            if search_query.lower()
            in process[
                "name"
            ].lower()
        ]

        if not displayed_processes:

            displayed_processes = random.sample(
                processes,
                k=min(
                    4,
                    len(
                        processes
                    ),
                ),
            )


    # ======================================================
    # Active Tab
    # ======================================================

    if state in {
        "resources",
        "memory_pressure",
        "high_cpu",
        "network_activity",
    }:

        active_tab = "resources"

    elif state == "disk_usage":

        active_tab = "file_systems"

    else:

        active_tab = "processes"


    # ======================================================
    # Details Menu
    # ======================================================

    details_entries = [

        {
            "label":
                "Stop Process",

            "icon":
                "stop_circle",
        },

        {
            "label":
                "Continue Process",

            "icon":
                "play_circle",
        },

        {
            "label":
                "End Process",

            "icon":
                "cancel",
        },

        {
            "label":
                "Kill Process",

            "icon":
                "dangerous",
        },

        {
            "label":
                "Change Priority",

            "icon":
                "low_priority",
        },

        {
            "label":
                "Properties",

            "icon":
                "info",
        },
    ]


    # ======================================================
    # Result
    # ======================================================

    return {

        "state":
            state,

        "active_tab":
            active_tab,

        "processes":
            processes,

        "displayed_processes":
            displayed_processes,

        "selected_process":
            selected_process,

        "search_visible":
            state
            == "process_search",

        "search_query":
            search_query,

        "resources":
            generate_resource_values(
                state
            ),

        "disks":
            generate_disks(),

        "details_entries":
            details_entries,

        "total_processes":
            len(
                processes
            ),

        "running_processes":
            len(
                [
                    process
                    for process in processes
                    if process[
                        "state"
                    ]
                    == "Running"
                ]
            ),
    }