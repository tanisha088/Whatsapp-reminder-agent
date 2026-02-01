import pandas as pd
from datetime import datetime
from twilio.rest import Client
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import os

# ---------- Google Sheets ----------
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", SCOPE
)
gs = gspread.authorize(creds)

sheet = gs.open("Whatsapped sheet").sheet1   # <-- sheet name exactly
data = sheet.get_all_records()
df = pd.DataFrame(data)

# ---------- Select problem ----------
unsolved = df[df["Solved"] == False]

if unsolved.empty:
    print("All problems solved 🎉")
    exit()

# Least sent, oldest last sent
unsolved = unsolved.sort_values(
    by=["Sent_Count", "Last_Sent"],
    na_position="first"
)

row = unsolved.iloc[0]

# Extract problem name from URL
match = re.search(r"problems/([^/]+)", row["Question_Link"])
problem_name = match.group(1).replace("-", " ").title() if match else "LeetCode Problem"

row_idx = df.index[df["Question_Link"] == row["Question_Link"]][0] + 2

# ---------- Twilio ----------
client = Client(
    auth_token=os.environ["TWILIO_AUTH_TOKEN"],
    username=os.environ["TWILIO_ACCOUNT_SID"]
)

client.messages.create(
    from_="whatsapp:+14155238886",
    to="whatsapp:+917065650639",
    body=f"""📌 Daily NeetCode Problem

{problem_name}
{row['Question_Link']}

Focus on intuition, not speed."""
)

# ---------- Update Sheet ----------
sheet.update_cell(row_idx, 3, row["Sent_Count"] + 1)
sheet.update_cell(row_idx, 4, datetime.utcnow().strftime("%Y-%m-%d"))

print("Message sent successfully")
