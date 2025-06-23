import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setError("Please upload a .docx file");
      return;
    }

    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/process-docx/", formData);
      console.log("📥 Agent Output:", res.data.result);
      setResult(res.data.result);
    } catch (err) {
      console.error("❌ Upload error:", err);
      setError("Error uploading or processing the file.");
    } finally {
      setLoading(false);
    }
  };

  const renderOutput = (label, content) => {
    if (!content) return null;

    return (
      <div className="section">
        <h3>{label}</h3>
        <pre>{typeof content === "string" ? content : JSON.stringify(content, null, 2)}</pre>
      </div>
    );
  };

  return (
    <>
      {/* Floating background blobs */}
      <div className="blob blob1"></div>
      <div className="blob blob2"></div>

      <div className="container">
        <h2>📄 AI-Powered Case Study Generator</h2>

        <input
          type="file"
          accept=".docx"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Processing..." : "Upload and Generate"}
        </button>

        {error && <p className="error">{error}</p>}

        {result && (
          <div className="result">
            {renderOutput("📊 Structured Summary", result.structured_summary)}
            {renderOutput("📘 Case Study", result.case_study)}
            {renderOutput("🧠 Refined Case Study (RAG)", result.refined_case_study)}
            {renderOutput("🎯 Visual Aids", result.visuals)}
            {renderOutput("🎤 Pitch Feedback", result.pitch_feedback)}

            {!result.structured_summary &&
              !result.case_study &&
              !result.refined_case_study &&
              !result.visuals &&
              !result.pitch_feedback && (
                <>
                  <h3>📋 Full Raw Output</h3>
                  <pre>{JSON.stringify(result, null, 2)}</pre>
                </>
              )}
          </div>
        )}
      </div>
    </>
  );
}

export default App;
