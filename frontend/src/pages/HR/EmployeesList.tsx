"use client";

import { useState } from "react";

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

type Employee = {
  name: string;
  department: string;
  email: string;
  phone: string;
  role: string;
  manager: string;
  team: string;
  id: string;                    
  performanceUrl: string;         
  aadharUrl: string;              
  panUrl: string;                 
};

const departments = ["Finance", "HR", "Operations", "Sales", "Engineering"];

const initialEmployees = [
  {
    name: "Person A",
    department: "Finance",
    email: "a@domain.com",
    phone: "123456",
    role: "SDE-I",
    manager: "Manager 1",
    team: "Finance Team",
    id: "E0101",
    performanceUrl: "#",
    aadharUrl: "#",
    panUrl: "#",
  },
  {
    name: "Person B",
    department: "HR",
    email: "b@domain.com",
    phone: "987654",
    role: "HR Manager",
    manager: "Manager 2",
    team: "HR Team",
    id: "E0102",
    performanceUrl: "#",
    aadharUrl: "#",
    panUrl: "#",
  },
  // ...repeat with your real data as needed
];

export default function EmployeeList() {
  const [search, setSearch] = useState("");
  const [dept, setDept] = useState("");
  const [employees] = useState(initialEmployees);
  const [viewOpen, setViewOpen] = useState(false);
  const [editOpen, setEditOpen] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState(initialEmployees[0]);

  const filteredEmployees = employees.filter(
    (e) =>
      (search === "" || e.name.toLowerCase().includes(search.toLowerCase())) &&
      (dept === "" || e.department === dept)
  );

  // Used for editing
  const [editForm, setEditForm] = useState(selectedEmployee);

const handleEditStart = (emp: Employee) => {
  setSelectedEmployee(emp);
  setEditForm(emp);
  setEditOpen(true);
};

const handleViewStart = (emp: Employee) => {
  setSelectedEmployee(emp);
  setViewOpen(true);
};

  return (
    <div className="min-h-screen bg-[#fafafa] flex flex-col items-center py-8">
      <h1 className="text-2xl font-bold mb-8">Employee List</h1>
      <div className="flex gap-8 mb-8">
        <div className="bg-gray-200 flex items-center rounded w-80 px-4 py-2">
          <input
            type="text"
            className="bg-gray-200 outline-none w-full px-1"
            placeholder="Search Employees"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <span className="ml-2 text-gray-500">&#128269;</span>
        </div>
        <select
          value={dept}
          onChange={(e) => setDept(e.target.value)}
          className="bg-gray-200 rounded w-56 px-4 py-2"
        >
          <option value="">Department</option>
          {departments.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>
      </div>
      <div className="w-full flex justify-end pr-24 mb-2">
        <a
          href="/employees-list/add-new-employee"
          className="text-black underline font-medium text-lg"
        >
          Add New &rarr;
        </a>
      </div>
      <div className="flex justify-center w-full items-center">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead></TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Department</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredEmployees.map((emp, idx) => (
              <TableRow key={idx}>
                <TableCell></TableCell>
                <TableCell>{emp.name}</TableCell>
                <TableCell>{emp.department}</TableCell>
                <TableCell>
                  <button
                    className="underline mr-4"
                    onClick={() => handleViewStart(emp)}
                  >
                    Details
                  </button>
                  <button
                    className="underline mr-4"
                    onClick={() => handleEditStart(emp)}
                  >
                    Edit
                  </button>
                  <a href="#" className="underline">
                    Performance
                  </a>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      {/* View Employee Dialog */}
      <Dialog open={viewOpen} onOpenChange={setViewOpen}>
        <DialogContent className="max-w-xl">
          <DialogHeader>
            <DialogTitle>Employee details</DialogTitle>
          </DialogHeader>
          <div className="flex gap-8 py-2">
            {/* Left Side */}
            <div className="space-y-2 min-w-[210px]">
              <div>
                <span className="font-bold underline">Name:</span>&nbsp;
                {selectedEmployee?.name}
              </div>
              <div>
                <span className="font-bold underline">Email:</span>&nbsp;
                {selectedEmployee?.email}
              </div>
              <div>
                <span className="font-bold underline">Phone No.:</span>&nbsp;
                {selectedEmployee?.phone}
              </div>
              <div>
                <span className="font-bold underline">Department:</span>&nbsp;
                {selectedEmployee?.department}
              </div>
              <div>
                <span className="font-bold underline">Position/Role:</span>&nbsp;
                {selectedEmployee?.role}
              </div>
            </div>
            {/* Right Side */}
            <div className="space-y-2 min-w-[210px]">
              <div>
                <span className="font-bold underline">Manager Name:</span>&nbsp;
                {selectedEmployee?.manager}
              </div>
              <div>
                <span className="font-bold underline">Team:</span>&nbsp;
                {selectedEmployee?.team}
              </div>
              <div>
                <span className="font-bold underline">Employee ID:</span>&nbsp;
                {selectedEmployee?.id}
              </div>
              <div>
                <span className="font-bold underline">Submitted Documents:</span>
                <div>
                  <a href={selectedEmployee?.aadharUrl} className="underline mr-2">
                    Aadhar ↗
                  </a>
                  <a href={selectedEmployee?.panUrl} className="underline">
                    PAN ↗
                  </a>
                </div>
              </div>
              <div>
                <a href={selectedEmployee?.performanceUrl} className="underline">
                  View Performance Report &rarr;
                </a>
              </div>
            </div>
          </div>
          <div className="flex justify-end gap-4 mt-4">
            <button className="bg-red-200 px-6 py-2 rounded font-semibold border">
              Remove
            </button>
            <DialogClose asChild>
              <button
                className="bg-gray-200 px-6 py-2 rounded font-semibold border"
                onClick={() => { setEditForm(selectedEmployee); setEditOpen(true); setViewOpen(false); }}
              >
                Edit
              </button>
            </DialogClose>
          </div>
        </DialogContent>
      </Dialog>

      {/* Edit Employee Dialog */}
      <Dialog open={editOpen} onOpenChange={setEditOpen}>
        <DialogContent className="max-w-lg bg-white rounded-2xl shadow-xl px-8 py-7">
            <DialogHeader>
            <DialogTitle className="text-2xl font-semibold mb-6">Edit Employee Details</DialogTitle>
            </DialogHeader>
            <form>
            <div className="grid grid-cols-2 gap-x-8 gap-y-6">
                {/* Left Column */}
                <div className="flex flex-col gap-5">
                <div>
                    <label className="block text-sm font-bold mb-1">Name</label>
                    <input
                    name="name"
                    className="w-full border rounded px-3 py-2 bg-gray-100 focus:border-blue-500 outline-none"
                    value={editForm?.name}
                    onChange={e => setEditForm({ ...editForm, name: e.target.value })}
                    placeholder="Name"
                    />
                </div>
                <div>
                    <label className="block text-sm font-bold mb-1">Email</label>
                    <input
                    name="email"
                    className="w-full border rounded px-3 py-2 bg-gray-100 focus:border-blue-500 outline-none"
                    value={editForm?.email}
                    onChange={e => setEditForm({ ...editForm, email: e.target.value })}
                    type="email"
                    placeholder="Email"
                    />
                </div>
                <div>
                    <label className="block text-sm font-bold mb-1">Phone</label>
                    <input
                    name="phone"
                    className="w-full border rounded px-3 py-2 bg-gray-100 focus:border-blue-500 outline-none"
                    value={editForm?.phone}
                    onChange={e => setEditForm({ ...editForm, phone: e.target.value })}
                    placeholder="Phone"
                    />
                </div>
                </div>
                {/* Right Column */}
                <div className="flex flex-col gap-5">
                <div>
                    <label className="block text-sm font-bold mb-1">Department</label>
                    <select
                    name="department"
                    className="w-full border rounded px-3 py-2 bg-gray-100 focus:border-blue-500 outline-none"
                    value={editForm?.department}
                    onChange={e => setEditForm({ ...editForm, department: e.target.value })}
                    >
                    <option value="">Select department</option>
                    {departments.map(dep => (
                        <option value={dep} key={dep}>{dep}</option>
                    ))}
                    </select>
                </div>
                <div>
                    <label className="block text-sm font-bold mb-1">Role</label>
                    <input
                    name="role"
                    className="w-full border rounded px-3 py-2 bg-gray-100 focus:border-blue-500 outline-none"
                    value={editForm?.role}
                    onChange={e => setEditForm({ ...editForm, role: e.target.value })}
                    placeholder="Role"
                    />
                </div>
                <div className="flex gap-3">
                    <div className="flex-1">
                    <label className="block text-sm font-bold mb-1">Manager</label>
                    <input
                        name="manager"
                        className="w-full border rounded px-3 py-2 bg-gray-100 focus:border-blue-500 outline-none"
                        value={editForm?.manager}
                        onChange={e => setEditForm({ ...editForm, manager: e.target.value })}
                        placeholder="Manager"
                    />
                    </div>
                    <div className="flex-1">
                    <label className="block text-sm font-bold mb-1">Team</label>
                    <input
                        name="team"
                        className="w-full border rounded px-3 py-2 bg-gray-100 focus:border-blue-500 outline-none"
                        value={editForm?.team}
                        onChange={e => setEditForm({ ...editForm, team: e.target.value })}
                        placeholder="Team"
                    />
                    </div>
                </div>
                </div>
            </div>
            <DialogFooter className="mt-8 flex justify-end gap-4">
                <DialogClose asChild>
                <button
                    type="submit"
                    className="bg-blue-600 text-white px-7 py-2 rounded font-semibold hover:bg-blue-700 shadow"
                    onClick={e => { e.preventDefault(); setEditOpen(false); }}
                >
                    Update
                </button>
                </DialogClose>
            </DialogFooter>
            </form>
        </DialogContent>
        </Dialog>
    </div>
  );
}
