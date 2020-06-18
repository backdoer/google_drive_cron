from __future__ import print_function
import pickle
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None

    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(dir_path + 'token.pickle'):
        with open(dir_path + 'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                dir_path + 'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(dir_path + 'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Create the directory if it doesn't exist
    file_dir = "%s/Documents/Takeout" % os.environ['HOME']

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    # Call the Drive v3 API
    page_token = None
    while True:
        response = service.files().list(
            q="name contains 'takeout' and trashed = false and mimeType contains 'zip'",
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            file_id = file.get('id')
            file_name = file.get('name')

            print('Found file: %s (%s)' % (file_name, file_id))

            file_path = "%s/%s" % (file_dir, file_name)

            if not os.path.exists(file_path):
                file_count = len([name for name in os.listdir(
                    file_dir) if os.path.isfile(os.path.join(file_dir, name))])
                if file_count > 0:
                    os.system(
                        """osascript -e 'display notification "You need to take care of this" with title "No room for new Google Drive backup"'""")
                    break

                request = service.files().get_media(fileId=file_id)

                fh = io.FileIO(file_path, 'wb')
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print("Download and wrote %d%%." %
                          int(status.progress() * 100))

                    os.system(
                        """osascript -e 'display notification "You are good to go" with title "Data pulled from Google Drive"'""")

            else:
                print('File already exists: %s (%s)' % (file_name, file_id))

            service.files().update(
                fileId=file_id, body={
                    'trashed': True}).execute()

            print('Trashed file: %s (%s)' % (file_name, file_id))

        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break


if __name__ == '__main__':
    try:
        main()
    except:
        os.system(
            """osascript -e 'display notification "Check it out" with title "Oh no! Drive Sync Failed"'""")
