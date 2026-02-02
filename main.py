import requests
import time

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



URL = "https://vtuapi.internyet.in/api/v1/student/internship-diaries/store"

cookies = {
    "access_token": "",
    "refresh_token": ""
}

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Origin": "https://vtu.internyet.in",
    "Referer": "https://vtu.internyet.in/"
}

internship_id = 702

def submit_entry(entry):
    skill_ids = [SKILL_LOOKUP[s] for s in entry["skills"]]

    payload = {
        "internship_id": internship_id,
        "date": entry["date"],
        "description": entry["work_summary"],
        "hours": entry["hours"],
        "links": "",
        "blockers": entry["blockers"],
        "learnings": entry["learnings"],
        "mood_slider": 5,
        "skill_ids": skill_ids
    }

    response = requests.post(
        URL,
        json=payload,
        headers=headers,
        cookies=cookies
    )

    return response.status_code, response.text


for entry in ENTRIES:
    status, resp = submit_entry(entry)
    print(f"{entry['date']} → {status}")
    time.sleep(5)


# curl 'https://vtuapi.internyet.in/api/v1/student/internship-applys?page=1&status=6' \
#   -H 'Accept: application/json, text/plain, */*' \
#   -H 'Accept-Language: en-US,en;q=0.6' \
#   -H 'Connection: keep-alive' \
#   -b 'access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3Z0dWFwaS5pbnRlcm55ZXQuaW4vYXBpL3YxL2F1dGgvbG9naW4iLCJpYXQiOjE3NzAwNDExODgsImV4cCI6MTc3MDA0NDc4OCwibmJmIjoxNzcwMDQxMTg4LCJqdGkiOiJ4THdZcHVhUlVRbG9qVDk0Iiwic3ViIjoiNzE0ODgiLCJwcnYiOiIyM2JkNWM4OTQ5ZjYwMGFkYjM5ZTcwMWM0MDA4NzJkYjdhNTk3NmY3In0.cmzKYiZzImbBlAWmwNyvreAFH2RwDkPo2YeIgO_lVLA; refresh_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3Z0dWFwaS5pbnRlcm55ZXQuaW4vYXBpL3YxL2F1dGgvbG9naW4iLCJpYXQiOjE3NzAwNDExODgsImV4cCI6MTc3MDA2MTM0OCwibmJmIjoxNzcwMDQxMTg4LCJqdGkiOiJXbkQ1WWJmRHNWdjRGVlY1Iiwic3ViIjoiNzE0ODgiLCJwcnYiOiIyM2JkNWM4OTQ5ZjYwMGFkYjM5ZTcwMWM0MDA4NzJkYjdhNTk3NmY3IiwidHlwZSI6InJlZnJlc2gifQ.AJ7gzfiq-5BUiWh-v0zjXiekRpitDlOOAgHiPkZLuWA; twk_uuid_689c7188a7ee3319309bdeae=%7B%22uuid%22%3A%221.Sx0cMq5hpFP71DcrPalNbW1TQX8CBAjPPoQWe7RgzgFMLyKldXQrB1QTLDBtMtiLOGbVCumT4GzClnYKK0hSPXtEnCU6v75T1lqWBHyVbsw0Uh81jpFyR%22%2C%22version%22%3A3%2C%22domain%22%3A%22internyet.in%22%2C%22ts%22%3A1770041624101%7D' \
#   -H 'Origin: https://vtu.internyet.in' \
#   -H 'Referer: https://vtu.internyet.in/' \
#   -H 'Sec-Fetch-Dest: empty' \
#   -H 'Sec-Fetch-Mode: cors' \
#   -H 'Sec-Fetch-Site: same-site' \
#   -H 'Sec-GPC: 1' \
#   -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
#   -H 'sec-ch-ua: "Not(A:Brand";v="8", "Chromium";v="144", "Brave";v="144"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "Linux"'