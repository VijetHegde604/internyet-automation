import requests
import time
import os
import json
import argparse
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# ARGUMENTS
# ─────────────────────────────────────────────
parser = argparse.ArgumentParser(
    description="Internship diary submission tool"
)
parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Print payloads without submitting to the server"
)
args = parser.parse_args()
DRY_RUN = args.dry_run

# ─────────────────────────────────────────────
# ENV SETUP
# ─────────────────────────────────────────────
load_dotenv()

EMAIL = os.getenv("INTERNYET_EMAIL")
PASSWORD = os.getenv("INTERNYET_PASSWORD")

if not DRY_RUN:
    if not EMAIL or not PASSWORD:
        raise RuntimeError("❌ Missing INTERNYET_EMAIL or INTERNYET_PASSWORD in .env")

# ─────────────────────────────────────────────
# SESSION
# ─────────────────────────────────────────────
session = requests.Session()

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Origin": "https://vtu.internyet.in",
    "Referer": "https://vtu.internyet.in/",
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# ─────────────────────────────────────────────
# SKILL LOOKUP
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
    "Xcode": 60
}

# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
LOGIN_URL = "https://vtuapi.internyet.in/api/v1/auth/login"

if DRY_RUN:
    print("🧪 DRY-RUN MODE: Login skipped")
else:
    login_payload = {
        "email": EMAIL,
        "password": PASSWORD
    }

    resp = session.post(
        LOGIN_URL,
        json=login_payload,
        headers=HEADERS,
        timeout=15
    )

    if resp.status_code != 200:
        raise RuntimeError(f"❌ Login failed: {resp.status_code} → {resp.text}")

    print("✅ Logged in successfully")
    print("🍪 Cookies:", session.cookies.get_dict())

# ─────────────────────────────────────────────
# LOAD ENTRIES
# ─────────────────────────────────────────────
with open("entries.json", "r", encoding="utf-8") as f:
    ENTRIES = json.load(f)

print(f"📄 Loaded {len(ENTRIES)} entries")

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
SUBMIT_URL = "https://vtuapi.internyet.in/api/v1/student/internship-diaries/store"
INTERNSHIP_ID = 702

REQUEST_DELAY = 2
MAX_RETRIES = 3
TIMEOUT = 15

# ─────────────────────────────────────────────
# SUBMIT FUNCTION
# ─────────────────────────────────────────────
def submit_entry(entry):
    payload = {
        "internship_id": INTERNSHIP_ID,
        "date": entry["date"],
        "description": entry["work_summary"],
        "hours": entry["hours"],
        "links": "",
        "blockers": entry["blockers"],
        "learnings": entry["learnings"],
        "mood_slider": 5,
        "skill_ids": [SKILL_LOOKUP[s] for s in entry["skills"]]
    }

    if DRY_RUN:
        print("\n🧪 DRY-RUN PAYLOAD")
        print(payload)
        return True, "dry-run"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = session.post(
                SUBMIT_URL,
                json=payload,
                headers=HEADERS,
                timeout=TIMEOUT
            )

            if r.status_code == 200:
                return True, r.text

            print(f"⚠ Attempt {attempt}: {r.status_code}")
            time.sleep(2 * attempt)

        except Exception as e:
            print(f"❌ Attempt {attempt} failed: {e}")
            time.sleep(2 * attempt)

    return False, "Failed after retries"

# ─────────────────────────────────────────────
# SUBMIT ALL ENTRIES
# ─────────────────────────────────────────────
success = 0
failure = 0

for entry in ENTRIES:
    ok, resp = submit_entry(entry)

    if ok:
        print(f"✅ {entry['date']} {'checked' if DRY_RUN else 'submitted'}")
        success += 1
    else:
        print(f"❌ {entry['date']} failed → {resp}")
        failure += 1

    if not DRY_RUN:
        time.sleep(REQUEST_DELAY)

print("\n📊 SUMMARY")
print("Success:", success)
print("Failed :", failure)
