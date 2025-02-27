import React, { useState } from "react";
import axios from "axios";
import "./index.css";

function App() {
  const [file, setFile] = useState(null);
  const [encryptedData, setEncryptedData] = useState("");
  const [decryptedImage, setDecryptedImage] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleEncrypt = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post("http://localhost:5000/encrypt", formData);
    setEncryptedData(response.data.encrypted_data);
  };

  const handleDecrypt = async () => {
    const response = await axios.post(
      "http://localhost:5000/decrypt",
      { encrypted_data: encryptedData },
      { responseType: "blob" }
    );
    setDecryptedImage(URL.createObjectURL(response.data));
  };

  return (
    <div className="container">
      <h1>Image Encryption & Decryption</h1>
      <input type="file" onChange={handleFileChange} />
      <button className="encrypt" onClick={handleEncrypt}>Encrypt Image</button>

      {encryptedData && (
        <>
          <h3>Encrypted Data:</h3>
          <textarea readOnly value={encryptedData}></textarea>
          <button className="decrypt" onClick={handleDecrypt}>Decrypt Image</button>
        </>
      )}

      {decryptedImage && (
        <div>
          <h3>Decrypted Image:</h3>
          <img src={decryptedImage} alt="Decrypted" style={{ width: "100%", marginTop: "10px" }} />
        </div>
      )}
    </div>
  );
}

export default App;
