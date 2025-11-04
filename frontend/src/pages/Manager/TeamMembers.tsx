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
  DialogClose,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";

// Data type for a team member
type TeamMember = { id: number; name: string; };

const teamMembers: TeamMember[] = [
  { id: 1, name: "Person 1" },
  { id: 2, name: "Person 2" },
  { id: 3, name: "Person 3" },
];

// Set Goal Dialog
const SetGoalDialog = ({
  open,
  onClose,
  member,
}: {
  open: boolean;
  onClose: () => void;
  member: string | null;
}) => {
  const [goalTitle, setGoalTitle] = useState("");
  const [checklist, setChecklist] = useState(false);
  const [task, setTask] = useState("");
  const [deadline, setDeadline] = useState("");
  const [info, setInfo] = useState("");

  if (!open) return null;
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-xl bg-[#e9e9ea] rounded-2xl p-2">
        <DialogHeader>
          <DialogTitle>Set goal for {member}</DialogTitle>
        </DialogHeader>
        <form className="flex flex-col gap-4 p-4">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-lg">🎯</span>
            <span className="font-bold">Goal Title:</span>
            <input
              type="text"
              placeholder="Goal title..."
              className="ml-2 px-2 py-1 rounded w-full border"
              value={goalTitle}
              onChange={e => setGoalTitle(e.target.value)}
            />
          </div>
          <div className="flex items-center gap-2">
            <span className="font-semibold text-lg">☑️</span>
            <span className="font-bold underline">Checklist:</span>
            <Checkbox
              checked={checklist}
              onCheckedChange={v => setChecklist(!!v)}
              className="ml-2 mr-1"
            />
            <input
              type="text"
              placeholder="Add a task..."
              className="px-2 py-1 rounded w-full border"
              disabled={!checklist}
              value={task}
              onChange={e => setTask(e.target.value)}
            />
          </div>
          <div className="flex items-center gap-2">
            <span className="font-semibold text-lg">🗓️</span>
            <span className="font-bold underline">Deadline:</span>
            <input
              type="date"
              className="ml-2 px-2 py-1 rounded border"
              value={deadline}
              onChange={e => setDeadline(e.target.value)}
            />
          </div>
          <div className="font-bold underline mb-1">Additional Information:</div>
          <textarea
            className="rounded p-2 w-full border"
            rows={3}
            placeholder="Additional info..."
            value={info}
            onChange={e => setInfo(e.target.value)}
          />
          <div className="flex justify-end">
            <DialogClose asChild>
              <Button type="button">Set Goal</Button>
            </DialogClose>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};

// Feedback Dialog
const FeedbackDialog = ({
  open,
  onClose,
  member,
}: {
  open: boolean;
  onClose: () => void;
  member: string | null;
}) => {
  const [subject, setSubject] = useState("");
  const [feedback, setFeedback] = useState("");

  if (!open) return null;
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-xl bg-[#e9e9ea] rounded-2xl p-2">
        <DialogHeader>
          <DialogTitle>Feedback to {member}</DialogTitle>
        </DialogHeader>
        <form className="flex flex-col gap-4 p-4">
          <div>
            <span className="font-bold underline">Subject:</span>
            <input
              type="text"
              className="ml-2 px-2 py-1 rounded w-full border"
              placeholder="Subject for feedback..."
              value={subject}
              onChange={e => setSubject(e.target.value)}
            />
          </div>
          <div>
            <span className="font-bold underline">Feedback:</span>
            <textarea
              className="rounded p-2 w-full border"
              rows={3}
              placeholder="Feedback description..."
              value={feedback}
              onChange={e => setFeedback(e.target.value)}
            />
          </div>
          <div className="flex justify-end">
            <DialogClose asChild>
              <Button type="button">Send</Button>
            </DialogClose>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};

const TeamMembers = () => {
  const [goalDialogOpen, setGoalDialogOpen] = useState(false);
  const [feedbackDialogOpen, setFeedbackDialogOpen] = useState(false);
  const [selectedMember, setSelectedMember] = useState<string | null>(null);
  const [search, setSearch] = useState("");

  const filtered = teamMembers.filter(m =>
    !search || m.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-white flex flex-col items-center px-4 pt-12">
      <h1 className="text-2xl font-bold mb-6">Team Members</h1>
      <div className="flex justify-center mb-8 w-full">
        <input
          type="text"
          className="bg-gray-200 rounded px-4 h-10 w-[350px] mx-auto"
          placeholder="Search Members 🔍"
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
      </div>
      <div className="w-full max-w-3xl">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Teammate</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filtered.map(m => (
              <TableRow key={m.id}>
                <TableCell>{m.name}</TableCell>
                <TableCell>
                  <span className="space-x-2">
                    <a href="#" className="underline" tabIndex={-1}>View</a>
                    <span className="text-gray-400">|</span>
                    <button
                      className="underline"
                      onClick={() => {
                        setSelectedMember(m.name);
                        setGoalDialogOpen(true);
                      }}
                    >Set Goal</button>
                    <span className="text-gray-400">|</span>
                    <button
                      className="underline"
                      onClick={() => {
                        setSelectedMember(m.name);
                        setFeedbackDialogOpen(true);
                      }}
                    >Feedback</button>
                  </span>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      <SetGoalDialog
        open={goalDialogOpen}
        onClose={() => setGoalDialogOpen(false)}
        member={selectedMember}
      />
      <FeedbackDialog
        open={feedbackDialogOpen}
        onClose={() => setFeedbackDialogOpen(false)}
        member={selectedMember}
      />
    </div>
  );
};

export default TeamMembers;
