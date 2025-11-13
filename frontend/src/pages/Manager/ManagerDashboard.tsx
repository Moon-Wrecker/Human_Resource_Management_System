"use client";

import { useEffect, useState } from "react";
import EmployeeDashboardCard from "@/components/EmployeeDashboardCard";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { PieChart, Pie, Cell } from "recharts";
import { ChartContainer, ChartLegend, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";
import { Table, TableHeader, TableBody, TableHead, TableRow, TableCell } from "@/components/ui/table";
import { ScrollArea } from "@/components/ui/scroll-area";
import { dashboardService } from "@/services/dashboardService";
import type { ManagerDashboardData } from "@/services/dashboardService";

const attendanceChartConfig = {
  present: { label: "Present %", color: "#34d399" },
  absent: { label: "Absent %", color: "#ef4444" }
};

const leaderboardChartConfig = {
  score: { label: "Modules Completed", color: "#38bdf8" }
};

const ManagerDashboard = () => {
  const [dashboardData, setDashboardData] = useState<ManagerDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const data = await dashboardService.getManagerDashboard();
        setDashboardData(data);
      } catch (err: any) {
        console.error('Failed to fetch manager dashboard data:', err);
        setError(err.response?.data?.detail || 'Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <main className="flex items-center justify-center min-h-screen">
        <div className="text-xl font-semibold">Loading dashboard...</div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="flex items-center justify-center min-h-screen">
        <div className="text-xl font-semibold text-red-600">Error: {error}</div>
      </main>
    );
  }

  if (!dashboardData) {
    return null;
  }

  // Transform data for charts
  const doughnutData = [
    { key: "Completed", value: dashboardData.team_goals.completed_goals, fill: "#34d399" },
    { key: "Pending", value: dashboardData.team_goals.total_goals - dashboardData.team_goals.completed_goals, fill: "#ef4444" }
  ];

  const leaderboardData = dashboardData.team_modules_leaderboard
    .slice(0, 5)
    .map(member => ({
      name: member.employee_name.split(' ')[0], // First name only for display
      score: member.modules_completed
    }));

  // Format check-in/out times
  const checkInTime = dashboardData.today_attendance?.check_in_time 
    ? new Date(dashboardData.today_attendance.check_in_time).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
    : 'N/A';
  
  const checkOutTime = dashboardData.today_attendance?.check_out_time 
    ? new Date(dashboardData.today_attendance.check_out_time).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
    : 'N/A';

  return (
    <main className="min-h-screen bg-white flex flex-col items-center w-full py-10 px-2">
      <h2 className="text-3xl font-semibold text-center mt-2">
        Welcome, <span className="text-blue-700">Manager</span>
      </h2>
      <div className="w-full max-w-6xl flex flex-col gap-12 mx-auto mt-10">
        {/* Leave Balance Cards - 5 cards showing all leave types separately */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <EmployeeDashboardCard title="Casual Leave" content={dashboardData.personal_info.casual_leave.toString()} />
          <EmployeeDashboardCard title="Sick Leave" content={dashboardData.personal_info.sick_leave.toString()} />
          <EmployeeDashboardCard title="Annual Leave" content={dashboardData.personal_info.annual_leave.toString()} />
          <EmployeeDashboardCard title="WFH Left" content={dashboardData.personal_info.wfh_balance.toString()} />
          <EmployeeDashboardCard title="Learner Rank" content={dashboardData.learner_rank?.toString() || 'N/A'} />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg font-bold">Punch In / Out</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col items-center gap-2">
              <p className="text-lg">
                <span className="font-bold">Punch In Time: </span>{checkInTime}
              </p>
              <p className="text-lg">
                <span className="font-bold">Punch Out Time: </span>{checkOutTime}
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="text-lg font-bold">Upcoming Holidays</CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <ScrollArea className="h-56 w-full">
                <div className="flex flex-col p-4 space-y-4">
                  {dashboardData.upcoming_holidays.map((holiday) => (
                    <div
                      key={holiday.id}
                      className="flex flex-col p-3 rounded-lg border-b"
                    >
                      <h3 className="text-lg font-bold">{holiday.name}</h3>
                      <p className="text-sm">
                        {holiday.start_date === holiday.end_date
                          ? holiday.start_date
                          : `${holiday.start_date} - ${holiday.end_date}`}
                      </p>
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </CardContent>
          </Card>
        </div>
        <section>
          <h2 className="text-xl font-bold mb-6">Team Overview</h2>
          <div className="grid md:grid-cols-2 grid-cols-1 gap-6">
            {/* Team Goals Chart */}
            <Card>
              <CardHeader>
                <CardTitle>Team Goals</CardTitle>
              </CardHeader>
              <CardContent>
                <ChartContainer config={attendanceChartConfig} className="w-full h-64">
                  <PieChart>
                    <Pie
                      data={doughnutData}
                      dataKey="value"
                      nameKey="key"
                      innerRadius={45}
                      outerRadius={60}
                      label
                    >
                      {doughnutData.map((entry, idx) => (
                        <Cell key={`cell-${idx}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <ChartTooltip content={<ChartTooltipContent hideLabel={false} />} />
                    <ChartLegend />
                  </PieChart>
                </ChartContainer>
              </CardContent>
            </Card>
            {/* Learner Leaderboard */}
            <Card>
              <CardHeader>
                <CardTitle>Learner Leaderboard</CardTitle>
              </CardHeader>
              <CardContent>
                <ChartContainer config={leaderboardChartConfig} className="w-full h-64">
                  <BarChart data={leaderboardData} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number"/>
                    <YAxis dataKey="name" type="category"/>
                    <Bar dataKey="score" fill="#38bdf8" name="Modules" barSize={24} />
                    <ChartTooltip content={<ChartTooltipContent hideLabel={false} />} />
                    <ChartLegend />
                  </BarChart>
                </ChartContainer>
              </CardContent>
            </Card>
          </div>
          <div className="grid md:grid-cols-2 grid-cols-1 gap-6 mt-6">
            {/* Team Stats Cards */}
            <Card>
              <CardHeader>
                <CardTitle>Team Training Hours</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl text-center font-bold mt-2">
                  {dashboardData.team_stats?.team_training_hours.toFixed(1) || '0.0'}
                </div>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Team Performance Score</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl text-center font-bold mt-2">
                  {dashboardData.team_stats?.team_performance_score.toFixed(2) || '0.0'}
                </div>
              </CardContent>
            </Card>
          </div>
        </section>
      </div>
    </main>
  );
};

export default ManagerDashboard;
