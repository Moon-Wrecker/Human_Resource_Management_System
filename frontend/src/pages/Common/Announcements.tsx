import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ArrowRight, CalendarDays } from "lucide-react";

const Announcements = () => {
  const announcements = [
    {
      id: 1,
      title: "Office Closed for Diwali",
      message:
        "All branches will remain closed from November 14–16 for Diwali celebrations. Wishing everyone a joyous festival!",
      date: "2025-11-02",
      link: "https://intranet.company.com/holiday-calendar",
    },
    {
      id: 2,
      title: "Performance Review Cycle Begins",
      message:
        "Q3 performance reviews are now open. Please submit your self-assessment by November 10.",
      date: "2025-11-01",
      link: "https://hr.company.com/performance-review",
    },
    {
      id: 3,
      title: "New Expense Policy Update",
      message:
        "The revised travel and meal reimbursement policy is effective from November 5. Review the changes carefully.",
      date: "2025-10-30",
      link: "https://intranet.company.com/policies/expense-policy",
    },
    {
      id: 4,
      title: "Wellness Webinar",
      message:
        "Join our live wellness webinar on stress management hosted by Dr. Meera Patel on November 6 at 4 PM.",
      date: "2025-10-29",
      link: "https://events.company.com/wellness-webinar",
    },
    {
      id: 5,
      title: "System Downtime Notice",
      message:
        "The HRMS portal will be unavailable for scheduled maintenance on November 4 between 1 AM and 3 AM.",
      date: "2025-10-28",
      link: "https://status.company.com/hrms",
    },
    {
      id: 6,
      title: "New Employee Portal Features",
      message:
        "Explore new features added to the employee portal, including document uploads and leave tracking.",
      date: "2025-10-26",
      link: "https://intranet.company.com/employee-portal",
    },
    {
      id: 7,
      title: "Mandatory Cybersecurity Training",
      message:
        "All employees must complete the annual cybersecurity training by November 12.",
      date: "2025-10-25",
      link: "https://learn.company.com/cybersecurity-training",
    },
    {
      id: 8,
      title: "Blood Donation Drive",
      message:
        "Participate in our annual blood donation camp on November 8 at the HQ auditorium.",
      date: "2025-10-24",
      link: "https://intranet.company.com/events/blood-donation",
    },
    {
      id: 9,
      title: "New Joiners Announcement",
      message:
        "We’re thrilled to welcome 12 new team members this month! Check out their introductions on the HR portal.",
      date: "2025-10-23",
      link: "https://hr.company.com/new-joiners",
    },
    {
      id: 10,
      title: "Quarterly Town Hall Meeting",
      message:
        "Join our leadership team for the Q3 town hall on November 7 at 11 AM. Attendance is mandatory.",
      date: "2025-10-21",
      link: "https://events.company.com/townhall-q3",
    },
  ];

  return (
    <>
      <h2 className="text-3xl font-semibold text-center mt-8">Announcements</h2>

      <div className="grid grid-cols-3 my-8 px-4 gap-4">
        {announcements.map((announcement) => (
          <Card className="w-full shadow-md rounded-2xl border border-gray-200">
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
    </>
  );
};

export default Announcements;
