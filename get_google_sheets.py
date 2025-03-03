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
load_dotenv(override=True)
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
            print(f"spreadsheetId:{self.spreadsheetId}")
            print(f"range:{self.range_name}")
            return result.get("values", [])
        except HttpError as err:
          print(f"HTTP Error: {err}")
          return []
        except Exception as e:
          print(f"An error occurred: {e}")
          return []
        
    def filter_columns(self, data, selected_columns):
        """ get Google Sheets API selected column  """
        filtered_data = []
        for row in data:
            # get selected column（A=0, F=5, I=8）
            filtered_row = [row[i] if i < len(row) else "" for i in selected_columns]
            filtered_data.append(filtered_row)
        return filtered_data


if __name__ == "__main__":
    sheets_service = GoogleSheetsService()
    data = sheets_service.read_sheets()
    selected_columns = [0, 5, 8]
    filtered_data = sheets_service.filter_columns(data, selected_columns)

    for row in filtered_data:
        if row: 
            print(row)
        else:
            print("No data found.")
