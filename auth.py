import os.path
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Load the .env file
load_dotenv()

# File paths for Google API credentials and token
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS", "credentials.json")  # Path to client secret JSON
TOKEN_FILE = os.getenv("GOOGLE_TOKEN", "token.json")  # Path for token JSON


class GoogleAuth:
    """
    Handles Google API authorization and token management.

    This class facilitates obtaining, refreshing, and storing credentials
    for interacting with Google APIs.
    """
    def __init__(self,scope):
        self.scope = scope
        self.creds = None

    def authenticate_google_api(self):
        """
        Execute authorization logic and obtain credentials (Credentials)

        If valid credentials exist in the token file, they are used.
        Otherwise, a new login flow is initiated, and the credentials are stored.
        """

        # Check if a valid token file exists
        if os.path.exists(TOKEN_FILE):
            self.creds = Credentials.from_authorized_user_file(TOKEN_FILE, self.scope)

        # If no valid credentials, initiate authentication
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                # Refresh expired credentials
                self.creds.refresh(Request())
            else:
                # Start new login flow
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, self.scope)
                self.creds = flow.run_local_server(port=0)
            
            # Save the credentials for future use
            with open(TOKEN_FILE, "w") as token:
                token.write(self.creds.to_json())
    
    def get_credentials(self):
        """
        Get the authenticated credentials for Google API access.

        Returns:
            google.oauth2.credentials.Credentials: The authenticated credentials.
        """
        # if not yet auth
        if not self.creds:
            self.authenticate_google_api()
        
        return self.creds

if __name__ == "__main__":
    SCOPES = [
        "https://www.googleapis.com/auth/drive.metadata.readonly",
        "https://www.googleapis.com/auth/spreadsheets.readonly"
    ]
    google_auth = GoogleAuth(SCOPES)
    google_auth.authenticate_google_api()