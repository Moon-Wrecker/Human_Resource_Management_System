import EmployeeDashboardCard from "@/components/EmployeeDashboardCard";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";

const ManagerDashboard = () => {
  const holidays = [
    {
      name: "Diwali",
      startDate: "2025-11-01",
      endDate: "2025-11-01",
    },
    {
      name: "Christmas",
      startDate: "2025-12-25",
      endDate: "2025-12-25",
    },
    {
      name: "New Year",
      startDate: "2026-01-01",
      endDate: "2026-01-01",
    },
    {
      name: "Makar Sankranti",
      startDate: "2026-01-14",
      endDate: "2026-01-14",
    },
    {
      name: "Republic Day",
      startDate: "2026-01-26",
      endDate: "2026-01-26",
    },
  ];

  return (
    <main className="flex items-center justify-center flex-col gap-2 my-4">
      <h2 className="text-3xl font-semibold text-center mt-8">
        Welcome, <span className="text-blue-700">John Doe</span>
      </h2>
      <div className="flex items-center justify-center flex-col w-full gap-4">
        <div className="grid grid-cols-3 w-[80%] gap-4 px-4 mt-16">
          <EmployeeDashboardCard title="WFH Left" content="8" />
          <EmployeeDashboardCard title="Leaves Left" content="8" />
        </div>
        <div className="grid grid-cols-2 gap-4 px-4 w-[80%]">
          <div className="flex flex-col items-center gap-4 justify-center w-full">
            <Card className="text-center w-full">
              <CardContent className="flex flex-col gap-4 items-center justify-center">
                <p className="text-lg">
                  <span className="font-bold">Punch In Time: </span>09:04 AM
                </p>
                <p className="text-lg">
                  <span className="font-bold">Punch Out Time: </span>N/A
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
                    {holidays.map((holiday, index) => (
                      <div
                        key={index}
                        className="flex flex-col p-4 rounded-lg border-b "
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
        </div>
      </div>
    </main>
  );
};

export default ManagerDashboard;