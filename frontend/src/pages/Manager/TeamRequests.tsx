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
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button"; // Added Button import

import requestService, {
  type TeamRequest,
  type RequestStatus,
} from "@/services/requestService";

const statusDot = (status: RequestStatus | string) => {
  if (status === "pending") return <Badge variant="warning">Pending</Badge>;
  if (status === "approved") return <Badge variant="success">Approved</Badge>;
  if (status === "rejected")
    return (
      <Badge variant="destructive" className="text-white">
        Rejected
      </Badge>
    );
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
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Request by {request.employee_name}</DialogTitle>
        </DialogHeader>
        <div className="flex items-center gap-6 mb-2 mt-2">
          {statusDot(request.status)}
          <p className="font-medium">
            {requestService.getRequestTypeLabel(request.request_type)}
          </p>
        </div>
        <p className="text-sm font-semibold mb-1">
          Subject: <span className="font-normal">{request.subject}</span>
        </p>
        <p className="text-sm font-semibold mb-1">Description:</p>
        <p className="text-sm mb-3">{request.description}</p>
        <div className="flex justify-end gap-3">
          {request.status === "pending" && (
            <>
              <Button
                variant="outline"
                onClick={() => {
                  onApprove();
                  onClose();
                }}
              >
                Approve
              </Button>
              <Button
                variant="destructive"
                onClick={() => {
                  onReject();
                  onClose();
                }}
              >
                Reject
              </Button>
            </>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};

const TeamRequests = () => {
  const [requests, setRequests] = useState<TeamRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedReq, setSelectedReq] = useState<TeamRequest | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);

  // Filters
  const [type, setType] = useState("all");
  const [status, setStatus] = useState("all");

  const fetchRequests = () => {
    setLoading(true);
    requestService
      .getTeamRequests({
        request_type: type === "all" ? undefined : type,
        status: status === "all" ? undefined : status,
      })
      .then((response) => {
        const sortedRequests = response.requests.sort((a, b) => {
          if (a.status === "pending" && b.status !== "pending") return -1;
          if (a.status !== "pending" && b.status === "pending") return 1;
          return 0;
        });
        setRequests(sortedRequests);
      })
      .catch((err) => {
        console.error(err);
        setError("Failed to fetch team requests.");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchRequests();
  }, [type, status]); // date is a dependency, but not used in filter

  const handleApprove = () => {
    if (!selectedReq) return;
    requestService.approveRequest(selectedReq.id).then(() => {
      fetchRequests();
    });
  };

  const handleReject = () => {
    if (!selectedReq) return;
    requestService
      .rejectRequest(selectedReq.id, "Rejected by manager")
      .then(() => {
        // Rejection reason is hardcoded
        fetchRequests();
      });
  };

  return (
    <div className="min-h-screen bg-white flex flex-col items-center px-4 pt-12">
      <h1 className="text-3xl font-bold mb-10">Team Requests</h1>
      <div className="flex gap-4 items-center mb-8 w-full max-w-4xl justify-center">
        <Select value={type} onValueChange={setType}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Request type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Types</SelectItem>
            <SelectItem value="leave">Leave request</SelectItem>
            <SelectItem value="wfh">Work From Home</SelectItem>
            <SelectItem value="equipment">Equipment</SelectItem>
            <SelectItem value="travel">Travel</SelectItem>
            <SelectItem value="other">Other</SelectItem>
          </SelectContent>
        </Select>
        <Select value={status} onValueChange={setStatus}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Request Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Status</SelectItem>
            <SelectItem value="pending">Pending</SelectItem>
            <SelectItem value="approved">Approved</SelectItem>
            <SelectItem value="rejected">Rejected</SelectItem>
          </SelectContent>
        </Select>
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
            {loading ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center">
                  Loading...
                </TableCell>
              </TableRow>
            ) : error ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center text-red-500">
                  {error}
                </TableCell>
              </TableRow>
            ) : (
              requests.map((req) => (
                <TableRow key={req.id}>
                  <TableCell>{req.employee_name}</TableCell>
                  <TableCell>
                    {requestService.getRequestTypeLabel(req.request_type)}
                  </TableCell>
                  <TableCell>{statusDot(req.status)}</TableCell>
                  <TableCell>
                    {requestService.formatDate(req.submitted_date)}
                  </TableCell>
                  <TableCell>
                    <Button
                      variant="link"
                      className="p-0 h-auto underline"
                      onClick={() => {
                        setSelectedReq(req);
                        setDialogOpen(true);
                      }}
                    >
                      View
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
      <ViewRequestDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        request={selectedReq}
        onApprove={handleApprove}
        onReject={handleReject}
      />
    </div>
  );
};

export default TeamRequests;
