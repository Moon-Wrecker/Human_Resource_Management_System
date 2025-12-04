"use client";

import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
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
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { format, set } from "date-fns";
import { Calendar as CalendarIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";

import departmentService, {
  type Department,
} from "@/services/departmentService";

const locations = ["Remote", "Mumbai", "Chennai", "Bangalore", "Pune"];

const JobListings = () => {
  const [search, setSearch] = useState("");
  const [filterDeptId, setFilterDeptId] = useState<string>("");
  const [filterLoc, setFilterLoc] = useState<string>("all-locations");
  const [selectedJob, setSelectedJob] = useState<JobListing | null>(null);
  const [showEdit, setShowEdit] = useState(false);
  const [showView, setShowView] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [departments, setDepartments] = useState<Department[]>([]);

  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        const response = await departmentService.getAllDepartments();
        setDepartments(response.departments);
      } catch (error) {
        console.error("Failed to fetch departments", error);
      }
    };
    fetchDepartments();
  }, []);

  const [jobsResponse, setJobsResponse] = useState<JobListingsResponse | null>(
    null,
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [editedJob, setEditedJob] = useState<UpdateJobRequest>({});
  const [editDeadline, setEditDeadline] = useState<Date>();

  const fetchJobs = async (page = currentPage, size = pageSize) => {
    try {
      setLoading(true);
      setError(null);

      const filters: JobFilters = {
        search: search || undefined,
        location: (filterLoc && filterLoc !== 'all-locations') ? filterLoc : undefined,
        department_id: filterDeptId ? Number(filterDeptId) : undefined,
        is_active: true,
        page,
        page_size: size > 0 ? size : undefined,
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
  }, [search, filterLoc, filterDeptId]);

  useEffect(() => {
    fetchJobs(currentPage, pageSize);
  }, [currentPage, pageSize, search, filterLoc, filterDeptId]);
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
    if (job.application_deadline) {
      setEditDeadline(new Date(job.application_deadline));
    } else {
      setEditDeadline(undefined);
    }
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
          <Link
            to={"/hr/add-new-job"}
            className="text-black underline font-medium text-lg"
          >
            {" "}
            Add New &rarr;
          </Link>
        </div>
        {/* Filter Row */}
        <div className="flex gap-4 mb-8">
          <Input
            type="text"
            placeholder="Search Positions"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-64"
          />
          <Select value={filterLoc} onValueChange={setFilterLoc}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Location" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all-locations">All Locations</SelectItem>
              {locations.map((loc) => (
                <SelectItem key={loc} value={loc}>
                  {loc}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select value={filterDeptId} onValueChange={setFilterDeptId}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="All Departments">
                {filterDeptId
                  ? departments.find((d) => d.id === Number(filterDeptId))?.name
                  : "All Departments"}
              </SelectValue>
            </SelectTrigger>
            <SelectContent>
              {departments.map((dep) => (
                <SelectItem key={dep.id} value={String(dep.id)}>
                  {dep.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
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
            {jobs.map((job) => (
              <TableRow key={job.id}>
                <TableCell>{job.position}</TableCell>
                <TableCell>{job.location}</TableCell>
                <TableCell>{job.department_name}</TableCell>
                <TableCell>
                  <button
                    className="underline mr-2"
                    onClick={() => {
                      setSelectedJob(job);
                      setShowView(true);
                    }}
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
          <div className="text-sm text-muted-foreground">
            Showing {jobs.length > 0 ? (currentPage - 1) * pageSize + 1 : 0} to{" "}
            {Math.min(currentPage * pageSize, totalJobs)} of {totalJobs} jobs
          </div>

          <div className="flex items-center gap-4">
            <Pagination>
              <PaginationContent>
                <PaginationItem>
                  <PaginationPrevious href="#" onClick={(e) => { e.preventDefault(); handlePageChange(currentPage - 1); }} className={currentPage === 1 ? "pointer-events-none opacity-50" : ""} />
                </PaginationItem>
                {/* Simplified pagination logic for brevity */}
                {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => (
                  <PaginationItem key={page}>
                    <PaginationLink href="#" onClick={(e) => { e.preventDefault(); handlePageChange(page); }} isActive={currentPage === page}>
                      {page}
                    </PaginationLink>
                  </PaginationItem>
                ))}
                <PaginationItem>
                  <PaginationNext href="#" onClick={(e) => { e.preventDefault(); handlePageChange(currentPage + 1); }} className={currentPage === totalPages ? "pointer-events-none opacity-50" : ""} />
                </PaginationItem>
              </PaginationContent>
            </Pagination>

            <div className="flex items-center gap-2">
                <p className="text-sm font-medium whitespace-nowrap">Rows per page</p>
                <Select
                    value={`${pageSize}`}
                    onValueChange={(value) => {
                        setPageSize(Number(value))
                        setCurrentPage(1)
                    }}
                >
                    <SelectTrigger className="h-8 w-[120px]">
                    <SelectValue placeholder={`${pageSize}`} />
                    </SelectTrigger>
                    <SelectContent side="top">
                    {[5, 10, 25, 50].map((size) => (
                        <SelectItem key={size} value={`${size}`}>
                        {size}
                        </SelectItem>
                    ))}
                    </SelectContent>
                </Select>
            </div>
          </div>
        </div>
      </div>

      {/* View Dialog */}
      <Dialog open={showView} onOpenChange={setShowView}>
        <DialogContent className="sm:max-w-2xl">
          <DialogHeader>
            <DialogTitle className="text-2xl">
              {selectedJob?.position}
            </DialogTitle>
            <DialogDescription>
              {selectedJob?.location} • {selectedJob?.department_name}
            </DialogDescription>
          </DialogHeader>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-6 text-sm">
            <div>
              <p className="font-semibold text-foreground">Employment Type</p>
              <p className="text-muted-foreground">
                {selectedJob?.employment_type}
              </p>
            </div>
            <div>
              <p className="font-semibold text-foreground">Experience</p>
              <p className="text-muted-foreground">
                {selectedJob?.experience_required}
              </p>
            </div>
            <div>
              <p className="font-semibold text-foreground">Salary Range</p>
              <p className="text-muted-foreground">
                {selectedJob?.salary_range
                  ? `₹ ${selectedJob.salary_range}`
                  : "N/A"}
              </p>
            </div>
            <div className="col-span-2 md:col-span-3">
              <p className="font-semibold text-foreground">Skills Required</p>
              <p className="text-muted-foreground">
                {selectedJob?.skills_required}
              </p>
            </div>
            <div>
              <p className="font-semibold text-foreground">
                Application Deadline
              </p>
              <p className="text-muted-foreground">
                {selectedJob?.application_deadline
                  ? new Date(
                      selectedJob.application_deadline,
                    ).toLocaleDateString()
                  : "N/A"}
              </p>
            </div>
          </div>

          <div className="space-y-2">
            <h3 className="font-semibold text-foreground">Job Description</h3>
            <ScrollArea className="h-60 w-full rounded-md border p-4">
              <div className="prose prose-sm dark:prose-invert max-w-none">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeRaw]}
                >
                  {selectedJob?.description || "No description available."}
                </ReactMarkdown>
              </div>
            </ScrollArea>
          </div>
          <DialogFooter className="flex justify-end gap-3">
            <Button
              variant="destructive"
              onClick={() => {
                handleDelete(selectedJob!.id);
                setShowView(false);
              }}
            >
              Delete
            </Button>
            <Button
              variant="outline"
              onClick={() => {
                handleEditClick(selectedJob!);
                setShowView(false);
              }}
            >
              Edit
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={showEdit} onOpenChange={setShowEdit}>
        <DialogContent className="sm:max-w-3xl">
          <DialogHeader>
            <DialogTitle>Edit Job Post</DialogTitle>
            <DialogDescription>
              Make changes to the job listing below. Click save when you're
              done.
            </DialogDescription>
          </DialogHeader>
          <div className="py-4 max-h-[75vh] overflow-y-auto pr-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="edit-position">Position Name</Label>
                <Input
                  id="edit-position"
                  value={editedJob.position ?? ""}
                  onChange={(e) =>
                    setEditedJob({ ...editedJob, position: e.target.value })
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit-department">Department</Label>
                <Select
                  value={String(editedJob.department_id ?? "")}
                  onValueChange={(value) =>
                    setEditedJob({ ...editedJob, department_id: Number(value) })
                  }
                >
                  <SelectTrigger id="edit-department">
                    <SelectValue placeholder="Select Department" />
                  </SelectTrigger>
                  <SelectContent>
                    {departments.map((dep) => (
                      <SelectItem key={dep.id} value={String(dep.id)}>
                        {dep.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit-location">Location</Label>
                <Select
                  value={editedJob.location ?? ""}
                  onValueChange={(value) =>
                    setEditedJob({ ...editedJob, location: value })
                  }
                >
                  <SelectTrigger id="edit-location">
                    <SelectValue placeholder="Select Location" />
                  </SelectTrigger>
                  <SelectContent>
                    {locations.map((loc) => (
                      <SelectItem key={loc} value={loc}>
                        {loc}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit-employment-type">Employment Type</Label>
                <Select
                  value={editedJob.employment_type ?? ""}
                  onValueChange={(value) =>
                    setEditedJob({
                      ...editedJob,
                      employment_type: value as any,
                    })
                  }
                >
                  <SelectTrigger id="edit-employment-type">
                    <SelectValue placeholder="Select Employment Type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="full-time">Full-time</SelectItem>
                    <SelectItem value="part-time">Part-time</SelectItem>
                    <SelectItem value="contract">Contract</SelectItem>
                    <SelectItem value="internship">Internship</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit-experience">Experience Required</Label>
                <Input
                  id="edit-experience"
                  value={editedJob.experience_required ?? ""}
                  onChange={(e) =>
                    setEditedJob({
                      ...editedJob,
                      experience_required: e.target.value,
                    })
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit-salary">Salary Range</Label>
                <Input
                  id="edit-salary"
                  value={editedJob.salary_range ?? ""}
                  onChange={(e) =>
                    setEditedJob({ ...editedJob, salary_range: e.target.value })
                  }
                />
              </div>
              <div className="md:col-span-2 space-y-2">
                <Label htmlFor="edit-skills">Skills Required</Label>
                <Input
                  id="edit-skills"
                  value={editedJob.skills_required ?? ""}
                  onChange={(e) =>
                    setEditedJob({
                      ...editedJob,
                      skills_required: e.target.value,
                    })
                  }
                  placeholder="e.g., React, Node.js, SQL"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="edit-application-deadline">
                  Application Deadline
                </Label>
                <Popover>
                  <PopoverTrigger asChild>
                    <Button
                      variant={"outline"}
                      className={cn(
                        "w-full justify-start text-left font-normal",
                        !editDeadline && "text-muted-foreground",
                      )}
                    >
                      <CalendarIcon className="mr-2 h-4 w-4" />
                      {editDeadline ? (
                        format(editDeadline, "PPP")
                      ) : (
                        <span>Pick a date</span>
                      )}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0">
                    <Calendar
                      mode="single"
                      selected={editDeadline}
                      onSelect={(date) => {
                        setEditDeadline(date);
                        setEditedJob({
                          ...editedJob,
                          application_deadline: date
                            ? format(date, "yyyy-MM-dd")
                            : undefined,
                        });
                      }}
                      initialFocus
                    />
                  </PopoverContent>
                </Popover>
              </div>
              <div className="md:col-span-2 space-y-2">
                <Label htmlFor="edit-description">Job Description</Label>
                <Tabs defaultValue="write">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="write">Write</TabsTrigger>
                    <TabsTrigger value="preview">Preview</TabsTrigger>
                  </TabsList>
                  <TabsContent value="write">
                    <Textarea
                      id="edit-description"
                      value={editedJob.description ?? ""}
                      onChange={(e) =>
                        setEditedJob({
                          ...editedJob,
                          description: e.target.value,
                        })
                      }
                      rows={8}
                      className="mt-2"
                      placeholder="Use Markdown for formatting..."
                    />
                  </TabsContent>
                  <TabsContent value="preview">
                    <ScrollArea className="h-48 w-full rounded-md border mt-2">
                      <div className="p-4 prose prose-sm dark:prose-invert max-w-none">
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          rehypePlugins={[rehypeRaw]}
                        >
                          {editedJob.description || "Nothing to preview."}
                        </ReactMarkdown>
                      </div>
                    </ScrollArea>
                  </TabsContent>
                </Tabs>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="edit-is_active"
                  checked={editedJob.is_active}
                  onCheckedChange={(checked) =>
                    setEditedJob({ ...editedJob, is_active: Boolean(checked) })
                  }
                />
                <Label htmlFor="edit-is_active">Active</Label>
              </div>
            </div>
          </div>
          <DialogFooter>
            <DialogClose asChild>
              <Button variant="outline">Cancel</Button>
            </DialogClose>
            <Button onClick={handleSave}>Save Changes</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default JobListings;
