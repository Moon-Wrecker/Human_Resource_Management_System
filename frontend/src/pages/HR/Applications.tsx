"use client";

import { useState } from "react";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";

// Application type
type Application = {
  id: number;
  applicant: string;
  position: string;
  department: string;
  appliedOn: string;
  source: string;
  resumeUrl: string;
};

// Sample data
const initialApplications: Application[] = [
  {
    id: 1,
    applicant: "Person 1",
    position: "Project Manager",
    department: "Engineering",
    appliedOn: "11-09-2025",
    source: "Referral",
    resumeUrl: "/resumes/person1.pdf",
  },
  {
    id: 2,
    applicant: "Person 2",
    position: "Project Manager",
    department: "Engineering",
    appliedOn: "12-09-2025",
    source: "Self-Applied",
    resumeUrl: "/resumes/person2.pdf",
  },
  {
    id: 3,
    applicant: "Person 3",
    position: "SDE-I",
    department: "Engineering",
    appliedOn: "23-09-2025",
    source: "Self-Applied",
    resumeUrl: "/resumes/person3.pdf",
  },
  {
    id: 4,
    applicant: "Person 4",
    position: "Position 1",
    department: "Finance",
    appliedOn: "28-09-2025",
    source: "Self-Applied",
    resumeUrl: "/resumes/person4.pdf",
  },
  {
    id: 5,
    applicant: "Person 5",
    position: "Position 2",
    department: "Sales",
    appliedOn: "30-09-2025",
    source: "Referral",
    resumeUrl: "/resumes/person5.pdf",
  },
  {
    id: 6,
    applicant: "Person 6",
    position: "Position 3",
    department: "Finance",
    appliedOn: "01-10-2025",
    source: "Self-Applied",
    resumeUrl: "/resumes/person6.pdf",
  },
];

// Dialog for viewing application
const ViewApplicationDialog = ({
  open,
  onClose,
  app,
  onAccept,
  onReject,
}: {
  open: boolean;
  onClose: () => void;
  app: Application | null;
  onAccept: () => void;
  onReject: () => void;
}) => {
  if (!open || !app) return null;
  return (
    <div className="fixed inset-0 bg-black bg-opacity-20 flex items-center justify-center z-50">
      <div className="bg-[#e9e9ea] rounded-2xl w-[430px] shadow-xl relative p-2">
        {/* Header */}
        <div className="flex items-center justify-between px-5 pt-4 pb-3 border-b">
          <span className="font-medium text-lg">View Application</span>
          <button onClick={onClose} className="w-7 h-7 flex items-center justify-center text-xl hover:bg-gray-300 rounded-full">
            ×
          </button>
        </div>
        {/* Content */}
        <div className="p-6 pt-4 text-black space-y-3">
          <div>
            <span className="font-semibold underline">Applicant Name:</span>
            &nbsp; {app.applicant}
          </div>
          <div>
            <span className="font-semibold underline">Position:</span>
            &nbsp; {app.position}
          </div>
          <div>
            <span className="font-semibold underline">Department:</span>
            &nbsp; {app.department}
          </div>
          <div>
            <span className="font-semibold underline">Applied On:</span>
            &nbsp; {app.appliedOn}
          </div>
          <div>
            <span className="font-semibold underline">Source:</span>
            &nbsp; {app.source}
          </div>
          <div>
            <span className="font-semibold underline">Resume:</span>
            <a
              href={app.resumeUrl}
              download
              className="ml-4 bg-gray-200 px-4 py-1.5 rounded font-semibold hover:bg-gray-300 transition inline-flex items-center"
              target="_blank"
              rel="noopener noreferrer"
            >
              Download <span className="ml-2">⬇️</span>
            </a>
          </div>
          <div className="flex justify-end gap-4 mt-6">
            <button
              onClick={onReject}
              className="bg-gray-200 px-6 py-2 rounded font-semibold border hover:bg-gray-300"
            >
              Reject
            </button>
            <button
              onClick={onAccept}
              className="bg-gray-200 px-6 py-2 rounded font-semibold border hover:bg-gray-300"
            >
              Accept
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const Applications = () => {
  const [applications] = useState<Application[]>(initialApplications);
  const [selectedApp, setSelectedApp] = useState<Application | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  // Filtering/search state (implementation can be expanded)
  const [search, setSearch] = useState("");
  const [role, setRole] = useState("");
  const [source, setSource] = useState("");
  const [timePeriod, setTimePeriod] = useState("");

  const filteredApps = applications.filter(app =>
    (search === "" || app.applicant.toLowerCase().includes(search.toLowerCase())) &&
    (role === "" || app.position === role) &&
    (source === "" || app.source === source)
    // time period filtering can be added if dates are in a sortable format
  );

  return (
    <div className="min-h-screen bg-white flex flex-col items-center px-4 pt-12">
      <h1 className="text-2xl font-bold mb-10">Applications</h1>
      {/* Filters */}
      <div className="flex gap-4 items-center mb-8 w-full max-w-5xl">
        <input
          type="text"
          className="bg-gray-200 rounded px-4 h-10 flex-1"
          placeholder="Search Applicants"
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        <select value={role} onChange={e => setRole(e.target.value)} className="bg-gray-200 rounded h-10 px-4">
          <option value="">Role/Position</option>
          {/* Populate as needed */}
        </select>
        <select value={source} onChange={e => setSource(e.target.value)} className="bg-gray-200 rounded h-10 px-4">
          <option value="">Source</option>
          <option value="Referral">Referral</option>
          <option value="Self-Applied">Self-Applied</option>
        </select>
        <select value={timePeriod} onChange={e => setTimePeriod(e.target.value)} className="bg-gray-200 rounded h-10 px-4">
          <option value="">Time Period</option>
          {/* Future implementation */}
        </select>
      </div>
      {/* Applications Table */}
      <div className="w-full max-w-5xl">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Applicant</TableHead>
              <TableHead>Position</TableHead>
              <TableHead>Source</TableHead>
              <TableHead>Applied on</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredApps.map(app => (
              <TableRow key={app.id}>
                <TableCell>{app.applicant}</TableCell>
                <TableCell>{app.position}</TableCell>
                <TableCell>{app.source}</TableCell>
                <TableCell>{app.appliedOn}</TableCell>
                <TableCell>
                  <button
                    className="underline font-medium"
                    onClick={() => {
                      setSelectedApp(app);
                      setDialogOpen(true);
                    }}
                  >
                    View
                  </button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      {/* View Dialog */}
      <ViewApplicationDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        app={selectedApp}
        onAccept={() => { setDialogOpen(false); }}
        onReject={() => { setDialogOpen(false); }}
      />
    </div>
  );
};

export default Applications;
