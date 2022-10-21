import base64
import requests
from datetime import datetime, timedelta

client_id = "67362eb92fdf4d51ab0aac3a2066be1a"
client_secret = "ebc05e60d89748dab3845c6558bcbd0b"
token_url = 'https://accounts.spotify.com/api/token'

# client_creads = f"{client_id}:{client_secret}"
# client_creads_b64 = base64.b64encode(client_creads.encode())


# method = ""
# token_data = {
#     "grant_type": "client_credentials"
# }
# token_header = {
#     "Authorization" : f"Basic {client_creads_b64.decode()}"  #Basic <base64 encoded client_id:client_secret>
# }

# r = requests.post(token_url, data=token_data, headers=token_header)
# token_response_data = r.json()

# now = datetime.now()
# access_token = token_response_data['access_token']
# expire_in = token_response_data['expires_in']
# expires = now + timedelta(seconds=expire_in)

# did_expire = expires < now

# print(did_expire)


class SpotifyAPI():
    access_token = None
    access_token_expires =  datetime.now()
    access_token_did_expire = True
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
            expire_in = data['expires_in']
            expires = now + timedelta(seconds=expire_in)
            self.access_token_expires = expires
            self.access_token_did_expire = expires < now
            return True
        else:
            return False


obj = SpotifyAPI(client_id,client_secret)
obj.extract_access_token()
print(obj.access_token)
headers  = {
    'Authorization': f'Bearer {obj.access_token}' 
}
print(headers)
response = requests.get("https://api.spotify.com/v1/browse/new-releases", headers=headers)
print(response.json())
