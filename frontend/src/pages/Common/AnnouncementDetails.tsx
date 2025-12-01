import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { ArrowLeft, CalendarDays, User } from "lucide-react";
import { useNavigate, useParams } from "react-router-dom";
import type { Announcement } from "@/services/announcementService";
import { useEffect, useState } from "react";
import announcementService from "@/services/announcementService";

const AnnouncementDetails = () => {
  const navigate = useNavigate();
  const { id: announcementId } = useParams();
  const [announcement, setAnnouncement] = useState<Announcement>();

  useEffect(() => {
    announcementService
      .getAnnouncementById(parseInt(announcementId || "0"))
      .then((res) => setAnnouncement(res));
  }, []);

  if (!announcement) return <p>Loading...</p>;

  return (
    <div className="flex justify-center my-8">
      <Card className="w-[70%] shadow-lg rounded-2xl border border-gray-200">
        {/* Header */}
        <CardHeader className="border-b">
          <div className="flex justify-between items-start">
            <div>
              <CardTitle className="text-2xl font-bold">
                {announcement.title}
              </CardTitle>
              <CardDescription className="flex items-center text-sm text-gray-500 mt-1 space-x-4">
                <span className="flex items-center gap-1">
                  <CalendarDays className="w-4 h-4" />
                  {new Date(announcement.published_date).toLocaleDateString(
                    "en-IN",
                    {
                      day: "2-digit",
                      month: "short",
                      year: "numeric",
                    },
                  )}
                </span>
                {announcement.created_by_name && (
                  <span className="flex items-center gap-1">
                    <User className="w-4 h-4" /> {announcement.created_by_name}
                  </span>
                )}
                {announcement.is_urgent && (
                  <Badge variant="destructive" className="text-white">
                    URGENT
                  </Badge>
                )}
              </CardDescription>
            </div>

            <Button
              variant="outline"
              size="sm"
              onClick={() => navigate(-1)}
              className="flex items-center gap-1"
            >
              <ArrowLeft className="w-4 h-4" /> Back
            </Button>
          </div>
        </CardHeader>

        {/* Content */}
        <CardContent className="space-y-4 mt-4">
          <p className="text-gray-700 text-sm leading-relaxed">
            {announcement.message}
          </p>

          {announcement.target_departments && (
            <p className="text-gray-600 text-sm">
              <span className="font-semibold">Target Departments:</span>{" "}
              {announcement.target_departments}
            </p>
          )}
          {announcement.target_roles && (
            <p className="text-gray-600 text-sm">
              <span className="font-semibold">Target Roles:</span>{" "}
              {announcement.target_roles}
            </p>
          )}
          {announcement.expiry_date && (
            <p className="text-gray-600 text-sm">
              <span className="font-semibold">Expiry Date:</span>{" "}
              {new Date(announcement.expiry_date).toLocaleDateString("en-IN", {
                day: "2-digit",
                month: "short",
                year: "numeric",
              })}
            </p>
          )}
        </CardContent>

        {/* Footer */}
        <CardFooter className="flex justify-between items-center border-t mt-4">
          {announcement.link ? (
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
                View Link <ArrowLeft className="w-4 h-4 rotate-180" />
              </a>
            </Button>
          ) : (
            <span className="text-sm text-gray-500">No external link</span>
          )}

          <span className="text-sm text-gray-500">
            {announcement.is_active ? "Active" : "Inactive"} |{" "}
            {announcement.is_expired ? "Expired" : "Valid"}
          </span>
        </CardFooter>
      </Card>
    </div>
  );
};

export default AnnouncementDetails;
