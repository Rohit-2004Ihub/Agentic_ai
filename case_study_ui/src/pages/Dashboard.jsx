import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  Upload,
  FileText,
  Brain,
  Target,
  Mic,
  Clock,
  User,
  Loader2,
  AlertCircle,
  CheckCircle,
  LogOut
} from "lucide-react";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [expandedIndex, setExpandedIndex] = useState(null);
  const navigate = useNavigate();

  const user_id =
    typeof window !== "undefined" ? localStorage.getItem("user_id") : null;

  const handleUpload = async () => {
    if (!file || !user_id) {
      setError("Please upload a .docx file and login first.");
      return;
    }

    setLoading(true);
    setError("");
    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", user_id);

    try {
      const res = await axios.post("http://localhost:8000/process-docx/", formData);
      setResult(res.data.result);
      fetchHistory();
    } catch (err) {
      console.error("❌ Upload error:", err);
      setError("Error uploading or processing the file.");
    } finally {
      setLoading(false);
    }
  };

  const fetchHistory = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/user-history/?user_id=${user_id}`);
      setHistory(res.data.history);
    } catch (err) {
      console.error("❌ Error fetching history:", err);
    }
  };

  useEffect(() => {
    if (user_id) fetchHistory();
    else navigate("/login");
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user_id");
    navigate("/login");
  };

  const renderOutput = (icon, label, content) =>
    content && (
      <div className="bg-white rounded-xl p-6 shadow-lg border border-red-100 hover:shadow-xl transition-shadow">
        <div className="flex items-center gap-3 mb-4">
          {icon}
          <h3 className="text-lg font-semibold text-gray-800">{label}</h3>
        </div>
        <div className="bg-red-50 rounded-lg p-4 border border-red-100">
          <pre className="whitespace-pre-wrap text-sm text-gray-700 font-mono leading-relaxed">
            {typeof content === "string" ? content : JSON.stringify(content, null, 2)}
          </pre>
        </div>
      </div>
    );

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-white py-10 px-4 flex flex-col items-center">
      <div className="w-full max-w-5xl">

        {/* Header */}
        <div className="text-center mb-10 relative">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="p-3 bg-red-600 rounded-full shadow-md">
              <Brain className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold text-gray-800">Case Study Generator</h1>
          </div>
          <p className="text-gray-600 text-lg">Turn your project documents into professional case studies</p>

          <button
            onClick={handleLogout}
            className="absolute top-0 right-0 flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white font-medium px-4 py-2 rounded-lg shadow transition"
          >
            <LogOut className="w-4 h-4" />
            Logout
          </button>
        </div>

        {/* Upload Section */}
        <div className="bg-white border border-red-100 shadow-xl rounded-2xl p-8 mb-10">
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Upload Project Document (.docx)
          </label>

          <div className="relative">
            <input
              type="file"
              accept=".docx"
              onChange={(e) => setFile(e.target.files[0])}
              className="hidden"
              id="file-upload"
            />
            <label
              htmlFor="file-upload"
              className="flex items-center justify-center w-full px-6 py-4 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-red-500 hover:bg-red-50 transition-colors"
            >
              <div className="text-center">
                <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                <p className="text-gray-600">{file ? file.name : "Click to upload .docx file"}</p>
                <p className="text-sm text-gray-400 mt-1">Drag & drop or browse your files</p>
              </div>
            </label>
          </div>

          <button
            onClick={handleUpload}
            disabled={loading || !file}
            className="w-full mt-6 bg-red-600 hover:bg-red-700 disabled:bg-red-300 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 transform hover:scale-[1.02] disabled:scale-100 disabled:cursor-not-allowed shadow-lg hover:shadow-xl flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <FileText className="w-5 h-5" />
                Upload & Generate
              </>
            )}
          </button>

          {/* Alerts */}
          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-red-500" />
              <p className="text-red-700">{error}</p>
            </div>
          )}

          {result && !loading && (
            <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-500" />
              <p className="text-green-700">Case study generated successfully!</p>
            </div>
          )}
        </div>

        {/* Generated Output */}
        {result && (
          <div className="mb-10">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
              <Target className="w-6 h-6 text-red-600" />
              Generated Results
            </h2>
            <div className="grid gap-6">
              {renderOutput(<FileText className="w-5 h-5 text-red-600" />, "Structured Summary", result.structured_summary)}
              {renderOutput(<Brain className="w-5 h-5 text-red-600" />, "Case Study", result.case_study)}
              {renderOutput(<Target className="w-5 h-5 text-red-600" />, "Refined Case Study (RAG)", result.refined_case_study)}
              {renderOutput(<Upload className="w-5 h-5 text-red-600" />, "Visual Aids", result.visuals)}
              {renderOutput(<Mic className="w-5 h-5 text-red-600" />, "Pitch Feedback", result.pitch_feedback)}
            </div>
          </div>
        )}

        {/* History Section */}
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-red-100">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
            <Clock className="w-6 h-6 text-red-600" />
            Your History
          </h2>

          {history.length === 0 ? (
            <div className="text-center py-8">
              <User className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">No documents processed yet.</p>
              <p className="text-sm text-gray-400 mt-1">Upload your first document to get started!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {history.map((item, idx) => (
                <div key={idx} className="bg-red-50 rounded-lg p-6 border border-red-200 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <FileText className="w-5 h-5 text-red-600" />
                      <h3 className="font-semibold text-gray-800">{item.document_name}</h3>
                    </div>
                    <span className="text-sm text-gray-500">{new Date(item.timestamp).toLocaleString()}</span>
                  </div>

                  <p className="text-gray-600 text-sm leading-relaxed whitespace-pre-wrap mb-2">
                    {expandedIndex === idx
                      ? item.refined_text
                      : `${item.refined_text.slice(0, 200)}...`}
                  </p>

                  <div className="flex justify-between items-center text-xs text-gray-500">
                    <div className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      <span>Generated on {new Date(item.timestamp).toLocaleDateString()}</span>
                    </div>
                    <button
                      onClick={() =>
                        setExpandedIndex(expandedIndex === idx ? null : idx)
                      }
                      className="text-red-600 font-medium hover:underline"
                    >
                      {expandedIndex === idx ? "Show less" : "Read more"}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
