"use client";

import { useState } from "react";

const Policies = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  return (
    <div className="min-h-screen bg-[#fafafa] flex flex-col items-center px-4 pt-12">
      {/* Page Title */}
      <h1 className="text-2xl font-bold mb-12">Policies</h1>

      {/* Download Current Policy Section */}
      <div className="w-full max-w-xl mx-auto mb-12">
        <div className="flex items-center bg-white border rounded-xl px-6 py-5 shadow">
          <span className="font-bold text-lg mr-4">
            Download current policy document :
          </span>
          <button
            className="bg-gray-300 px-6 py-2 rounded font-semibold hover:bg-gray-400 transition ml-auto"
            onClick={() => {
              // Replace with actual download logic
              window.open("/policy.pdf", "_blank");
            }}
          >
            Download
          </button>
        </div>
      </div>

      {/* Update Policy Section */}
      <h2 className="text-xl font-bold mb-6">Update Policies</h2>
      <div className="flex flex-col items-center mb-6">
        <label
          htmlFor="upload-policy-file"
          className="w-56 h-56 border-2 border-gray-400 flex flex-col items-center justify-center rounded-xl cursor-pointer bg-white hover:bg-gray-100 transition"
        >
          <span className="text-4xl mb-2">&#128206;</span>
          <span className="font-medium text-lg">
            Upload policy document
          </span>
          <input
            id="upload-policy-file"
            type="file"
            className="hidden"
            onChange={e => setSelectedFile(e.target.files?.[0] ?? null)}
          />
        </label>
        {selectedFile && (
          <span className="mt-2 text-gray-600">{selectedFile.name}</span>
        )}
      </div>
      <button
        className="bg-gray-300 px-7 py-2 rounded font-semibold hover:bg-gray-400 transition"
        disabled={!selectedFile}
        onClick={() => {
          // Replace with actual upload logic
          if (selectedFile) {
            alert(`Uploading: ${selectedFile.name}`);
          }
        }}
      >
        Upload
      </button>
    </div>
  );
};

export default Policies;
