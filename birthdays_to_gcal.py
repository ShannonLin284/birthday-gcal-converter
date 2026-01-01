import pandas as pd
import datetime
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/calendar"]

# CONFIGURATION (edit as needed)
TARGET_CALENDAR_NAME = "Cornell Assistive Technologies Subteam Calendar"
CSV_FILE = "birthdays.csv"

COL_NAME = "First and Last Name"
COL_BDAY = "Birthday!! YAY"
BDAY_FORMAT = "%m/%d/%Y"


def get_calendar_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                raise FileNotFoundError(
                    "credentials.json not found. Ask the calendar owner to generate it."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def get_calendar_id(service, calendar_name):
    calendars = service.calendarList().list().execute()

    for cal in calendars["items"]:
        if cal["summary"] == calendar_name:
            return cal["id"]

    print("\nCalendar not found. Available calendars:")
    for cal in calendars["items"]:
        print(" -", cal["summary"])

    raise ValueError("Target calendar not found. Check the name exactly.")


def event_exists(service, calendar_id, summary):
    events = service.events().list(
        calendarId=calendar_id,
        q=summary,
        singleEvents=True,
        maxResults=10
    ).execute()

    return len(events.get("items", [])) > 0


def add_birthday(service, calendar_id, name, birthday):
    summary = f"🎂 {name}'s Birthday"

    if event_exists(service, calendar_id, summary):
        print(f"Skipped (already exists): {name}")
        return

    event = {
        "summary": summary,
        "start": {
            "date": birthday.strftime("%Y-%m-%d")
        },
        "end": {
            "date": birthday.strftime("%Y-%m-%d")
        },
        "recurrence": [
            "RRULE:FREQ=YEARLY"
        ],
        "transparency": "transparent"
    }

    service.events().insert(
        calendarId=calendar_id,
        body=event
    ).execute()

    print(f"Added: {name}")


def main():
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError("birthdays.csv not found.")

    df = pd.read_csv(CSV_FILE)

    for col in [COL_NAME, COL_BDAY]:
        if col not in df.columns:
            raise ValueError(
                f'Missing column "{col}". Found: {list(df.columns)}'
            )

    service = get_calendar_service()
    calendar_id = get_calendar_id(service, TARGET_CALENDAR_NAME)

    print(f'\nUsing calendar: "{TARGET_CALENDAR_NAME}"\n')

    for _, row in df.iterrows():
        name = str(row[COL_NAME]).strip()
        bday_raw = str(row[COL_BDAY]).strip()

        if not name or name.lower() == "nan":
            continue
        if not bday_raw or bday_raw.lower() == "nan":
            continue

        birthday = datetime.datetime.strptime(
            bday_raw, BDAY_FORMAT
        ).date()

        add_birthday(service, calendar_id, name, birthday)

    print("\nDone.")


if __name__ == "__main__":
    main()
