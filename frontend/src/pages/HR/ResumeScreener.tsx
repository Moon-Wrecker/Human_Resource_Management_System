"use client";

import { useState } from "react";

const roles = [
  "SDE-I",
  "SDE-II",
  "SDE-III",
  "Frontend Engineer",
  "Backend Engineer"
];

const ResumeScreenerUpload = () => {
  const [selectedRole, setSelectedRole] = useState("");
  const [jobDescFile, setJobDescFile] = useState<File | null>(null);
  const [resumeFiles, setResumeFiles] = useState<File[]>([]);
  const [uploadingIdx, setUploadingIdx] = useState<number | null>(0);

  // Simulate upload progress on first file
  const [progress, setProgress] = useState(70); // Hardcode for demo

  // Handle resume file uploads
  const handleResumeFiles = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setResumeFiles([...resumeFiles, ...Array.from(e.target.files)]);
    }
  };

  // Remove resume by index
  const handleRemoveResume = (idx: number) => {
    setResumeFiles(prev => prev.filter((_, i) => i !== idx));
  };

  return (
    <div className="min-h-screen bg-white flex flex-col items-center px-4 pt-12">
      {/* Page Title */}
      <h1 className="text-2xl font-bold mb-12">Resume Screener</h1>
      <form className="w-full max-w-2xl mx-auto">
        {/* Step 1: Select Role */}
        <div className="mb-8 flex gap-4 items-center">
          <span className="font-bold text-lg">1.</span>
          <select
            className="border rounded bg-gray-200 h-12 px-5 w-72 font-medium"
            value={selectedRole}
            onChange={e => setSelectedRole(e.target.value)}
          >
            <option value="">Select Role</option>
            {roles.map(role => (
              <option key={role} value={role}>{role}</option>
            ))}
          </select>
        </div>
        {/* Step 2: Upload JD */}
        <div className="mb-6 flex gap-4 items-center">
          <span className="font-bold text-lg">2.</span>
          <label
            htmlFor="jd-upload"
            className="flex-1 border rounded-xl h-24 flex items-center justify-center cursor-pointer bg-white hover:bg-gray-100"
          >
            <span className="text-3xl mr-2">&#128190;</span>
            <span className="font-medium text-lg">Upload Job Description</span>
            <input
              id="jd-upload"
              type="file"
              className="hidden"
              onChange={e => setJobDescFile(e.target.files?.[0] ?? null)}
            />
          </label>
        </div>
        {/* Step 3: Upload Resumes */}
        <div className="mb-8 flex gap-4 items-center">
          <span className="font-bold text-lg">3.</span>
          <label
            htmlFor="resume-upload"
            className="flex-1 border rounded-xl h-24 flex items-center justify-center cursor-pointer bg-white hover:bg-gray-100"
          >
            <span className="text-3xl mr-2">&#128190;</span>
            <span className="font-medium text-lg">Upload Resume Files</span>
            <input
              id="resume-upload"
              type="file"
              multiple
              className="hidden"
              onChange={handleResumeFiles}
            />
          </label>
        </div>
        <div className="flex flex-col gap-2 mb-8">
          {resumeFiles.map((file, idx) => (
            <div key={file.name + idx} className="flex items-center border rounded px-2 py-1 bg-white">
              <span className="font-medium">{file.name}</span>
              {idx === uploadingIdx ? (
                <span className="ml-3 text-xs text-gray-500">Uploading</span>) : null
              }
              {idx === uploadingIdx ? (
                <div className="h-2 w-48 bg-gray-200 rounded mx-2">
                  <div style={{ width: `${progress}%` }} className="bg-green-500 h-2 rounded"></div>
                </div>
              ) : null}
              <button
                type="button"
                className="ml-auto px-2 text-lg text-gray-500 hover:text-red-700"
                onClick={() => handleRemoveResume(idx)}
                title="remove"
              >
                ×
              </button>
            </div>
          ))}
        </div>
        <button
          type="button"
          className="bg-gray-300 px-7 py-2 rounded font-semibold hover:bg-gray-400 transition block mx-auto"
          onClick={() => alert("Uploading all files...")}
        >
          Upload
        </button>
      </form>
    </div>
  );
};

export default ResumeScreenerUpload;
