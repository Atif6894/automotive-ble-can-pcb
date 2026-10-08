"""Submit the WindBorne Electrical Engineer Intern application. Run manually: python submit_windborne.py"""
import json
import sys
import urllib.error
import urllib.request

NAME = "Mohammed Atif"
EMAIL = "REPLACE_WITH_EMAIL"
RESUME_URL = "REPLACE_WITH_PUBLIC_RESUME_URL"
SUBMISSION_URL = "REPLACE_WITH_GITHUB_URL"
NOTES = ("Designed a compact automotive BLE-to-CAN board (TCAN4550 + CC2340R5-Q1) with 9-36 V protection, "
         "CAN FD, backup-battery power path, SWD/test access and full fab outputs.")

URL = "https://windbornesystems.com/career_applications.json"

for k, v in {"EMAIL": EMAIL, "RESUME_URL": RESUME_URL, "SUBMISSION_URL": SUBMISSION_URL}.items():
    if v.startswith("REPLACE_WITH"):
        sys.exit(f"ERROR: fill in {k} before submitting.")

payload = {"career_application": {
    "name": NAME, "email": EMAIL, "role": "Electrical Engineer Intern",
    "notes": NOTES, "submission_url": SUBMISSION_URL, "resume_url": RESUME_URL}}

req = urllib.request.Request(URL, data=json.dumps(payload).encode(), method="POST",
                             headers={"Content-Type": "application/json", "Accept": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        status, body = r.status, r.read().decode(errors="replace")
except urllib.error.HTTPError as e:
    status, body = e.code, e.read().decode(errors="replace")

print("HTTP status:", status)
print("Response body:", body)
if status == 200:
    print("SUCCESS: application accepted (HTTP 200).")
else:
    print("FAILED: status was not 200. Fix the issue and resubmit.")
    sys.exit(1)
