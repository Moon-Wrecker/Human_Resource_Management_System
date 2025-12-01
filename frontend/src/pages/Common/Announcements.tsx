import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import announcementService, {
  type Announcement,
} from "@/services/announcementService";
import { ArrowRight, CalendarDays } from "lucide-react";
import { useEffect, useState } from "react";

const Announcements = () => {
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);

  useEffect(() => {
    announcementService
      .getAnnouncements()
      .then((res) => setAnnouncements(res.announcements || []))
      .catch((err) => console.error(err));
  }, []);

  if (!announcements || announcements.length === 0)
    return <p className="text-center mt-8">No announcements found!</p>;

  return (
    <>
      <h2 className="text-3xl font-semibold text-center mt-8">Announcements</h2>

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
                {new Date(announcement.published_date).toLocaleDateString(
                  "en-IN",
                  {
                    day: "2-digit",
                    month: "short",
                    year: "numeric",
                  },
                )}
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
