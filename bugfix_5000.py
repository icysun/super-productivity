import requests
from requests.auth import HTTPBasicAuth
import json

class WebDAVClient:
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(self.username, self.password)

    def list_files(self, path):
        try:
            response = self.session.propfind(url=self.url + path, props=[
                ('allprop', None),
                ('resourcetype', None)
            ], depth=1)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def upload_file(self, path, file_data):
        try:
            files = {'file': ('file', file_data, 'text/plain')}
            response = self.session.put(url=self.url + path, files=files)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

# Test cases
def test_webdav_client():
    url = "https://dav.jianguoyun.com/dav/"
    username = "your_username"
    password = "your_password"

    # Create a WebDAV client instance
    client = WebDAVClient(url, username, password)

    # List files in the root directory
    print("Listing files in root directory:")
    print(client.list_files("/"))

    # Upload a file
    file_data = b"Hello, WebDAV!"
    print("Uploading a file:")
    print(client.upload_file("/test_file.txt", file_data))

# Run the test cases
test_webdav_client()