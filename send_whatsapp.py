import os
import pandas as pd
import random
from twilio.rest import Client
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Config ---
DEBUG_MODE = True  # Set to False to actually send WhatsApp

# --- Google Sheets setup ---
scopes = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes)
gs = gspread.authorize(creds)

# Exact name of your Google Sheet
sheet_name = "Whatsapped sheet"
sheet = gs.open(sheet_name).sheet1

# Load data into pandas
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Filter unsolved problems
unsolved = df[df['Solved'] == False]

if unsolved.empty:
    print("All problems solved! 🎉")
    exit(0)

# Pick a random unsolved problem
target_row = unsolved.sample(1).iloc[0]
question_link = target_row['Question_Link']

# --- Debug print ---
print("DEBUG MODE:", DEBUG_MODE)
print("Today's random problem URL:", question_link)

# Show first 3 unsolved problems
print("\nFirst 3 unsolved problems (for sanity check):")
for i, link in enumerate(unsolved['Question_Link'].head(3), start=1):
    print(f"{i}. {link}")

# --- Twilio WhatsApp ---
if not DEBUG_MODE:
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token)

    my_number = "whatsapp:+91XXXXXXXXXX"  # <-- replace with your number

    message = client.messages.create(
        from_="whatsapp:+14155238886",  # Twilio Sandbox number
        body=f"Time to grind! Today's question: {question_link}",
        to=my_number
    )

    print("WhatsApp message sent successfully!")
