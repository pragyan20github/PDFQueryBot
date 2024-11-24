import React, { useState, useEffect } from "react";
import "./styles.css";

function App() {
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState("");
  const [question, setQuestion] = useState("");
  const [conversation, setConversation] = useState([]);
  const [uploadedPdfs, setUploadedPdfs] = useState([]); // List of uploaded PDFs
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchUploadedPdfs(); // Fetch uploaded PDFs on component load
  }, []);

  // Fetch the list of uploaded PDFs
  const fetchUploadedPdfs = async () => {
    try {
      const res = await fetch("http://localhost:8000/get_chats"); // Change this if necessary
      const data = await res.json();
      setUploadedPdfs(data.chats || []); // Assuming this will return a list of uploaded PDFs
    } catch (err) {
      console.error("Error fetching PDFs:", err);
    }
  };

  // Handle file change
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!file) {
      setError("Please select a PDF file first.");
      return;
    }

    setLoading(true);
    setError("");
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (data.message) {
        setUploadedPdfs((prev) => [...prev, data.filename]); // Add to the list
        setFilename(data.filename); // Set as active
        alert(data.message);
      } else {
        setError("Failed to upload the file. Please try again.");
      }
    } catch (err) {
      setError("Error uploading file.");
    } finally {
      setLoading(false);
    }
  };

  // Handle selecting a PDF and fetching the chat history
  const handleSelectPdf = async (pdf) => {
    setFilename(pdf); // Set active filename

    // Fetch chat history for the selected PDF
    try {
      setLoading(true);
      const res = await fetch(`http://localhost:8000/get_chats/${pdf}`);
      const data = await res.json();

      if (data && data.chats) {
        setConversation(data.chats); // Set the conversation with the fetched history
      } else {
        setConversation([]); // If no chats, reset conversation
      }
    } catch (err) {
      setError("Error fetching chat history.");
      setConversation([]); // Clear any previous conversation if an error occurs
    } finally {
      setLoading(false);
    }
  };

  // Handle asking a question
  const handleAskQuestion = async () => {
    if (!filename) {
      setError("Please select a PDF to ask a question.");
      return;
    }

    if (!question) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError("");

    // Temporarily add user's question to the conversation
    const userMessage = {
      type: "user",
      content: question,
    };
    setConversation((prev) => [...prev, userMessage]);

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename, question }),
      });

      const data = await res.json();
      const botMessage = {
        type: "bot",
        content: data.answer || "No answer available.",
      };

      setConversation((prev) => [...prev, botMessage]);
      setQuestion("");
    } catch (err) {
      setError("Error processing your question.");
    } finally {
      setLoading(false);
    }
  };

  // Handle starting a new chat
  const handleNewChat = () => {
    setConversation([]);
    setQuestion("");
  };

  return (
    <div className="app-container">
      {/* Taskbar */}
      <div className="taskbar">
        <h1 className="title">PDFQueryBot</h1>
        <button className="new-chat-btn" onClick={handleNewChat}>
          New Chat
        </button>
      </div>

      <div className="content">
        {/* Sidebar for PDF navigation */}
        <div className="sidebar">
          <h2>My PDFs</h2>
          <div className="pdf-list">
            {uploadedPdfs.map((pdf, index) => (
              <div
                key={index}
                className={`pdf-item ${pdf === filename ? "active" : ""}`}
                onClick={() => handleSelectPdf(pdf)}
              >
                {pdf}
              </div>
            ))}
          </div>
        </div>

        {/* Main content area */}
        <div className="main">
          {/* Upload Section */}
          <div className="upload-section">
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload} disabled={loading}>
              {loading ? "Uploading..." : "Upload PDF"}
            </button>
          </div>

          {/* Conversation Section */}
          <div className="conversation-section">
            {conversation.map((entry, index) => (
              <div
                key={index}
                className={`chat-entry ${
                  entry.type === "user" ? "user-message" : "bot-message"
                }`}
              >
                {entry.content}
              </div>
            ))}
          </div>

          {/* Ask Question Section */}
          <div className="ask-question-section">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask your question"
            />
            <button onClick={handleAskQuestion} disabled={loading}>
              {loading ? "Asking..." : "Ask"}
            </button>
          </div>

          {/* Error Display */}
          {error && <div className="error">{error}</div>}
        </div>
      </div>
    </div>
  );
}

export default App;
