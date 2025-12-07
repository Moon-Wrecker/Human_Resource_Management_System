import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import announcementService, {
  type Announcement,
} from "@/services/announcementService";
import { ArrowRight, CalendarDays } from "lucide-react";
import { useEffect, useState } from "react";
import { useAuth } from "@/contexts/AuthContext";

type AddAnnouncementDialogProps = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSave: (obj: {
    title: string;
    message: string;
    link?: string;
    target_departments?: string;
    target_roles?: string;
    is_urgent?: boolean;
    expiry_date?: string;
  }) => Promise<void> | void;
};

const AddAnnouncementDialog = ({
  open,
  onOpenChange,
  onSave,
}: AddAnnouncementDialogProps) => {
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");
  const [link, setLink] = useState("");
  const [isUrgent, setIsUrgent] = useState(false);
  const [targetDept, setTargetDept] = useState("");
  const [targetRole, setTargetRole] = useState("");
  const [expiryDate, setExpiryDate] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const departments = [
  "Finance",
  "HR",
  "Operations",
  "Sales",
  "Engineering",
  "Product Management",
  "Quality Assurance",
  "Customer Success",
  "Data Science",
  "DevOps",
  "Legal",
  "Research and Development",
  "IT Support",
  "Business Intelligence",
];

const deptMap: Record<string, number> = {
  "Engineering": 1,
  "HR": 2,
  "Finance": 3,
  "Sales": 4,
  "Marketing": 5,
  "Operations": 6,
  "Product Management": 7,
  "Quality Assurance": 8,
  "Customer Success": 9,
  "Data Science": 10,
  "DevOps": 11,
  "Legal": 12,
  "Research and Development": 13,
  "IT Support": 14,
  "Business Intelligence": 15,
};
  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    if (!title.trim() || !desc.trim()) return;
    try {
      setSubmitting(true);
      await onSave({
        title: title.trim(),
        message: desc.trim(),
        link: link.trim() || undefined,
        target_departments: targetDept || undefined,
        target_roles: targetRole || undefined,
        is_urgent: isUrgent,
        expiry_date: expiryDate ? new Date(expiryDate + 'T00:00:00').toISOString() : undefined,
      });
      setTitle("");
      setDesc("");
      setLink("");
      setIsUrgent(false);
      setTargetDept("");
      setTargetRole("");
      setExpiryDate("");
      onOpenChange(false);
    } catch (error) {
      console.error("Failed to create announcement:", error);
    }
    finally {
      setSubmitting(false);
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl p-0 max-h-[90vh]">
        <DialogHeader className="p-6 pb-4 border-b">
          <DialogTitle className="text-2xl font-bold">Create Announcement</DialogTitle>
        </DialogHeader>
        <form className="p-6 space-y-6" onSubmit={handleSave}>
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="title" className="text-sm font-semibold">Title</Label>
              <Input
                id="title"
                placeholder="Enter announcement title..."
                className="h-12"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="message" className="text-sm font-semibold">Message</Label>
              <Textarea
                id="message"
                placeholder="Enter announcement message..."
                className="min-h-[120px] resize-none"
                value={desc}
                onChange={(e) => setDesc(e.target.value)}
                required
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="link" className="text-sm font-semibold">Link (optional)</Label>
                <Input
                  id="link"
                  type="url"
                  placeholder="https://example.com"
                  value={link}
                  onChange={(e) => setLink(e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="expiry" className="text-sm font-semibold">Expiry Date (optional)</Label>
                <Input
                  id="expiry"
                  type="date"
                  value={expiryDate}
                  onChange={(e) => setExpiryDate(e.target.value)}
                  className="h-12"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label className="text-sm font-semibold">Target Department</Label>
                <Select value={targetDept} onValueChange={setTargetDept}>
                    <SelectTrigger id="department">
                      <SelectValue placeholder="Select Department" />
                    </SelectTrigger>
                    <SelectContent>
                      {departments.map((dept) => (
                        <SelectItem key={dept} value={dept.toString()}>
                          {dept}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>               
              </div>

              <div className="space-y-2">
                <Label className="text-sm font-semibold">Target Role</Label>
                <Select value={targetRole} onValueChange={setTargetRole}>
                  <SelectTrigger className="h-12">
                    <SelectValue placeholder="All roles" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="developer">Developer</SelectItem>
                    <SelectItem value="manager">Manager</SelectItem>
                    <SelectItem value="intern">Intern</SelectItem>
                    <SelectItem value="hr">HR</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="flex items-center space-x-2 p-3 border rounded-lg">
              <Checkbox
                id="urgent"
                checked={isUrgent}
                onCheckedChange={(checked: boolean) => setIsUrgent(checked)}
              />
              <Label
                htmlFor="urgent"
                className="font-medium leading-none peer-disabled:cursor-not-allowed"
              >
                Mark as urgent
              </Label>
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={submitting}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={!title.trim() || !desc.trim() || submitting}
            >
              {submitting ? "Creating..." : "Create Announcement"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};

// Rest of the component remains exactly the same...
const Announcements = () => {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);
  const { user } = useAuth();
  const isHR = user?.role === "hr" || user?.role === "admin";

  async function loadAnnouncements() {
    try {
      const res = await announcementService.getAnnouncements();
      setAnnouncements(res.announcements || []);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    loadAnnouncements();
  }, []);

  async function handleSaveAnnouncement(data: {
  title: string;
  message: string;
  link?: string;
  target_departments?: string;
  target_roles?: string;
  is_urgent?: boolean;
  expiry_date?: string;
  }) {
    const payload = {
    title: data.title,
    message: data.message,
    link: data.link || undefined,
    target_departments: data.target_departments || undefined,
    target_roles: data.target_roles || undefined,
    is_urgent: data.is_urgent ?? false,
    expiry_date: data.expiry_date || undefined,
  };
    await announcementService.createAnnouncement(payload);
    await loadAnnouncements();
  }

  if (!announcements || announcements.length === 0)
    return (
      <div className="mt-8 text-center">
        <h2 className="text-3xl font-semibold mb-4">Announcements</h2>
        {isHR && (
          <Button
            onClick={() => setDialogOpen(true)}
            variant="ghost"
            className="mb-4"
          >
            Create New &rarr;
          </Button>
        )}
        <p>No announcements found!</p>
        <AddAnnouncementDialog
          open={dialogOpen}
          onOpenChange={setDialogOpen}
          onSave={handleSaveAnnouncement}
        />
      </div>
    );

  return (
    <>
      <h2 className="text-3xl font-semibold text-center mt-8">Announcements</h2>
      {isHR && (
        <div className="flex items-center justify-between px-8 mt-10">
          <Button onClick={() => setDialogOpen(true)} variant="ghost">
            Create New &rarr;
          </Button>
        </div>
      )}
      <AddAnnouncementDialog
        open={dialogOpen}
        onOpenChange={setDialogOpen}
        onSave={handleSaveAnnouncement}
      />
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 my-8 px-4 gap-6">
        {announcements.map((announcement) => (
          <Card
            key={announcement.id}
            className="flex flex-col h-full shadow-md rounded-2xl border border-gray-200"
          >
            <CardHeader>
              <CardTitle className="text-lg font-semibold text-gray-900">
                {announcement.title}
              </CardTitle>
              <CardDescription className="flex items-center text-sm text-gray-500 mt-1">
                <CalendarDays className="w-4 h-4 mr-1" />
                {new Date(
                  announcement.published_date
                ).toLocaleDateString("en-IN", {
                  day: "2-digit",
                  month: "short",
                  year: "numeric",
                })}
              </CardDescription>
            </CardHeader>

            <CardContent className="flex-1">
              <p className="text-gray-700 text-sm leading-relaxed">
                {announcement.message}
              </p>
            </CardContent>

            <CardFooter className="flex justify-between items-center mt-auto">
              <div className="flex-1">
                {announcement.is_urgent && (
                  <Badge variant="destructive" className="text-white">
                    URGENT
                  </Badge>
                )}
              </div>
              <Button
                asChild
                variant="outline"
                className="flex items-center gap-2"
              >
                <a
                  href={`announcements/${announcement.id}`}
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
    </>
  );
};

export default Announcements;
