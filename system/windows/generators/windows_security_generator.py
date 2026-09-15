from __future__ import annotations

import random


# ==========================================================
# States
# ==========================================================

WINDOWS_SECURITY_STATES = [
    "home",
    "virus_protection",
    "quick_scan",
    "scan_in_progress",
    "threat_found",
    "protection_history",
    "firewall",
    "app_browser_control",
    "device_security",
    "account_protection",
    "security_settings",
    "threat_action_dialog",
]


# ==========================================================
# Navigation
# ==========================================================

SECURITY_NAVIGATION = [
    {
        "id": "home",
        "label": "Home",
        "icon": "home",
    },
    {
        "id": "virus_protection",
        "label": "Virus & threat protection",
        "icon": "security",
    },
    {
        "id": "account_protection",
        "label": "Account protection",
        "icon": "person",
    },
    {
        "id": "firewall",
        "label": "Firewall & network protection",
        "icon": "network_check",
    },
    {
        "id": "app_browser_control",
        "label": "App & browser control",
        "icon": "verified_user",
    },
    {
        "id": "device_security",
        "label": "Device security",
        "icon": "shield",
    },
]


# ==========================================================
# Home Areas
# ==========================================================

HOME_SECURITY_AREAS = [
    {
        "title": "Virus & threat protection",
        "subtitle": "No current threats",
        "icon": "security",
    },
    {
        "title": "Account protection",
        "subtitle": "No action needed",
        "icon": "person",
    },
    {
        "title": "Firewall & network protection",
        "subtitle": "Firewall is on",
        "icon": "network_check",
    },
    {
        "title": "App & browser control",
        "subtitle": "No action needed",
        "icon": "verified_user",
    },
    {
        "title": "Device security",
        "subtitle": "Security processor is ready",
        "icon": "shield",
    },
]


# ==========================================================
# Threat Pool
# ==========================================================

THREAT_POOL = [
    {
        "name": "Potentially unwanted app",
        "severity": "Low",
        "status": "Quarantined",
    },
    {
        "name": "Suspicious script",
        "severity": "Medium",
        "status": "Blocked",
    },
    {
        "name": "Trojan:Demo/TestThreat",
        "severity": "Severe",
        "status": "Active",
    },
]


# ==========================================================
# Protection History
# ==========================================================

HISTORY_POOL = [
    {
        "title": "Threat blocked",
        "detail": "A potentially unwanted app was blocked.",
        "time": "Today",
        "icon": "block",
    },
    {
        "title": "Threat quarantined",
        "detail": "A suspicious file was moved to quarantine.",
        "time": "Yesterday",
        "icon": "inventory_2",
    },
    {
        "title": "Scan completed",
        "detail": "Quick scan completed successfully.",
        "time": "2 days ago",
        "icon": "task_alt",
    },
    {
        "title": "Security settings changed",
        "detail": "Real-time protection was updated.",
        "time": "Last week",
        "icon": "settings",
    },
]


# ==========================================================
# Helpers
# ==========================================================

def random_toggle(
    probability: float = 0.80,
) -> bool:

    return (
        random.random()
        < probability
    )


def generate_scan_stats() -> dict:

    return {
        "files_scanned":
            random.randint(
                9000,
                85000,
            ),

        "elapsed":
            random.choice(
                [
                    "00:01:21",
                    "00:03:42",
                    "00:08:15",
                ]
            ),

        "remaining":
            random.choice(
                [
                    "About 1 minute",
                    "About 3 minutes",
                    "About 5 minutes",
                ]
            ),
    }


# ==========================================================
# Home
# ==========================================================

def generate_home_data() -> dict:

    areas = []

    for item in HOME_SECURITY_AREAS:

        warning = (
            random.random()
            < 0.16
        )

        areas.append(
            {
                **item,

                "warning":
                    warning,

                "subtitle":
                    (
                        random.choice(
                            [
                                "Action recommended",
                                "Review settings",
                            ]
                        )
                        if warning
                        else item["subtitle"]
                    ),
            }
        )

    return {
        "areas":
            areas,
    }


# ==========================================================
# Virus Protection
# ==========================================================

def generate_virus_data(
    state: str,
) -> dict:

    progress = None

    threat = None


    if state == "scan_in_progress":

        progress = random.randint(
            8,
            88,
        )


    if state in {
        "threat_found",
        "threat_action_dialog",
    }:

        threat = random.choice(
            THREAT_POOL
        )


    return {
        "last_scan":
            random.choice(
                [
                    "Today at 3:18 PM",
                    "Yesterday at 9:32 PM",
                    "September 3, 2026 at 11:04 AM",
                ]
            ),

        "scan_type":
            random.choice(
                [
                    "Quick scan",
                    "Full scan",
                ]
            ),

        "progress":
            progress,

        "stats":
            generate_scan_stats(),

        "threat":
            threat,

        "real_time":
            random_toggle(
                0.92
            ),

        "cloud":
            random_toggle(
                0.88
            ),

        "sample_submission":
            random_toggle(
                0.85
            ),

        "tamper":
            random_toggle(
                0.95
            ),
    }


# ==========================================================
# Firewall
# ==========================================================

def generate_firewall_data() -> dict:

    return {
        "networks": [
            {
                "name": "Domain network",
                "status": random.choice(
                    [
                        "Not connected",
                        "Connected",
                    ]
                ),
                "firewall": True,
                "icon": "domain",
            },
            {
                "name": "Private network",
                "status": "Connected",
                "firewall": random_toggle(
                    0.96
                ),
                "icon": "home",
            },
            {
                "name": "Public network",
                "status": "Not connected",
                "firewall": random_toggle(
                    0.94
                ),
                "icon": "public",
            },
        ],
    }


# ==========================================================
# App / Browser
# ==========================================================

def generate_app_browser_data() -> dict:

    return {
        "items": [
            {
                "title": "Reputation-based protection",
                "subtitle": "Protect your device from malicious apps and files",
                "icon": "verified",
                "enabled": random_toggle(
                    0.90
                ),
            },
            {
                "title": "Exploit protection",
                "subtitle": "Protect your device against attacks",
                "icon": "security",
                "enabled": random_toggle(
                    0.95
                ),
            },
            {
                "title": "Smart App Control",
                "subtitle": "Block untrusted or potentially dangerous apps",
                "icon": "shield",
                "enabled": random_toggle(
                    0.75
                ),
            },
        ],
    }


# ==========================================================
# Device Security
# ==========================================================

def generate_device_security_data() -> dict:

    return {
        "items": [
            {
                "title": "Core isolation",
                "subtitle": "Memory integrity and virtualization security",
                "icon": "memory",
                "status": random.choice(
                    [
                        "On",
                        "On",
                        "Off",
                    ]
                ),
            },
            {
                "title": "Security processor",
                "subtitle": "TPM security processor",
                "icon": "developer_board",
                "status": "Ready",
            },
            {
                "title": "Secure boot",
                "subtitle": "Helps prevent malicious software during startup",
                "icon": "lock",
                "status": random.choice(
                    [
                        "On",
                        "On",
                        "Off",
                    ]
                ),
            },
        ],
    }


# ==========================================================
# Account Protection
# ==========================================================

def generate_account_data() -> dict:

    return {
        "user":
            random.choice(
                [
                    "Shweta",
                    "Alex Kim",
                    "Jordan Lee",
                ]
            ),

        "items": [
            {
                "title": "Microsoft account",
                "subtitle": "Account security is up to date",
                "icon": "account_circle",
                "status": "Good",
            },
            {
                "title": "Windows Hello",
                "subtitle": "Sign in securely with PIN or biometrics",
                "icon": "fingerprint",
                "status": random.choice(
                    [
                        "Set up",
                        "Available",
                    ]
                ),
            },
            {
                "title": "Dynamic lock",
                "subtitle": "Lock your PC when you are away",
                "icon": "lock_person",
                "status": random.choice(
                    [
                        "On",
                        "Off",
                    ]
                ),
            },
        ],
    }


# ==========================================================
# Protection History
# ==========================================================

def generate_history() -> list[dict]:

    count = random.randint(
        3,
        len(HISTORY_POOL),
    )

    return random.sample(
        HISTORY_POOL,
        k=count,
    )


# ==========================================================
# Main Generator
# ==========================================================

def generate_windows_security_data(
    state: str | None = None,
) -> dict:

    if state is None:

        state = random.choice(
            WINDOWS_SECURITY_STATES
        )


    if state not in WINDOWS_SECURITY_STATES:

        raise ValueError(
            f"Unknown Windows Security state: {state}"
        )


    active_nav = state


    if state in {
        "quick_scan",
        "scan_in_progress",
        "threat_found",
        "protection_history",
        "security_settings",
        "threat_action_dialog",
    }:

        active_nav = (
            "virus_protection"
        )


    return {
        "state":
            state,

        "active_nav":
            active_nav,

        "navigation":
            SECURITY_NAVIGATION,

        "home":
            generate_home_data(),

        "virus":
            generate_virus_data(
                state
            ),

        "history":
            generate_history(),

        "firewall":
            generate_firewall_data(),

        "app_browser":
            generate_app_browser_data(),

        "device_security":
            generate_device_security_data(),

        "account":
            generate_account_data(),
    }