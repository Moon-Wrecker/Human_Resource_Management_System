"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
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
  getScreeningResults,
  type ResumeScreeningResult,
} from "@/services/aiResumeScreenerService";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const ResumeScreenerResults = () => {
  const [searchParams] = useSearchParams();
  const [results, setResults] = useState<ResumeScreeningResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const analysisId = searchParams.get("analysis_id");
    if (analysisId) {
      getScreeningResults(analysisId)
        .then((data) => {
          setResults(data);
          setLoading(false);
        })
        .catch((error) => {
          console.error("Failed to fetch screening results:", error);
          setLoading(false);
        });
    }
  }, [searchParams]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center">
        <p>Loading results...</p>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center">
        <p>Failed to load results.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-12 px-4">
      <div className="w-full max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          Resume Screening Results
        </h1>
        <p className="text-gray-600 mb-8">
          Results for Role:{" "}
          <span className="font-semibold text-gray-800">
            {results.job_title}
          </span>
        </p>

        <Card>
          <CardHeader>
            <CardTitle>Screening Summary</CardTitle>
          </CardHeader>
          <CardContent className="grid grid-cols-3 gap-4">
            <div className="flex flex-col items-center">
              <p className="text-sm text-gray-500">Total Resumes Analyzed</p>
              <p className="text-2xl font-bold">{results.total_analyzed}</p>
            </div>
            <div className="flex flex-col items-center">
              <p className="text-sm text-gray-500">Average Score</p>
              <p className="text-2xl font-bold">
                {results.average_score?.toFixed(2)} / 100
              </p>
            </div>
            <div className="flex flex-col items-center">
              <p className="text-sm text-gray-500">Top Candidate</p>
              <Badge className="text-lg">{results.top_candidate}</Badge>
            </div>
          </CardContent>
        </Card>

        <div className="bg-white p-6 rounded-lg shadow-md mt-8">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Candidate</TableHead>
                <TableHead>Overall Score</TableHead>
                <TableHead>Strengths</TableHead>
                <TableHead>Gaps</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {results.results.map((r) => (
                <TableRow key={r.candidate_name}>
                  <TableCell className="font-medium">
                    {r.candidate_name}
                  </TableCell>
                  <TableCell>{r.overall_fit_score}</TableCell>
                  <TableCell className="whitespace-normal">
                    {r.strengths.join(", ")}
                  </TableCell>
                  <TableCell className="whitespace-normal">
                    {r.gaps.join(", ")}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>

        <div className="mt-8 flex justify-between">
          <a href="/hr/resume-screener">
            <Button variant="outline">Back</Button>
          </a>
          <a href="/hr/applications">
            <Button>Go to Applications &rarr;</Button>
          </a>
        </div>
      </div>
    </div>
  );
};

export default ResumeScreenerResults;
