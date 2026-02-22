import { useEffect, useState } from "react";

export default function ResultCard({ result }) {
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    setTimeout(() => setAnimate(true), 100);
  }, []);

  const sem = (result.semantic_similarity * 100).toFixed(2);
  const lex = (result.lexical_similarity * 100).toFixed(2);
  const final = (result.final_similarity * 100).toFixed(2);

  const isPlag = result.classification === "Plagiarized";

  const getColor = (value) => {
    if (value >= 80) return "bg-red-600";
    if (value >= 60) return "bg-yellow-500";
    return "bg-green-600";
  };

  return (
    <div className="mt-10 p-8 rounded-2xl bg-slate-900 shadow-2xl space-y-8">

      <h2 className="text-2xl font-semibold">
        Similarity Breakdown
      </h2>

      {/* Semantic Graph */}
      <div>
        <p className="mb-2">Semantic Similarity: {sem}%</p>
        <div className="w-full bg-gray-700 h-4 rounded-full overflow-hidden">
          <div
            className={`h-4 transition-all duration-1000 ${getColor(sem)}`}
            style={{ width: animate ? `${sem}%` : "0%" }}
          />
        </div>
      </div>

      {/* Lexical Graph */}
      <div>
        <p className="mb-2">Lexical Similarity: {lex}%</p>
        <div className="w-full bg-gray-700 h-4 rounded-full overflow-hidden">
          <div
            className={`h-4 transition-all duration-1000 ${getColor(lex)}`}
            style={{ width: animate ? `${lex}%` : "0%" }}
          />
        </div>
      </div>

      {/* Final Graph */}
      <div>
        <p className="mb-2 font-semibold">
          Final Similarity Score: {final}%
        </p>
        <div className="w-full bg-gray-700 h-6 rounded-full overflow-hidden">
          <div
            className={`h-6 transition-all duration-1000 ${getColor(final)}`}
            style={{ width: animate ? `${final}%` : "0%" }}
          />
        </div>
      </div>

      {/* Classification Badge */}
      <div
        className={`px-6 py-3 rounded-xl text-center text-lg font-semibold ${
          isPlag
            ? "bg-red-600 text-white"
            : "bg-green-600 text-white"
        }`}
      >
        {result.classification}
      </div>

    </div>
  );
}