"use client";

import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";

const resumeResults = [
  {
    name: "Resume_2.pdf",
    overallScore: 98.5,
    skillRelevancy: 92.3,
    highlight: "High exp match",
    missing: "-"
  },
  {
    name: "Resume_3.pdf",
    overallScore: 93.4,
    skillRelevancy: 89.7,
    highlight: "",
    missing: "-"
  },
  {
    name: "Resume_1.pdf",
    overallScore: 89.1,
    skillRelevancy: 85.2,
    highlight: "",
    missing: "-"
  },
];

const ResumeScreenerResults = () => (
  <div className="min-h-screen bg-[#fafafa] flex flex-col items-center px-4 pt-12">
    <h1 className="text-2xl font-bold mb-9">Resume Screener</h1>
    <div className="mb-9 font-semibold text-lg underline">
      Results for Role : SDE - II
    </div>
    <div className="w-full max-w-2xl">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="underline">Resume</TableHead>
            <TableHead className="underline">Overall Score</TableHead>
            <TableHead className="underline">Skill relevancy</TableHead>
            <TableHead className="underline">Highlight</TableHead>
            <TableHead className="underline">Missing</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {resumeResults.map(r => (
            <TableRow key={r.name}>
              <TableCell className="font-medium underline">{r.name}</TableCell>
              <TableCell>{r.overallScore}</TableCell>
              <TableCell>{r.skillRelevancy}</TableCell>
              <TableCell>{r.highlight || "-"}</TableCell>
              <TableCell>{r.missing || "-"}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
    <a href="/applications" className="bg-gray-300 px-7 py-2 rounded font-semibold hover:bg-gray-400 transition mt-8">
      Go to Applications &rarr;
    </a>
  </div>
);

export default ResumeScreenerResults;
