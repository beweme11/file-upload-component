import os
from zipfile import ZipFile
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from azure.storage.blob import BlobServiceClient


@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            zip_uploaded_file = request.FILES['file']
            print(f"uploading file {zip_uploaded_file.name} ...")

            with ZipFile(zip_uploaded_file, 'r') as zip_ref:
                first_folder = zip_ref.namelist()[0].split('/')[0]
                extracted_directory_path = os.path.join("temp_extracted", zip_uploaded_file.name[:-4],zip_uploaded_file.name[:-4] )
                extracted_directory_path_topass = os.path.join("temp_extracted", zip_uploaded_file.name[:-4])
                zip_ref.extractall(extracted_directory_path)

            azure_storage_connection_string = "DefaultEndpointsProtocol=https;AccountName=interntest;AccountKey=taxo/Bu8Yv1B0gigOcnpexj2PMa3Z8AP/LI+F3z/hKa9py3NmJWxpVWtStKeN+j1wqp0DjVJCpb0+AStcrva4A==;EndpointSuffix=core.windows.net"
            container_name = "apistorage4"
            blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
            container_client = blob_service_client.get_container_client(container_name)
            upload_files_recursively(extracted_directory_path_topass, container_client, "")

            print("Files uploaded successfully.")
            #cleanup extracted files
            cleanup_temp_files(extracted_directory_path)
            return HttpResponse('File uploaded successfully!')
        except Exception as e:
            print("Error uploading file: ", e)
            return HttpResponse('An error occurred during file upload.', status=500)
    else:
        return HttpResponse('No file provided.', status=400)

def upload_files_recursively(local_directory, container_client, relative_path):
    for root, _, files in os.walk(local_directory):
        for file in files:
            local_file_path = os.path.join(root, file)
            # remove the leading directory (local_directory) from the local file path
            relative_file_path = os.path.relpath(local_file_path, local_directory)
            # construct the blob name using the relative file path within the extracted directory structure
            blob_name = os.path.join(relative_path, relative_file_path)
            # replace backslashes with forward slashes (for Windows paths)
            blob_name = blob_name.replace("\\", "/")
            # upload the file to the container with the constructed blob name
            with open(local_file_path, "rb") as data:
                blob_client = container_client.get_blob_client(blob_name)
                blob_client.upload_blob(data)


def cleanup_temp_files(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(directory)
