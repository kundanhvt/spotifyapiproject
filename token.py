import requests
from datetime import datetime, timedelta
import base64


class SpotifyAPI():
    access_token = None
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs) -> None:
        super().__init__(*args,**kwargs)
        self.client_id=client_id
        self.client_secret=client_secret

    def get_client_credentials(self):
        """
            return Base 64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        client_creads = f"{client_id}:{client_secret}"
        client_creads_b64 = base64.b64encode(client_creads.encode())
        return client_creads_b64.decode()

    def get_token_header(self):
        client_creads_b64 = self.get_client_credentials()
        return {
            "Authorization" : f"Basic {client_creads_b64}"  #Basic <base64 encoded client_id:client_secret>
        }
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def extract_access_token(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_header = self.get_token_header()
        r = requests.post(token_url, data=token_data, headers=token_header)
        print(r)
        valid_request = r.status_code in range(200,299)
        if valid_request:
            data = r.json()
            now = datetime.now()
            self.access_token = data['access_token']
            return True
        else:
            return False

