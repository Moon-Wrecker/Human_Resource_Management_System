"use client";

import { useState, useEffect } from "react";
import applicationService, {
  type ApplicationResponse,
  type ApplicationFilters,
  formatDate,
  formatApplicationSource,
} from "@/services/applicationService";
import jobService, { type JobListing } from "@/services/jobService";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogTrigger,
  DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Download, FileText, Search, Loader2 } from "lucide-react";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { useToast } from "@/hooks/use-toast";

const Applications = () => {
  const { toast } = useToast();
  const [applications, setApplications] = useState<ApplicationResponse[]>([]);
  const [jobs, setJobs] = useState<JobListing[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [totalApplications, setTotalApplications] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  // Filtering/search state
  const [search, setSearch] = useState("");
  const [jobId, setJobId] = useState<string>("all");
  const [source, setSource] = useState<string>("all");
  const [status, setStatus] = useState<string>("all");

  // Dialog state
  const [selectedApp, setSelectedApp] = useState<ApplicationResponse | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);

  // Fetch jobs for filter
  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await jobService.getAllJobs();
        setJobs(response.jobs);
      } catch (error) {
        console.error("Failed to fetch jobs", error);
      }
    };
    fetchJobs();
  }, []);

  // Fetch applications
  const fetchApplications = async () => {
    try {
      setLoading(true);
      setError(null);

      const filters: ApplicationFilters = {
        search: search || undefined,
        job_id: jobId !== "all" ? Number(jobId) : undefined,
        source: source !== "all" ? source : undefined,
        status: status !== "all" ? status : undefined,
      };

      console.log("Fetching applications with filters:", filters);
      console.log("Status value:", status, "Type:", typeof status);

      const data = await applicationService.getAllApplications(
        currentPage,
        pageSize,
        filters
      );

      console.log("Received applications:", data.applications.length, "Total:", data.total);

      setApplications(data.applications);
      setTotalApplications(data.total);
      setTotalPages(data.total_pages);
    } catch (e: any) {
      setError(e?.message || "Failed to load applications");
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to load applications",
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setCurrentPage(1);
  }, [search, jobId, source, status]);

  useEffect(() => {
    fetchApplications();
  }, [currentPage, pageSize, search, jobId, source, status]);

  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  const getSourceBadgeVariant = (source: string) => {
    if (source === "referral") return "default";
    if (source === "self-applied") return "secondary";
    return "outline";
  };

  const getStatusBadgeVariant = (status: string) => {
    if (status === "hired") return "default";
    if (status === "shortlisted") return "secondary";
    if (status === "rejected") return "destructive";
    return "outline";
  };

  const handleUpdateStatus = async (applicationId: number, newStatus: "shortlisted" | "rejected" | "hired") => {
    try {
      setActionLoading(true);
      await applicationService.updateApplicationStatus(applicationId, {
        status: newStatus,
      });
      
      toast({
        title: "Success",
        description: `Application ${newStatus} successfully`,
      });
      
      setDialogOpen(false);
      fetchApplications();
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error",
        description: error?.message || `Failed to update application status`,
      });
    } finally {
      setActionLoading(false);
    }
  };

  const handleDownloadResume = async (applicationId: number, applicantName: string) => {
    try {
      const blob = await applicationService.downloadResume(applicationId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${applicantName.replace(/\s+/g, "_")}_Resume.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      toast({
        title: "Success",
        description: "Resume downloaded successfully",
      });
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error",
        description: error?.message || "Failed to download resume",
      });
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight">Applications</h1>
          <p className="text-muted-foreground mt-2">
            View and manage job applications
          </p>
        </div>

        {/* Filters Card */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="text-lg font-medium">Filters</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Search Input */}
              <div className="space-y-2">
                <Label htmlFor="search">Search Applicants</Label>
                <div className="relative">
                  <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="search"
                    type="text"
                    placeholder="Search by name..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="pl-9"
                  />
                </div>
              </div>

              {/* Job Filter */}
              <div className="space-y-2">
                <Label htmlFor="job">Job Position</Label>
                <Select value={jobId} onValueChange={setJobId}>
                  <SelectTrigger id="job">
                    <SelectValue placeholder="All Positions" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Positions</SelectItem>
                    {jobs.map((job) => (
                      <SelectItem key={job.id} value={String(job.id)}>
                        {job.position}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Source Filter */}
              <div className="space-y-2">
                <Label htmlFor="source">Source</Label>
                <Select value={source} onValueChange={setSource}>
                  <SelectTrigger id="source">
                    <SelectValue placeholder="All Sources" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Sources</SelectItem>
                    <SelectItem value="self-applied">Self Applied</SelectItem>
                    <SelectItem value="referral">Referral</SelectItem>
                    <SelectItem value="recruitment">Recruitment Agency</SelectItem>
                    <SelectItem value="internal">Internal</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Status Filter */}
              <div className="space-y-2">
                <Label htmlFor="status">Status</Label>
                <Select value={status} onValueChange={setStatus}>
                  <SelectTrigger id="status">
                    <SelectValue placeholder="All Statuses" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Statuses</SelectItem>
                    <SelectItem value="pending">Pending</SelectItem>
                    <SelectItem value="reviewed">Reviewed</SelectItem>
                    <SelectItem value="shortlisted">Shortlisted</SelectItem>
                    <SelectItem value="rejected">Rejected</SelectItem>
                    <SelectItem value="hired">Hired</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Applications Table Card */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-lg font-medium">
                Applications List
              </CardTitle>
              <p className="text-sm text-muted-foreground">
                {totalApplications} application{totalApplications !== 1 ? "s" : ""}
              </p>
            </div>
          </CardHeader>
          <CardContent>
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="font-semibold">Applicant</TableHead>
                    <TableHead className="font-semibold">Position</TableHead>
                    <TableHead className="font-semibold">Source</TableHead>
                    <TableHead className="font-semibold">Status</TableHead>
                    <TableHead className="font-semibold">Applied On</TableHead>
                    <TableHead className="font-semibold text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {loading ? (
                    <TableRow>
                      <TableCell colSpan={6} className="text-center py-8">
                        <Loader2 className="h-6 w-6 animate-spin mx-auto text-muted-foreground" />
                      </TableCell>
                    </TableRow>
                  ) : applications.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={6} className="text-center py-8 text-muted-foreground">
                        No applications found
                      </TableCell>
                    </TableRow>
                  ) : (
                    applications.map((app) => (
                      <TableRow key={app.id} className="hover:bg-muted/50">
                        <TableCell className="font-medium">{app.applicant_name}</TableCell>
                        <TableCell>{app.job_position || "N/A"}</TableCell>
                        <TableCell>
                          <Badge variant={getSourceBadgeVariant(app.source)}>
                            {formatApplicationSource(app.source)}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <Badge variant={getStatusBadgeVariant(app.status)} className={app.status === "rejected" ? "text-white" : ""}>
                            {app.status.charAt(0).toUpperCase() + app.status.slice(1)}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-muted-foreground">
                          {formatDate(app.applied_date)}
                        </TableCell>
                        <TableCell className="text-right">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => {
                              setSelectedApp(app);
                              setDialogOpen(true);
                            }}
                          >
                            <FileText className="h-4 w-4 mr-2" />
                            View
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-between mt-4">
                <div className="text-sm text-muted-foreground">
                  Showing {applications.length > 0 ? (currentPage - 1) * pageSize + 1 : 0} to{" "}
                  {Math.min(currentPage * pageSize, totalApplications)} of {totalApplications} applications
                </div>

                <div className="flex items-center gap-4">
                  <Pagination>
                    <PaginationContent>
                      <PaginationItem>
                        <PaginationPrevious
                          href="#"
                          onClick={(e) => {
                            e.preventDefault();
                            handlePageChange(currentPage - 1);
                          }}
                          className={currentPage === 1 ? "pointer-events-none opacity-50" : ""}
                        />
                      </PaginationItem>
                      {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
                        let pageNum;
                        if (totalPages <= 5) {
                          pageNum = i + 1;
                        } else if (currentPage <= 3) {
                          pageNum = i + 1;
                        } else if (currentPage >= totalPages - 2) {
                          pageNum = totalPages - 4 + i;
                        } else {
                          pageNum = currentPage - 2 + i;
                        }
                        return (
                          <PaginationItem key={pageNum}>
                            <PaginationLink
                              href="#"
                              onClick={(e) => {
                                e.preventDefault();
                                handlePageChange(pageNum);
                              }}
                              isActive={currentPage === pageNum}
                            >
                              {pageNum}
                            </PaginationLink>
                          </PaginationItem>
                        );
                      })}
                      <PaginationItem>
                        <PaginationNext
                          href="#"
                          onClick={(e) => {
                            e.preventDefault();
                            handlePageChange(currentPage + 1);
                          }}
                          className={currentPage === totalPages ? "pointer-events-none opacity-50" : ""}
                        />
                      </PaginationItem>
                    </PaginationContent>
                  </Pagination>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* View Application Dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="sm:max-w-[600px]">
          <DialogHeader>
            <DialogTitle className="text-2xl">
              Application Details
            </DialogTitle>
            <DialogDescription>
              Review the applicant's information and resume
            </DialogDescription>
          </DialogHeader>

          {selectedApp && (
            <div className="space-y-6 py-4">
              {/* Applicant Info Grid */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">
                    Applicant Name
                  </p>
                  <p className="text-base font-semibold">
                    {selectedApp.applicant_name}
                  </p>
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">
                    Email
                  </p>
                  <p className="text-base">{selectedApp.applicant_email}</p>
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">
                    Phone
                  </p>
                  <p className="text-base">{selectedApp.applicant_phone || "N/A"}</p>
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">
                    Position
                  </p>
                  <p className="text-base font-semibold">
                    {selectedApp.job_position || "N/A"}
                  </p>
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">
                    Department
                  </p>
                  <p className="text-base">{selectedApp.job_department || "N/A"}</p>
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">
                    Applied On
                  </p>
                  <p className="text-base">{formatDate(selectedApp.applied_date)}</p>
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">
                    Source
                  </p>
                  <Badge variant={getSourceBadgeVariant(selectedApp.source)}>
                    {formatApplicationSource(selectedApp.source)}
                  </Badge>
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">
                    Status
                  </p>
                  <Badge variant={getStatusBadgeVariant(selectedApp.status)} className={selectedApp.status === "rejected" ? "text-white" : ""}>
                    {selectedApp.status.charAt(0).toUpperCase() + selectedApp.status.slice(1)}
                  </Badge>
                </div>
              </div>

              {selectedApp.cover_letter && (
                <>
                  <Separator />
                  <div className="space-y-2">
                    <p className="text-sm font-medium text-muted-foreground">
                      Cover Letter
                    </p>
                    <p className="text-sm bg-muted p-4 rounded-md">
                      {selectedApp.cover_letter}
                    </p>
                  </div>
                </>
              )}

              {selectedApp.referrer_name && (
                <>
                  <Separator />
                  <div className="space-y-2">
                    <p className="text-sm font-medium text-muted-foreground">
                      Referred By
                    </p>
                    <p className="text-base font-medium">
                      {selectedApp.referrer_name}
                    </p>
                  </div>
                </>
              )}

              <Separator />

              {/* Resume Section */}
              <div className="space-y-3">
                <p className="text-sm font-medium text-muted-foreground">
                  Resume
                </p>
                {selectedApp.resume_path ? (
                  <Button
                    variant="secondary"
                    className="w-full"
                    onClick={() => handleDownloadResume(selectedApp.id, selectedApp.applicant_name)}
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Download Resume
                  </Button>
                ) : (
                  <p className="text-sm text-muted-foreground italic">No resume uploaded</p>
                )}
              </div>

              <Separator />

              {/* Action Buttons */}
              <DialogFooter className="flex justify-end gap-3">
                {selectedApp.status === "pending" || selectedApp.status === "reviewed" ? (
                  <>
                    <Button
                      variant="destructive"
                      onClick={() => handleUpdateStatus(selectedApp.id, "rejected")}
                      disabled={actionLoading}
                    >
                      {actionLoading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                      Reject Application
                    </Button>
                    <Button
                      variant="secondary"
                      onClick={() => handleUpdateStatus(selectedApp.id, "shortlisted")}
                      disabled={actionLoading}
                    >
                      {actionLoading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                      Shortlist
                    </Button>
                    <Button
                      onClick={() => handleUpdateStatus(selectedApp.id, "hired")}
                      disabled={actionLoading}
                    >
                      {actionLoading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                      Hire
                    </Button>
                  </>
                ) : (
                  <p className="text-sm text-muted-foreground">
                    Application status: {selectedApp.status.charAt(0).toUpperCase() + selectedApp.status.slice(1)}
                  </p>
                )}
              </DialogFooter>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Applications;
