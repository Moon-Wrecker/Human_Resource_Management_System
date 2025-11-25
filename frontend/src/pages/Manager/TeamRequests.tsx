"use client";

import { useState } from "react";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

// Request data type
type RequestStatus = "Pending" | "Approved" | "Rejected";
type TeamRequest = {
  id: number;
  teammate: string;
  requestType: string;
  status: RequestStatus;
  date: string;
  subject: string;
  description: string;
};

// Example data
const initialTeamRequests: TeamRequest[] = [
  {
    id: 1,
    teammate: "Person 1",
    requestType: "Leave request",
    status: "Pending",
    date: "11-09-2025",
    subject: "Request for Leave",
    description:
      "I'd like to request a leave for personal reasons. Please approve.",
  },
  {
    id: 2,
    teammate: "Person 2",
    requestType: "Career development",
    status: "Approved",
    date: "21-09-2025",
    subject: "Request for Training",
    description:
      "I am interested in career development training this quarter.",
  },
  {
    id: 3,
    teammate: "Person 3",
    requestType: "Leave request",
    status: "Rejected",
    date: "13-10-2025",
    subject: "Request for Sick Leave",
    description:
      "Not feeling well, requesting a sick leave for 2 days.",
  },
];

const statusDot = (status: RequestStatus | string) => {
  if (status === "Pending") return <span className="inline-block w-3 h-3 rounded-full bg-yellow-400 mr-1" />;
  if (status === "Approved") return <span className="inline-block w-3 h-3 rounded-full bg-blue-400 mr-1" />;
  if (status === "Rejected") return <span className="inline-block w-3 h-3 rounded-full bg-red-400 mr-1" />;
  return null;
};

// Dialog for viewing/acting on a request
const ViewRequestDialog = ({
  open,
  onClose,
  request,
  onApprove,
  onReject,
}: {
  open: boolean;
  onClose: () => void;
  request: TeamRequest | null;
  onApprove: () => void;
  onReject: () => void;
}) => {
  if (!open || !request) return null;

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-md bg-[#e9e9ea] rounded-2xl shadow-xl p-2">
        <DialogHeader>
          <DialogTitle>
            Request by {request.teammate}
          </DialogTitle>
        </DialogHeader>
        <div className="flex items-center gap-6 mb-2 mt-2">
          <span>{statusDot("Pending")} Pending</span>
          <span>{statusDot("Approved")} Leave Request</span>
        </div>
        <div className="mb-2">
          <span className="underline font-bold">Subject:</span>{" "}
          <span>{request.subject}</span>
        </div>
        <div className="mb-1">
          <span className="underline font-bold">Description:</span>
        </div>
        <div className="mb-3">{request.description}</div>
        <div className="flex justify-end gap-3">
          <Button
            variant="secondary"
            className="px-5"
            onClick={() => {
              onApprove();
              onClose();
            }}
          >
            Approve
          </Button>
          <Button
            variant="secondary"
            className="px-5"
            onClick={() => {
              onReject();
              onClose();
            }}
          >
            Reject
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};

const TeamRequests = () => {
  const [requests] = useState<TeamRequest[]>(initialTeamRequests);
  const [selectedReq, setSelectedReq] = useState<TeamRequest | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  // Filters (demo only, no logic; add logic as needed)
  const [search, setSearch] = useState("");
  const [type, setType] = useState("");
  const [status, setStatus] = useState("");
  const [date, setDate] = useState("");

  const filteredRequests = requests.filter((r) =>
    (search === "" || r.teammate.toLowerCase().includes(search.toLowerCase())) &&
    (type === "" || r.requestType === type) &&
    (status === "" || r.status === status) &&
    (date === "" || r.date === date)
  );

  return (
    <div className="min-h-screen bg-white flex flex-col items-center px-4 pt-12">
      <h1 className="text-2xl font-bold mb-10">Team Requests</h1>
      <div className="flex gap-4 items-center mb-8 w-full max-w-4xl">
        <input
          type="text"
          className="bg-gray-200 rounded px-4 h-10 flex-1"
          placeholder="Search Requests"
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        <select value={type} onChange={e => setType(e.target.value)} className="bg-gray-200 rounded h-10 px-4">
          <option value="">Request type</option>
          <option value="Leave request">Leave request</option>
          <option value="Career development">Career development</option>
        </select>
        <select value={status} onChange={e => setStatus(e.target.value)} className="bg-gray-200 rounded h-10 px-4">
          <option value="">Request Status</option>
          <option value="Pending">Pending</option>
          <option value="Approved">Approved</option>
          <option value="Rejected">Rejected</option>
        </select>
        <select value={date} onChange={e => setDate(e.target.value)} className="bg-gray-200 rounded h-10 px-4">
          <option value="">Date</option>
          {/* Populate as needed */}
        </select>
      </div>
      <div className="w-full max-w-4xl">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Teammate</TableHead>
              <TableHead>Request type</TableHead>
              <TableHead>Request Status</TableHead>
              <TableHead>Date</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredRequests.map((req) => (
              <TableRow key={req.id}>
                <TableCell>{req.teammate}</TableCell>
                <TableCell>{req.requestType}</TableCell>
                <TableCell>
                  {statusDot(req.status)}
                  {req.status}
                </TableCell>
                <TableCell>{req.date}</TableCell>
                <TableCell>
                  <button
                    className="underline font-medium"
                    onClick={() => {
                      setSelectedReq(req);
                      setDialogOpen(true);
                    }}
                  >
                    View
                  </button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      <ViewRequestDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        request={selectedReq}
        onApprove={() => {}}
        onReject={() => {}}
      />
    </div>
  );
};

export default TeamRequests;
