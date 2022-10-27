import json
from lib2to3.pgen2 import token
import logging
from urllib import response

import azure.functions as func
from azure.storage.blob import BlobClient
from azure.storage.blob import BlobServiceClient
import requests
from datetime import datetime
from .token import SpotifyAPI

client_id = "67362eb92fdf4d51ab0aac3a2066be1a"
client_secret = "ebc05e60d89748dab3845c6558bcbd0b"

def get_spotify_response():
    token_obj= SpotifyAPI(client_id,client_secret)
    token_obj.extract_access_token()
    headers  = {
        'Authorization': f'Bearer {token_obj.access_token}' 
    }
    print(headers)
    response = requests.get("https://api.spotify.com/v1/browse/new-releases", headers=headers)
    return response


def upload_data_into_container(conn_str, data):
    file = f'spotify_{datetime.now().timestamp()}_scraped.json'
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    blob_client = blob_service_client.get_blob_client(container = 'scrape', blob=file)
    upload_data =bytes(json.dumps(data,indent=4), 'utf-8')
    blob_client.upload_blob(upload_data)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    conn_str = "DefaultEndpointsProtocol=https;AccountName=kundanstorage;AccountKey=QWkF1g4pHLh2KEwz8hnEM5kxa58qdz2nEKtX+u6jX/7Rkkp3frl9Lo2YsPH5CnfogCzFGz8ujH8P+AStudhZjg==;EndpointSuffix=core.windows.net"

    response = get_spotify_response()
    if response.status_code == 200:
        upload_data_into_container(conn_str,response.json())
    return func.HttpResponse('success fine!')
