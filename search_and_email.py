import os
import smtplib
from email.mime.text import MIMEText
import requests

# Example using Remotive API (free job board API for developers)
# You can add more APIs like RemoteOK, Adzuna, or Google Programmable Search.
API_URL = "https://remotive.com/api/remote-jobs"

QUERIES = [
    "frontend developer intern",
    "python developer intern",
    "sql developer intern",
    "backend developer intern",
]

def fetch_jobs():
    jobs = []
    for query in QUERIES:
        resp = requests.get(API_URL, params={"search": query})
        if resp.status_code == 200:
            data = resp.json()
            for job in data.get("jobs", [])[:5]:  # take top 5 per query
                jobs.append(f"<b>{job['title']}</b> at {job['company_name']}<br>"
                            f"<a href='{job['url']}'>{job['url']}</a><br><br>")
    return jobs

def send_email(jobs):
    user = os.environ["SMTP_USER"]
    password = os.environ["SMTP_PASS"]
    recipient = os.environ["RECIPIENT_EMAIL"]

    body = "<h2>Daily Job Search Results</h2>" + "".join(jobs)
    msg = MIMEText(body, "html")
    msg["Subject"] = "Job search results (Frontend / Python / SQL / Backend Internships)"
    msg["From"] = user
    msg["To"] = recipient

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(user, password)
        server.send_message(msg)

if __name__ == "__main__":
    jobs = fetch_jobs()
    if jobs:
        send_email(jobs)
    else:
        print("No jobs found.")
