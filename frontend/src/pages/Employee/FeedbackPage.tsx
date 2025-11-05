"use client";

import { Card, CardHeader, CardContent } from "@/components/ui/card";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";

const feedbackData = [
  {
    date: "10 Oct 2025",
    subject: "Related to Goal1",
    feedback: "Good Job completing Goal 1, Keep it up!",
    givenBy: "Manager 1",
  },
  {
    date: "2 Sep 2025",
    subject: "Subject 2",
    feedback:
      "veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commod",
    givenBy: "Manager 2",
  },
  {
    date: "23 Aug 2025",
    subject: "Subject 3",
    feedback:
      "veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commod",
    givenBy: "Manager 1",
  },
  {
    date: "24 July 2025",
    subject: "Subject 4",
    feedback:
      "veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commod",
    givenBy: "Manager 3",
  },
  {
    date: "12 June 2025",
    subject: "Subject 5",
    feedback:
      "veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commod",
    givenBy: "Manager 2",
  },
];

const timePeriods = ["Jan - Apr", "May - Aug", "Sep - Dec"];

const FeedbackReport = () => (
  <div className="min-h-screen flex flex-col items-center w-full bg-white px-4 py-8">
    <h1 className="text-3xl font-bold text-center mb-6">Feedback Report</h1>
    <div className="flex justify-center mb-6">
      <select className="border rounded bg-gray-100 h-12 px-5 w-64 font-semibold text-lg focus:outline-none">
        <option value="">Time Period</option>
        {timePeriods.map((p) => (
          <option key={p} value={p}>
            {p}
          </option>
        ))}
      </select>
    </div>
    <div className="font-semibold text-xl text-center mb-5">
      Feedback report for Sep - Dec
    </div>
    <Card className="w-full max-w-4xl">
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Date</TableHead>
              <TableHead>Subject</TableHead>
              <TableHead>Feedback</TableHead>
              <TableHead>Given By</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {feedbackData.map((entry, idx) => (
              <TableRow key={idx}>
                <TableCell>{entry.date}</TableCell>
                <TableCell>{entry.subject}</TableCell>
                <TableCell>{entry.feedback}</TableCell>
                <TableCell>{entry.givenBy}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  </div>
);

export default FeedbackReport;
