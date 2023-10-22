# Schedule Announcer Mate

# Imports

import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build

from threading import Thread

# Get Structured Date Function
def get_current_structured_date():
    current_datetime = datetime.datetime.now()
    current_day_of_the_month = current_datetime.strftime("%d")
    current_month = current_datetime.strftime("%B")
    current_year = current_datetime.strftime("%Y")
    current_date = f"{current_day_of_the_month} {current_month} {current_year}"
    return current_date

# Google Sheets Variables

credentials = service_account.Credentials.from_service_account_file("../credentials.json",  scopes=['https://www.googleapis.com/auth/spreadsheets'])
service = build("sheets", "v4", credentials=credentials)

spreadsheet_id = "1R1ooZQYaSHPByec1VqjOjUUd1SFjH_YsCsgpeZGXssI"

# Getting Schedule Accordingly From Google Sheets
def get_schedule(schedule_date):
    sheet_name = schedule_date
    schedule_range = f"{sheet_name}!B3:D290"

    # Response Structure
    # response = {values: arrays_of(time, task, task_details)}

    response = service.spreadsheets().values().get(spreadsheetId = spreadsheet_id, range = schedule_range).execute()
    return response

# Dictionary For Announcements With Their Times

# Structure = {"time": {"task": "task details"}}
CURRENT_SCHEDULE = {}

# Function For Populating Global Schedule Dictionary With A Proper Format

def populate_current_schedule(schedule_to_populate_with):
    
    global CURRENT_SCHEDULE

# Thread For Checking And Updating Date | Accordingly, Configuring The Dictionary

# To Check:
    # Date Changes
    # New Changes In Sheet

def keeping_schedule_up_to_date():
    
    previous_date = get_current_structured_date()
    previous_schedule = get_schedule(previous_date)

    while True:

        new_date = get_current_structured_date()
        new_schedule = get_schedule(new_date)

        if new_date != previous_date:

            populate_current_schedule(new_schedule)
            previous_date = new_date

        else:

            if new_schedule != previous_schedule:
                populate_current_schedule(new_schedule)
                previous_schedule = new_schedule

thread_for_keeping_schedule_up_to_date = Thread(target=keeping_schedule_up_to_date)


# Thread For Schedule Announcement For The Day | Going Through The Dictionary, Checking For Each's Time


# Main With Everything Compiled