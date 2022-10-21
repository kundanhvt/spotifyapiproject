import logging

import azure.functions as func
from azure.storage.blob import BlobServiceClient
from datetime import datetime


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")


    # downloading from scrape
    # print(myblob.read())

    conn_str ="DefaultEndpointsProtocol=https;AccountName=kundanstorage;AccountKey=QWkF1g4pHLh2KEwz8hnEM5kxa58qdz2nEKtX+u6jX/7Rkkp3frl9Lo2YsPH5CnfogCzFGz8ujH8P+AStudhZjg==;EndpointSuffix=core.windows.net"
    ## uploading when blobTrigger fire
    file = f'spotify_{datetime.now().timestamp()}_processed.json'
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    blob_client = blob_service_client.get_blob_client(container = 'procesed', blob=file) #myblob.read
    # print(file)
    # data =bytes(myblob.read(), 'utf-8')
    blob_client.upload_blob(myblob.read())






