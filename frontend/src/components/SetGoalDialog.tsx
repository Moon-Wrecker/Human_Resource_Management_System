"use client";

import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogClose,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { type TeamMember } from "@/services/profileService";
import goalService, { GoalPriority } from "@/services/goalService";

const SetGoalDialog = ({
  open,
  onClose,
  member,
}: {
  open: boolean;
  onClose: () => void;
  member: TeamMember | null;
}) => {
  const [goalTitle, setGoalTitle] = useState("");
  const [checkpoints, setCheckpoints] = useState([{ title: "", description: "" }]);
  const [deadline, setDeadline] = useState("");
  const [info, setInfo] = useState("");

  if (!open) return null;
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-xl p-4 py-8">
        <DialogHeader>
          <DialogTitle className="text-center">
            Set goal for {member?.name}
          </DialogTitle>
        </DialogHeader>
        <form className="flex flex-col gap-4 p-4">
          <div className="flex items-center gap-2">
            <Label htmlFor="goalTitle" className="text-nowrap">
              Goal Title:
            </Label>
            <Input
              id="goalTitle"
              type="text"
              placeholder="Goal title..."
              className="ml-2 px-2 py-1 w-full"
              value={goalTitle}
              onChange={(e) => setGoalTitle(e.target.value)}
            />
          </div>
          <div className="flex flex-col gap-2">
            <Label htmlFor="goalChecklist" className="text-nowrap">
              Checkpoints:
            </Label>
            {checkpoints.map((checkpoint, index) => (
              <div key={index} className="flex flex-col gap-2 border p-2 rounded">
                <div className="flex items-center gap-2">
                  <Input
                    type="text"
                    placeholder={`Checkpoint ${index + 1} Title`}
                    className="px-2 py-1 w-full"
                    value={checkpoint.title}
                    onChange={(e) => {
                      const newCheckpoints = [...checkpoints];
                      newCheckpoints[index].title = e.target.value;
                      setCheckpoints(newCheckpoints);
                    }}
                  />
                  <Button
                    type="button"
                    variant="destructive"
                    size="sm"
                    onClick={() => {
                      const newCheckpoints = checkpoints.filter((_, i) => i !== index);
                      setCheckpoints(newCheckpoints);
                    }}
                  >
                    Remove
                  </Button>
                </div>
                <Textarea
                  placeholder={`Checkpoint ${index + 1} Description`}
                  className="px-2 py-1 w-full"
                  value={checkpoint.description}
                  onChange={(e) => {
                    const newCheckpoints = [...checkpoints];
                    newCheckpoints[index].description = e.target.value;
                    setCheckpoints(newCheckpoints);
                  }}
                />
              </div>
            ))}
            <Button
              type="button"
              variant="secondary"
              onClick={() => setCheckpoints([...checkpoints, { title: "", description: "" }])}
            >
              Add Checkpoint
            </Button>
          </div>
          <div className="flex items-center gap-2">
            <Label className="text-nowrap" htmlFor="goalDeadline">
              Deadline:
            </Label>
            <Input
              type="date"
              className="ml-2 px-2 py-1"
              value={deadline}
              onChange={(e) => setDeadline(e.target.value)}
            />
          </div>
          <Label htmlFor="goalAdditionalInfo" className="mb-1">
            Additional Information:
          </Label>
          <Textarea
            className="rounded p-2 w-full border"
            rows={3}
            placeholder="Additional info..."
            value={info}
            onChange={(e) => setInfo(e.target.value)}
          />
          <div className="flex justify-end">
            <DialogClose asChild>
              <Button
                onClick={() => {
                  if (!member) return;
                  goalService.createGoal({
                    title: goalTitle,
                    description: info,
                    priority: GoalPriority.MEDIUM,
                    start_date: new Date().toISOString().split("T")[0],
                    target_date: deadline,
                    employee_id: member.id,
                    checkpoints: checkpoints.map((checkpoint, index) => ({
                      ...checkpoint,
                      sequence_number: index + 1,
                    })),
                  });
                }}
                type="button"
              >
                Set Goal
              </Button>
            </DialogClose>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default SetGoalDialog;