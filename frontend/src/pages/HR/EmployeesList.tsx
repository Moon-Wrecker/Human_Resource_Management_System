"use client";

import { useState, useEffect } from "react";
import employeeService from "@/services/employeeService";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogClose,
} from "@/components/ui/dialog";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { Alert, AlertDescription } from "@/components/ui/alert";
import { Search } from "lucide-react";

// Type definitions
interface Employee {
  id: number;
  name: string;
  email: string;
  phone?: string;
  department?: string;
  department_id?: number;
  role?: string;
  job_role?: string;
  manager?: string;
  manager_id?: number;
  team?: string;
  employee_id?: string;
  hire_date?: string;
  is_active: boolean;
}

interface EmployeesResponse {
  employees: Employee[];
  total: number;
}

const departments = [
  "Engineering",
  "HR",
  "Finance",
  "Operations",
  "Sales",
  "Marketing",
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

export default function EmployeeList() {
  // Filters
  const [search, setSearch] = useState("");
  const [dept, setDept] = useState("");
  const [role, setRole] = useState("");

  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);

  // Data & State
  const [employeesResponse, setEmployeesResponse] = useState<EmployeesResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Dialog states
  const [viewOpen, setViewOpen] = useState(false);
  const [editOpen, setEditOpen] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null);
  const [editForm, setEditForm] = useState<Partial<Employee> | null>(null);
  const [editLoading, setEditLoading] = useState(false);

  // Fetch employees
  const fetchEmployees = async (page = currentPage, size = pageSize) => {
    try {
      setLoading(true);
      setError(null);

      let deptId: number | undefined;
      if (dept) {
        const deptMap: Record<string, number> = {
          "Engineering": 1, 
          "HR": 2,
          "Finance": 3,
          "Operations": 4,
          "Sales": 5,
          "Marketing": 6,
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
        deptId = deptMap[dept];
      }

      const response = await employeeService.getEmployees({
        page,
        page_size: size,
        search: search || undefined,
        department_id: deptId,
        role: role || undefined,
        is_active: true,
      });

      console.log("Employees response:", response);
      setEmployeesResponse(response);
    } catch (err: any) {
      console.error("Fetch employees error:", err);
      setError(err?.message || "Failed to load employees");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setCurrentPage(1);
  }, [search, dept, role]);

  useEffect(() => {
    fetchEmployees(currentPage, pageSize);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentPage, pageSize, search, dept, role]);

  const employees = employeesResponse?.employees ?? [];
  const totalEmployees = employeesResponse?.total ?? 0;
  const totalPages = pageSize > 0 ? Math.ceil(totalEmployees / pageSize) : 1;

  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  const handleViewStart = (emp: Employee) => {
    setSelectedEmployee(emp);
    setViewOpen(true);
  };

  const handleEditStart = (emp: Employee) => {
    setSelectedEmployee(emp);
    setEditForm({ ...emp });
    setEditOpen(true);
  };

  const handleSaveEdit = async () => {
    if (!selectedEmployee || !editForm) return;

    try {
      setEditLoading(true);
      setError(null);

      await employeeService.updateEmployee(selectedEmployee.id, {
        name: editForm.name,
        email: editForm.email,
        phone: editForm.phone,
        job_role: editForm.job_role,
        department_id: editForm.department_id,
        manager_id: editForm.manager_id,
      });

      setEditOpen(false);
      await fetchEmployees(currentPage, pageSize);
    } catch (err: any) {
      console.error("Save edit error:", err);
      setError(err?.message || "Failed to update employee");
    } finally {
      setEditLoading(false);
    }
  };

  const handleDeleteEmployee = async (empId: number) => {
    if (!window.confirm("Are you sure you want to deactivate this employee?"))
      return;

    try {
      setError(null);
      await employeeService.deactivateEmployee(empId);
      setViewOpen(false);
      await fetchEmployees(currentPage, pageSize);
    } catch (err: any) {
      console.error("Delete error:", err);
      setError(err?.message || "Failed to deactivate employee");
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-semibold tracking-tight mb-2">Employees</h1>
          <p className="text-muted-foreground">Manage your company employees</p>
        </div>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Filters */}
        <div className="flex gap-3 mb-6 flex-wrap">
          <div className="relative flex-1 min-w-64">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              type="text"
              className="pl-10"
              placeholder="Search by name or email..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <Select value={dept} onValueChange={setDept}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Department" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="__all__">All Departments</SelectItem>
              {departments.map((d) => (
                <SelectItem key={d} value={d}>
                  {d}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select value={role} onValueChange={setRole}>
            <SelectTrigger className="w-48">
              <SelectValue placeholder="Role" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="__all__">All Roles</SelectItem>
              <SelectItem value="employee">Employee</SelectItem>
              <SelectItem value="manager">Manager</SelectItem>
              <SelectItem value="hr">HR</SelectItem>
              <SelectItem value="admin">Admin</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Add New Button */}
        <div className="flex justify-end mb-6">
          <Button asChild>
            <a href="add-new-employee">Add New Employee</a>
          </Button>
        </div>

        {/* Table */}
        <div className="border rounded-lg overflow-hidden">
          {loading ? (
            <div className="text-center py-12 text-muted-foreground">
              Loading employees...
            </div>
          ) : employees.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground">
              No employees found
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Department</TableHead>
                  <TableHead>Role</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {employees.map((emp) => (
                  <TableRow key={emp.id}>
                    <TableCell className="font-medium">{emp.name}</TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {emp.email}
                    </TableCell>
                    <TableCell>{emp.department || "—"}</TableCell>
                    <TableCell>{emp.role || "—"}</TableCell>
                    <TableCell className="text-right">
                      <div className="flex gap-2 justify-end">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleViewStart(emp)}
                        >
                          View
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleEditStart(emp)}
                        >
                          Edit
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </div>

        {/* Pagination */}
        <div className="flex justify-between items-center mt-6">
          <div className="text-sm text-muted-foreground">
            Showing {employees.length > 0 ? (currentPage - 1) * pageSize + 1 : 0}{" "}
            to {Math.min(currentPage * pageSize, totalEmployees)} of{" "}
            {totalEmployees} employees
          </div>

          <div className="flex gap-2 items-center">
            <Button
              variant="outline"
              size="sm"
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
            >
              Previous
            </Button>

            <div className="flex gap-1">
              {Array.from({ length: totalPages }, (_, i) => i + 1)
                .slice(Math.max(0, currentPage - 2), Math.min(totalPages, currentPage + 2))
                .map((page) => (
                  <Button
                    key={page}
                    variant={currentPage === page ? "default" : "outline"}
                    size="sm"
                    onClick={() => handlePageChange(page)}
                  >
                    {page}
                  </Button>
                ))}
            </div>

            <Button
              variant="outline"
              size="sm"
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === totalPages}
            >
              Next
            </Button>

            <Select
              value={pageSize.toString()}
              onValueChange={(val) => {
                setPageSize(Number(val));
                setCurrentPage(1);
              }}
            >
              <SelectTrigger className="w-32">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="5">5 per page</SelectItem>
                <SelectItem value="10">10 per page</SelectItem>
                <SelectItem value="25">25 per page</SelectItem>
                <SelectItem value="50">50 per page</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>

      {/* View Dialog */}
      <Dialog open={viewOpen} onOpenChange={setViewOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Employee Details</DialogTitle>
          </DialogHeader>
          <div className="grid grid-cols-2 gap-6 py-4">
            <div className="space-y-4">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Name</p>
                <p className="text-base">{selectedEmployee?.name}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">Email</p>
                <p className="text-base">{selectedEmployee?.email}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">Phone</p>
                <p className="text-base">{selectedEmployee?.phone || "—"}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  Department
                </p>
                <p className="text-base">{selectedEmployee?.department || "—"}</p>
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Role</p>
                <p className="text-base">{selectedEmployee?.job_role || "—"}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">Manager</p>
                <p className="text-base">{selectedEmployee?.manager || "—"}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">Team</p>
                <p className="text-base">{selectedEmployee?.team || "—"}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  Status
                </p>
                <p className="text-base">
                  {selectedEmployee?.is_active ? "Active" : "Inactive"}
                </p>
              </div>
            </div>
          </div>
          <DialogFooter className="gap-2">
            <DialogClose asChild>
              <Button variant="outline">Close</Button>
            </DialogClose>
            <Button
              variant="destructive"
              onClick={() =>
                selectedEmployee && handleDeleteEmployee(selectedEmployee.id)
              }
            >
              Deactivate
            </Button>
            <Button
              onClick={() => {
                setEditForm({ ...selectedEmployee });
                setEditOpen(true);
                setViewOpen(false);
              }}
            >
              Edit
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Edit Dialog */}
      <Dialog open={editOpen} onOpenChange={setEditOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Employee</DialogTitle>
          </DialogHeader>
          <div className="grid grid-cols-2 gap-4 py-4">
            <div className="col-span-2">
              <label className="text-sm font-medium mb-2 block">Name</label>
              <Input
                value={editForm?.name || ""}
                onChange={(e) =>
                  setEditForm({ ...editForm, name: e.target.value })
                }
                placeholder="Full name"
              />
            </div>
            <div className="col-span-2">
              <label className="text-sm font-medium mb-2 block">Email</label>
              <Input
                type="email"
                value={editForm?.email || ""}
                onChange={(e) =>
                  setEditForm({ ...editForm, email: e.target.value })
                }
                placeholder="Email address"
              />
            </div>
            <div>
              <label className="text-sm font-medium mb-2 block">Phone</label>
              <Input
                value={editForm?.phone || ""}
                onChange={(e) =>
                  setEditForm({ ...editForm, phone: e.target.value })
                }
                placeholder="Phone number"
              />
            </div>
            <div>
              <label className="text-sm font-medium mb-2 block">Job Role</label>
              <Input
                value={editForm?.job_role || ""}
                onChange={(e) =>
                  setEditForm({ ...editForm, job_role: e.target.value })
                }
                placeholder="Job role"
              />
            </div>
          </div>
          <DialogFooter className="gap-2">
            <DialogClose asChild>
              <Button variant="outline">Cancel</Button>
            </DialogClose>
            <Button
              onClick={handleSaveEdit}
              disabled={editLoading}
            >
              {editLoading ? "Saving..." : "Update"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}