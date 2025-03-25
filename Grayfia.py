# File Sharing 
import os.path

# Datetime
from datetime import datetime, timedelta

# Google Cloud Console
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly', 'https://www.googleapis.com/auth/tasks.readonly']

class Grayfia:
    """
    A class to manage Google API interractions, including authentication,
    calendar event retrieval, and task list retrieval
    """

    def __init__(self):
        """Initialises Grayfia and attempts to authenticate"""
        self.creds = self._authenticate() # _authenticate is a private method

    def _authenticate(self):
        """
        Authenticates the user and obtains Google API credentials.

        This is a private method, indicated by the leading underscore.

        Returns:
            Credentials: An object containing the user's authentication credentials, or None if authentication fails.
        """
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
        return creds
    
    def get_events(self, calendar_id='primary', time_min=None, time_max=None):
        """
        Retrieves events from a Google Calendar, with time_max defaulting to the end of the current week.

        Args:
            calendar_id (str, optional): The ID of the calendar to retrieve events from. Defaults to 'primary'.
            time_min (str, optional): The minimum start time for events (ISO 8601 format). Defaults to current time.
            time_max (str, optional): The maximum start time for events (ISO 8601 format). Defaults to the end of the current week.

        Returns:
            list: A list of event dictionaries, or an empty list if no events are found or an error occurs.
        """
        try:
            service = build('calendar', 'v3', credentials=self.creds)
            now = datetime.utcnow()
            if not time_min:
                time_min = now.isoformat() + 'Z'
            if not time_max:
                days_until_sunday = (6 - now.weekday()) % 7
                end_of_week = now + timedelta(days=days_until_sunday, hours=23, minutes=59, seconds=59)
                time_max = end_of_week.isoformat() + 'Z'
            events = service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max, singleEvents=True, orderBy='startTime').execute()
            events = events.get('items', [])
            if not events:
                print('No upcoming events found.')
                return []
            return events
        except Exception as e:
            print(e)
            return []


    def get_task_lists(self): # renamed to get_task_lists
        """
        Retrieves task lists from Google Tasks.

        Returns:
            list: A list of task list dictionaries, or an empty list if no task lists are found or an error occurs.
        """
        try:
            service = build('tasks', 'v1', credentials=self.creds)
            results = service.tasklists().list().execute()
            task_lists = results.get('items', []) # renamed to task_lists
            if not task_lists:
                print('No task lists found.')
                return []
            return task_lists
        except Exception as e:
            print(e)
            return []
