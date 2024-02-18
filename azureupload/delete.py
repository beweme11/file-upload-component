import os
from zipfile import ZipFile
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

azure_storage_connection_string = "DefaultEndpointsProtocol=https;AccountName=interntest;AccountKey=taxo/Bu8Yv1B0gigOcnpexj2PMa3Z8AP/LI+F3z/hKa9py3NmJWxpVWtStKeN+j1wqp0DjVJCpb0+AStcrva4A==;EndpointSuffix=core.windows.net"  # Your Azure Storage account connection string
container_name = "zipfilestorage"  
zip_file_path = "/content/Django-Polls-App.zip" 

with ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall("temp_extracted")

def upload_files_recursively(local_directory, container_client):
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            local_file_path = os.path.join(root, file)
            azure_blob_name = os.path.relpath(local_file_path, local_directory).replace("\\", "/")
            blob_client = container_client.get_blob_client(azure_blob_name)
            with open(local_file_path, "rb") as data:
                blob_client.upload_blob(data)

blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)

container_client = blob_service_client.get_container_client(container_name)
upload_files_recursively("temp_extracted", container_client)

for root, dirs, files in os.walk("temp_extracted", topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
os.rmdir("temp_extracted")

print("Files uploaded successfully.")