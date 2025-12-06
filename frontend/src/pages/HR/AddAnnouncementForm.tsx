"use client";
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { format } from "date-fns";
import {
  Calendar as CalendarIcon,
  ArrowLeft,
  Loader2,
  Wand2,
} from "lucide-react";
import jobService, { type EmploymentType } from "@/services/jobService";
import departmentService, {
  type Department,
} from "@/services/departmentService";
import aiJobDescriptionService, {
  type GenerateJDRequest,
} from "@/services/aiJobDescriptionService";
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
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { useToast } from "@/hooks/use-toast";
import ReactMarkdown from "react-markdown";
import rehypeRaw from "rehype-raw";
import remarkGfm from "remark-gfm";

const AddJobForm = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [isAiDialogOpen, setIsAiDialogOpen] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);

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

  const [aiFormData, setAiFormData] = useState({
    job_level: "Mid-level",
    responsibilities: "",
  });

  const [deadline, setDeadline] = useState<Date>();

  useEffect(() => {
    const fetchDepartments = async () => {
      try {
        const response = await departmentService.getAllDepartments();
        setDepartments(response.departments);
      } catch (error) {
        console.error("Failed to fetch departments", error);
        toast({
          title: "Error",
          description: "Could not fetch departments. Please try again.",
          variant: "destructive",
        });
      }
    };
    fetchDepartments();
  }, [toast]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleAiFormChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    const { name, value } = e.target;
    setAiFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSelectChange = (name: string, value: string) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleAiSelectChange = (name: string, value: string) => {
    setAiFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = (name: string, checked: boolean) => {
    setFormData((prev) => ({ ...prev, [name]: checked }));
  };

  const handleDateChange = (date: Date | undefined) => {
    if (date) {
      setDeadline(date);
      setFormData((prev) => ({
        ...prev,
        application_deadline: format(date, "yyyy-MM-dd"),
      }));
    }
  };

  const handleGenerateJD = async () => {
    if (!formData.position || !formData.skills_required) {
      toast({
        title: "Missing Information",
        description:
          "Please fill in 'Position Name' and 'Skills Required' before generating with AI.",
        variant: "destructive",
      });
      return;
    }
    setIsAiDialogOpen(true);
  };

  const onAiGenerate = async () => {
    setAiLoading(true);
    try {
      const payload: GenerateJDRequest = {
        job_title: formData.position,
        job_level: aiFormData.job_level,
        responsibilities: aiFormData.responsibilities
          .split("\n")
          .filter((r) => r.trim() !== ""),
        requirements: formData.skills_required
          .split(",")
          .map((s) => ({ requirement: s.trim(), is_required: true })),
        department: departments.find(
          (d) => d.id === parseInt(formData.department_id),
        )?.name,
        location: formData.location,
        employment_type: formData.employment_type,
        salary_range: formData.salary_range,
      };

      const response =
        await aiJobDescriptionService.generateJobDescription(payload);

      if (response.success) {
        setFormData((prev) => ({
          ...prev,
          description: response.data.full_description,
        }));
        toast({
          title: "Success",
          description: "AI Job Description generated and filled in.",
        });
        setIsAiDialogOpen(false);
      } else {
        throw new Error(response.message || "Failed to generate description.");
      }
    } catch (err) {
      console.error("AI Generation failed", err);
      toast({
        title: "AI Generation Failed",
        description: "Could not generate job description. Please try again.",
        variant: "destructive",
      });
    } finally {
      setAiLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.position || !formData.department_id || !formData.location) {
      setError("Please fill in all required fields.");
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const payload = {
        ...formData,
        department_id: parseInt(formData.department_id, 10),
        employment_type: formData.employment_type as EmploymentType,
        skills_required: formData.skills_required || "",
        application_deadline: formData.application_deadline ? new Date(formData.application_deadline).toISOString() : undefined,
      };
      await jobService.createJob(payload);
      toast({
        title: "Success",
        description: `Job listing for ${formData.position} has been created.`,
      });
      navigate("/hr/joblistings");
    } catch (err: any) {
      setError(err.message || "Failed to create job listing.");
      toast({
        title: "Error",
        description:
          "Failed to create job listing. Please check the form and try again.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center py-12 px-4">
      <Card className="w-full max-w-3xl">
        <CardHeader>
          <div className="mb-4">
            <Link
              to="/hr/joblistings"
              className="flex items-center text-sm text-muted-foreground hover:text-primary"
            >
              <ArrowLeft className="w-4 h-4 mr-1" />
              Back to Job Listings
            </Link>
          </div>
          <CardTitle>Add a New Position</CardTitle>
          <CardDescription>
            Fill in the details to create a new job listing.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="mb-4 p-4 bg-destructive/10 border border-destructive/50 text-destructive rounded-lg">
              {error}
            </div>
          )}
          <form id="add-job-form" onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="position">Position Name *</Label>
                <Input
                  id="position"
                  name="position"
                  placeholder="e.g., Senior Software Engineer"
                  value={formData.position}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="department_id">Department *</Label>
                <Select
                  name="department_id"
                  onValueChange={(value) =>
                    handleSelectChange("department_id", value)
                  }
                  value={formData.department_id}
                  required
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select Department" />
                  </SelectTrigger>
                  <SelectContent>
                    {departments.map((dept) => (
                      <SelectItem key={dept.id} value={String(dept.id)}>
                        {dept.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="location">Location *</Label>
                <Select
                  name="location"
                  onValueChange={(value) =>
                    handleSelectChange("location", value)
                  }
                  value={formData.location}
                  required
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select Location" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Remote">Remote</SelectItem>
                    <SelectItem value="Mumbai">Mumbai</SelectItem>
                    <SelectItem value="Chennai">Chennai</SelectItem>
                    <SelectItem value="Bangalore">Bangalore</SelectItem>
                    <SelectItem value="Pune">Pune</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="employment_type">Employment Type</Label>
                <Select
                  name="employment_type"
                  onValueChange={(value) =>
                    handleSelectChange("employment_type", value)
                  }
                  value={formData.employment_type}
                >
                  <SelectTrigger>
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
                <Label htmlFor="experience_required">Experience Required</Label>
                <Input
                  id="experience_required"
                  name="experience_required"
                  placeholder="e.g., 3-5 years"
                  value={formData.experience_required}
                  onChange={handleChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="salary_range">Salary Range</Label>
                <Input
                  id="salary_range"
                  name="salary_range"
                  placeholder="e.g., 50,000 - 70,000"
                  value={formData.salary_range}
                  onChange={handleChange}
                />
              </div>

              <div className="md:col-span-2 space-y-2">
                <Label htmlFor="skills_required">Skills Required</Label>
                <Input
                  id="skills_required"
                  name="skills_required"
                  placeholder="e.g., React, Node.js, SQL (comma-separated)"
                  value={formData.skills_required}
                  onChange={handleChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="application_deadline">
                  Application Deadline
                </Label>
                <Popover>
                  <PopoverTrigger asChild>
                    <Button
                      variant={"outline"}
                      className={cn(
                        "w-full justify-start text-left font-normal",
                        !deadline && "text-muted-foreground",
                      )}
                    >
                      <CalendarIcon className="mr-2 h-4 w-4" />
                      {deadline ? (
                        format(deadline, "PPP")
                      ) : (
                        <span>Pick a date</span>
                      )}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0">
                    <Calendar
                      mode="single"
                      selected={deadline}
                      onSelect={handleDateChange}
                      initialFocus
                    />
                  </PopoverContent>
                </Popover>
              </div>

              <div className="flex items-center pt-8">
                <Checkbox
                  id="is_active"
                  name="is_active"
                  checked={formData.is_active}
                  onCheckedChange={(checked) =>
                    handleCheckboxChange("is_active", checked as boolean)
                  }
                />
                <Label htmlFor="is_active" className="ml-2 font-medium">
                  Is Active
                </Label>
              </div>

              <div className="md:col-span-2 space-y-2">
                <div className="flex justify-between items-center">
                  <Label htmlFor="description">Job Description</Label>

                  <Button
                    variant="link"
                    type="button"
                    onClick={handleGenerateJD}
                    className="text-primary px-0"
                  >
                    <Wand2 className="w-4 h-4 mr-2" />
                    Generate with AI
                  </Button>
                </div>

                <Tabs defaultValue="write">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="write">Write</TabsTrigger>

                    <TabsTrigger value="preview">Preview</TabsTrigger>
                  </TabsList>

                  <TabsContent value="write">
                    <Textarea
                      id="description"
                      name="description"
                      placeholder="Write a compelling job description using Markdown..."
                      value={formData.description}
                      onChange={handleChange}
                      rows={12}
                      className="mt-2"
                    />
                  </TabsContent>

                  <TabsContent value="preview" className="flex">
                    <div className="prose min-w-full prose-sm dark:prose-invert min-h-[260px] rounded-md border border-input p-4 mt-2">
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        rehypePlugins={[rehypeRaw]}
                      >
                        {formData.description || "Nothing to preview yet."}
                      </ReactMarkdown>
                    </div>
                  </TabsContent>
                </Tabs>
              </div>
            </div>
          </form>
        </CardContent>
        <CardFooter className="flex justify-end gap-4">
          <Button variant="outline" asChild>
            <Link to="/hr/joblistings">Cancel</Link>
          </Button>
          <Button type="submit" form="add-job-form" disabled={loading}>
            {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            {loading ? "Creating..." : "Create Job Listing"}
          </Button>
        </CardFooter>
      </Card>

      <Dialog open={isAiDialogOpen} onOpenChange={setIsAiDialogOpen}>
        <DialogContent className="sm:max-w-xl">
          <DialogHeader>
            <DialogTitle>Generate Job Description</DialogTitle>
            <DialogDescription>
              Provide additional details to generate a high-quality job
              description with AI.
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="ai-job-level" className="text-right">
                Job Level
              </Label>
              <Select
                name="job_level"
                value={aiFormData.job_level}
                onValueChange={(value) =>
                  handleAiSelectChange("job_level", value)
                }
              >
                <SelectTrigger className="col-span-3">
                  <SelectValue placeholder="Select Level" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Entry-level">Entry-level</SelectItem>
                  <SelectItem value="Mid-level">Mid-level</SelectItem>
                  <SelectItem value="Senior-level">Senior-level</SelectItem>
                  <SelectItem value="Lead">Lead</SelectItem>
                  <SelectItem value="Manager">Manager</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="ai-responsibilities" className="text-right">
                Responsibilities
              </Label>
              <Textarea
                id="ai-responsibilities"
                name="responsibilities"
                value={aiFormData.responsibilities}
                onChange={handleAiFormChange}
                className="col-span-3"
                placeholder="List key responsibilities, one per line..."
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsAiDialogOpen(false)}>
              Cancel
            </Button>
            <Button onClick={onAiGenerate} disabled={aiLoading}>
              {aiLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Generate
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default AddJobForm;
