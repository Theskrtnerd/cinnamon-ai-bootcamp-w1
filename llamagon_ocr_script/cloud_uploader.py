import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]


def authorize_google():
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
    return creds


def create_folder(service, folder_name):
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }

    file = service.files().create(body=file_metadata, fields="id").execute()
    print(f'Folder ID: "{file.get("id")}".')
    return file.get("id")


def upload_folder(folder_name, save_dir):
    creds = authorize_google()

    try:
        service = build("drive", "v3", credentials=creds)

        folder_id = create_folder(service, folder_name)

        print(os.listdir(f"./{save_dir}/{folder_name}/"))

        for file_name in os.listdir(f"./{save_dir}/{folder_name}/"):
            upload_file(service, folder_name, folder_id, file_name, save_dir)

    except HttpError as error:
        print(f"An error occurred: {error}")


def upload_file(service, folder_name, folder_id, file_name, save_dir):

    file_metadata = {"name": file_name, "parents": [folder_id]}
    media = MediaFileUpload(f"./{save_dir}/{folder_name}/{file_name}")

    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    print(f'File ID: {file.get("id")}')

    return file.get("id")
