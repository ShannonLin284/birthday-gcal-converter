# Birthday to Google Calendar Import (Team Calendar)

This project imports birthdays from a spreadsheet and creates yearly recurring birthday events in a shared Google Calendar.

It is designed for the Cornell Assistive Technologies Subteam Calendar, but can be customized for any calendar.


## What this does

Reads birthdays from a CSV exported from Google Sheets  
Creates all-day, yearly recurring birthday events  
Adds them to a specific shared Google Calendar  
Uses Google OAuth (no passwords, access can be revoked)


## What you need

1. Python 3.9 or higher
2. Edit access to the target Google Calendar
3. A one-time Google API file called credentials.json
4. A CSV file with birthdays


## Folder structure

After setup, your folder should look like this:

```
birthday-gcal-import/
   birthdays_to_gcal.py
   birthdays.csv
   credentials.json
   token.json
```

birthdays.csv, credentials.json, and token.json should not be committed to GitHub.

---

## Step 1) Prepare the spreadsheet

Your Google Sheet must have these exact column headers:

Timestamp  
First and Last Name  
Birthday!! YAY  

Birthday format must be:

MM/DD/YYYY

Example row:

2025-12-31 21:58:00,Shannon Lin,4/17/2006

Export as CSV using:  
Google Sheets → File → Share → Download → CSV

Name the file:

birthdays.csv


## Step 2) Install dependencies

Run this once:

```bash
pip install pandas google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Step 3) Get credentials.json (one time)

This must be done by the Google account that owns the calendar or has full access.

1. Go to https://console.cloud.google.com/
2. Create a new project (any name is fine)
3. Enable Google Calendar API
4. Go to APIs & Services → Credentials
5. Click Create Credentials → OAuth Client ID
6. Application type: Desktop app
7. Download the file
8. Rename it to:

credentials.json

Place credentials.json in the project folder.

This does not share passwords.  
Access can be revoked at any time in Google Account → Security → Third-party access.


## Step 4) Set the calendar name

Open birthdays_to_gcal.py and set:

```python
TARGET_CALENDAR_NAME = "Project Team Calendar..."
```

The name must match exactly as it appears in Google Calendar.

## Step 5) Run the script

From the project folder:

```bash
python birthdays_to_gcal.py
```

On first run:
A browser window opens  
Log into Google  
Click Allow  

This creates token.json so you do not need to log in again.


## Added!

Each birthday becomes a yearly recurring all-day event  
Events are added to the team calendar  


## Customization

### Change event title

Edit this line in birthdays_to_gcal.py:

```python
"summary": f"🎂 {name}'s Birthday"
```

### Add reminders (optional)

Uncomment this block in the event definition:

```python
"reminders": {
  "useDefault": False,
  "overrides": [
    {"method": "popup", "minutes": 1440},
    {"method": "popup", "minutes": 10080}
  ]
}
```

### Change birthday format

If your dates are not MM/DD/YYYY, update:

```python
BDAY_FORMAT = "%m/%d/%Y"
```


## Common problems

Calendar not found  
You must have edit access  
The calendar name must match exactly  

credentials.json missing  
Make sure the file is in the same folder as the script  

Permission denied  
You need permission to make changes to events, not view-only  


## Security notes

Do not commit credentials.json or token.json  
No passwords are stored  
Access can be revoked at any time  


## Done

Once this is set up, adding new birthdays only requires:
Updating the Google Sheet  
Exporting the CSV  
Running the script again

