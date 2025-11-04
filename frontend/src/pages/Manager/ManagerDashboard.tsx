import EmployeeDashboardCard from "@/components/EmployeeDashboardCard";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";

const attendanceData = [
  { emp: "Emp1", present: 80, absent: 20 },
  { emp: "Emp2", present: 55, absent: 45 },
  { emp: "Emp3", present: 70, absent: 30 },
  { emp: "Emp4", present: 75, absent: 25 },
  { emp: "Emp5", present: 65, absent: 35 },
];

const leaderboardData = [
  { emp: "Emp2", score: 5 },
  { emp: "Emp4", score: 4.5 },
  { emp: "Emp3", score: 4 },
  { emp: "Emp1", score: 3.8 },
  { emp: "Emp5", score: 3 },
];

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
      <hr/>
      <div className="min-h-screen bg-white flex flex-col items-center px-6 pt-10">
        <h2 className="text-xl font-bold mb-3">Team Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6 w-full max-w-4xl">
          {/* Team Goals Donut */}
          <Card>
            <CardHeader>
            <span className="font-bold text-lg block">Team Goals</span>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col items-center justify-center">
                {/* SVG Donut */}
                <svg width="120" height="120" viewBox="0 0 42 42" className="mb-3">
                  <circle cx="21" cy="21" r="15" fill="none" stroke="#eee" strokeWidth="6" />
                  {/* Completed */}
                  <circle
                    cx="21" cy="21" r="15"
                    fill="none" stroke="#95e39c" strokeWidth="6"
                    strokeDasharray={`${2 * Math.PI * 15 * 0.74} ${2 * Math.PI * 15 * 0.26}`}
                    strokeDashoffset={2 * Math.PI * 15 * 0.13}
                  />
                  {/* Pending */}
                  <circle
                    cx="21" cy="21" r="15"
                    fill="none" stroke="#ee6557" strokeWidth="6"
                    strokeDasharray={`${2 * Math.PI * 15 * 0.26} ${2 * Math.PI * 15 * 0.74}`}
                    strokeDashoffset={-(2 * Math.PI * 15 * 0.87)}
                  />
                  <text x="13" y="23" fontSize="8" fontWeight="bold">74%</text>
                  <text x="29" y="29" fontSize="8" fontWeight="bold">26%</text>
                </svg>
                <div className="flex gap-5 text-sm">
                  <span className="flex items-center gap-1">
                    <span className="w-3 h-3 rounded-full inline-block" style={{ background: "#95e39c" }} /> Completed
                  </span>
                  <span className="flex items-center gap-1">
                    <span className="w-3 h-3 rounded-full inline-block" style={{ background: "#ee6557" }} /> Pending
                  </span>
                </div>
              </div>
             </CardContent>
            </Card>
            {/* Attendance Bar Chart */}
            <Card>
              <CardHeader>
                <span className="font-bold text-lg block">Attendance</span>
              </CardHeader>
              <CardContent>
                <svg width="220" height="100">
                  {/* Axes */}
                  <line x1="30" y1="75" x2="190" y2="75" stroke="#222" />
                  <line x1="30" y1="20" x2="30" y2="75" stroke="#222" />
                  {/* Bars */}
                  {attendanceData.map((d, i) => (
                    <g key={d.emp}>
                      <rect x={40 + i * 32} y={75 - d.present * 0.5} width="10" height={d.present * 0.5} fill="#95e39c" />
                      <rect x={52 + i * 32} y={75 - d.absent * 0.5} width="10" height={d.absent * 0.5} fill="#ee6557" />
                      <text x={45 + i * 32} y={90} fontSize={10} textAnchor="middle">{d.emp}</text>
                    </g>
                  ))}
                </svg>
                <div className="flex gap-4 mt-2 text-sm">
                  <span className="flex items-center gap-1">
                    <span className="w-3 h-3 inline-block rounded-full bg-[#95e39c]" /> Present %
                  </span>
                  <span className="flex items-center gap-1">
                    <span className="w-3 h-3 inline-block rounded-full bg-[#ee6557]" /> Absent %
                  </span>
                </div>
              </CardContent>
            </Card>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5 w-full max-w-4xl">
            {/* Team training hours */}
            <Card>
              <CardContent className="py-6 text-center">
                <div className="font-bold text-lg">Team training hours</div>
                <div className="text-xl font-bold mt-2">1.3k</div>
              </CardContent>
            </Card>
            {/* Learner Leaderboard */}
            <Card>
              <CardHeader>
                <span className="font-bold text-lg block">Learner leader board</span>
                <span className="text-xs text-gray-500">(Modules completion leader board)</span>
              </CardHeader>
              <CardContent>
                <svg width="190" height="90">
                  {/* Axes */}
                  <line x1="55" y1="80" x2="180" y2="80" stroke="#222" />
                  <line x1="55" y1="30" x2="55" y2="80" stroke="#222" />
                  {/* Bars and labels */}
                  {leaderboardData.map((d, i) => (
                    <g key={d.emp}>
                      <rect x="55" y={35 + i * 10} width={d.score * 25} height="8" fill="#95e39c" />
                      <text x="45" y={42 + i * 10} fontSize={9} textAnchor="end">{d.emp}</text>
                      <text x={60 + d.score * 25} y={42 + i * 10} fontSize={9}>{d.score}</text>
                    </g>
                  ))}
                </svg>
              </CardContent>
            </Card>
            {/* Team performance score */}
            <Card>
              <CardContent className="py-6 text-center">
                <div className="font-bold text-lg">Team performance score</div>
                <div className="text-xl font-bold mt-2">3.9</div>
              </CardContent>
            </Card>
          </div>
        </div>
    </main>
  );
};

export default ManagerDashboard;