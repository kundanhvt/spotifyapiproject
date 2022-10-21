
from azure.storage.blob import BlobServiceClient

conn_str ='DefaultEndpointsProtocol=https;AccountName=kundanstorage;AccountKey=QHuydUW3psYs+m1z7vEuKVftLMK/jBHdYZEle+h5viFtz4TArdU6+FgmtlVKwbYtJ2RXGYrPssP0+AStTyq9Xg==;EndpointSuffix=core.windows.net'
blob_service_client_instance = BlobServiceClient.from_connection_string(conn_str)
blob_client_instance = blob_service_client_instance.get_blob_client(container = 'scrape', blob='kundan.json', snapshot=None)
blob_data = blob_client_instance.download_blob()
data = blob_data.readall()
print(data)
