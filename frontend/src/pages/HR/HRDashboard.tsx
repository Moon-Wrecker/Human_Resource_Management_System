"use client";

import { useEffect, useState } from 'react';
import { ChartContainer, ChartTooltip, ChartTooltipContent } from '@/components/ui/chart';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";

import { dashboardService } from '@/services/dashboardService';
import type { HRDashboardData } from '@/services/dashboardService';

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

const HRDashboard = () => {
  const [dashboardData, setDashboardData] = useState<HRDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const data = await dashboardService.getHRDashboard();
        setDashboardData(data);
      } catch (err: any) {
        console.error('Failed to fetch HR dashboard data:', err);
        setError(err.response?.data?.detail || 'Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-xl font-semibold">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-xl font-semibold text-red-600">Error: {error}</div>
      </div>
    );
  }

  if (!dashboardData) {
    return null;
  }

  // Transform data for charts
  const attendanceData = dashboardData.department_attendance.map(dept => ({
    name: dept.department_name.substring(0, 8), // Shorten for display
    present: dept.present_percentage,
    absent: dept.absent_percentage
  }));

  const leaderboardData = dashboardData.department_modules
    .sort((a, b) => b.modules_completed - a.modules_completed)
    .slice(0, 5)
    .map(dept => ({
      dept: dept.department_name,
      score: dept.modules_completed
    }));

  return (
  <div className="min-h-screen bg-white p-0 m-0">
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
              {dashboardData.departments.map((row) => (
                <TableRow key={row.department_id}>
                  <TableCell>{row.department_name}</TableCell>
                  <TableCell>{row.employee_count}</TableCell>
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
              {dashboardData.active_applications.map((app) => (
                <TableRow key={app.application_id}>
                  <TableCell className="flex items-center gap-2">
                    <span className="w-6 h-6 flex items-center justify-center rounded-full bg-purple-100 text-purple-700">👤</span> 
                    {app.applicant_name}
                  </TableCell>
                  <TableCell>{app.applied_role}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <a href="hr/applications" className="text-blue-600 text-sm mt-2 block w-full text-right">View all applications &gt;</a>
        </div>
      </div>
    </div>
  </div>
  );
};

export default HRDashboard;
