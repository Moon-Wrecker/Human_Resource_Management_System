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
import feedbackService from "@/services/feedbackService";

export const FeedbackDialog = ({
  open,
  onClose,
  member,
}: {
  open: boolean;
  onClose: () => void;
  member: TeamMember | null;
}) => {
  const [subject, setSubject] = useState("");
  const [feedback, setFeedback] = useState("");

  const handleSubmit = () => {
    if (!member) return;
    feedbackService.createFeedback({
        employee_id: member.id,
        subject: subject,
        description: feedback,
    });
    onClose();
  }

  if (!open) return null;
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-xl p-4 py-8">
        <DialogHeader>
          <DialogTitle className="text-center">Feedback to {member?.name}</DialogTitle>
        </DialogHeader>
        <form className="flex flex-col gap-4 p-4">
          <div className="flex items-center gap-2">
            <Label htmlFor="feedbackSubject" className="text-nowrap">
              Subject:
            </Label>
            <Input
              id="feedbackSubject"
              type="text"
              placeholder="Feedback subject..."
              className="ml-2 px-2 py-1 w-full"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
            />
          </div>
          <Label htmlFor="feedbackMessage" className="mb-1">
            Feedback Message:
          </Label>
          <Textarea
            id="feedbackMessage"
            className="rounded p-2 w-full border"
            rows={3}
            placeholder="Feedback description..."
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
          />
          <div className="flex justify-end">
            <DialogClose asChild>
              <Button
                onClick={handleSubmit}
                type="button"
              >
                Send
              </Button>
            </DialogClose>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};
