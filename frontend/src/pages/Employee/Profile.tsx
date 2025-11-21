import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Edit, ExternalLink, Upload, Trash2, User } from "lucide-react";
import { useState, useEffect } from "react";
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
import profileService from "@/services/profileService";
import type { ProfileData, ManagerInfo, UserDocuments } from "@/services/profileService";
import { API_BASE_URL } from "@/config/api";

const Profile = () => {
  // State for modal open/close
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Profile data state
  const [profileData, setProfileData] = useState<ProfileData | null>(null);
  const [managerInfo, setManagerInfo] = useState<ManagerInfo | null>(null);
  const [documents, setDocuments] = useState<UserDocuments>({});

  // Edit form state
  const [editForm, setEditForm] = useState({
    name: "",
    phone: "",
  });

  // File upload states
  const [uploadingImage, setUploadingImage] = useState(false);
  const [uploadingDoc, setUploadingDoc] = useState<string | null>(null);

  // Fetch profile data on component mount
  useEffect(() => {
    fetchProfileData();
  }, []);

  const fetchProfileData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch profile
      const profile = await profileService.getMyProfile();
      setProfileData(profile);
      setEditForm({
        name: profile.name,
        phone: profile.phone || "",
      });

      // Fetch manager info
      try {
        const manager = await profileService.getMyManager();
        setManagerInfo(manager);
      } catch (err) {
        console.log("No manager assigned");
      }

      // Fetch documents
      try {
        const docs = await profileService.getMyDocuments();
        setDocuments(docs);
      } catch (err) {
        console.log("No documents uploaded");
      }
    } catch (err: any) {
      setError(err.message || "Failed to fetch profile data");
    } finally {
      setLoading(false);
    }
  };

  // Handle input change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEditForm({ ...editForm, [e.target.name]: e.target.value });
  };

  // Handle form submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setError(null);
      const updated = await profileService.updateMyProfile(editForm);
      setProfileData(updated);
      setSuccessMessage("Profile updated successfully!");
      setOpen(false);
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err: any) {
      setError(err.message || "Failed to update profile");
    }
  };

  // Handle profile image upload
  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError("File size must be less than 10MB");
      return;
    }

    try {
      setUploadingImage(true);
      setError(null);
      await profileService.uploadProfileImage(file);
      setSuccessMessage("Profile image uploaded successfully!");
      setTimeout(() => setSuccessMessage(null), 3000);
      fetchProfileData(); // Refresh profile
    } catch (err: any) {
      setError(err.message || "Failed to upload image");
    } finally {
      setUploadingImage(false);
    }
  };

  // Handle document upload
  const handleDocumentUpload = async (
    e: React.ChangeEvent<HTMLInputElement>,
    documentType: "aadhar" | "pan"
  ) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError("File size must be less than 10MB");
      return;
    }

    try {
      setUploadingDoc(documentType);
      setError(null);
      await profileService.uploadDocument(documentType, file);
      setSuccessMessage(`${documentType.toUpperCase()} document uploaded successfully!`);
      setTimeout(() => setSuccessMessage(null), 3000);
      fetchProfileData(); // Refresh documents
    } catch (err: any) {
      setError(err.message || "Failed to upload document");
    } finally {
      setUploadingDoc(null);
    }
  };

  // Handle document delete
  const handleDeleteDocument = async (documentType: "profile_image" | "aadhar" | "pan") => {
    if (!confirm(`Are you sure you want to delete this document?`)) return;

    try {
      setError(null);
      await profileService.deleteDocument(documentType);
      setSuccessMessage("Document deleted successfully!");
      setTimeout(() => setSuccessMessage(null), 3000);
      fetchProfileData(); // Refresh documents
    } catch (err: any) {
      setError(err.message || "Failed to delete document");
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="text-center">Loading profile...</div>
      </div>
    );
  }

  if (!profileData) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="text-center text-red-600">Failed to load profile</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6 text-center">Profile</h1>

      {/* Success/Error Messages */}
      {successMessage && (
        <div className="mb-4 p-3 bg-green-100 text-green-800 rounded-md">
          {successMessage}
        </div>
      )}
      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-800 rounded-md">
          {error}
        </div>
      )}

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
                    value={editForm.name}
                    onChange={handleChange}
                    placeholder="Enter name"
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
                    value={editForm.phone}
                    onChange={handleChange}
                    placeholder="Enter phone number"
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
          {/* Avatar with Upload */}
          <div className="flex-shrink-0 relative">
            {profileData.profile_image_url ? (
              <div className="relative">
                <img
                  src={`${API_BASE_URL}${profileData.profile_image_url}`}
                  alt={profileData.name}
                  className="rounded-full w-28 h-28 object-cover"
                />
                <Button
                  variant="ghost"
                  size="sm"
                  className="absolute bottom-0 right-0 rounded-full bg-white shadow-md p-1"
                  onClick={() => handleDeleteDocument("profile_image")}
                >
                  <Trash2 className="w-4 h-4 text-red-600" />
                </Button>
              </div>
            ) : (
              <div className="bg-purple-200 rounded-full w-28 h-28 flex items-center justify-center">
                <User className="w-14 h-14 text-purple-700" />
              </div>
            )}
            <label
              htmlFor="profile-image-upload"
              className="absolute bottom-0 right-0 cursor-pointer"
            >
              <div className="rounded-full bg-blue-600 text-white shadow-md p-2 hover:bg-blue-700">
                <Upload className="w-4 h-4" />
              </div>
              <input
                id="profile-image-upload"
                type="file"
                accept="image/*"
                className="hidden"
                onChange={handleImageUpload}
                disabled={uploadingImage}
              />
            </label>
          </div>

          {/* Details */}
          <div className="flex-grow grid grid-cols-1 sm:grid-cols-2 gap-y-3 gap-x-6 text-sm font-semibold">
            <div>
              <span>Name : </span>
              <span className="font-normal">{profileData.name}</span>
            </div>
            <div>
              <span>Job Role : </span>
              <span className="font-normal">{profileData.job_role || "N/A"}</span>
            </div>
            <div>
              <span>Department : </span>
              <span className="font-normal">{profileData.department_name || "N/A"}</span>
            </div>
            <div>
              <span>Team Name : </span>
              <span className="font-normal">{profileData.team_name || "N/A"}</span>
            </div>
            <div>
              <span>Phone No. : </span>
              <span className="font-normal">{profileData.phone || "N/A"}</span>
            </div>
            <div>
              <span>Email : </span>
              <span className="font-normal">{profileData.email}</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Additional Details */}
      <div className="border-t pt-6 space-y-4 text-sm max-w-3xl mx-auto">
        <div>
          <span className="">Employee ID: </span>
          <span className="font-semibold">{profileData.employee_id || "N/A"}</span>
        </div>

        <div className="flex items-center justify-between max-w-md">
          <div>
            <span className="">Manager Name: </span>
            <span className="font-semibold">
              {managerInfo ? managerInfo.name : "Not assigned"}
            </span>
          </div>
        </div>

        <div>
          <p className="font-semibold mb-2">Leave Balance:</p>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div>Casual Leave: {profileData.casual_leave_balance}</div>
            <div>Sick Leave: {profileData.sick_leave_balance}</div>
            <div>Annual Leave: {profileData.annual_leave_balance}</div>
            <div>WFH Balance: {profileData.wfh_balance}</div>
          </div>
        </div>

        <div>
          <p className="font-semibold mb-2">Submitted Documents:</p>
          <div className="space-y-3">
            {/* Aadhar Card */}
            <div className="flex items-center gap-3">
              <span className="w-24">Aadhar Card:</span>
              {documents.aadhar_card ? (
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" asChild>
                    <a
                      href={`${API_BASE_URL}${documents.aadhar_card.url}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-1"
                    >
                      View <ExternalLink className="w-4 h-4" />
                    </a>
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDeleteDocument("aadhar")}
                  >
                    <Trash2 className="w-4 h-4 text-red-600" />
                  </Button>
                </div>
              ) : (
                <label htmlFor="aadhar-upload" className="cursor-pointer">
                  <Button variant="outline" size="sm" asChild>
                    <span>
                      {uploadingDoc === "aadhar" ? "Uploading..." : "Upload"}
                    </span>
                  </Button>
                  <input
                    id="aadhar-upload"
                    type="file"
                    accept=".pdf,.doc,.docx"
                    className="hidden"
                    onChange={(e) => handleDocumentUpload(e, "aadhar")}
                    disabled={uploadingDoc === "aadhar"}
                  />
                </label>
              )}
            </div>

            {/* PAN Card */}
            <div className="flex items-center gap-3">
              <span className="w-24">PAN Card:</span>
              {documents.pan_card ? (
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" asChild>
                    <a
                      href={`${API_BASE_URL}${documents.pan_card.url}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-1"
                    >
                      View <ExternalLink className="w-4 h-4" />
                    </a>
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDeleteDocument("pan")}
                  >
                    <Trash2 className="w-4 h-4 text-red-600" />
                  </Button>
                </div>
              ) : (
                <label htmlFor="pan-upload" className="cursor-pointer">
                  <Button variant="outline" size="sm" asChild>
                    <span>
                      {uploadingDoc === "pan" ? "Uploading..." : "Upload"}
                    </span>
                  </Button>
                  <input
                    id="pan-upload"
                    type="file"
                    accept=".pdf,.doc,.docx"
                    className="hidden"
                    onChange={(e) => handleDocumentUpload(e, "pan")}
                    disabled={uploadingDoc === "pan"}
                  />
                </label>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
