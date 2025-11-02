import { HorizontalBarChart } from "@/components/ui/horizontal-bar-chart";
import { ChartBarMultiple } from "@/components/ui/multi-bar-chart";

const EmployeeDashboard = () => {
  return (
    <main className="flex items-center justify-center flex-col gap-2 my-4">
      <div className="grid grid-cols-2 gap-6 p-6 w-[80%]">
        <div className="flex items-center justify-center gap-2 flex-col w-full">
          <ChartBarMultiple title="Department-wise Attendance" />
        </div>{" "}
        <div className="flex items-center justify-center gap-2 flex-col w-full">
          <HorizontalBarChart
            title="Department-wise leader board"
            desc="(Skill modules completion leader board)"
          />
        </div>
        <div className="bg-red-500">H</div>
        <div className="bg-red-500">H</div>
      </div>
    </main>
  );
};

export default EmployeeDashboard;
