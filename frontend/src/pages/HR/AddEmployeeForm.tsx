"use client";

import { useState } from "react";
import { UploadCloud } from "lucide-react";
const departments = ["Finance", "HR", "Operations", "Sales", "Engineering"];

const AddEmployeeForm = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [department, setDepartment] = useState("");
  const [role, setRole] = useState("");
  const [team, setTeam] = useState("");
  const [manager, setManager] = useState("");
  const [aadhar, setAadhar] = useState<File | null>(null);
  const [pan, setPan] = useState<File | null>(null);

  return (
    <div className="min-h-screen bg-white flex flex-col items-center px-4 pt-12">
      <a href="/employees-list" className="text-black underline font-medium self-start mb-4">
        ⬅️ Back to Employee List
      </a>
      <h1 className="text-2xl font-bold mb-8 text-center">Add New Employee</h1>
      <form className="w-full max-w-xl mx-auto">
        <div className="grid grid-cols-2 gap-x-6 gap-y-4">
          <label className="text-right pt-2 font-medium underline">Name</label>
          <input
            className="border w-full h-12 px-3 rounded bg-gray-100"
            type="text"
            placeholder="Employee Name"
            value={name}
            onChange={e => setName(e.target.value)}
          />
          <label className="text-right pt-2 font-medium underline">Email</label>
          <input
            className="border w-full h-12 px-3 rounded bg-gray-100"
            type="email"
            placeholder="Employee Email"
            value={email}
            onChange={e => setEmail(e.target.value)}
          />
          <label className="text-right pt-2 font-medium underline">Phone No.</label>
          <input
            className="border w-full h-12 px-3 rounded bg-gray-100"
            type="text"
            placeholder="Phone No."
            value={phone}
            onChange={e => setPhone(e.target.value)}
          />
          <label className="text-right pt-2 font-medium underline">Department</label>
          <select
            className="border w-full h-12 px-3 rounded bg-gray-100"
            value={department}
            onChange={e => setDepartment(e.target.value)}
          >
            <option value="">Select department</option>
            {departments.map(dep => (
              <option key={dep} value={dep}>{dep}</option>
            ))}
          </select>
          <label className="text-right pt-2 font-medium underline">Position/Role</label>
          <input
            className="border w-full h-12 px-3 rounded bg-gray-100"
            type="text"
            placeholder="Assign a Role"
            value={role}
            onChange={e => setRole(e.target.value)}
          />
          <label className="text-right pt-2 font-medium underline">Team</label>
          <input
            className="border w-full h-12 px-3 rounded bg-gray-100"
            type="text"
            placeholder="Assign a Team"
            value={team}
            onChange={e => setTeam(e.target.value)}
          />
          <label className="text-right pt-2 font-medium underline">Manager</label>
          <input
            className="border w-full h-12 px-3 rounded bg-gray-100"
            type="text"
            placeholder="Assign a Manager"
            value={manager}
            onChange={e => setManager(e.target.value)}
          />
        </div>
        {/* Upload Documents */}
        <div className="flex items-center mt-5 gap-6">
          <span className="font-medium underline min-w-[160px] text-right block">Upload Documents:</span>
          <label className="font-bold flex items-center gap-2 bg-white rounded px-3 py-2 cursor-pointer">
            Aadhar <UploadCloud className="inline w-4 h-4" />
            <input
              type="file"
              className="hidden"
              onChange={e => setAadhar(e.target.files?.[0] ?? null)}
              accept=".pdf,.jpg,.jpeg,.png"
            />
          </label>
          <label className="font-bold flex items-center gap-2 bg-white rounded px-3 py-2 cursor-pointer">
            PAN <UploadCloud className="inline w-4 h-4" />
            <input
              type="file"
              className="hidden"
              onChange={e => setPan(e.target.files?.[0] ?? null)}
              accept=".pdf,.jpg,.jpeg,.png"
            />
          </label>
        </div>
        {/* Add Button */}
        <div className="flex justify-end mt-8">
          <button
            type="submit"
            className="bg-white border border-gray-400 rounded px-8 py-3 font-semibold text-lg flex items-center gap-1 hover:bg-black hover:text-white transition"
          >
            Add +
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddEmployeeForm;
