import { useLocation } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function AIReportPage() {
  const location = useLocation();
  const { state } = location;
  const aiReport = state?.aiReport;

  if (!aiReport) {
    return (
      <div className="text-center py-10">
        No AI report data found. Please generate a report first.
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 md:p-8">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">
            AI Generated Performance Report
          </CardTitle>
        </CardHeader>
        <CardContent className="prose max-w-none">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeRaw]}
          >
            {aiReport.report_markdown.replace(/\n/g, "\n\n").trim("\n")}
          </ReactMarkdown>
        </CardContent>
      </Card>
    </div>
  );
}
