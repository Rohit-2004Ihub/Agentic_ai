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
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/process-docx/", formData);
      console.log("📥 Backend response:", res.data);
      setResult(res.data);
    } catch (err) {
      console.error("❌ Upload error:", err);
      setError("Error uploading or processing the file.");
    } finally {
      setLoading(false);
    }
  };

  return (
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
          {result.case_study && (
            <>
              <h3>📘 Case Study</h3>
              <pre>{result.case_study}</pre>
            </>
          )}

          {result.refined_case_study && (
            <>
              <h3>🧠 Refined Case Study (RAG)</h3>
              <pre>{result.refined_case_study}</pre>
            </>
          )}

          {result.visuals && (
            <>
              <h3>🎯 Visual Aids</h3>
              <pre>{result.visuals}</pre>
            </>
          )}

          {result.pitch_feedback && (
            <>
              <h3>🎤 Pitch Feedback</h3>
              <pre>
                {typeof result.pitch_feedback === "string"
                  ? result.pitch_feedback
                  : JSON.stringify(result.pitch_feedback, null, 2)}
              </pre>
            </>
          )}

          {/* Fallback: if none of the structured fields exist */}
          {!result.case_study &&
            !result.refined_case_study &&
            !result.visuals &&
            !result.pitch_feedback && (
              <>
                <h3>📄 Output</h3>
                <pre>{JSON.stringify(result, null, 2)}</pre>
              </>
            )}
        </div>
      )}
    </div>
  );
}

export default App;
