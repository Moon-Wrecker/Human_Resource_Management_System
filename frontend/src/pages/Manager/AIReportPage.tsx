import { useLocation, useNavigate } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";

type TeamAIReportResponse = {
  report_id: string;
  team_id: number;
  team_name: string;
  report_type: string;
  generated_at: string;
  time_period_start: string;
  time_period_end: string;
  template_used: string;
  team_summary_markdown: string;
  team_comparative_markdown: string;
  member_reports: any[];
  team_data_summary: Record<string, any>;
  generation_time_seconds: number;
};

export default function AIReportPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { state } = location;
  const teamAIReport = state?.teamAIReport as TeamAIReportResponse | undefined;

  if (!teamAIReport) {
    return (
      <div className="text-center py-10">
        No team AI report data found. Please generate a report first.
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 md:p-8 max-w-6xl">
      <div className="flex items-center justify-between mb-6">
        <Button 
          variant="ghost" 
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 h-9"
        >
          <ArrowLeft className="h-4 w-4" />
          Back
        </Button>
      </div>
      
      <Card className="w-full">
        <CardHeader className="pb-6">
          <CardTitle className="text-3xl font-bold text-center">
            AI Generated Team Performance Report
          </CardTitle>
          <div className="text-center text-lg text-muted-foreground mt-2">
            {teamAIReport.team_name} | {teamAIReport.time_period_start} - {teamAIReport.time_period_end}
          </div>
        </CardHeader>
        <CardContent className="prose prose-lg max-w-none prose-headings:font-bold prose-headings:text-gray-900 max-h-[80vh] overflow-y-auto">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
          >
            {teamAIReport.team_summary_markdown.replace(/\n/g, "\n\n").trim("\n")}
          </ReactMarkdown>
        </CardContent>
      </Card>
    </div>
  );
}
