import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Edit, ExternalLink } from "lucide-react";
import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTrigger,
} from "@/components/ui/dialog";
import { DialogTitle } from "@radix-ui/react-dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";

const Profile = () => {
  // State for modal open/close
  const [open, setOpen] = useState(false);

  // State for editable fields
  const [profileData, setProfileData] = useState({
    name: "",
    jobRole: "",
    department: "",
    teamName: "",
    phone: "",
    email: "",
  });

  // Handle input change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setProfileData({ ...profileData, [e.target.name]: e.target.value });
  };

  // Handle form submit (for now just close modal)
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setOpen(false);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6 text-center">Profile</h1>

      <Card className="w-full border-none shadow-none">
        <CardHeader className="flex justify-between items-center border-b pb-2">
          <h2 className="text-lg font-semibold">Primary Details</h2>
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
              <Button variant="ghost" size="sm" className="p-0">
                <Edit className="w-5 h-5" />
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-lg">
              <DialogHeader>
                <DialogTitle>Edit Profile Details</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="name" className="pb-3">
                    Name
                  </Label>
                  <Input
                    id="name"
                    name="name"
                    value={profileData.name}
                    onChange={handleChange}
                    placeholder="Enter name"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="jobRole" className="pb-3">
                    Job Role
                  </Label>
                  <Input
                    id="jobRole"
                    name="jobRole"
                    value={profileData.jobRole}
                    onChange={handleChange}
                    placeholder="Enter job role"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="department" className="pb-3">
                    Department
                  </Label>
                  <Input
                    id="department"
                    name="department"
                    value={profileData.department}
                    onChange={handleChange}
                    placeholder="Enter department"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="teamName" className="pb-3">
                    Team Name
                  </Label>
                  <Input
                    id="teamName"
                    name="teamName"
                    value={profileData.teamName}
                    onChange={handleChange}
                    placeholder="Enter team name"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="phone" className="pb-3">
                    Phone No.
                  </Label>
                  <Input
                    id="phone"
                    name="phone"
                    value={profileData.phone}
                    onChange={handleChange}
                    placeholder="Enter phone number"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="email" className="pb-3">
                    Email
                  </Label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    value={profileData.email}
                    onChange={handleChange}
                    placeholder="Enter email"
                    required
                  />
                </div>
                <DialogFooter>
                  <Button type="submit">Save</Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </CardHeader>

        <CardContent className="flex flex-col sm:flex-row items-center gap-6 pt-4">
          {/* Avatar */}
          <div className="flex-shrink-0 bg-purple-200 rounded-full w-28 h-28 flex items-center justify-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="w-14 h-14 text-purple-700"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <circle cx="12" cy="7" r="4" />
              <path d="M5.5 21c0-3 5-5 6.5-5s6.5 2 6.5 5" />
            </svg>
          </div>

          {/* Details */}
          <div className="flex-grow grid grid-cols-1 sm:grid-cols-2 gap-y-3 gap-x-6 text-sm font-semibold">
            <div>
              <span>Name : </span>
              <span className="font-normal">John Doe</span>
            </div>
            <div>
              <span>Job Role : </span>
              <span className="font-normal">Software Developer</span>
            </div>
            <div>
              <span>Department : </span>
              <span className="font-normal">IT & Software</span>
            </div>
            <div>
              <span>Team Name : </span>
              <span className="font-normal">Team 1</span>
            </div>
            <div>
              <span>Phone No. : </span>
              <span className="font-normal">+91 835483</span>
            </div>
            <div>
              <span>Email : </span>
              <span className="font-normal">john.doe@acme.inc</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Additional Details */}
      <div className="border-t pt-6 space-y-4 text-sm max-w-3xl mx-auto">
        <div>
          <span className="">Employee ID: </span>
          <span className="font-semibold">E0102</span>
        </div>

        <div className="flex items-center justify-between max-w-md">
          <div>
            <span className="">Manager Name: </span>
            <span className="font-semibold">Manager 1</span>
          </div>

          <a
            href="#"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm underline flex items-center gap-1 cursor-pointer"
          >
            View Team Hierarchy <ExternalLink className="w-4 h-4" />
          </a>
        </div>

        <div>
          <p className="font-semibold mb-2">Submitted Documents:</p>
          <div className="flex gap-3">
            <Button variant="outline" asChild>
              <a
                href="#"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1"
              >
                Aadhar Card <ExternalLink className="w-4 h-4" />
              </a>
            </Button>
            <Button variant="outline" asChild>
              <a
                href="#"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1"
              >
                PAN Card <ExternalLink className="w-4 h-4" />
              </a>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
