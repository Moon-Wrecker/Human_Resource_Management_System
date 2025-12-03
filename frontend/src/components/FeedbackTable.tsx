"use client";

import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { FeedbackResponse } from "@/services/feedbackService";
import feedbackService from "@/services/feedbackService";
import { useEffect, useState } from "react";

export default function EmployeeFeedbackTable({
  startDate,
  endDate,
}: {
  startDate: string;
  endDate: string;
}) {
  const [feedbackData, setFeedbackData] = useState<FeedbackResponse[]>([]);

  useEffect(() => {
    feedbackService
      .getMyFeedback({
        start_date: `${startDate}T00:00:00`,
        end_date: `${endDate}T23:59:59`,
      })
      .then((res) => setFeedbackData(res.feedback));
  }, [startDate, endDate]);

  return (
    <div className="w-full max-w-5xl mx-auto mt-10 flex flex-col justify-center items-center gap-6">
      {/* Feedback Table */}
      <Table className="gap-4">
        <TableCaption>Your previous feedback records</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[120px]">Date</TableHead>
            <TableHead>Subject</TableHead>
            <TableHead>Feedback</TableHead>
            <TableHead>Given By</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {feedbackData.length > 0 ? (
            feedbackData.map((f) => (
              <TableRow key={f.id} className="py-8">
                <TableCell>
                  {new Date(f.given_on).toLocaleDateString("en-IN", {
                    day: "2-digit",
                    month: "short",
                    year: "numeric",
                  })}
                </TableCell>
                <TableCell className="font-medium">{f.subject}</TableCell>
                <TableCell className="max-w-md text-muted-foreground whitespace-pre-wrap break-words ">
                  {f.description}
                </TableCell>
                <TableCell>{f.given_by_name}</TableCell>
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell
                colSpan={4}
                className="text-center text-muted-foreground py-6"
              >
                No feedbacks found.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
}
