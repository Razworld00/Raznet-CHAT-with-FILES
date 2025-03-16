import React, { useState } from 'react';
import { ChainlitClient } from '@chainlit/react-client';

function App() {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => setFile(event.target.files[0]);
  const handleUpload = async () => {
    if (file) {
      const client = new ChainlitClient({ url: 'http://localhost:8000' });
      await client.sendMessage({ type: 'file_upload', files: [file] });
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={!file}>Upload</button>
      <ChainlitClient url="http://localhost:8000" />
    </div>
  );
}

export default App;
