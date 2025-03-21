# OS
import os.path

# Datetime
from datetime import datetime

# Google Client Imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/tasks.readonly'] # Add the scopes that your app will need.

def get_events(calendar_id='primary', time_min=None, time_max=None):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8000)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('calendar', 'v3', credentials=creds)

        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        if not time_min:
            time_min = now
        if not time_max:
            time_max = '2021-12-31T23:59:59Z'

        events = service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max, singleEvents=True, orderBy='startTime').execute()
        events = events.get('items', [])

        if not events:
            print('No upcoming events found.')
            return []
        
        return events
    
    except Exception as e:
        print(e)
        return []

def get_tasks():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8000)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('tasks', 'v1', credentials=creds)

        results = service.tasklists().list().execute()
        tasks = results.get('items', [])

        if not tasks:
            print('No task found.')
            return []
        
        return tasks
    
    except Exception as e:
        print(e)
        return []
    
if __name__ == '__main__':
    tasks = get_tasks()
    if tasks:
        for task in tasks:
            print(f"Title: {task['title']}")
            if 'due' in task:
                print(f"Due: {task['due']}")