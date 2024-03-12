import os.path
import io
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
DRIVE_ID = "0AL1DtB4TdEWdUk9PVA"
DATA_FOLDER = "13JitBJQLNgMvFwx4QJcvrmDwKOYAShVx"

def upload_or_update_drive_file(creds, fpath_local, fname_drive, folder_id):
    """Uploads or updates a file within a Shared Drive."""
    try:
        # Create Drive API client
        service = build("drive", "v3", credentials=creds)

        # Corrected search for existing file with the same name in the specified folder
        response = service.files().list(
            q=f"'{folder_id}' in parents and name = '{fname_drive}'",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            fields='files(id, name)'
        ).execute()
        
        files = response.get('files', []) #Returns a list of dictionaries with same name
        print("Files:", files)

        # Define file metadata
        file_metadata = {"name": fname_drive, "parents": [folder_id]}
        media = MediaFileUpload(fpath_local, resumable=True)

        if files:
            # File exists, so update it
            file_id = files[0].get('id')
            print(file_id)
            updated_file = service.files().update(
                fileId=file_id,
                media_body=media,
                fields='id'
            ).execute()
            print(f'File updated. File ID: {updated_file.get("id")}')
        else:
            # File does not exist, so create it
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id',
                supportsAllDrives=True
            ).execute()
            print(f'File uploaded. File ID: {file.get("id")}')

    except Exception as error:
        print(f"An error occurred: {error}")
        return None


        
def download_from_shared_drive(creds, file_id, fname_local):
    """Downloads a file from a Shared Drive."""
    try:
        # Create Drive API client
        service = build("drive", "v3", credentials=creds)

        # Download the file
        request = service.files().get_media(fileId=file_id)
        fh = open(fname_local, "wb")
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")

        print(f"File downloaded to {fname_local}.")
    except Exception as error:  # Catch more general exception.
        print(f"An error occurred: {error}")

def get_creds_drive():
    """Shows basic usage of the Drive v3 API."""
    creds = None
    if os.path.exists("credentials_drive/token.json"):
        creds = Credentials.from_authorized_user_file("credentials_drive/token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials_drive/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("credentials_drive/token.json", "w") as token:
            token.write(creds.to_json())
    return creds
        
    
def list_shared_drive_contents(creds, folder_id, drive_id):
    """Lists the contents of the specified folder in a Shared Drive."""
    service = build("drive", "v3", credentials=creds)

    try:
        # List files in the specified folder of the Shared Drive
        response = service.files().list(
            q=f"'{folder_id}' in parents",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            driveId=drive_id,  # Specify the ID of the Shared Drive
            corpora='drive',  # Ensure to set corpora to 'drive' when using driveId
            fields="nextPageToken, files(id, name)"
        ).execute()

        items = response.get('files', [])
        if not items:
            print("No files found in the folder.")
        else:
            print("Files in the folder:")
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
    except Exception as error:
        print(f'An error occurred: {error}')
            

def download_csv_as_pd_dataframe(creds, file_id):
    """Downloads a CSV file from Google Drive and returns it as a Pandas DataFrame."""
    service = build("drive", "v3", credentials=creds)

    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False

    while not done:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    # The file's contents are now in fh, which we can use to create a Pandas DataFrame
    fh.seek(0)  # Move cursor to the beginning of the file before reading
    df = pd.read_csv(fh)
    return df


    

    

if __name__ == "__main__":
    creds = get_creds_drive()
    list_shared_drive_contents(creds, DATA_FOLDER, DRIVE_ID)
    upload_or_update_drive_file(creds, "allReposCleaned.csv", "allReposCleaned.csv", DATA_FOLDER)