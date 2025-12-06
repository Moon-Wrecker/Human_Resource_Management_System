"use client";

import { useState, useEffect } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Upload, File } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import jobService, { type JobListing } from "@/services/jobService";
import applicationService, {
  type ApplicationResponse,
} from "@/services/applicationService";
import {
  screenResumes,
  type ResumeScreeningRequest,
} from "@/services/aiResumeScreenerService";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Checkbox } from "@/components/ui/checkbox";
import { Progress } from "@/components/ui/progress";
import { Textarea } from "@/components/ui/textarea";

const ResumeScreenerUpload = () => {
  const [selectedRole, setSelectedRole] = useState("");
  const [resumeFiles, setResumeFiles] = useState<File[]>([]);
  const [jobs, setJobs] = useState<JobListing[]>([]);
  const [jobDescription, setJobDescription] = useState("");
  const [jdInputMethod, setJdInputMethod] = useState<"upload" | "text">(
    "upload",
  );
  const [jdFile, setJdFile] = useState<File | null>(null);
  const [isScreening, setIsScreening] = useState(false);
  const [applications, setApplications] = useState<ApplicationResponse[]>([]);
  const [selectedApplications, setSelectedApplications] = useState<number[]>(
    [],
  );

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await jobService.getAllJobs({ is_active: true });
        setJobs(response.jobs);
      } catch (error) {
        console.error("Failed to fetch jobs:", error);
      }
    };
    fetchJobs();
  }, []);

  useEffect(() => {
    if (selectedRole) {
      const fetchApplications = async () => {
        try {
          const response = await applicationService.getAllApplications(1, 100, {
            job_id: parseInt(selectedRole, 10),
          });
          setApplications(response.applications);
        } catch (error) {
          console.error("Failed to fetch applications:", error);
        }
      };
      fetchApplications();
    }
  }, [selectedRole]);

  const handleResumeFiles = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setResumeFiles([...resumeFiles, ...Array.from(e.target.files)]);
    }
  };

  const handleJdFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setJdFile(e.target.files[0]);
    }
  };

  const handleRemoveResume = (idx: number) => {
    setResumeFiles((prev) => prev.filter((_, i) => i !== idx));
  };

  const handleNewResumes = async () => {
    if (resumeFiles.length === 0) return [];

    const newApplicationIds: number[] = [];

    for (const file of resumeFiles) {
      try {
        const application = await applicationService.createApplication({
          job_id: parseInt(selectedRole, 10),
          applicant_name: file.name.split(".")[0],
          applicant_email: `${file.name.split(".")[0].split(" ")[0]}@example.com`,
          source: "referral",
        });

        await applicationService.uploadResume(application.id, file);
        newApplicationIds.push(application.id);
      } catch (error) {
        console.error("Failed to upload resume:", error);
      }
    }

    return newApplicationIds;
  };

  const handleToggleApplication = (applicationId: number) => {
    setSelectedApplications((prev) =>
      prev.includes(applicationId)
        ? prev.filter((id) => id !== applicationId)
        : [...prev, applicationId],
    );
  };
  const handleScreenResumes = async () => {
    if (!selectedRole) return;

    setIsScreening(true);

    const newApplicationIds = await handleNewResumes();
    const allApplicationIds = [...selectedApplications, ...newApplicationIds];

    let jd = jobDescription;
    if (jdInputMethod === "upload" && jdFile) {
      jd = await jdFile.text();
    }

    const request: ResumeScreeningRequest = {
      job_id: parseInt(selectedRole, 10),
      resume_ids: allApplicationIds,
      job_description: jd,
    };

    try {
      await screenResumes(request);
    } catch (error) {
      console.error("Failed to screen resumes:", error);
    } finally {
      setIsScreening(false);
    }
  };
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-12 px-4">
      <div className="w-full max-w-2xl mx-auto mb-8">
        <Accordion type="single" collapsible>
          <AccordionItem value="item-1">
            <AccordionTrigger>How to Use the Resume Screener</AccordionTrigger>
            <AccordionContent className="space-y-4 text-gray-700">
              <p>
                1. <strong>Select a Role:</strong> Choose an existing job role
                from the dropdown. The job description will be pre-filled if
                available.
              </p>
              <p>
                2. <strong>Provide Job Description:</strong> Either upload a job
                description file or enter it manually in the text area.
              </p>
              <p>
                3. <strong>Upload Resumes:</strong> Upload new resume files
                (PDF, DOC, DOCX).
                <br />
                <span className="font-semibold text-red-500">
                  Important: Please name resume files as "Candidate Name.pdf"
                  for accurate processing.
                </span>
              </p>
              <p>
                4. <strong>Select Existing Resumes:</strong> Choose from resumes
                previously uploaded for this role.
              </p>
              <p>
                5. <strong>Screen Resumes:</strong> Click "Screen Resumes" to
                start the AI analysis. You'll see results on the next page.
              </p>
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </div>
      <Card className="w-full max-w-2xl mx-auto">
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle className="text-3xl font-bold text-gray-800">
              AI-Powered Resume Screener
            </CardTitle>
            <a href="/hr/screening-history">
              <Button variant="outline">View History</Button>
            </a>
          </div>
          <CardDescription className="text-gray-600">
            Streamline your hiring process with our intelligent resume screening
            tool.
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-8">
          {/* Step 1: Select Role */}
          <div>
            <h2 className="text-lg font-semibold mb-2 text-gray-700">
              1. Select Role
            </h2>
            <Select
              value={selectedRole}
              onValueChange={(value) => {
                setSelectedRole(value);
                const selectedJob = jobs.find(
                  (job) => job.id.toString() === value,
                );
                if (selectedJob) {
                  setJobDescription(selectedJob.description || "");
                }
              }}
            >
              <SelectTrigger className="w-full h-12">
                <SelectValue placeholder="Select a role" />
              </SelectTrigger>
              <SelectContent>
                {jobs.map((job) => (
                  <SelectItem key={job.id} value={job.id.toString()}>
                    {job.position}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Existing Resumes */}
          {applications.length > 0 && (
            <div>
              <h3 className="text-md font-semibold mb-2 text-gray-700">
                Existing Resumes
              </h3>
              <div className="space-y-2">
                {applications.map((app) => (
                  <div key={app.id} className="flex items-center space-x-2">
                    <Checkbox
                      id={`app-${app.id}`}
                      checked={selectedApplications.includes(app.id)}
                      onCheckedChange={() => handleToggleApplication(app.id)}
                    />
                    <label
                      htmlFor={`app-${app.id}`}
                      className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    >
                      {app.applicant_name}
                    </label>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Step 2: Upload JD */}
          <div>
            <h2 className="text-lg font-semibold mb-2 text-gray-700">
              2. Job Description
            </h2>
            <Select
              value={jdInputMethod}
              onValueChange={(value: "upload" | "text") =>
                setJdInputMethod(value)
              }
            >
              <SelectTrigger className="w-full h-12 mb-4">
                <SelectValue placeholder="Select JD input method" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="upload">Upload Job Description</SelectItem>
                <SelectItem value="text">
                  Enter Job Description Manually
                </SelectItem>
              </SelectContent>
            </Select>
            {jdInputMethod === "upload" ? (
              <label
                htmlFor="jd-upload"
                className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed rounded-lg cursor-pointer hover:bg-gray-100"
              >
                <Upload className="w-8 h-8 text-gray-500 mb-2" />
                <span className="text-gray-600">
                  Click to upload Job Description
                </span>
                <Input
                  id="jd-upload"
                  type="file"
                  className="hidden"
                  onChange={handleJdFile}
                />
              </label>
            ) : (
              <Textarea
                placeholder="Paste the job description here"
                className="w-full h-32"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
              />
            )}
          </div>

          {/* Step 2: Upload Resumes */}
          <div>
            <h2 className="text-lg font-semibold mb-2 text-gray-700">
              2. Upload Resumes
            </h2>
            <label
              htmlFor="resume-upload"
              className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed rounded-lg cursor-pointer hover:bg-gray-100"
            >
              <Upload className="w-8 h-8 text-gray-500 mb-2" />
              <span className="text-gray-600">Click to upload resumes</span>
              <Input
                id="resume-upload"
                type="file"
                multiple
                className="hidden"
                onChange={handleResumeFiles}
              />
            </label>
          </div>

          {/* Uploaded Resumes List */}
          {resumeFiles.length > 0 && (
            <div>
              <h3 className="text-md font-semibold mb-2 text-gray-700">
                Uploaded Resumes
              </h3>
              <div className="space-y-2">
                {resumeFiles.map((file, idx) => (
                  <div
                    key={file.name + idx}
                    className="flex items-center bg-white p-2 border rounded-lg"
                  >
                    <File className="w-5 h-5 text-gray-500 mr-2" />
                    <span className="text-sm font-medium text-gray-700">
                      {file.name}
                    </span>
                    <button
                      type="button"
                      className="ml-auto text-gray-500 hover:text-red-600"
                      onClick={() => handleRemoveResume(idx)}
                    >
                      &#x2715;
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {isScreening && (
            <div className="w-full text-center">
              <p className="text-lg font-semibold">
                Screening in progress...
              </p>
              <p className="text-gray-500">
                You can check the results on the Screening History page in 5-10 minutes.
              </p>
            </div>
          )}

          <div className="flex justify-end mt-4">
            {isScreening ? (
              <a href="/hr/screening-history">
                <Button size="lg">View History</Button>
              </a>
            ) : (
              <Button
                size="lg"
                onClick={handleScreenResumes}
                disabled={
                  !selectedRole ||
                  (resumeFiles.length === 0 &&
                    selectedApplications.length === 0) ||
                  isScreening
                }
              >
                {isScreening ? "Screening..." : "Screen Resumes"}
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ResumeScreenerUpload;
