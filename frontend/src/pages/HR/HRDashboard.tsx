"use client";

import { ChartContainer, ChartTooltip, ChartTooltipContent } from '@/components/ui/chart';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
  TableCaption,
} from "@/components/ui/table";

const attendanceData = [
  { name: "HR", present: 80, absent: 20 },
  { name: "Finance", present: 60, absent: 40 },
  { name: "Sales", present: 50, absent: 50 },
  { name: "Engg.", present: 90, absent: 10 },
  { name: "Oper.", present: 65, absent: 35 },
];

const leaderboardData = [
  { dept: "Dept 2", score: 15 },
  { dept: "Dept 4", score: 14.5 },
  { dept: "Dept 3", score: 14 },
  { dept: "Dept 1", score: 13.8 },
  { dept: "Dept 5", score: 13 },
];

const attendanceChartConfig = {
  present: {
    label: "Present %",
    color: "#34d399"
  },
  absent: {
    label: "Absent %",
    color: "#ef4444"
  }
};

const leaderboardChartConfig = {
  score: {
    label: "Modules Completed",
    color: "#22d3ee"
  }
};

const employeeData = [
  { department: "Finance", count: 5 },
  { department: "HR", count: 10 },
  { department: "Engineering", count: 20 },
  { department: "Operations", count: 10 },
  { department: "Sales", count: 5 },
  { department: "Department 7", count: 7 },
];

const activeApplications = [
  { name: "Person 1", position: "SDE - III" },
  { name: "Person 2", position: "Project Manager" },
  { name: "Person 3", position: "SDE - III" },
  { name: "Person 4", position: "SDE - II" },
];

const HRDashboard = () => (
  <div className="min-h-screen bg-[#fafafa] p-0 m-0">
    {/* Main content grid */}
    <div className="px-12 py-8">
      <h1 className="text-2xl font-bold text-center mb-6">HR Manager Dashboard</h1>
      <div className="grid grid-cols-2 gap-8 mb-6">
        {/* Attendance Graph */}
        <div className="bg-white rounded-xl shadow p-4 flex flex-col items-center">
          <span className="font-semibold mb-2 text-center">Department-wise Attendance</span>
          <ChartContainer config={attendanceChartConfig} className="w-full h-64">
            <BarChart data={attendanceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Bar dataKey="present" fill={attendanceChartConfig.present.color} name="Present %" />
              <Bar dataKey="absent" fill={attendanceChartConfig.absent.color} name="Absent %" />
              <ChartTooltip content={<ChartTooltipContent indicator="dot" />} />
            </BarChart>
          </ChartContainer>
          <div className="flex justify-center mt-4 gap-6 text-sm">
            <div className="flex items-center gap-1"><span className="w-3 h-3 bg-[#34d399] inline-block rounded-full"></span>Present %</div>
            <div className="flex items-center gap-1"><span className="w-3 h-3 bg-[#ef4444] inline-block rounded-full"></span>Absent %</div>
          </div>
        </div>
        {/* Leaderboard Graph */}
        <div className="bg-white rounded-xl shadow p-4 flex flex-col items-center">
          <span className="font-semibold mb-2 text-center">Department-wise leader board</span>
          <span className="text-xs text-gray-500 mb-1">(Skill modules completion leader board)</span>
          <ChartContainer config={leaderboardChartConfig} className="w-full h-64">
            <BarChart data={leaderboardData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="dept" type="category" />
              <Bar dataKey="score" fill={leaderboardChartConfig.score.color} name="Score" barSize={20} />
              <ChartTooltip content={<ChartTooltipContent indicator="dot" />} />
            </BarChart>
          </ChartContainer>
        </div>
      </div>
      {/* Department and Applications details */}
      <div className="grid grid-cols-3 gap-8">
        {/* Department Employee Table */}
        <div className="col-span-2 bg-white rounded-xl shadow p-5">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Department</TableHead>
                <TableHead>Employee Count</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {employeeData.map((row) => (
                <TableRow key={row.department}>
                  <TableCell>{row.department}</TableCell>
                  <TableCell>{row.count}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
        {/* Active Applications Table */}
        <div className="bg-white rounded-xl shadow p-5 flex flex-col items-start w-full">
          <h3 className="font-bold mb-2">Active Applications</h3>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Position</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {activeApplications.map((app, idx) => (
                <TableRow key={idx}>
                  <TableCell className="flex items-center gap-2">
                    <span className="w-6 h-6 flex items-center justify-center rounded-full bg-purple-100 text-purple-700">👤</span> 
                    {app.name}
                  </TableCell>
                  <TableCell>{app.position}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <a href="/applications" className="text-blue-600 text-sm mt-2 block w-full text-right">View all applications &gt;</a>
        </div>
      </div>
    </div>
  </div>
);

export default HRDashboard;
