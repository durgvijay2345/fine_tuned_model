import { useState } from "react";
import UploadSection from "./UploadSection";
import ResultCard from "./ResultCard";
import Loader from "./Loader";

export default function CompareSection() {
  const [mode, setMode] = useState("text");

  const [text1, setText1] = useState("");
  const [text2, setText2] = useState("");

  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const API_BASE= "https://shubham-t-fine-tuned-model.hf.space"
  const handleAnalyze = async () => {
    setLoading(true);
    setResult(null);

    try {
      let response;

      // ========================
      // TEXT MODE
      // ========================
      if (mode === "text") {
        if (!text1 || !text2) {
          alert("Please enter both texts");
          setLoading(false);
          return;
        }

        response = await fetch(`${API_BASE}/predict`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text1: text1,
            text2: text2,
          }),
        });
      }

      // ========================
      // FILE MODE
      // ========================
      if (mode === "file") {
        if (!file1 || !file2) {
          alert("Please upload both files");
          setLoading(false);
          return;
        }

        const formData = new FormData();
        formData.append("file1", file1);
        formData.append("file2", file2);

        response = await fetch(`${API_BASE}/predict-file`, {
          method: "POST",
          body: formData,
        });
      }

      if (!response.ok) {
        throw new Error("Backend error");
      }

      const data = await response.json();

      setResult(data);

    } catch (error) {
      console.error("API Error:", error);
      alert("Failed to connect to backend");
    }

    setLoading(false);
  };

  return (
    <div className="space-y-10">

      {/* =========================
          MODE TOGGLE
      ========================== */}
      <div className="flex gap-4">
        <button
          onClick={() => setMode("text")}
          className={`px-6 py-2 rounded-xl transition ${
            mode === "text"
              ? "bg-indigo-600 text-white"
              : "bg-slate-700 text-gray-300"
          }`}
        >
          Text Mode
        </button>

        <button
          onClick={() => setMode("file")}
          className={`px-6 py-2 rounded-xl transition ${
            mode === "file"
              ? "bg-indigo-600 text-white"
              : "bg-slate-700 text-gray-300"
          }`}
        >
          File Mode
        </button>
      </div>

      {/* =========================
          TEXT MODE
      ========================== */}
      {mode === "text" && (
        <div className="grid md:grid-cols-2 gap-6">
          <textarea
            className="bg-slate-800 p-4 rounded-xl h-40 focus:outline-none"
            placeholder="Enter First Text..."
            value={text1}
            onChange={(e) => setText1(e.target.value)}
          />

          <textarea
            className="bg-slate-800 p-4 rounded-xl h-40 focus:outline-none"
            placeholder="Enter Second Text..."
            value={text2}
            onChange={(e) => setText2(e.target.value)}
          />
        </div>
      )}

      {/* =========================
          FILE MODE
      ========================== */}
      {mode === "file" && (
        <div className="grid md:grid-cols-2 gap-6">
          <UploadSection
            label="Upload First File"
            setFile={setFile1}
          />
          <UploadSection
            label="Upload Second File"
            setFile={setFile2}
          />
        </div>
      )}

      {/* =========================
          ANALYZE BUTTON
      ========================== */}
      <button
        onClick={handleAnalyze}
        className="px-8 py-3 bg-indigo-600 hover:bg-indigo-700 transition text-white rounded-xl"
      >
        Analyze
      </button>

      {/* =========================
          LOADER
      ========================== */}
      {loading && <Loader />}

      {/* =========================
          RESULT
      ========================== */}
      {result && <ResultCard result={result} />}
    </div>
  );
}
