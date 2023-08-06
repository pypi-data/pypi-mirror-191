import argparse
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def get_creds(client_secret_json_filename):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_json_filename, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def read_file_from_drive(file_id, client_secret_json_filename):
    creds = get_creds(client_secret_json_filename)
    if creds:
        service = build("drive", "v3", credentials=creds)
        request = service.files().get_media(fileId=file_id)
        file_content = request.execute()
        return file_content
    return None


def main():
    parser = argparse.ArgumentParser(description="Read a file from your personal Google Drive account")
    parser.add_argument("file_id", help="The document ID of the file to read")
    parser.add_argument("--client-secret-file", help="The client secret file (JSON)")
    args = parser.parse_args()
    file_content = read_file_from_drive(args.file_id, args.client_secret_file)
    if file_content:
        print(file_content)
    else:
        print("Error reading file")


if __name__ == "__main__":
    main()
