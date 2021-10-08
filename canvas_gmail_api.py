import os
import requests
import json
import datetime
from datetime import timedelta
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class Canvas_Gmail_Script:

    def __init__(self, gmail, api, term_start, school):
        self.gui_gmail = gmail
        self.gui_canvas_api = api
        self.headers = {'Authorization': f'Bearer {self.gui_canvas_api}'}
        self.term_start_date = term_start
        self.school = school
        self.url = f"https://{self.school}.instructure.com/api/v1/courses"
        # create variables to hold all courses and assignments
        self.course_dict = {}
        self.assignment_names = []
        self.assignment_due_date = []
        self.course_ids = []
        self.final_dates = []
        self.event_ids = []

    def get_canvas_data(self):
        response = requests.get(self.url, headers=self.headers)
        print("Authorized Correctly, now fetching the data")
        data = response.json()
        print(json.dumps(data,indent=4))
        return data

    def get_courses(self, data):
        for course in data:
            self.course_dict.update({course["id"]: course["name"]})
        print("Got all courses, now printing them out")
        print(self.course_dict)
        return self.course_dict

    def get_all_assignments(self, course_dictionary):
        print("Starting to get all the assignments...")
        for course_id in self.course_dict.keys():
            self.url = f"https://auburn.instructure.com/api/v1/courses/{course_id}/assignments"
            response = requests.get(self.url, headers=self.headers, params={"order_by": "due_at"})
            assignments = response.json()
            for assignment in assignments:
                # modify due_date(convert to datetime object, subtract 1 day, and reformat)
                if assignment["due_at"] != None:
                    assignment_date = datetime.datetime.strptime(
                        assignment["due_at"], "%Y-%m-%dT%H:%M:%SZ")
                    assignment_date = assignment_date.date() - datetime.timedelta(days=1)
                    assignment_date = datetime.datetime.strftime(
                        assignment_date, "%Y-%m-%d")
                    # append to list
                    if str(assignment_date) >= self.term_start_date:
                        self.assignment_names.append(assignment["name"])
                        self.assignment_due_date.append(assignment_date)
                        self.course_ids.append(assignment["course_id"])

            # pagination - use response.links to check "next" for url
            while response.links["current"]["url"] != response.links["last"]["url"]:
                response = requests.get(
                    response.links["next"]["url"], headers=self.headers, params={"order_by": "due_at"})
                next_group = response.json()
                for next_item in next_group:
                    if next_item["due_at"] != None:
                        # modify due_date(convert to datetime object, subtract 1 day, and reformat)
                        next_assignment_date = datetime.datetime.strptime(
                            next_item["due_at"], "%Y-%m-%dT%H:%M:%SZ")
                        next_assignment_date = next_assignment_date.date() - datetime.timedelta(days=1)
                        next_assignment_date = datetime.datetime.strftime(
                            next_assignment_date, "%Y-%m-%d")

                        # assignment due date needs to be later than term start date
                        # append to list
                        if str(next_assignment_date) >= self.term_start_date:
                            self.assignment_names.append(next_item["name"])
                            self.assignment_due_date.append(next_assignment_date)
                            self.course_ids.append(next_item["course_id"])
        print("These are the assignment names")
        print(self.assignment_names)
        return self.assignment_names, self.assignment_due_date, self.course_ids


    def get_calendar_service(self):
        GOOGLE_CRED = "/Users/philiplee/Desktop/Personal_Projects/canvasGUI/credentials.json"
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        creds = None
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    GOOGLE_CRED, SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.pickle", "wb") as token:
                pickle.dump(creds,token)
        service = build("calendar","v3", credentials=creds)
        return service

    def create_events(self):
        service = self.get_calendar_service()
        for name, due_date, course_id in zip(self.assignment_names,self.assignment_due_date,self.course_ids):
            for key, value in self.course_dict.items():
                if course_id == int(key):
                    final_name = name + " " + value
                    start = datetime.datetime(int(due_date.split("-")[0]),int(due_date.split("-")[1]),int(due_date.split("-")[2])).isoformat()
                    event_result = service.events().insert(calendarId="philipyjlee95@gmail.com",body= {
                        "summary": final_name,
                        "start": {"dateTime" : start, "timeZone" : "PST"},
                        "end" : {"dateTime" : start, "timeZone" : "PST"}
                    }).execute()
                    self.event_ids.append(event_result["id"])
                    print("Added event")
                    print(event_result)
        return self.event_ids

    def delete_all_events(self):
        service = self.get_calendar_service()
        for event_id in self.event_ids:
            service.events().delete(
                calendarId="primary",
                eventId=event_id
            ).execute()
            print(event_id + " was deleted")
        return