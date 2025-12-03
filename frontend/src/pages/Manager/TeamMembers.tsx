"use client";

import { useEffect, useState } from "react";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";
import profileService, { type TeamMember } from "@/services/profileService";
import { Input } from "@/components/ui/input";
import { Link } from "react-router-dom";
import SetGoalDialog from "@/components/SetGoalDialog";
import { FeedbackDialog } from "@/components/FeedbackDialog";

const TeamMembers = () => {
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>();
  const [goalDialogOpen, setGoalDialogOpen] = useState(false);
  const [feedbackDialogOpen, setFeedbackDialogOpen] = useState(false);
  const [selectedMember, setSelectedMember] = useState<TeamMember | null>(null);
  const [search, setSearch] = useState("");

  useEffect(() => {
    profileService.getMyTeam().then((res) => setTeamMembers(res.members));
  }, []);

  const filtered = teamMembers?.filter(
    (m) => !search || m.name.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <div className="min-h-screen bg-white flex flex-col items-center px-4 pt-12">
      <h1 className="text-2xl font-bold mb-6">Team Members</h1>
      <div className="flex justify-center mb-8 w-full">
        <Input
          type="text"
          className="px-4 h-10 w-[350px] mx-auto"
          placeholder="Search Members"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>
      <div className="w-full max-w-3xl">
        {teamMembers && filtered ? (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Teammate</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map((m) => (
                <TableRow key={m.id}>
                  <TableCell>{m.name}</TableCell>
                  <TableCell>
                    <span className="space-x-2">
                      <Link to={`/manager/team-members/view/${m.id}`} className="underline">
                        View
                      </Link>
                      <span className="text-gray-400">|</span>
                      <button
                        className="underline"
                        onClick={() => {
                          setSelectedMember(m);
                          setGoalDialogOpen(true);
                        }}
                      >
                        Set Goal
                      </button>
                      <span className="text-gray-400">|</span>
                      <button
                        className="underline"
                        onClick={() => {
                          setSelectedMember(m);
                          setFeedbackDialogOpen(true);
                        }}
                      >
                        Feedback
                      </button>
                    </span>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        ) : (
          <p className="text-center text-muted-foreground">No members found!</p>
        )}
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
