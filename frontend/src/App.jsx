import { useState } from "react";
import FileUpload from "./components/FileUpload";
import Chat from "./components/Chat";
import "./App.css";

function App() {
  const [isDocumentUploaded, setIsDocumentUploaded] = useState(false);
  const [documentName, setDocumentName] = useState("");

  const handleUploadSuccess = (fileName) => {
    setIsDocumentUploaded(true);
    setDocumentName(fileName);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>📄 Document Q&A Assistant</h1>
        <p>Upload a PDF and ask questions about it</p>
      </header>
      <main className="app-main">
        {!isDocumentUploaded ? (
          <FileUpload onUploadSuccess={handleUploadSuccess} />
        ) : (
          <Chat documentName={documentName} />
        )}
      </main>
    </div>
  );
}

export default App;