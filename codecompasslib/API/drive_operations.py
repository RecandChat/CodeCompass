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

PARENT_PATH = os.path.abspath(os.path.join((__file__), '..', '..', '..'))  # Get the parent directory of the current directory (codecompasslib)
print(PARENT_PATH)

def get_creds_drive():
    
    """Get the credentials for Google Drive.
    This will generate a token.json file in the credentials_drive folder if there is none.
    NB! If the scope changes, the token.json file must be deleted and the user must re-authenticate.
    
    Returns:
        creds: The credentials for Google Drive. 
    """
    #Need to go bck two directories to access the credentials folder which is in the root

    creds = None
    print(PARENT_PATH + "/credentials_drive/token.json")
    if os.path.exists(PARENT_PATH + "/credentials_drive/token.json"):
        creds = Credentials.from_authorized_user_file(PARENT_PATH + "/credentials_drive/token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(PARENT_PATH + "/credentials_drive/credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open(PARENT_PATH + "/credentials_drive/token.json", "w") as token:
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
            print("\nFiles in the folder:")
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
        print("\nDownload %d%%." % int(status.progress() * 100))

    # The file's contents are now in fh, which we can use to create a Pandas DataFrame
    fh.seek(0)  # Move cursor to the beginning of the file before reading
    df = pd.read_csv(fh)
    return df


def upload_df_to_drive_as_csv(creds, df, filename, folder_id):
    """Uploads or updates a Pandas DataFrame as a CSV file within a Shared Drive."""
    try:
        # Convert the DataFrame to a CSV file
        temp_csv_path = f"/tmp/{filename}"  # Adjust based on your OS/environment
        df.to_csv(temp_csv_path, index=False)

        # Create Drive API client
        service = build("drive", "v3", credentials=creds)

        # Search for existing file with the same name in the specified folder
        response = service.files().list(
            q=f"'{folder_id}' in parents and name = '{filename}'",
            spaces='drive',
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            fields='files(id, name)'
        ).execute()

        files = response.get('files', [])

        # Define file metadata and media
        file_metadata = {"name": filename, "parents": [folder_id]}
        media = MediaFileUpload(temp_csv_path, mimetype='text/csv', resumable=True)

        if files:
            # File exists, so update it
            for file in files:
                file_id = file.get('id')
                file = service.files().update(
                    fileId=file_id,
                    media_body=media,
                    fields='id',
                    supportsAllDrives=True,
                ).execute()
                print(f'\nFile updated. File ID: {file.get("id")}')
        else:
            # File does not exist, so create it
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id',
                supportsAllDrives=True
            ).execute()
            print(f'\nFile uploaded. File ID: {file.get("id")}')

        # Clean up the temporary CSV file
        os.remove(temp_csv_path)

    except Exception as error:
        print(f"An error occurred: {error}")
        return None



if __name__ == "__main__":
    creds = get_creds_drive()
    list_shared_drive_contents(creds=creds, folder_id=DATA_FOLDER, drive_id=DRIVE_ID)
    df = download_csv_as_pd_dataframe(creds,"1jIYBQQJNo2s1bo3LHlYgKzUNNM0ueuhQ")
    upload_df_to_drive_as_csv(creds, df, "test.csv", DATA_FOLDER)
    print(df.head())