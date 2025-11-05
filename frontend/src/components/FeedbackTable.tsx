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

type Feedback = {
  id: number;
  date: string;
  subject: string;
  feedback: string;
  givenBy: string;
};

const feedbackData: Feedback[] = [
  {
    id: 1,
    date: "2025-10-30",
    subject: "Project Alpha Completion",
    feedback:
      "Excellent performance in delivering Project Alpha ahead of schedule. Your attention to detail, proactive problem-solving, and ability to collaborate across teams significantly contributed to the project’s success. Keep maintaining this consistency.",
    givenBy: "Ravi Kumar (Manager)",
  },
  {
    id: 2,
    date: "2025-09-15",
    subject: "Quarterly Performance Review",
    feedback:
      "You have shown remarkable improvement this quarter. Your time management and ability to prioritize key deliverables have stood out. Continue focusing on upskilling in backend optimization to further enhance project impact.",
    givenBy: "Priya Sharma (HR)",
  },
  {
    id: 3,
    date: "2025-08-20",
    subject: "Training Participation",
    feedback:
      "Actively participated in the leadership development training. Your contributions during discussions were insightful, and your willingness to mentor new joiners was appreciated. Suggest continuing this momentum in upcoming sessions.",
    givenBy: "Anil Verma (Trainer)",
  },
  {
    id: 4,
    date: "2025-07-05",
    subject: "Module X Development",
    feedback:
      "Delivered core components of Module X successfully. The implementation quality was good, but please pay closer attention to code comments and maintainability for larger-scale integrations. Excellent adaptability under tight deadlines.",
    givenBy: "Ravi Kumar (Manager)",
  },
  {
    id: 5,
    date: "2025-06-12",
    subject: "Team Collaboration",
    feedback:
      "Demonstrated strong teamwork during the recent sprint. Your quick assistance to teammates helped avoid potential blockers. Keep working on enhancing communication clarity during daily standups.",
    givenBy: "Sneha Patel (Lead)",
  },
];

export default function EmployeeFeedbackTable() {
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
                  {new Date(f.date).toLocaleDateString("en-IN", {
                    day: "2-digit",
                    month: "short",
                    year: "numeric",
                  })}
                </TableCell>
                <TableCell className="font-medium">{f.subject}</TableCell>
                <TableCell className="max-w-md text-muted-foreground whitespace-pre-wrap break-words ">
                  {f.feedback}
                </TableCell>
                <TableCell>{f.givenBy}</TableCell>
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
