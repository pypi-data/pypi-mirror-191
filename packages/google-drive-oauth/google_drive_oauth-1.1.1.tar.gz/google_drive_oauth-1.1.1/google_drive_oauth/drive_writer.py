import argparse
from googleapiclient.http import MediaFileUpload
from get_service import get_service


def upload_binary_file_to_drive(file_path, file_name, client_secret_json_filename, parent_folder_id=None):
    service = get_service(client_secret_json_filename)
    media = MediaFileUpload(file_path, mimetype='application/octet-stream')
    file_metadata = {'name': file_name}
    if parent_folder_id:
        file_metadata['parents'] = [parent_folder_id]
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File ID: {file.get("id")}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a binary file to Google Drive")
    parser.add_argument("file_path", help="The path to the binary file to upload")
    parser.add_argument("file_name", help="The name of the file in Google Drive")
    parser.add_argument("client_secret_file", help="The client secret file (JSON)")
    parser.add_argument("--parent-folder-id", help="The ID of the parent folder in Google Drive")
    args = parser.parse_args()
    # Call the upload function and pass in the Drive API service and optional parent folder ID
    upload_binary_file_to_drive(args.file_path, args.file_name, args.client_secret_file, args.parent_folder_id)
