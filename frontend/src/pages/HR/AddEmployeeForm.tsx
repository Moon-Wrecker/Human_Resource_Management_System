"use client";

import { useState , useEffect} from "react";
import { useNavigate } from "react-router-dom";
import employeeService from "@/services/employeeService";
import type { 
  EmployeeCreate,
} from "@/services/employeeService";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Upload } from "lucide-react";
import profileService, { type TeamData } from "@/services/profileService";

const departments = [
  "Finance",
  "HR",
  "Operations",
  "Sales",
  "Engineering",
  "Product Management",
  "Quality Assurance",
  "Customer Success",
  "Data Science",
  "DevOps",
  "Legal",
  "Research and Development",
  "IT Support",
  "Business Intelligence",
];

const deptMap: Record<string, number> = {
  "Engineering": 1,
  "HR": 2,
  "Finance": 3,
  "Sales": 4,
  "Marketing": 5,
  "Operations": 6,
  "Product Management": 7,
  "Quality Assurance": 8,
  "Customer Success": 9,
  "Data Science": 10,
  "DevOps": 11,
  "Legal": 12,
  "Research and Development": 13,
  "IT Support": 14,
  "Business Intelligence": 15,
};

const roles = ["employee", "manager", "hr", "admin"];

export default function AddEmployeeForm() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [managersState, setManagersState] = useState<{ id: number; name: string }[]>([]);
  const [teamsState, setTeamsState] = useState<TeamData | null>(null);

  const [formData, setFormData] = useState<EmployeeCreate>({
    name: "",
    email: "",
    password: "",
    phone: "",
    employee_id: "",
    job_role: "",
    department_id: undefined,
    role: "employee",
    hire_date: "",
    date_of_birth: "",
    salary: undefined,
    emergency_contact: "",
    casual_leave_balance: 12,
    sick_leave_balance: 12,
    annual_leave_balance: 15,
    wfh_balance: 24,
  });

  const [documents, setDocuments] = useState<{
    aadhar: File | null;
    pan: File | null;
  }>({
    aadhar: null,
    pan: null,
  });

  const handleChange = (field: keyof EmployeeCreate, value: any) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleFileChange = (docType: "aadhar" | "pan", file: File | null) => {
    setDocuments((prev) => ({
      ...prev,
      [docType]: file,
    }));
  };

    const fetchTeams = async (managerId: number) => {
    try {
      profileService.getTeamByManager(managerId).then(res=>{
        setTeamsState(res);
      });
    }
    catch (err: any) {
      console.error("[AddEmployeeForm] Error fetching teams:", err);
      setError(`Unable to load teams: ${err.message}`);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validation
    if (
      !formData.name ||
      !formData.email ||
      !formData.password ||
      !formData.department_id ||
      !formData.job_role
    ) {
      setError("Please fill in all required fields (Name, Email, Password, Department, Job Role).");
      return;
    }

    try {
      setLoading(true);
      setError(null);

      await employeeService.createEmployee({
        ...formData,
        department_id: formData.department_id,
      });

      // TODO: Handle document uploads separately if needed
      // For now, documents would be uploaded via a separate endpoint

      navigate("/employees-list");
    } catch (err: any) {
      console.error("Create employee error:", err);
      setError(err?.message || "Failed to create employee.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        // try using employeeService.getEmployees to fetch managers (returns employees list)
        const resp = await employeeService.getEmployees?.({
          page: 1,
          page_size: 100,
          role: "manager",
        } as any);
        const mgrs = resp?.employees?.map((e: any) => ({ id: e.id, name: e.name })) ?? [];
        if (mounted) setManagersState(mgrs);
      } catch (err) {
        // fallback: empty managers
        if (mounted) setManagersState([]);
      }
    })();
    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    if (!formData.manager_id) {
      setTeamsState(null);
      return;
    }
    fetchTeams(formData.manager_id);
  }, [formData.manager_id]);

  return (
    <div className="min-h-screen bg-background">
      <div className="px-8 py-8">
        <div className="mb-8">
          <a
            href="employees-list"
            className="text-sm font-medium text-muted-foreground hover:text-foreground mb-4 inline-block"
          >
            ← Back to Employees
          </a>
          <h1 className="text-3xl font-semibold tracking-tight mb-2">
            Add New Employee
          </h1>
          <p className="text-muted-foreground">
            Create a new employee account and set up their information.
          </p>
        </div>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <form onSubmit={handleSubmit} className="max-w-2xl space-y-8">
          {/* Basic Information */}
          <fieldset className="space-y-4 pb-6 border-b">
            <h2 className="text-lg font-semibold">Basic Information</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-1">
                <Label htmlFor="name">Name *</Label>
                <Input
                  id="name"
                  type="text"
                  placeholder="Full Name"
                  value={formData.name}
                  onChange={(e) => handleChange("name", e.target.value)}
                  required
                />
              </div>
              <div className="col-span-1">
                <Label htmlFor="email">Email *</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="Email Address"
                  value={formData.email}
                  onChange={(e) => handleChange("email", e.target.value)}
                  required
                />
              </div>
              <div className="col-span-1">
                <Label htmlFor="password">Password *</Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="Initial Password"
                  value={formData.password}
                  onChange={(e) => handleChange("password", e.target.value)}
                  required
                />
              </div>
              <div className="col-span-1">
                <Label htmlFor="phone">Phone</Label>
                <Input
                  id="phone"
                  type="tel"
                  placeholder="Phone Number"
                  value={formData.phone || ""}
                  onChange={(e) => handleChange("phone", e.target.value)}
                />
              </div>
              <div className="col-span-2">
                <Label htmlFor="emergency_contact">Emergency Contact</Label>
                <Input
                  id="emergency_contact"
                  type="text"
                  placeholder="Emergency Contact Number/Name"
                  value={formData.emergency_contact || ""}
                  onChange={(e) =>
                    handleChange("emergency_contact", e.target.value)
                  }
                />
              </div>
            </div>
          </fieldset>

          {/* Work Information */}
          <fieldset className="space-y-4 pb-6 border-b">
            <h2 className="text-lg font-semibold">Work Information</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-1">
                <Label htmlFor="employee_id">Employee ID</Label>
                <Input
                  id="employee_id"
                  type="text"
                  placeholder="Employee ID (auto-generated)"
                  value={formData.employee_id || ""}
                  onChange={(e) => handleChange("employee_id", e.target.value)}
                />
              </div>
              <div className="col-span-1">
                <Label htmlFor="department">Department *</Label>
                <Select
                  value={formData.department_id?.toString() || ""}
                  onValueChange={(val) =>
                    handleChange("department_id", parseInt(val, 10))
                  }
                >
                  <SelectTrigger id="department">
                    <SelectValue placeholder="Select Department" />
                  </SelectTrigger>
                  <SelectContent>
                    {departments.map((dept) => (
                      <SelectItem key={dept} value={deptMap[dept].toString()}>
                        {dept}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="col-span-1">
                <Label htmlFor="job_role">Job Role *</Label>
                <Input
                  id="job_role"
                  type="text"
                  placeholder="e.g., Senior Engineer"
                  value={formData.job_role || ""}
                  onChange={(e) => handleChange("job_role", e.target.value)}
                  required
                />
              </div>
              <div className="col-span-1">
                <Label htmlFor="role">System Role</Label>
                <Select
                  value={formData.role || "employee"}
                  onValueChange={(val) =>
                    handleChange("role", val as "employee" | "manager" | "hr" | "admin")
                  }
                >
                  <SelectTrigger id="role">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {roles.map((r) => (
                      <SelectItem key={r} value={r}>
                        {r.charAt(0).toUpperCase() + r.slice(1)}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="col-span-1">
                <Label htmlFor="salary">Salary</Label>
                <Input
                  id="salary"
                  type="number"
                  placeholder="Annual Salary"
                  value={formData.salary || ""}
                  onChange={(e) =>
                    handleChange("salary", parseFloat(e.target.value))
                  }
                />
              </div>
            </div>
          </fieldset>

          {/* Personal Information */}
          <fieldset className="space-y-4 pb-6 border-b">
            <h2 className="text-lg font-semibold">Personal Information</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-1">
                <Label htmlFor="date_of_birth">Date of Birth</Label>
                <Input
                  id="date_of_birth"
                  type="date"
                  value={formData.date_of_birth || ""}
                  onChange={(e) => handleChange("date_of_birth", e.target.value)}
                />
              </div>
              <div className="col-span-1">
                <Label htmlFor="hire_date">Hire Date</Label>
                <Input
                  id="hire_date"
                  type="date"
                  value={formData.hire_date || ""}
                  onChange={(e) => handleChange("hire_date", e.target.value)}
                />
              </div>
            </div>
          </fieldset>

          {/* Leave Balances */}
          <fieldset className="space-y-4 pb-6 border-b">
            <h2 className="text-lg font-semibold">Manager & Team Assignment</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-1">
                <Label htmlFor="manager">Manager</Label>
                <Select
                  value={formData.manager_id?.toString() ?? "__none__"}
                  onValueChange={(val) =>
                    handleChange(
                      "manager_id",
                      val === "__none__" ? undefined : parseInt(val, 10)
                    )
                  }
                >
                  <SelectTrigger id="manager">
                    <SelectValue placeholder="Select manager" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="__none__">No manager</SelectItem>
                    {managersState.map((m) => (
                      <SelectItem key={m.id} value={m.id.toString()}>
                        {m.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="col-span-1">
                <Label htmlFor="team">Team</Label>
                <Input
                  id="team"
                  type="text"
                  readOnly
                  disabled
                  value={teamsState?.team_name || ""}
                  placeholder={formData.manager_id ? "Team will load..." : "Select manager first"}
                  className="bg-muted cursor-not-allowed"
                />
              </div>
            </div>
          </fieldset>

          {/* Document Upload */}
          <fieldset className="space-y-4 pb-6 border-b">
            <h2 className="text-lg font-semibold">Documents</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-1">
                <Label htmlFor="aadhar">Aadhar Document</Label>
                <label
                  htmlFor="aadhar"
                  className="flex items-center justify-center gap-2 border border-input rounded-md p-4 cursor-pointer hover:bg-accent transition"
                >
                  <Upload className="w-4 h-4" />
                  <span className="text-sm">
                    {documents.aadhar?.name || "Upload Aadhar"}
                  </span>
                  <input
                    id="aadhar"
                    type="file"
                    className="hidden"
                    accept=".pdf,.jpg,.jpeg,.png"
                    onChange={(e) =>
                      handleFileChange("aadhar", e.target.files?.[0] || null)
                    }
                  />
                </label>
              </div>
              <div className="col-span-1">
                <Label htmlFor="pan">PAN Document</Label>
                <label
                  htmlFor="pan"
                  className="flex items-center justify-center gap-2 border border-input rounded-md p-4 cursor-pointer hover:bg-accent transition"
                >
                  <Upload className="w-4 h-4" />
                  <span className="text-sm">
                    {documents.pan?.name || "Upload PAN"}
                  </span>
                  <input
                    id="pan"
                    type="file"
                    className="hidden"
                    accept=".pdf,.jpg,.jpeg,.png"
                    onChange={(e) =>
                      handleFileChange("pan", e.target.files?.[0] || null)
                    }
                  />
                </label>
              </div>
            </div>
          </fieldset>

          {/* Action Buttons */}
          <div className="flex justify-end gap-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate("employees-list")}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? "Creating..." : "Create Employee"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}