"use client";

import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, X } from "lucide-react";
import { useState } from "react";

type Job = {
  id: number;
  title: string;
  department: string;
  location: string;
  type: string;
  postedOn: string;
  link: string;
};

const jobListings = [
  {
    id: 1,
    title: "Frontend Developer",
    department: "Engineering",
    location: "Mumbai, India",
    type: "Full-time",
    postedOn: "2025-10-30",
    link: "https://company.com/jobs/frontend-developer",
  },
  {
    id: 2,
    title: "Backend Developer",
    department: "Engineering",
    location: "Bangalore, India",
    type: "Full-time",
    postedOn: "2025-10-28",
    link: "https://company.com/jobs/backend-developer",
  },
  {
    id: 3,
    title: "UI/UX Designer",
    department: "Design",
    location: "Remote",
    type: "Contract",
    postedOn: "2025-10-25",
    link: "https://company.com/jobs/ui-ux-designer",
  },
  {
    id: 4,
    title: "HR Executive",
    department: "Human Resources",
    location: "Pune, India",
    type: "Full-time",
    postedOn: "2025-10-22",
    link: "https://company.com/jobs/hr-executive",
  },
  {
    id: 5,
    title: "Product Manager",
    department: "Product",
    location: "Hyderabad, India",
    type: "Full-time",
    postedOn: "2025-10-20",
    link: "https://company.com/jobs/product-manager",
  },
  {
    id: 6,
    title: "Data Analyst",
    department: "Analytics",
    location: "Delhi, India",
    type: "Full-time",
    postedOn: "2025-10-18",
    link: "https://company.com/jobs/data-analyst",
  },
  {
    id: 7,
    title: "Customer Success Manager",
    department: "Support",
    location: "Remote",
    type: "Full-time",
    postedOn: "2025-10-15",
    link: "https://company.com/jobs/customer-success-manager",
  },
  {
    id: 8,
    title: "Marketing Specialist",
    department: "Marketing",
    location: "Chennai, India",
    type: "Part-time",
    postedOn: "2025-10-12",
    link: "https://company.com/jobs/marketing-specialist",
  },
  {
    id: 9,
    title: "DevOps Engineer",
    department: "Engineering",
    location: "Remote",
    type: "Full-time",
    postedOn: "2025-10-10",
    link: "https://company.com/jobs/devops-engineer",
  },
  {
    id: 10,
    title: "Finance Associate",
    department: "Finance",
    location: "Ahmedabad, India",
    type: "Internship",
    postedOn: "2025-10-08",
    link: "https://company.com/jobs/finance-associate",
  },
];

const submitSearch = (e: React.FormEvent) => {
  e.preventDefault();
};

const handleJobApply = () => {};

export default function JobListingsTable() {
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);

  const handleOpenModal = (job: Job) => setSelectedJob(job);
  const handleCloseModal = () => setSelectedJob(null);

  return (
    <div className="w-full max-w-5xl mx-auto mt-10 flex flex-col justify-center items-center gap-4">
      <form
        onSubmit={submitSearch}
        className="w-[50%] flex items-center justify-center gap-1"
      >
        <Input placeholder="Search by location, title and department.. " />
        <Button type="submit" variant="outline">
          <Search />
        </Button>
      </form>

      <Table>
        <TableCaption>Open Positions as of November 2025</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[220px]">Position</TableHead>
            <TableHead>Department</TableHead>
            <TableHead>Location</TableHead>
            <TableHead>Type</TableHead>
            <TableHead>Posted On</TableHead>
            <TableHead className="text-right px-5">Action</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {jobListings.map((job) => (
            <TableRow key={job.id}>
              <TableCell className="font-medium">{job.title}</TableCell>
              <TableCell>{job.department}</TableCell>
              <TableCell>{job.location}</TableCell>
              <TableCell>{job.type}</TableCell>
              <TableCell>
                {new Date(job.postedOn).toLocaleDateString("en-IN", {
                  day: "2-digit",
                  month: "short",
                  year: "numeric",
                })}
              </TableCell>
              <TableCell className="text-right">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleOpenModal(job)}
                >
                  Apply
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {/* Modal */}
      {selectedJob && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex justify-center items-center z-50 animate-in fade-in duration-200">
          {/* Modal Card */}
          <div className="relative bg-white dark:bg-neutral-900 rounded-xl shadow-2xl p-8 w-full max-w-md mx-4 border border-gray-200 dark:border-neutral-700">
            {/* Close Button */}
            <button
              onClick={handleCloseModal}
              className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            {/* Header */}
            <div className="mb-6 text-center">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
                Apply for {selectedJob.title}
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                {selectedJob.department} • {selectedJob.location}
              </p>
            </div>

            {/* Body */}
            <div className="space-y-2 mb-8 text-sm text-gray-600 dark:text-gray-300">
              <div className="flex justify-between">
                <span className="font-medium text-gray-700 dark:text-gray-200">
                  Department:
                </span>
                <span>{selectedJob.department}</span>
              </div>
              <div className="flex justify-between">
                <span className="font-medium text-gray-700 dark:text-gray-200">
                  Location:
                </span>
                <span>{selectedJob.location}</span>
              </div>
              <div className="flex justify-between">
                <span className="font-medium text-gray-700 dark:text-gray-200">
                  Type:
                </span>
                <span>{selectedJob.type}</span>
              </div>
              <div className="flex justify-between">
                <span className="font-medium text-gray-700 dark:text-gray-200">
                  Posted On:
                </span>
                <span>
                  {new Date(selectedJob.postedOn).toLocaleDateString("en-IN", {
                    day: "2-digit",
                    month: "short",
                    year: "numeric",
                  })}
                </span>
              </div>
            </div>

            {/* Upload Resume */}
            <div className="mb-6">
              <label
                htmlFor="resume-upload"
                className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2"
              >
                Upload Resume
              </label>
              <input
                id="resume-upload"
                type="file"
                accept=".pdf,.doc,.docx"
                className="w-full text-sm text-gray-600 dark:text-gray-300 border border-gray-300 dark:border-neutral-700 rounded-md p-2 file:mr-3 file:py-1 file:px-3 file:rounded-md file:border-0 file:bg-gray-900 file:text-white hover:file:bg-gray-800 cursor-pointer"
              />
            </div>

            {/* Footer Actions */}
            <div className="flex justify-end gap-1">
              <Button
                variant="outline"
                onClick={handleCloseModal}
                className="px-5 border-gray-300 dark:border-neutral-600"
              >
                Cancel
              </Button>
              <Button onClick={() => handleJobApply()}>Apply Now</Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
