import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]


def upload_photo(file_name):
    creds = None
    if os.path.exists("ENV/token.json"):
        creds = Credentials.from_authorized_user_file("ENV/token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "ENV/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("ENV/token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("drive", "v3", credentials=creds)

        file_metadata = {"name": file_name}
        media = MediaFileUpload(file_name)

        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        print(f'File ID: {file.get("id")}')
    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    return file.get("id")


if __name__ == "__main__":
    upload_photo("testing_photos/emoji.jpg")
