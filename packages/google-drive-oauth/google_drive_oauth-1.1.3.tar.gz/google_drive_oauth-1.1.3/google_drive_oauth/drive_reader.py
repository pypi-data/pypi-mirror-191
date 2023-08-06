import argparse

from google_drive_oauth.get_service import get_service


def read_file_from_drive(file_id, client_secret_json_filename):
    try:
        service = get_service(client_secret_json_filename)
        request = service.files().get_media(fileId=file_id)
        file_content = request.execute()
        return file_content
    except Exception as e:
        print('Exception, drive_reader.py, read_file_from_drive', e)
        return None


def main():
    parser = argparse.ArgumentParser(description="Read a file from your personal Google Drive account")
    parser.add_argument("file_id", help="The document ID of the file to read")
    parser.add_argument("client_secret_file", help="The client secret file (JSON)")
    args = parser.parse_args()
    file_content = read_file_from_drive(args.file_id, args.client_secret_file)
    if file_content:
        print('file_content', file_content)
    else:
        print("Error reading file")


if __name__ == "__main__":
    main()
