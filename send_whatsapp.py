import os
import pandas as pd
import random
from twilio.rest import Client
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Google Sheets setup ---
scopes = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes)
gs = gspread.authorize(creds)

# Replace with the exact name of your Google Sheet
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

# --- Twilio WhatsApp ---
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

# Change to your WhatsApp number
my_number = "whatsapp:+917065650639"

message = client.messages.create(
    from_="whatsapp:+14155238886",  # Twilio Sandbox number
    body=f"Time to grind! Today's question: {question_link}",
    to=my_number
)

print("WhatsApp message sent successfully!")
print("Question URL:", question_link)

# Optional: mark as solved in the sheet (if you want automation)
# sheet.update_cell(target_row.name + 2, df.columns.get_loc("Solved")+1, True)
