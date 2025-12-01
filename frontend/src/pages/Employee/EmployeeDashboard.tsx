import { useEffect, useState } from "react";
import EmployeeDashboardCard from "@/components/EmployeeDashboardCard";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { DoughnutChart } from "@/components/ui/dougnut-chart";
import { ScrollArea } from "@/components/ui/scroll-area";
import { dashboardService } from "@/services/dashboardService";
import type { EmployeeDashboardData } from "@/services/dashboardService";

const EmployeeDashboard = () => {
  const [dashboardData, setDashboardData] =
    useState<EmployeeDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const data = await dashboardService.getEmployeeDashboard();
        setDashboardData(data);
      } catch (err) {
        console.error("Failed to fetch employee dashboard data:", err);
        setError(err.response?.data?.detail || "Failed to load dashboard data");
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
  const learningGoalsData = [
    {
      label: "Completed",
      value: dashboardData.learning_goals.completed_goals,
      fill: "#00ff00",
    },
    {
      label: "Pending",
      value: dashboardData.learning_goals.pending_goals,
      fill: "#ff0000",
    },
  ];

  // Format check-in/out times
  const checkInTime = dashboardData.today_attendance?.check_in_time
    ? new Date(dashboardData.today_attendance.check_in_time).toLocaleTimeString(
        "en-US",
        { hour: "2-digit", minute: "2-digit" },
      )
    : "N/A";

  const checkOutTime = dashboardData.today_attendance?.check_out_time
    ? new Date(
        dashboardData.today_attendance.check_out_time,
      ).toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" })
    : "N/A";

  return (
    <main className="flex items-center justify-center flex-col gap-2 my-4">
      <h2 className="text-3xl font-semibold text-center mt-8">
        Welcome,{" "}
        <span className="text-blue-700">{dashboardData.employee_name}</span>
      </h2>
      <div className="flex items-center justify-center flex-col w-full gap-4">
        {/* Leave Balance Cards - 5 cards in a grid */}
        <div className="grid grid-cols-5 w-[90%] gap-4 px-4 mt-16">
          <EmployeeDashboardCard
            title="Casual Leave"
            content={dashboardData.leave_balance.casual_leave.toString()}
          />
          <EmployeeDashboardCard
            title="Sick Leave"
            content={dashboardData.leave_balance.sick_leave.toString()}
          />
          <EmployeeDashboardCard
            title="Annual Leave"
            content={dashboardData.leave_balance.annual_leave.toString()}
          />
          <EmployeeDashboardCard
            title="WFH Left"
            content={dashboardData.leave_balance.wfh_balance.toString()}
          />
          <EmployeeDashboardCard
            title="Learner Rank"
            content={dashboardData.learner_rank?.toString() || "N/A"}
          />
        </div>
        <div className="grid grid-cols-2 gap-4 px-4 w-[80%]">
          <DoughnutChart title="Learning Goals" data={learningGoalsData} />
          <div className="flex flex-col items-center gap-4 justify-center w-full">
            <Card className="text-center w-full">
              <CardContent className="flex flex-col gap-4 items-center justify-center">
                <p className="text-lg">
                  <span className="font-bold">Punch In Time: </span>
                  {checkInTime}
                </p>
                <p className="text-lg">
                  <span className="font-bold">Punch Out Time: </span>
                  {checkOutTime}
                </p>
              </CardContent>
            </Card>
            <Card className="text-center w-full">
              <CardHeader className="font-bold text-2xl">
                Upcoming Holidays
              </CardHeader>
              <CardContent className="overflow-auto max-h-56">
                <ScrollArea className="h-full w-full">
                  <div className="flex flex-col space-y-4 p-4">
                    {dashboardData.upcoming_holidays.map((holiday) => (
                      <div
                        key={holiday.id}
                        className="flex flex-col p-4 rounded-lg border-b "
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
        </div>
      </div>
    </main>
  );
};

export default EmployeeDashboard;
