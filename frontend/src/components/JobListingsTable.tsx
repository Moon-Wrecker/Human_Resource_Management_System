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
import { Search, X, Loader2 } from "lucide-react";
import { useState, useEffect } from "react";
import jobService from "@/services/jobService";
import type { JobListing } from "@/services/jobService";
import { useToast } from "@/hooks/use-toast";
import { Badge } from "@/components/ui/badge";

export default function JobListingsTable() {
  const { toast } = useToast();
  const [jobs, setJobs] = useState<JobListing[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedJob, setSelectedJob] = useState<JobListing | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [resumeFile, setResumeFile] = useState<File | null>(null);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const response = await jobService.getAllJobs({ 
        is_active: true,
        page_size: 50
      });
      setJobs(response.jobs);
    } catch (error: any) {
      console.error("Error fetching jobs:", error);
      const errorMessage = error?.response?.data?.detail || error?.message || "Failed to load job listings";
      toast({
        variant: "destructive",
        title: "Error",
        description: errorMessage,
      });
    } finally {
      setLoading(false);
    }
  };

  const submitSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await jobService.getAllJobs({ 
        search: searchTerm,
        is_active: true,
        page_size: 50
      });
      setJobs(response.jobs);
    } catch (error: any) {
      console.error("Error searching jobs:", error);
      const errorMessage = error?.response?.data?.detail || error?.message || "Search failed";
      toast({
        variant: "destructive",
        title: "Error",
        description: errorMessage,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleJobApply = () => {
    if (!resumeFile) {
      toast({
        variant: "destructive",
        title: "Resume Required",
        description: "Please upload your resume before applying",
      });
      return;
    }

    toast({
      title: "Application Submitted!",
      description: `Your application for ${selectedJob?.position} has been submitted successfully.`,
    });
    handleCloseModal();
  };

  const handleOpenModal = (job: JobListing) => {
    setSelectedJob(job);
    setResumeFile(null);
  };
  
  const handleCloseModal = () => {
    setSelectedJob(null);
    setResumeFile(null);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        toast({
          variant: "destructive",
          title: "File Too Large",
          description: "Resume must be less than 5MB",
        });
        return;
      }
      setResumeFile(file);
    }
  };

  if (loading && jobs.length === 0) {
    return (
      <div className="w-full max-w-5xl mx-auto mt-10 flex justify-center items-center">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="w-full max-w-5xl mx-auto mt-10 flex flex-col justify-center items-center gap-4">
      <form
        onSubmit={submitSearch}
        className="w-[50%] flex items-center justify-center gap-1"
      >
        <Input 
          placeholder="Search by location, title and department.." 
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <Button type="submit" variant="outline" disabled={loading}>
          {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search />}
        </Button>
      </form>

      <Table>
        <TableCaption>
          {jobs.length > 0 ? `${jobs.length} Open Positions` : 'No job openings available'}
        </TableCaption>
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
          {jobs.map((job) => (
            <TableRow key={job.id}>
              <TableCell className="font-medium">{job.position}</TableCell>
              <TableCell>{job.department_name || 'N/A'}</TableCell>
              <TableCell>{job.location || 'Remote'}</TableCell>
              <TableCell>
                <Badge variant={jobService.getEmploymentTypeBadge(job.employment_type).color as any}>
                  {jobService.getEmploymentTypeBadge(job.employment_type).label}
                </Badge>
              </TableCell>
              <TableCell>
                {jobService.formatDate(job.posted_date)}
              </TableCell>
              <TableCell className="text-right">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleOpenModal(job)}
                >
                  View
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
          <div className="relative bg-white dark:bg-neutral-900 rounded-xl shadow-2xl p-8 w-full max-w-2xl mx-4 border border-gray-200 dark:border-neutral-700 max-h-[90vh] overflow-y-auto">
            {/* Close Button */}
            <button
              onClick={handleCloseModal}
              className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            {/* Header */}
            <div className="mb-6">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
                {selectedJob.position}
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                {selectedJob.department_name} • {selectedJob.location}
              </p>
            </div>

            {/* Job Details */}
            <div className="space-y-3 mb-6 text-sm text-gray-600 dark:text-gray-300">
              <div className="flex justify-between items-center py-2 border-b border-gray-200 dark:border-neutral-700">
                <span className="font-medium text-gray-700 dark:text-gray-200">Department:</span>
                <span>{selectedJob.department_name || 'N/A'}</span>
              </div>
              <div className="flex justify-between items-center py-2 border-b border-gray-200 dark:border-neutral-700">
                <span className="font-medium text-gray-700 dark:text-gray-200">Location:</span>
                <span>{selectedJob.location || 'Remote'}</span>
              </div>
              <div className="flex justify-between items-center py-2 border-b border-gray-200 dark:border-neutral-700">
                <span className="font-medium text-gray-700 dark:text-gray-200">Type:</span>
                <Badge variant={jobService.getEmploymentTypeBadge(selectedJob.employment_type).color as any}>
                  {jobService.getEmploymentTypeBadge(selectedJob.employment_type).label}
                </Badge>
              </div>
              {selectedJob.experience_required && (
                <div className="flex justify-between items-center py-2 border-b border-gray-200 dark:border-neutral-700">
                  <span className="font-medium text-gray-700 dark:text-gray-200">Experience:</span>
                  <span>{selectedJob.experience_required}</span>
                </div>
              )}
              {selectedJob.salary_range && (
                <div className="flex justify-between items-center py-2 border-b border-gray-200 dark:border-neutral-700">
                  <span className="font-medium text-gray-700 dark:text-gray-200">Salary Range:</span>
                  <span>{selectedJob.salary_range}</span>
                </div>
              )}
              <div className="flex justify-between items-center py-2 border-b border-gray-200 dark:border-neutral-700">
                <span className="font-medium text-gray-700 dark:text-gray-200">Posted On:</span>
                <span>{jobService.formatDate(selectedJob.posted_date)}</span>
              </div>
              {selectedJob.application_deadline && (
                <div className="flex justify-between items-center py-2 border-b border-gray-200 dark:border-neutral-700">
                  <span className="font-medium text-gray-700 dark:text-gray-200">Deadline:</span>
                  <span className={jobService.isDeadlineApproaching(selectedJob.application_deadline) ? 'text-warning' : ''}>
                    {jobService.formatDate(selectedJob.application_deadline)}
                  </span>
                </div>
              )}
            </div>

            {/* Description */}
            {selectedJob.description && (
              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Description:</h3>
                <p className="text-sm text-gray-600 dark:text-gray-300 whitespace-pre-wrap">
                  {selectedJob.description}
                </p>
              </div>
            )}

            {/* Skills */}
            {selectedJob.skills_required && (
              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Required Skills:</h3>
                <p className="text-sm text-gray-600 dark:text-gray-300">
                  {selectedJob.skills_required}
                </p>
              </div>
            )}

            {/* Upload Resume */}
            <div className="mb-6">
              <label
                htmlFor="resume-upload"
                className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2"
              >
                Upload Resume <span className="text-red-500">*</span>
              </label>
              <input
                id="resume-upload"
                type="file"
                accept=".pdf,.doc,.docx"
                onChange={handleFileChange}
                className="w-full text-sm text-gray-600 dark:text-gray-300 border border-gray-300 dark:border-neutral-700 rounded-md p-2 file:mr-3 file:py-1 file:px-3 file:rounded-md file:border-0 file:bg-gray-900 file:text-white hover:file:bg-gray-800 cursor-pointer"
              />
              {resumeFile && (
                <p className="text-xs text-green-600 mt-1">
                  Selected: {resumeFile.name}
                </p>
              )}
            </div>
            
            {/* Footer Actions */}
            <div className="flex justify-end gap-2">
              <Button
                variant="outline"
                onClick={handleCloseModal}
                className="px-5 border-gray-300 dark:border-neutral-600"
              >
                Cancel
              </Button>
              <Button onClick={handleJobApply} disabled={!resumeFile}>
                Apply Now
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
