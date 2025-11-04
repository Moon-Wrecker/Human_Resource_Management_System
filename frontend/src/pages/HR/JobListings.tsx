"use client";

import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from "@/components/ui/dialog";

import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";

type Job = {
  position: string;
  location: string;
  department: string;
  experience?: string;
  skills?: string;
  description?: string;
};

const jobs: Job[] = [
  {
    position: "Project Manager",
    location: "Remote/London, UK",
    department: "Operations",
    experience: "5 years",
    skills: "Leadership, Agile, Communication",
    description: "Manage multiple projects across global teams with high impact.",
  },
  {
    position: "Project Manager",
    location: "Gurugram",
    department: "Operations",
    experience: "4 years",
    skills: "PMP, Operations, Team Building",
    description: "Lead operations and strategic planning in Gurgaon HQ.",
  },
  {
    position: "SDE-I",
    location: "Remote/ Gurugram",
    department: "Engineering",
    experience: "2 years",
    skills: "HTML, CSS, JS and React JS",
    description: "Frontend engineering for scalable HR systems.",
  },
  {
    position: "Position 1",
    location: "Remote/London, UK",
    department: "HR",
    experience: "2 years",
    skills: "HR Systems, Payroll",
    description: "Supports team with recruitment and HR operations.",
  },
  {
    position: "Position 2",
    location: "Remote/Delhi",
    department: "Sales",
    experience: "1 year",
    skills: "Salesforce, Client Relations",
    description: "Drives sales for our digital HR products.",
  },
  {
    position: "Position 3",
    location: "Ghaziabad, UP",
    department: "Finance",
    experience: "3 years",
    skills: "Accounting, Excel, Financial Reporting",
    description: "Finances and vendor management for HR division.",
  },
];

const departments = ["Operations", "Engineering", "HR", "Sales", "Finance"];
const locations = [
  "Remote/London, UK",
  "Gurugram",
  "Remote/ Gurugram",
  "Remote/Delhi",
  "Ghaziabad, UP",
];

const JobListings = () => {
  const [search, setSearch] = useState<string>("");
  const [filterDept, setFilterDept] = useState<string>("");
  const [filterLoc, setFilterLoc] = useState<string>("");
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [showEdit, setShowEdit] = useState<boolean>(false);
  const [showView, setShowView] = useState<boolean>(false);

  // Editable state for the Edit modal
  const [editedJob, setEditedJob] = useState<Job>({
    position: "",
    location: "",
    department: "",
    experience: "",
    skills: "",
    description: "",
  });

  // Prepare filtered jobs
  const filteredJobs: Job[] = jobs.filter(
    (job) =>
      (search === "" ||
        job.position.toLowerCase().includes(search.toLowerCase())) &&
      (filterDept === "" || job.department === filterDept) &&
      (filterLoc === "" || job.location === filterLoc)
  );

  // Handle opening Edit modal with pre-filled job data
  const handleEditClick = (job: Job) => {
    setSelectedJob(job);
    setEditedJob({
      position: job.position,
      location: job.location,
      department: job.department,
      experience: job.experience ?? "",
      skills: job.skills ?? "",
      description: job.description ?? "",
    });
    setShowEdit(true);
  };

  return (
    <div className="min-h-screen bg-white">
      <div className="px-12 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold text-center mb-6">Job Listings</h1>
          <a
            href="/joblistings/add-new-job"
            className="text-black underline font-medium text-lg"
          >
            Add New &rarr;
          </a>
        </div>
        {/* Filter Row */}
        <div className="flex gap-4 mb-8">
          <div className="bg-gray-200 flex items-center rounded w-64 px-4 py-2">
            <input
              type="text"
              placeholder="Search Positions"
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="bg-gray-200 outline-none w-full px-1"
            />
            <span className="ml-2 text-gray-500">&#128269;</span>
          </div>
          <select
            value={filterLoc}
            onChange={e => setFilterLoc(e.target.value)}
            className="bg-gray-200 rounded w-48 px-4 py-2"
          >
            <option value="">Location</option>
            {locations.map(loc => (
              <option key={loc} value={loc}>{loc}</option>
            ))}
          </select>
          <select
            value={filterDept}
            onChange={e => setFilterDept(e.target.value)}
            className="bg-gray-200 rounded w-48 px-4 py-2"
          >
            <option value="">Department</option>
            {departments.map(dep => (
              <option key={dep} value={dep}>{dep}</option>
            ))}
          </select>
        </div>
        {/* Jobs Table (Shadcn table) */}
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Position</TableHead>
              <TableHead>Location</TableHead>
              <TableHead>Department</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredJobs.map((job, idx) => (
              <TableRow key={idx}>
                <TableCell>{job.position}</TableCell>
                <TableCell>{job.location}</TableCell>
                <TableCell>{job.department}</TableCell>
                <TableCell>
                  <button
                    className="underline mr-2"
                    onClick={() => { setSelectedJob(job); setShowView(true); }}
                  >View</button>
                  |
                  <button
                    className="underline mx-2"
                    onClick={() => handleEditClick(job)}
                  >Edit</button>
                  |
                  <button className="underline ml-2 text-red-500">Delete</button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      {/* View Dialog */}
      <Dialog open={showView} onOpenChange={setShowView}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Job Post</DialogTitle>
          </DialogHeader>
          <DialogDescription>
            <div>
              <div className="mb-2">
                <span className="font-semibold underline mr-1">Title:</span>
                {selectedJob?.position}
              </div>
              <div className="mb-2">
                <span className="font-semibold underline mr-1">Experience Required:</span>
                {selectedJob?.experience}
              </div>
              <div className="mb-2">
                <span className="font-semibold underline mr-1">Skills Required:</span>
                {selectedJob?.skills}
              </div>
              <div className="mb-2">
                <span className="font-semibold underline mr-1">Job Description:</span>
                <div className="bg-gray-100 rounded p-2 mt-1">{selectedJob?.description}</div>
              </div>
            </div>
          </DialogDescription>
          <DialogFooter className="flex justify-end gap-3">
            <button
              className="px-4 py-2 bg-red-200 hover:bg-red-400 rounded font-medium"
              onClick={() => setShowView(false)}
            >
              Delete
            </button>
            <DialogClose asChild>
              <button
                className="px-4 py-2 bg-gray-200 hover:bg-gray-400 rounded font-medium"
                onClick={() => { setShowEdit(true); setShowView(false); }}
              >
                Edit
              </button>
            </DialogClose>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Edit Dialog */}
      <Dialog open={showEdit} onOpenChange={setShowEdit}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Edit Job Post</DialogTitle>
          </DialogHeader>
          <DialogDescription>
            <div className="mb-2 flex items-center">
              <span className="font-semibold min-w-[130px]">Title:</span>
              <input 
                className="flex-1 ml-2 border rounded px-2 py-1" 
                value={editedJob.position} onChange={e=>setEditedJob({ ...editedJob, position: e.target.value })} 
              />
            </div>
            <div className="mb-2 flex items-center">
              <span className="font-semibold min-w-[130px]">Experience Required:</span>
              <input 
                className="flex-1 ml-2 border rounded px-2 py-1" 
                value={editedJob.experience} onChange={e=>setEditedJob({ ...editedJob, experience: e.target.value })} 
              />
            </div>
            <div className="mb-2 flex items-center">
              <span className="font-semibold min-w-[130px]">Skills Required:</span>
              <input 
                className="flex-1 ml-2 border rounded px-2 py-1" 
                value={editedJob.skills} onChange={e=>setEditedJob({ ...editedJob, skills: e.target.value })} 
              />
            </div>
            <div className="mb-3">
              <span className="font-semibold min-w-[130px] block">Job Description:</span>
              <textarea 
                className="w-full mt-1 border rounded px-2 py-1 bg-gray-100" 
                rows={3}
                value={editedJob.description} onChange={e=>setEditedJob({ ...editedJob, description: e.target.value })}
              />
            </div>
          </DialogDescription>
          <DialogFooter>
            <DialogClose asChild>
              <button
                className="ml-auto flex items-center justify-end px-4 py-2 bg-black text-white rounded font-medium"
                onClick={() => setShowEdit(false)}
              >
                Save &rarr;
              </button>
            </DialogClose>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default JobListings;
