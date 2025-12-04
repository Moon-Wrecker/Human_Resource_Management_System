"use client";

import { useState , useEffect} from "react";
import { Link} from "react-router-dom"
import jobService from "@/services/jobService"; 

import type {
  JobListing,
  JobListingsResponse,
  JobFilters,
  UpdateJobRequest,
} from "@/services/jobService";

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
import { set } from "date-fns";

type Job = {
  position: string;
  location: string;
  department: string;
  experience?: string;
  skills?: string;
  description?: string;
};



const departments = ["Engineering", "HR", "Finance", "Sales", "Marketing", "Opertions", "Product Management","Quality Assurance", "Customer Success", "Data Science", "Devops", "Legal", "Research and Development", "IT Support", "Business Intelligence"];
const locations = [
  "Remote",
  "Mumbai",
  "Chennai",
  "Bangalore",
  "Pune",
];

const JobListings = () => {
  const [search, setSearch] = useState("");
  const [filterDept, setFilterDept] = useState<string>("");
  const [filterLoc, setFilterLoc] = useState<string>("");
  const [selectedJob, setSelectedJob] = useState<JobListing | null>(null);
  const [showEdit, setShowEdit] = useState(false);
  const [showView, setShowView] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);

  const [jobsResponse, setJobsResponse] = useState<JobListingsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [editedJob, setEditedJob] = useState<UpdateJobRequest>({});

  const fetchJobs = async (page = currentPage, size = pageSize) => {
    try {
      setLoading(true);
      setError(null);

      const filters: JobFilters = {
        search: search || undefined,
        location: filterLoc || undefined,
        department_id: filterDept ? departments.indexOf(filterDept)+1: undefined,
        is_active: true,
        page,
        page_size: size>0? size : undefined,
      };

      const data = await jobService.getAllJobs(filters);
      setJobsResponse(data);
    } catch (e: any) {
      setError(e?.message || "Failed to load jobs");
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    setCurrentPage(1);
    fetchJobs();
  }, [search, filterLoc, filterDept]);

  useEffect(() => {
    fetchJobs(currentPage, pageSize);}, [currentPage, pageSize, search, filterLoc /*, filterDeptId */]);
  const jobs = jobsResponse?.jobs ?? [];
  const totalJobs = jobsResponse?.total ?? 0;
  const totalPages = pageSize > 0 ? Math.ceil(totalJobs / pageSize) : 1;

  const handlePageChange = (page: number) => {
    if (page >= 1 || page <= totalPages) {
      setCurrentPage(page);
    }
  };

const handleEditClick = (job: JobListing) => {
  setSelectedJob(job);
  setEditedJob({
    position: job.position,
    experience_required: job.experience_required,
    skills_required: job.skills_required,
    description: job.description,
    location: job.location,
    department_id: job.department_id,
    employment_type: job.employment_type as any,
    salary_range: job.salary_range,
    application_deadline: job.application_deadline,
    is_active: job.is_active,
  });
  setShowEdit(true);
};

const handleSave = async () => {
  if (!selectedJob) return;
  await jobService.updateJob(selectedJob.id, editedJob);
  setShowEdit(false);
  await fetchJobs();
};

const handleDelete = async (jobId: number) => {
  await jobService.deleteJob(jobId);
  await fetchJobs();
};

  return (
    <div className="min-h-screen bg-white">
      <div className="px-12 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold text-center mb-6">Job Listings</h1>
          <Link to={"/hr/add-new-job"} className="text-black underline font-medium text-lg"> Add New &rarr;</Link>
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
        {/* Jobs Table */}
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
            {jobs.map(job => (
              <TableRow key={job.id}>
                <TableCell>{job.position}</TableCell>
                <TableCell>{job.location}</TableCell>
                <TableCell>{job.department_name}</TableCell>
                <TableCell>
                  <button
                    className="underline mr-2"
                    onClick={() => { setSelectedJob(job); setShowView(true); }}
                  >
                    View
                  </button>
                  |
                  <button
                    className="underline mx-2"
                    onClick={() => handleEditClick(job)}
                  >
                    Edit
                  </button>
                  |
                  <button
                    className="underline ml-2 text-red-500"
                    onClick={() => handleDelete(job.id)}
                  >
                    Delete
                  </button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        {/* Pagination Controls */}
        <div className="flex justify-between items-center mt-8">
          <div className="text-sm text-gray-600">
            Showing {jobs.length > 0 ? (currentPage - 1) * pageSize + 1 : 0} to {Math.min(currentPage * pageSize, totalJobs)} of {totalJobs} jobs
          </div>
          
          <div className="flex gap-2 items-center">
            <button
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
              className="px-3 py-1 border rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
            >
              Previous
            </button>

            <div className="flex gap-1">
              {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => (
                <button
                  key={page}
                  onClick={() => handlePageChange(page)}
                  className={`px-3 py-1 border rounded ${
                    currentPage === page
                      ? "bg-blue-600 text-white"
                      : "hover:bg-gray-100"
                  }`}
                >
                  {page}
                </button>
              ))}
            </div>

            <button
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="px-3 py-1 border rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
            >
              Next
            </button>

            <select
              value={pageSize}
              onChange={e => {
                setPageSize(Number(e.target.value));
                setCurrentPage(1);
              }}
              className="border rounded px-2 py-1 ml-4"
            >
              <option value={5}>5 per page</option>
              <option value={10}>10 per page</option>
              <option value={25}>25 per page</option>
              <option value={50}>50 per page</option>
            </select>
          </div>
        </div>
      </div>

      {/* View Dialog */}
      <Dialog open={showView} onOpenChange={setShowView}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Job Post</DialogTitle>
          </DialogHeader>
          <DialogDescription>
            <div>
              <span className="font-semibold underline mr-1">Title:</span>
              {selectedJob?.position}
              <br />
              <span className="font-semibold underline mr-1">Experience Required:</span>
              {selectedJob?.experience_required}
              <br />
              <span className="font-semibold underline mr-1">Skills Required:</span>
              {selectedJob?.skills_required}
              <br />
              <div className="bg-gray-100 rounded p-2 mt-1">
                {selectedJob?.description}
              </div>
              <br />
            </div>
          </DialogDescription>
          <DialogFooter className="flex justify-end gap-3">
            <button
              className="px-4 py-2 bg-red-200 hover:bg-red-400 rounded font-medium"
              onClick={() => {handleDelete(selectedJob!.id) ; setShowView(false); }}
            >
              Delete
            </button>
            <DialogClose asChild>
              <button
                className="px-4 py-2 bg-gray-200 hover:bg-gray-400 rounded font-medium"
                onClick={() => { handleEditClick(selectedJob!); setShowView(false); }}
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
              {/* Edit Dialog inputs */}
              <input
                className="flex-1 ml-2 border rounded px-2 py-1"
                value={editedJob.position ?? ""}
                onChange={e => setEditedJob({ ...editedJob, position: e.target.value })}
              />

              <input
                className="flex-1 ml-2 border rounded px-2 py-1"
                value={editedJob.experience_required ?? ""}
                onChange={e => setEditedJob({ ...editedJob, experience_required: e.target.value })}
              />

              <input
                className="flex-1 ml-2 border rounded px-2 py-1"
                value={editedJob.skills_required ?? ""}
                onChange={e => setEditedJob({ ...editedJob, skills_required: e.target.value })}
              />

              <textarea
                className="w-full mt-1 border rounded px-2 py-1 bg-gray-100"
                rows={3}
                value={editedJob.description ?? ""}
                onChange={e => setEditedJob({ ...editedJob, description: e.target.value })}
              />

            </div>
          </DialogDescription>
          <DialogFooter>
            <DialogClose asChild>
              <button
                className="ml-auto flex items-center justify-end px-4 py-2 bg-black text-white rounded font-medium"
                onClick={handleSave}
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
