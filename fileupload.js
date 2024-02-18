import React, { useState } from 'react';
import axios from 'axios';

function FileUpload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:8000/api/upload/', formData, {
        headers: {
          'Content-Type': 'Zip File',
        }
      });
      setUploadMessage(response.data); 
      console.log('File uploaded successfully:', response.data);
    } catch (error) {
      setUploadMessage('Error uploading file');
      console.log('Error uploading file:', error);
    }
  };

  return (
    <div>
      <h2>Upload a Zip File</h2>
      <input type="file" onChange={handleFileChange} accept=".zip" />
      <button onClick={handleUpload}>Upload</button>
      {uploadMessage && <p>{uploadMessage}</p>} 
    </div>
  );
}

export default FileUpload;
