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
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardFooter,
  CardDescription,
} from "@/components/ui/card";
import { ArrowRight, CalendarDays } from "lucide-react";

const initialAnnouncements = [
  {
    id: 1,
    title: "Office Closed for Diwali",
    message: "All branches will remain closed from November 14–16 for Diwali celebrations. Wishing everyone a joyous festival!",
    date: "2025-11-02",
    link: "https://intranet.company.com/holiday-calendar",
  },
  {
    id: 2,
    title: "Performance Review Cycle Begins",
    message: "Q3 performance reviews are now open. Please submit your self-assessment by November 10.",
    date: "2025-11-01",
    link: "https://hr.company.com/performance-review",
  },
  {
    id: 3,
    title: "New Expense Policy Update",
    message: "The revised travel and meal reimbursement policy is effective from November 5. Review the changes carefully.",
    date: "2025-10-30",
    link: "https://intranet.company.com/policies/expense-policy",
  },
  {
    id: 4,
    title: "Wellness Webinar",
    message: "Join our live wellness webinar on stress management hosted by Dr. Meera Patel on November 6 at 4 PM.",
    date: "2025-10-29",
    link: "https://events.company.com/wellness-webinar",
  },
  {
    id: 5,
    title: "System Downtime Notice",
    message: "The HRMS portal will be unavailable for scheduled maintenance on November 4 between 1 AM and 3 AM.",
    date: "2025-10-28",
    link: "https://status.company.com/hrms",
  },
  {
    id: 6,
    title: "New Employee Portal Features",
    message: "Explore new features added to the employee portal, including document uploads and leave tracking.",
    date: "2025-10-26",
    link: "https://intranet.company.com/employee-portal",
  },
];

const AddAnnouncementDialog = ({
  open,
  onClose,
  onSave,
}: {
  open: boolean;
  onClose: () => void;
  onSave: (obj: any) => void;
}) => {
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");
  const [links, setLinks] = useState<string[]>([]);
  const [linkInput, setLinkInput] = useState("");

  function addLink() {
    if (linkInput.trim()) {
      setLinks((prev) => [...prev, linkInput.trim()]);
      setLinkInput("");
    }
  }
  function removeLink(i: number) {
    setLinks((prev) => prev.filter((_, idx) => idx !== i));
  }
  function handleSave(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim() || !desc.trim()) return;
    onSave({
      id: Date.now(),
      title: title.trim(),
      message: desc.trim(),
      date: new Date().toISOString(),
      link: links[0] ?? "",
    });
    onClose();
    setTitle("");
    setDesc("");
    setLinks([]);
    setLinkInput("");
  }

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-xl bg-[#e9e9ea] rounded-2xl p-2">
        <DialogHeader>
          <DialogTitle>Add Announcement</DialogTitle>
        </DialogHeader>
        <form className="flex flex-col p-4 gap-5" onSubmit={handleSave}>
          <div>
            <label className="font-bold underline block mb-1">
              Title:
              <input
                type="text"
                placeholder="Announce something..."
                className="w-full px-2 py-1 rounded border ml-2 font-normal"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </label>
          </div>
          <div>
            <label className="font-bold underline block mb-1">
              Description:
              <textarea
                placeholder="Add Announcement Description..."
                className="w-full rounded border p-2 mt-1 font-normal"
                rows={3}
                value={desc}
                onChange={(e) => setDesc(e.target.value)}
                required
              />
            </label>
          </div>
          <div>
            <label className="font-bold underline block mb-1">
              Links (optional):
            </label>
            <div className="flex items-center gap-2 mb-2">
              <input
                type="url"
                placeholder="https://... (optional)"
                value={linkInput}
                className="border rounded px-2 py-1 flex-1"
                onChange={(e) => setLinkInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    addLink();
                  }
                }}
              />
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={addLink}
              >
                + Add link
              </Button>
            </div>
            {links.length > 0 && (
              <ul className="pl-2 mt-2 space-y-1">
                {links.map((link, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm">
                    <span className="truncate">{link}</span>
                    <Button
                      type="button"
                      size="icon"
                      onClick={() => removeLink(i)}
                      className="h-6 w-6 p-0"
                    >
                      &times;
                    </Button>
                  </li>
                ))}
              </ul>
            )}
          </div>
          <div className="flex justify-end">
            <DialogClose asChild>
              <Button
                type="submit"
                className="px-6 py-2 font-semibold"
                disabled={!title.trim() || !desc.trim()}
              >
                Save &rarr;
              </Button>
            </DialogClose>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};

const Announcements = () => {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [announcements, setAnnouncements] = useState(initialAnnouncements);

  function handleSave(announcement: any) {
    setAnnouncements((prev) => [announcement, ...prev]);
  }

  return (
    <>
      <div className="flex items-center justify-between px-8 mt-10">
        <h2 className="text-3xl font-semibold">Announcements</h2>
        <Button onClick={() => setDialogOpen(true)} variant="ghost">
          Create New &rarr;
        </Button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 my-8 px-4 gap-4">
        {announcements.map((announcement) => (
          <Card
            className="w-full shadow-md rounded-2xl border border-gray-200"
            key={announcement.id}
          >
            <CardHeader>
              <CardTitle className="text-lg font-semibold text-gray-900">
                {announcement.title}
              </CardTitle>
              <CardDescription className="flex items-center text-sm text-gray-500 mt-1">
                <CalendarDays className="w-4 h-4 mr-1" />
                {new Date(announcement.date).toLocaleDateString("en-IN", {
                  day: "2-digit",
                  month: "short",
                  year: "numeric",
                })}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 text-sm leading-relaxed">
                {announcement.message}
              </p>
            </CardContent>
            <CardFooter className="flex justify-end">
              <Button
                asChild
                variant="outline"
                className="flex items-center gap-2"
              >
                <a
                  href={announcement.link}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  View Details
                  <ArrowRight className="w-4 h-4" />
                </a>
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
      <AddAnnouncementDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        onSave={handleSave}
      />
    </>
  );
};

export default Announcements;
