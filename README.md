# Setting Up the Frontend

## Setting Django Server Address:

1. Open the `FileUpload.js` file in the frontend code.

2. Locate the `handleUpload` function.

3. Modify the `axios.post` URL to point to your Django server address.
   
   Example:
   ```javascript
   axios.post('http://localhost:8000/api/upload/', formData, { ... })
   
# Setting Up the Backend

## Setting Azure Connection String and Container Name:

1. Open the `views.py` file in the backend code.

2. Locate the `upload_file` function.

3. Set the `azure_storage_connection_string` variable to your Azure Storage connection string.
   
   Example:
   ```python
   azure_storage_connection_string = "YOUR_AZURE_STORAGE_CONNECTION_STRING"

   ## The frontend will display error or success message and the backend will print out the error in case of an error
