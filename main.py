import argparse
import json
import os
import sys
import time
from datetime import datetime

import requests
from dotenv import load_dotenv
from colorama import Fore, Style, init

init(autoreset=True)

# ─────────────────────────────────────────────
# CLI ARGUMENTS
# ─────────────────────────────────────────────
parser = argparse.ArgumentParser(
    description="✨ InternYet Internship Diary Tool"
)

parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Validate and print payloads without submitting"
)

parser.add_argument(
    "--fetch-only",
    action="store_true",
    help="Only fetch and backup existing portal entries"
)

parser.add_argument(
    "--internship-id",
    type=int,
    help="Internship ID to use for diary submission"
)

parser.add_argument(
    "--discover-internships",
    action="store_true",
    help="List available internships from your account and exit"
)

parser.add_argument(
    "--select-internship",
    action="store_true",
    help="Interactively select internship from discovered internships"
)

args = parser.parse_args()
DRY_RUN = args.dry_run
FETCH_ONLY = args.fetch_only
CLI_INTERNSHIP_ID = args.internship_id
DISCOVER_INTERNSHIPS = args.discover_internships
SELECT_INTERNSHIP = args.select_internship

START_TIME = time.time()

# ─────────────────────────────────────────────
# ENV SETUP
# ─────────────────────────────────────────────
load_dotenv()

EMAIL = os.getenv("INTERNYET_EMAIL")
PASSWORD = os.getenv("INTERNYET_PASSWORD")
ENV_INTERNSHIP_ID = os.getenv("INTERNYET_INTERNSHIP_ID")

if not DRY_RUN and not FETCH_ONLY:
    if not EMAIL or not PASSWORD:
        raise RuntimeError("❌ Missing INTERNYET_EMAIL or INTERNYET_PASSWORD in .env")

# ─────────────────────────────────────────────
# SESSION SETUP
# ─────────────────────────────────────────────
session = requests.Session()

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Origin": "https://vtu.internyet.in",
    "Referer": "https://vtu.internyet.in/",
}

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
LOGIN_URL = "https://vtuapi.internyet.in/api/v1/auth/login"
FETCH_URL = "https://vtuapi.internyet.in/api/v1/student/internship-diaries"
SUBMIT_URL = FETCH_URL + "/store"
INTERNSHIP_APPLYS_URL = "https://vtuapi.internyet.in/api/v1/student/internship-applys"
REQUEST_DELAY = 5
MAX_RETRIES = 3
TIMEOUT = 15

# ─────────────────────────────────────────────
# FULL SKILL LOOKUP (KEEP COMPLETE)
# ─────────────────────────────────────────────
SKILL_LOOKUP = {
    "3D PRINTING CONCEPTS, DESIGN AND PRINTING": 85,
    "Android Studio": 61,
    "Angular": 32,
    "AWS": 12,
    "Azure": 13,
    "BIM CONCEPTS WITH MEP AND PRODUCT DESIGN": 84,
    "BIM FOR ARCHITECTURE": 78,
    "BIM FOR CONSTRUCTION": 77,
    "BIM FOR HIGHWAY ENGINEERING": 81,
    "BIM FOR STRUCTURES": 80,
    "C++": 11,
    "CakePHP": 5,
    "Cassandra": 23,
    "Circuit Design": 68,
    "Cloud access control": 40,
    "CodeIgniter": 36,
    "computer vision": 27,
    "CSS": 30,
    "D3.js": 56,
    "Data encryption": 41,
    "Data modeling": 44,
    "Data visualization": 16,
    "Database design": 19,
    "Design with FPGA": 72,
    "DevOps": 24,
    "DHCP": 47,
    "Digital Design": 71,
    "Docker": 65,
    "Embedded Systems": 75,
    "FilamentPHP": 8,
    "Firewall configuration": 50,
    "Flutter": 7,
    "Git": 63,
    "Google Cloud": 14,
    "HTML": 29,
    "IaaS": 37,
    "Indexing": 45,
    "Intelligent Machines": 76,
    "INTERIOR AND EXTERIOR DESIGN": 79,
    "IoT": 74,
    "Java": 10,
    "JavaScript": 1,
    "Keras": 51,
    "Kotlin": 62,
    "Kubernetes": 64,
    "LAN": 48,
    "Laravel": 4,
    "Layout Design": 69,
    "Machine learning": 15,
    "Manufacturing": 86,
    "MongoDB": 22,
    "MySQL": 42,
    "Natural language processing": 28,
    "Network architecture": 18,
    "Node.js": 34,
    "NoSQL": 21,
    "Objective-C": 59,
    "PaaS": 38,
    "PHP": 2,
    "Physical Design": 70,
    "PostgreSQL": 43,
    "Power BI": 55,
    "PRODUCT DESIGN & 3D PRINTING": 82,
    "PRODUCT DESIGN & MANUFACTURING": 83,
    "Python": 3,
    "PyTorch": 26,
    "React": 31,
    "React.js": 9,
    "Ruby on Rails": 35,
    "SaaS": 39,
    "scikit-learn": 53,
    "SQL": 20,
    "Statistical analysis": 17,
    "Swift": 58,
    "Tableau": 54,
    "TCP/IP": 46,
    "TensorFlow": 25,
    "TypeScript": 66,
    "Verification & Validations": 73,
    "VLSI Design": 67,
    "VPNs": 52,
    "Vue.js": 33,
    "WAN": 49,
    "WordPress": 6,
    "Xamarin": 57,
    "Xcode": 60,
}

# ─────────────────────────────────────────────
# UI HELPERS
# ─────────────────────────────────────────────
def banner():
    print(Fore.CYAN + Style.BRIGHT + "\n🚀 InternYet Diary Tool\n")


def success(msg):
    print(Fore.GREEN + f"✅ {msg}")


def warn(msg):
    print(Fore.YELLOW + f"⚠ {msg}")


def error(msg):
    print(Fore.RED + f"❌ {msg}")


# ─────────────────────────────────────────────
# BACKUP FUNCTION
# ─────────────────────────────────────────────
def save_existing_entries(entries):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"existing_entries_{ts}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    success(f"Backup saved → {filename}")


# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
def login():
    if DRY_RUN:
        warn("Dry-run mode: login skipped")
        return

    print(Fore.YELLOW + "⏳ Logging in...")

    r = session.post(
        LOGIN_URL,
        json={"email": EMAIL, "password": PASSWORD},
        headers=HEADERS,
        timeout=TIMEOUT,
    )

    if r.status_code != 200:
        raise RuntimeError(f"Login failed: {r.status_code} → {r.text}")

    success("Logged in successfully")


# ─────────────────────────────────────────────
# FETCH EXISTING ENTRIES
# ─────────────────────────────────────────────
def fetch_existing_entries():
    print(Fore.YELLOW + "⏳ Fetching existing portal entries...")

    page = 1
    all_entries = []

    while True:
        r = session.get(
            FETCH_URL,
            headers=HEADERS,
            params={"page": page},
            timeout=TIMEOUT,
        )

        if r.status_code != 200:
            raise RuntimeError("Failed to fetch entries")

        data_block = r.json().get("data", {})
        entries = data_block.get("data", [])
        last_page = data_block.get("last_page", page)

        all_entries.extend(entries)

        if page >= last_page:
            break

        page += 1
        time.sleep(0.5)

    success(f"Fetched {len(all_entries)} existing entries")
    return all_entries


# ─────────────────────────────────────────────
# FETCH INTERNSHIPS
# ─────────────────────────────────────────────
def fetch_internships():
    print(Fore.YELLOW + "⏳ Discovering internships...")

    page = 1
    internships = []

    while True:
        r = session.get(
            INTERNSHIP_APPLYS_URL,
            headers=HEADERS,
            params={"page": page},
            timeout=TIMEOUT,
        )

        if r.status_code != 200:
            raise RuntimeError("Failed to fetch internships")

        data_block = r.json().get("data", {})
        apply_records = data_block.get("data", [])
        last_page = data_block.get("last_page", page)

        for apply_record in apply_records:
            internship_id = apply_record.get("internship_id")
            details = apply_record.get("internship_details") or {}
            internship_name = details.get("name", "Unknown internship")

            if internship_id is not None:
                internships.append({"id": internship_id, "name": internship_name})

        if page >= last_page:
            break

        page += 1
        time.sleep(0.5)

    unique = {}
    for internship in internships:
        unique[internship["id"]] = internship["name"]

    resolved = [{"id": key, "name": value} for key, value in unique.items()]
    resolved.sort(key=lambda item: item["id"])

    success(f"Discovered {len(resolved)} internships")
    return resolved


def print_internships(internships):
    print(Fore.CYAN + "\n🎯 Available internships:\n")
    for internship in internships:
        print(f"  - {internship['id']} → {internship['name']}")


def select_internship(internships):
    print_internships(internships)
    selected = input(Fore.MAGENTA + "\nEnter internship ID: ").strip()

    try:
        selected_id = int(selected)
    except ValueError as exc:
        raise ValueError("Invalid internship ID. Enter a numeric value.") from exc

    valid_ids = {i["id"] for i in internships}
    if selected_id not in valid_ids:
        raise ValueError(f"Internship ID {selected_id} not found in discovered list.")

    return selected_id


def resolve_internship_id():
    if CLI_INTERNSHIP_ID is not None:
        success(f"Using internship ID from CLI: {CLI_INTERNSHIP_ID}")
        return CLI_INTERNSHIP_ID

    if ENV_INTERNSHIP_ID:
        try:
            env_id = int(ENV_INTERNSHIP_ID)
        except ValueError as exc:
            raise ValueError("INTERNYET_INTERNSHIP_ID must be numeric.") from exc
        success(f"Using internship ID from .env: {env_id}")
        return env_id

    if DRY_RUN:
        raise RuntimeError(
            "Dry-run requires --internship-id or INTERNYET_INTERNSHIP_ID "
            "(discovery requires login)."
        )

    internships = fetch_internships()
    if not internships:
        raise RuntimeError("No internships found for this account.")

    if SELECT_INTERNSHIP:
        selected_id = select_internship(internships)
        success(f"Selected internship ID: {selected_id}")
        return selected_id

    if len(internships) == 1:
        selected_id = internships[0]["id"]
        success(f"Auto-selected internship ID: {selected_id}")
        return selected_id

    print_internships(internships)
    raise RuntimeError(
        "Multiple internships found. Use --select-internship or --internship-id."
    )


# ─────────────────────────────────────────────
# SUBMIT / UPDATE ENTRY
# ─────────────────────────────────────────────
def submit_or_update(entry, index, total, date_to_id, internship_id):

    for skill in entry["skills"]:
        if skill not in SKILL_LOOKUP:
            raise ValueError(f"Unknown skill: {skill}")

    payload = {
        "internship_id": internship_id,
        "date": entry["date"],
        "description": entry["work_summary"],
        "hours": entry["hours"],
        "blockers": entry["blockers"],
        "learnings": entry["learnings"],
        "links": "",
        "mood_slider": 5,
        "skill_ids": [SKILL_LOOKUP[s] for s in entry["skills"]],
    }

    action = "CREATE"

    if entry["date"] in date_to_id:
        payload["id"] = date_to_id[entry["date"]]
        action = "UPDATE"

    prefix = f"[{index}/{total}]"

    if DRY_RUN:
        print(Fore.BLUE + f"{prefix} 🧪 {action} {entry['date']}")
        return True

    for attempt in range(MAX_RETRIES):
        r = session.post(
            SUBMIT_URL,
            json=payload,
            headers=HEADERS,
            timeout=TIMEOUT,
        )

        if r.status_code in (200, 201):
            success(f"{prefix} {entry['date']} → {action}")
            return True

        warn(f"{prefix} retry {attempt+1}")
        time.sleep(2)

    error(f"{prefix} Failed {entry['date']}")
    return False


# ─────────────────────────────────────────────
# MAIN EXECUTION
# ─────────────────────────────────────────────
def main():
    banner()

    if DRY_RUN and (DISCOVER_INTERNSHIPS or SELECT_INTERNSHIP):
        raise RuntimeError("Discovery/selection requires login. Disable --dry-run.")

    login()

    internships = None
    if DISCOVER_INTERNSHIPS or SELECT_INTERNSHIP:
        internships = fetch_internships()

    if DISCOVER_INTERNSHIPS:
        print_internships(internships)
        print(Fore.CYAN + "\n📦 Discovery mode complete.\n")
        sys.exit(0)

    if FETCH_ONLY:
        existing = fetch_existing_entries()
        save_existing_entries(existing)
        print(Fore.CYAN + "\n📦 Fetch-only mode complete.\n")
        sys.exit(0)

    internship_id = resolve_internship_id()

    with open("entries.json", encoding="utf-8") as f:
        ENTRIES = json.load(f)

    print(Fore.CYAN + f"📄 Loaded {len(ENTRIES)} entries")

    date_to_id = {}

    if not DRY_RUN:
        existing = fetch_existing_entries()
        save_existing_entries(existing)
        date_to_id = {e["date"]: e["id"] for e in existing}

    success_count = 0
    fail_count = 0
    total = len(ENTRIES)

    print(Fore.MAGENTA + "\n📤 Processing Entries\n")

    for i, entry in enumerate(ENTRIES, start=1):
        ok = submit_or_update(entry, i, total, date_to_id, internship_id)

        if ok:
            success_count += 1
        else:
            fail_count += 1

        if not DRY_RUN:
            time.sleep(REQUEST_DELAY)

    elapsed = round(time.time() - START_TIME, 2)

    print(
        Fore.CYAN
        + "\n📊 SUMMARY\n"
        + f"Success : {success_count}\n"
        + f"Failed  : {fail_count}\n"
        + f"Time    : {elapsed}s\n"
    )


if __name__ == "__main__":
    main()
