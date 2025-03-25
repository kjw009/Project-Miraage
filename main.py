# OS
import os.path

# Datetime
from datetime import datetime

# Google Client Imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Grayfia Class
from Grayfia import Grayfia

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/tasks.readonly'] # Add the scopes that your app will need.

if __name__ == "__main__":
    grayfia = Grayfia()

    if grayfia.creds:
        events = grayfia.get_events()
        task_lists = grayfia.get_tasks()

        if events:
            print("---Events---")
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"Event: {event['summary']}, Start: {start}")
        
        if task_lists:
            print("---Task Lists---")
            for task_list in task_lists:
                print(f"Title: {task_list.get('title')}")
    
    else:
        print("Authentication Failed")