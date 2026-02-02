Here’s a **clean, professional, copy-paste-ready `README.md`** written in proper Markdown.
It’s structured so **anyone (including future-you)** can understand, set up, and run the project safely.

---

````markdown
# Internship Diary Submission Automation

This project automates the submission of internship diary entries to the **Internyet (VTU) portal** using its official API.

It logs in automatically, reads diary entries from a JSON file, and submits them at a safe, human-like rate.  
A `--dry-run` mode is included to preview payloads without making any changes on the server.

---

## ✨ Features

- Automatic login (no manual token copying)
- Uses a real browser User-Agent
- Reads entries from a JSON file
- Full skill name → skill ID lookup
- Safe rate limiting (university-friendly)
- Retry with backoff on failures
- Clear success/failure summary
- `--dry-run` mode for zero-risk testing

---

## 📁 Project Structure

```text
.
├── submit_diaries.py   # Main script
├── entries.json        # Diary entries (input)
├── .env                # Credentials (not committed)
├── README.md
````

---

## 🧰 Requirements

* Python **3.9+**
* An active Internyet account
* Internet connection

---

## 📦 Installation

### 1️⃣ Clone or copy the project

```bash
git clone <repo-url>
cd internship-diary-automation
```

---

### 2️⃣ Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```bash
pip install requests python-dotenv
```

---

## 🔐 Environment Setup

Create a `.env` file in the project root:

```env
INTERNYET_EMAIL=your_email@example.com
INTERNYET_PASSWORD=your_password_here
```

⚠️ **Important**

* Do **not** commit `.env` to version control
* Add this to `.gitignore`:

```gitignore
.env
```

---

## 📝 Creating `entries.json`

All diary entries are read from `entries.json`.

### ✅ Example `entries.json`

```json
[
  {
    "date": "2026-01-01",
    "work_summary": "Prepared a detailed Product Requirements Document (PRD) for the Nican Resort Management System.",
    "hours": 2,
    "learnings": "Documented full system requirements for a complex management platform.",
    "blockers": "None.",
    "skills": ["Database design"]
  },
  {
    "date": "2026-01-02",
    "work_summary": "Designed the UI/UX for a Payroll System webpage.",
    "hours": 4,
    "learnings": "Learned to design data-heavy pages focused on financial tracking.",
    "blockers": "None.",
    "skills": ["Data visualization", "Layout Design"]
  }
]
```

---

### 📌 Field Rules

| Field          | Description                                |
| -------------- | ------------------------------------------ |
| `date`         | Format: `YYYY-MM-DD`                       |
| `work_summary` | Description of work done                   |
| `hours`        | Number (integer)                           |
| `learnings`    | What you learned                           |
| `blockers`     | Issues faced (use `"None."` if none)       |
| `skills`       | List of skills (must match lookup exactly) |

⚠️ Skill names **must match exactly** (case-sensitive).

---

## 🧪 Dry-Run Mode (Recommended First)

Dry-run prints the payloads without submitting anything.

```bash
python submit_diaries.py --dry-run
```

Output example:

```text
🧪 DRY-RUN MODE: Login skipped
📄 Loaded 12 entries

🧪 DRY-RUN PAYLOAD
{'internship_id': 702, 'date': '2026-01-01', ...}

✅ 2026-01-01 checked
```

---

## 🚀 Real Submission

Once dry-run looks correct:

```bash
python submit_diaries.py
```

Example output:

```text
✅ Logged in successfully
📄 Loaded 12 entries
✅ 2026-01-01 submitted
✅ 2026-01-02 submitted

📊 SUMMARY
Success: 12
Failed : 0
```

---

## 🕒 Rate Limiting & Safety

* Requests are sent ~**2 seconds apart**
* Sequential submissions (no parallel requests)
* Mimics normal human usage
* Safe for university portals

---

## 🔐 Authentication Details

* Uses the same API as the web frontend
* Access & refresh tokens are handled automatically via cookies
* Tokens are never stored on disk
* No manual cookie copying required

---


## 🔒 Security Notes

* Credentials live only in `.env`
* No scraping or browser automation
* Uses official API endpoints
* No data is modified in dry-run mode

---

## ✅ Recommended Workflow

1. Prepare all diary entries
2. Add them to `entries.json`
3. Run `--dry-run`
4. Verify payloads
5. Run real submission
6. Confirm entries on the portal


## ⚠️ Disclaimer

This script is intended for **personal academic use** on your own account.
Do not use it to spam, scrape, or submit data you are not authorized to submit.

---

## ✅ Final Notes

This automation:

* Looks like real browser traffic
* Respects server limits
* Is safe for academic portals
* Saves significant manual effort


```
