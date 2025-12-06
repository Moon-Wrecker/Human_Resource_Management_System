"use client";

import { useState, useEffect } from "react";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import {
  getScreeningHistory,
  type ScreeningHistoryItem,
} from "@/services/aiResumeScreenerService";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const ScreeningHistory = () => {
  const [history, setHistory] = useState<ScreeningHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getScreeningHistory()
      .then((data) => {
        setHistory(data.history);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Failed to fetch screening history:", error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center">
        <p>Loading screening history...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-12 px-4">
      <div className="w-full mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">
          Screening History
        </h1>
        <Card>
          <CardHeader>
            <CardTitle>Past Screenings</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Job Title</TableHead>
                  <TableHead>Date</TableHead>
                  <TableHead>Total Analyzed</TableHead>
                  <TableHead>Average Score</TableHead>
                  <TableHead>Top Candidate</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {history.map((item) => (
                  <TableRow key={item.analysis_id}>
                    <TableCell>{item.job_title}</TableCell>
                    <TableCell>
                      {new Date(item.timestamp).toLocaleDateString()}
                    </TableCell>
                    <TableCell>{item.total_analyzed}</TableCell>
                    <TableCell>{item.average_score.toFixed(2)}</TableCell>
                    <TableCell>{item.top_candidate}</TableCell>
                    <TableCell>
                      <a
                        href={`/hr/resume-screener/results?analysis_id=${item.analysis_id}`}
                      >
                        <Button variant="outline">View</Button>
                      </a>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ScreeningHistory;
