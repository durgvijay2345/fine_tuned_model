import { UploadCloud } from "lucide-react";
import { useState } from "react";

export default function UploadSection({ label, setFile }) {
  const [fileName, setFileName] = useState("");

  const handleFile = (e) => {
    const selected = e.target.files[0];
    setFile(selected);
    setFileName(selected?.name);
  };

  return (
    <div className="border-2 border-dashed border-indigo-500 p-8 rounded-2xl text-center">
      <UploadCloud size={40} className="mx-auto mb-4 text-indigo-500" />
      <p className="text-gray-400 mb-4">{label}</p>

      <input type="file" onChange={handleFile} />

      {fileName && (
        <p className="mt-4 text-green-500">
          Uploaded: {fileName}
        </p>
      )}
    </div>
  );
}