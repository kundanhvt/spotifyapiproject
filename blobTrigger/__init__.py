import logging
from textwrap import indent
import pyodbc

import azure.functions as func
from azure.storage.blob import BlobServiceClient
from datetime import datetime
import json


def upload_data_into_container(type, conn_str, data):
    file = f'spotify_{type}_{datetime.now().timestamp()}_processed.json'
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    blob_client = blob_service_client.get_blob_client(container = 'procesed', blob=file)
    upload_data =bytes(json.dumps(data,indent=4), 'utf-8')
    blob_client.upload_blob(upload_data)

def filter_data(data):
    single_data = []
    album_data = []
    new_str = data.decode('utf-8')
    dict_data = json.loads(new_str)
    for item in dict_data["albums"]["items"]:
        if item["album_type"] == "single":
            single_data.append(item)
        elif item["album_type"] == "album":
            album_data.append(item)
    return [single_data,album_data]

def remove_extra_single_quote(str_data):
    new_str=str_data.replace("'","")
    return new_str

def upload_data_into_sql_container(data):
    new_str = data.decode('utf-8')
    dict_data = json.loads(new_str)
    conn=None
    cursor=None
    try:
        conn = pyodbc.connect('Driver={SQL Server};Server=tcp:sqlserverkundan.database.windows.net,1433;Database=mydb2;Uid=kundan;Pwd=AmanSingh123#;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        cursor = conn.cursor()
        records = list()
        for item in dict_data["albums"]["items"]:
            for subitem in item['artists']:
                record = f"( '{subitem['id']}' ,'{item['album_type']}' ,'{subitem['href']}' ,'{remove_extra_single_quote(subitem['name'])}' ,'{subitem['type']}' ,'{subitem['uri']}')"
                records.append(record)
        query = 'insert into dbo.spotify_api_data (id,album_type,href,name,type,uri) values '
        query+=", ".join(records)
        query +=";"
        logging.info(query)
        cursor.execute(query)
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.commit()
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    conn_str ="DefaultEndpointsProtocol=https;AccountName=kundanstorage;AccountKey=QWkF1g4pHLh2KEwz8hnEM5kxa58qdz2nEKtX+u6jX/7Rkkp3frl9Lo2YsPH5CnfogCzFGz8ujH8P+AStudhZjg==;EndpointSuffix=core.windows.net"
    data = myblob.read()
    upload_data_into_sql_container(data) 
    single_data,ablum_data = filter_data(data)
    upload_data_into_container('single',conn_str,single_data)
    upload_data_into_container('album',conn_str,ablum_data)
    print("=============================")
