# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START sheets_quickstart]
import os.path
from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from auth import GoogleAuth


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


# The ID and range of a sample spreadsheet.

# Load the .env file
load_dotenv()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE_NAME = os.getenv("RANGE_NAME")

class GoogleSheetsService:
    
    def __init__(self, scopes=SCOPES, spreadsheetId = SPREADSHEET_ID ,range_name = RANGE_NAME ):
        self.scopes = scopes
        self.spreadsheetId = spreadsheetId
        self.range_name = range_name 
        self.creds = None # auth later
        self.service = None # Init Sheets API later
    
    def auth(self):
        if not self.creds:
            google_auth = GoogleAuth(self.scopes) # init the auth
            self.creds = google_auth.get_credentials() # get the credentials
        return self.creds

    def read_sheets(self):
        """
        Read the Sheets API.
        """

        # move the auth to this stage to avoid call api when init
        if not self.service: 
            self.service = build("sheets", "v4", credentials=self.auth()) # Init Sheets API 
        try:
            # Call the Sheets API
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.spreadsheetId, range=self.range_name).execute()
            return result.get("values", [])
        except HttpError as err:
          print(f"HTTP Error: {err}")
          return []
        except Exception as e:
          print(f"An error occurred: {e}")
          return []


if __name__ == "__main__":
    sheets_service = GoogleSheetsService()
    data = sheets_service.read_sheets()
    if data:
        for row in data:
            print(row)
    else:
        print("No data found.")
