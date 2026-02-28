# InternYet Internship Diary Automation Tool

This project automates submission, updating, and backup of internship diary entries on the InternYet (VTU) portal using its official API.

The tool performs authenticated login, fetches existing diary entries, safely creates or updates entries, and maintains automatic local backups. It also includes validation and dry-run capabilities to prevent accidental submissions.

---

## Features

### Authentication

* Automatic login using credentials stored in `.env`
* No manual token or cookie handling required
* Uses official InternYet API endpoints

### Smart Submission

* Automatically creates or updates entries based on date
* Detects existing portal entries before submission
* Sequential submission to avoid server overload
* Retry mechanism with exponential backoff

### Backup Support

* Fetches all existing diary entries from the portal
* Stores timestamped JSON backups locally
* Dedicated fetch-only mode for safe archival

### Validation and Testing

* Dry-run mode for safe validation
* Skill name verification before submission
* Clear success and failure summaries

### CLI Improvements

* Progress tracking during submission
* Execution time reporting
* Structured terminal output

---

## Project Structure

```text
.
├── main.py                         # Main automation script
├── entries.json                    # Local internship diary entries
├── existing_entries_*.json         # Automatically generated backups
├── .env                            # Credentials (not committed)
├── README.md
```

---

## Requirements

* Python 3.9 or newer
* Active InternYet account
* Internet connection

---

## Installation

### Clone the repository

```bash
git clone <repo-url>
cd internship-diary-automation
```

### Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install requests python-dotenv colorama
```

---

## Environment Setup

Create a `.env` file in the project root directory:

```env
INTERNYET_EMAIL=your_email@example.com
INTERNYET_PASSWORD=your_password_here
```

Credentials are read only at runtime and are not stored elsewhere.

---

## Creating `entries.json`

Diary entries are read from `entries.json`.

### Example

```json
[
  {
    "date": "2026-01-01",
    "work_summary": "Prepared a detailed Product Requirements Document.",
    "hours": 8,
    "learnings": "Improved system documentation practices.",
    "blockers": "None.",
    "skills": ["Database design"]
  }
]
```

---

## Field Definitions

| Field          | Description                                  |
| -------------- | -------------------------------------------- |
| `date`         | Format: YYYY-MM-DD                           |
| `work_summary` | Description of work performed                |
| `hours`        | Integer value                                |
| `learnings`    | Key outcomes or knowledge gained             |
| `blockers`     | Issues faced (use `"None."` if none)         |
| `skills`       | List of skills matching lookup names exactly |

Skill names are case-sensitive and must exist in the internal skill lookup table.

---

## Dry-Run Mode

Dry-run validates entries and prints intended actions without submitting data.

```bash
python main.py --dry-run
```

Example output:

```text
Dry-run mode enabled
Loaded 12 entries

[1/12] CREATE 2026-01-01
[2/12] UPDATE 2026-01-02

SUMMARY
Success : 12
Failed  : 0
```

No portal data is modified.

---

## Fetch-Only Mode

Fetches all existing internship diary entries and saves them locally.

```bash
python main.py --fetch-only
```

This mode:

* Logs in
* Retrieves all portal entries
* Saves a timestamped backup file
* Exits without submitting anything

Example output:

```text
Fetching existing portal entries
Fetched 41 entries
Backup saved → existing_entries_20260228_183021.json
```

---

## Real Submission

After validating using dry-run:

```bash
python main.py
```

Example output:

```text
Logged in successfully
Loaded 41 entries
Fetching existing portal entries
Backup saved → existing_entries_20260228_190112.json

Processing Entries

[1/41] UPDATE 2025-12-24
[2/41] CREATE 2025-12-25

SUMMARY
Success : 41
Failed  : 0
Time    : 214.53s
```

---

## Create vs Update Logic

The tool automatically determines whether to create or update an entry:

* Existing date on portal → entry updated
* New date → entry created

This allows safe repeated execution without duplication.

---

## Rate Limiting and Safety

* Requests are sequential
* Configurable delay between submissions
* Retry handling for temporary failures
* Designed to mimic normal user interaction

The script is suitable for academic portal usage.

---

## Security Notes

* Credentials are stored only in `.env`
* No browser automation or scraping
* Official API endpoints are used
* Tokens are managed automatically by the session
* Backups remain local

---

## Recommended Workflow

1. Prepare diary entries in `entries.json`
2. Run dry-run validation:

   ```bash
   python main.py --dry-run
   ```
3. Verify output
4. Run submission:

   ```bash
   python main.py
   ```
5. Confirm entries on the portal
6. Keep generated backups safely

---

## Disclaimer

This tool is intended for personal academic use on your own InternYet account.

Do not use this script for unauthorized automation, excessive requests, or submission of data you are not permitted to manage.

---

## Notes

The automation respects server limits, uses authenticated API communication, and significantly reduces manual diary submission effort while maintaining safe operating behavior.
