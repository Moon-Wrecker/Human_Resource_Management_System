"use client";

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

const attendanceData = [
  { emp: "Emp1", present: 80, absent: 20 },
  { emp: "Emp2", present: 55, absent: 45 },
  { emp: "Emp3", present: 70, absent: 30 },
  { emp: "Emp4", present: 75, absent: 25 },
  { emp: "Emp5", present: 65, absent: 35 },
];

const attendanceChartConfig = {
  present: { label: "Present %", color: "#34d399" },
  absent: { label: "Absent %", color: "#ef4444" }
};

const leaderboardData = [
  { emp: "Emp2", score: 5 },
  { emp: "Emp4", score: 4.5 },
  { emp: "Emp3", score: 4 },
  { emp: "Emp1", score: 3.8 },
  { emp: "Emp5", score: 3 },
];

const leaderboardChartConfig = {
  score: { label: "Modules Completed", color: "#38bdf8" }
};

const holidays = [
  { name: "Diwali", startDate: "2025-11-01", endDate: "2025-11-01" },
  { name: "Christmas", startDate: "2025-12-25", endDate: "2025-12-25" },
  { name: "New Year", startDate: "2026-01-01", endDate: "2026-01-01" },
  { name: "Makar Sankranti", startDate: "2026-01-14", endDate: "2026-01-14" },
  { name: "Republic Day", startDate: "2026-01-26", endDate: "2026-01-26" },
];

const departments = [
  { department: "Finance", count: 5 },
  { department: "HR", count: 10 },
  { department: "Engineering", count: 20 },
  { department: "Operations", count: 10 },
  { department: "Sales", count: 5 },
  { department: "Department 7", count: 7 },
];

const doughnutData = [
  { key: "Completed", value: 74, fill: "#34d399" },
  { key: "Pending", value: 26, fill: "#ef4444" }
];

const ManagerDashboard = () => (
  <main className="min-h-screen bg-white flex flex-col items-center w-full py-10 px-2">
    <h2 className="text-3xl font-semibold text-center mt-2">
      Welcome, <span className="text-blue-700">John Doe</span>
    </h2>
    <div className="w-full max-w-6xl flex flex-col gap-12 mx-auto mt-10">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <EmployeeDashboardCard title="WFH Left" content="8" />
        <EmployeeDashboardCard title="Leaves Left" content="8" />
        <EmployeeDashboardCard title="Learner Rank" content="3" />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-bold">Punch In / Out</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col items-center gap-2">
            <p className="text-lg">
              <span className="font-bold">Punch In Time: </span>09:04 AM
            </p>
            <p className="text-lg">
              <span className="font-bold">Punch Out Time: </span>N/A
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
                {holidays.map((holiday, idx) => (
                  <div
                    key={idx}
                    className="flex flex-col p-3 rounded-lg border-b"
                  >
                    <h3 className="text-lg font-bold">{holiday.name}</h3>
                    <p className="text-sm">
                      {holiday.startDate === holiday.endDate
                        ? holiday.startDate
                        : `${holiday.startDate} - ${holiday.endDate}`}
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
          {/* Attendance Table */}
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
          {/* Leaderboard Table */}
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
                  <Bar dataKey="score" fill="#38bdf8" name="Score" barSize={24} />
                  <ChartTooltip content={<ChartTooltipContent hideLabel={false} />} />
                  <ChartLegend />
                </BarChart>
              </ChartContainer>
            </CardContent>
          </Card>
        </div>
        <div className="grid md:grid-cols-2 grid-cols-1 gap-6 mt-6">
          {/* Department Table */}
          <Card className="col-span-2">
            <CardHeader>
              <CardTitle>Department Employee Count</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Department</TableHead>
                    <TableHead>Employees</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {departments.map((row, idx) => (
                    <TableRow key={row.department}>
                      <TableCell>{row.department}</TableCell>
                      <TableCell>{row.count}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Team training hours</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl text-center font-bold mt-2">1.3k</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Team performance score</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl text-center font-bold mt-2">3.9</div>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  </main>
);

export default ManagerDashboard;
