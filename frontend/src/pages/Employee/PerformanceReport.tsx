import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { ArrowRight, Loader2 } from "lucide-react";
import { ChartAreaDefault } from "@/components/AreaChart";
import performanceReportService, {
  type PerformanceReportResponse,
} from "@/services/performanceReportService";
import aiPerformanceReportService, {
  type AIPerformanceReportResponse,
  AIReportTemplateEnum,
  AITimePeriodEnum,
} from "@/services/aiPerformanceReportService";
import { useAuth } from "@/contexts/AuthContext";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import feedbackService, {
  type FeedbackListResponse,
} from "@/services/feedbackService";

export default function PerformanceReport() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [timePeriod, setTimePeriod] = useState("Sep - Dec");
  const [reports, setReports] = useState<PerformanceReportResponse>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [feedback, setFeedback] = useState<FeedbackListResponse>();
  const [aiReportLoading, setAiReportLoading] = useState(false);

  useEffect(() => {
    const fetchReports = async () => {
      if (!user) return;
      try {
        setLoading(true);
        const [startDate, endDate] = timePeriod
          .split(" - ")
          .map((m, i) =>
            new Date(
              2025,
              [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
              ].indexOf(m) + i,
              i ? 0 : 1,
            )
              .toISOString()
              .slice(0, 10),
          );

        const response = await performanceReportService.getPerformanceReports({
          start_date: startDate,
          end_date: endDate,
        });
        setReports(response);
        feedbackService
          .getMyFeedback({
            limit: 1,
            start_date: `${startDate}T00:00:00`,
            end_date: `${endDate}T23:59:59`,
          })
          .then((res) => setFeedback(res));
        setError(null);
      } catch (err) {
        setError("Failed to fetch performance reports.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, [user, timePeriod]);

  const handleGenerateAIReport = async () => {
    if (!user) return;
    setAiReportLoading(true);
    setError(null);
    try {
      // Assuming a default time period and template for now
      const report =
        await aiPerformanceReportService.getPersonalPerformanceReport({
          time_period: AITimePeriodEnum.CURRENT_YEAR, // Example default
          template: AIReportTemplateEnum.COMPREHENSIVE_REVIEW, // Example default
        });
      navigate("/employee/performance-report/ai-report", {
        state: { aiReport: report },
      });
    } catch (err) {
      setError("Failed to generate AI performance report.");
      console.error(err);
    } finally {
      setAiReportLoading(false);
    }
  };

  useEffect(() => {}, []);

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
        {/* <Card className="w-full text-center"> */}
        {/*   <CardHeader className="text-xl font-bold">Learner Rank</CardHeader> */}
        {/*   <CardContent className="text-lg font-semibold">3</CardContent> */}
        {/* </Card> */}
        {/* TODO: Fetch Value */}
        <Card className="w-full text-center">
          <CardHeader className="text-xl font-bold">
            Get your AI generated performance report
          </CardHeader>
          <CardContent>
            <Button onClick={handleGenerateAIReport} disabled={aiReportLoading}>
              {aiReportLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              {aiReportLoading ? "Generating..." : "Generate Report"}
            </Button>
          </CardContent>
        </Card>
        <ChartAreaDefault
          chartData={reports?.monthly_modules.map((m) => ({
            modules_completed: m.modules_completed,
            month: new Date(m.month).toLocaleString("en-US", {
              month: "long",
            }),
          }))}
        />
        <Card className="w-full text-center">
          <CardHeader className="text-xl font-bold">Latest Feedback</CardHeader>
          <CardContent className="text-md h-full">
            {feedback && feedback.feedback[0] ? (
              <>
                {" "}
                <p>{feedback?.feedback[0].subject}</p>
                <p className="text-sm text-black/40 truncate">
                  {feedback?.feedback[0].description}
                </p>
              </>
            ) : (
              <p className="text-sm text-black/70">No feedback found!</p>
            )}
            {feedback && feedback.feedback[0] && (
              <a href="/employee/performance-report/feedbacks" className="mt-1">
                <Button variant="link" className="cursor-pointer">
                  View Previous feedbacks <ArrowRight />
                </Button>
              </a>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
