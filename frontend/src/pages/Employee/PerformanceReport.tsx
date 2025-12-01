import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { ArrowRight } from "lucide-react";
import { ChartAreaDefault } from "@/components/AreaChart";
import performanceReportService, {
  type PerformanceReportResponse,
} from "@/services/performanceReportService";
import { useAuth } from "@/contexts/AuthContext";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export default function PerformanceReport() {
  const { user } = useAuth();
  const [timePeriod, setTimePeriod] = useState("Sep - Dec");
  const [reports, setReports] = useState<PerformanceReportResponse>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchReports = async () => {
      if (!user) return;
      try {
        setLoading(true);
        const response = await performanceReportService.getPerformanceReports(
          {},
        );
        setReports(response);
        setError(null);
      } catch (err) {
        setError("Failed to fetch performance reports.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, [user]);

  if (loading) {
    return (
      <div className="text-center py-10">Loading performance reports...</div>
    );
  }

  if (error) {
    return <div className="text-center py-10 text-red-500">{error}</div>;
  }

  return (
    <div className="w-full px-4 flex items-center justify-center flex-col gap-6">
      <h2 className="text-3xl font-semibold text-center mt-8">
        Performance Report
      </h2>
      <Select onValueChange={(e) => setTimePeriod(e)} value={timePeriod}>
        <SelectTrigger className="w-[20%]">
          <SelectValue placeholder="Time Period" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="Sep - Dec">Sep - Dec</SelectItem>
          <SelectItem value="Jan - Mar">Jan - Mar</SelectItem>
          <SelectItem value="Apr - Jun">Apr - Jun</SelectItem>
          <SelectItem value="Jul - Sep">Jul - Sep</SelectItem>
        </SelectContent>
      </Select>
      <h3 className="text-xl font-semibold text-center">
        Performance Report for {timePeriod}
      </h3>
      <div className="grid grid-cols-3 gap-4 w-[80%] grid-rows-4">
        <Card className="w-full text-center">
          <CardHeader className="text-xl font-bold">Training Hours</CardHeader>
          <CardContent className="text-lg font-semibold">
            {(reports?.total_modules_completed || 0) * 2.5}
          </CardContent>
        </Card>
        {/* TODO: Fetch Value */}
        <Card className="w-full text-center">
          <CardHeader className="text-xl font-bold">
            Performance Score
          </CardHeader>
          <CardContent className="text-lg font-semibold">4.3</CardContent>
        </Card>
        <Card className="w-full text-center">
          <CardHeader className="text-xl font-bold">
            Modules Completed
          </CardHeader>
          <CardContent className="text-lg font-semibold">
            {reports?.total_modules_completed || "0"}
          </CardContent>
        </Card>
        <Card className="w-full text-center">
          <CardHeader className="text-xl font-bold">Learner Rank</CardHeader>
          <CardContent className="text-lg font-semibold">3</CardContent>
        </Card>
        <ChartAreaDefault chartData={reports?.monthly_modules} />
        {/* TODO: Fetch Value */}
        <Card className="w-full text-center">
          <CardHeader className="text-xl font-bold">
            Punctuality Score
          </CardHeader>
          <CardContent className="text-lg font-semibold">4.9</CardContent>
        </Card>
        <Card className="w-full text-center">
          <CardHeader className="text-xl font-bold">Latest Feedback</CardHeader>
          <CardContent className="text-md">
            <span>Good Work completing the milestone</span>
            <a href="/employee/performance-report/feedbacks" className="mt-1">
              <Button variant="link" className="cursor-pointer">
                View Previous feedbacks <ArrowRight />
              </Button>
            </a>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
