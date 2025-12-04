"use client";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import jobService from "@/services/jobService"; // adjust import path

const AddJobForm = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    position: "",
    department_id: "",
    location: "",
    employment_type: "full-time",
    experience_required: "",
    skills_required: "",
    salary_range: "",
    description: "",
    application_deadline: "",
    is_active: true,
  });

  const [aiDescription, setAiDescription] = useState("");

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  const handleGenerateJD = () => {
    const jd = `Job Description for ${formData.position || "the given role"}:\n\n` +
      `Experience Required: ${formData.experience_required}\n` +
      `Skills: ${formData.skills_required}\n\n` +
      `This is an AI-generated job description. Please review and edit as needed.`;
    setAiDescription(jd);
    setFormData((prev) => ({ ...prev, description: jd }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.position || !formData.department_id || !formData.location) {
      setError("Please fill in all required fields.");
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const payload = {
        ...formData,
        department_id: parseInt(formData.department_id, 10),
        employment_type: formData.employment_type as "full-time" | "part-time" | "contract" | "internship",
      };
      await jobService.createJob(payload);
      navigate("/hr/joblistings");
    } catch (err: any) {
      setError(err.message || "Failed to create job listing.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex flex-col items-center px-4 pt-12">
      <Link
        to="/hr/joblistings"
        className="text-black underline font-medium self-start mb-4"
      >
        ⬅️ Back to Job Listings
      </Link>

      <div className="mb-8 w-full max-w-2xl">
        <h1 className="text-3xl font-bold mb-2">Add a New Position</h1>
        <p className="text-gray-600">Fill in the details to create a new job listing.</p>
      </div>

      {error && (
        <div className="w-full max-w-2xl mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      <form className="w-full max-w-2xl" onSubmit={handleSubmit}>
        <div className="grid grid-cols-2 gap-4 mb-6">
          {/* Position */}
          <div>
            <label className="block font-medium mb-2">Position Name *</label>
            <input
              className="border w-full h-10 px-3 rounded"
              type="text"
              name="position"
              placeholder="e.g., Senior Software Engineer"
              value={formData.position}
              onChange={handleChange}
              required
            />
          </div>

          {/* Department */}
          <div>
            <label className="block font-medium mb-2">Department *</label>
            <select
              className="border w-full h-10 px-3 rounded"
              name="department_id"
              value={formData.department_id}
              onChange={handleChange}
              required
            >
              <option value="">Select Department</option>
              <option value="1">Engineering</option>
              <option value="2">HR</option>
              <option value="3">Finance</option>
              <option value="4">Sales</option>
              <option value="5">Marketing</option>
              <option value="6">Opertions</option>
              <option value="7">Product Management</option>
              <option value="8">Quality Assurance</option>
              <option value="9">Customer Success</option>
              <option value="10">Data Science</option>
              <option value="11">Devops</option>
              <option value="12">Legal</option>
              <option value="13">Research and Development</option>
              <option value="14">IT Support</option>
              <option value="15">Business Intelligence</option>
            </select>
          </div>

          {/* Location */}
          <div>
            <label className="block font-medium mb-2">Location *</label>
            <select
              className="border w-full h-10 px-3 rounded"
              name="location"
              value={formData.location}
              onChange={handleChange}
              required
            >
              <option value="">Select Location</option>
              <option value="Remote">Remote</option>
              <option value="Mumbai">Mumbai</option>
              <option value="Chennai">Chennai</option>
              <option value="Bangalore">Bangalore</option>
              <option value="Pune">Pune</option>
            </select>
          </div>

          {/* Employment Type */}
          <div>
            <label className="block font-medium mb-2">Employment Type</label>
            <select
              className="border w-full h-10 px-3 rounded"
              name="employment_type"
              value={formData.employment_type}
              onChange={handleChange}
            >
              <option value="full-time">Full-time</option>
              <option value="part-time">Part-time</option>
              <option value="contract">Contract</option>
              <option value="internship">Internship</option>
            </select>
          </div>

          {/* Experience Required */}
          <div>
            <label className="block font-medium mb-2">Experience Required</label>
            <input
              className="border w-full h-10 px-3 rounded"
              type="text"
              name="experience_required"
              placeholder="e.g., 3-5 years"
              value={formData.experience_required}
              onChange={handleChange}
            />
          </div>

          {/* Salary Range */}
          <div>
            <label className="block font-medium mb-2">Salary Range</label>
            <input
              className="border w-full h-10 px-3 rounded"
              type="text"
              name="salary_range"
              placeholder="e.g., 50,000 - 70,000"
              value={formData.salary_range}
              onChange={handleChange}
            />
          </div>

          {/* Skills Required */}
          <div className="col-span-2">
            <label className="block font-medium mb-2">Skills Required</label>
            <input
              className="border w-full h-10 px-3 rounded"
              type="text"
              name="skills_required"
              placeholder="e.g., React, Node.js, SQL (comma-separated)"
              value={formData.skills_required}
              onChange={handleChange}
            />
          </div>

          {/* Application Deadline */}
          <div>
            <label className="block font-medium mb-2">Application Deadline</label>
            <input
              className="border w-full h-10 px-3 rounded"
              type="date"
              name="application_deadline"
              value={formData.application_deadline}
              onChange={handleChange}
            />
          </div>

          {/* Active Status */}
          <div className="flex items-center">
            <label className="flex items-center cursor-pointer">
              <input
                type="checkbox"
                name="is_active"
                checked={formData.is_active}
                onChange={handleChange}
                className="w-5 h-5 mr-2"
              />
              <span className="font-medium">Active</span>
            </label>
          </div>
        </div>

        {/* Job Description */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <label className="block font-medium">Job Description</label>
            <button
              type="button"
              onClick={handleGenerateJD}
              className="text-blue-600 underline text-sm font-medium"
            >
              ✨ Generate with AI
            </button>
          </div>
          <textarea
            className="border w-full h-32 px-3 py-2 rounded resize-none"
            name="description"
            placeholder="Write job description..."
            value={formData.description}
            onChange={handleChange}
            rows={6}
          />
        </div>

        {/* Buttons */}
        <div className="flex gap-4 justify-center mb-8">
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white font-medium px-8 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Creating..." : "Create Job Listing"}
          </button>
          <Link
            to="/hr/joblistings"
            className="bg-gray-300 text-black font-medium px-8 py-2 rounded hover:bg-gray-400"
          >
            Cancel
          </Link>
        </div>
      </form>
    </div>
  );
};

export default AddJobForm;