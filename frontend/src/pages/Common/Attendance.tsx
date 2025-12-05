import {
  Calendar,
  CalendarCurrentDate,
  CalendarMonthView,
  CalendarNextTrigger,
  CalendarPrevTrigger,
  CalendarTodayTrigger,
} from "@/components/FullCalendar";
import AnimatedCounter from "@/components/AnimatedCounter";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast";
import {
  ChevronLeft,
  ChevronRight,
  Clock,
  CheckCircle,
  Home,
  Briefcase,
} from "lucide-react";
import { useState, useEffect } from "react";
import attendanceService from "@/services/attendanceService";
import type {
  AttendanceFilters,
  AttendanceRecord,
  AttendanceSummary,
  PunchInResponse,
  PunchOutResponse,
} from "@/services/attendanceService";
import skillService from "@/services/skillService";
import leaveService from "@/services/leaveService";
import requestService from "@/services/requestService";

const monthNames = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

const Attendance = () => {
  const { toast } = useToast();
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(today.getDate() + 1);
  const tomorrowISO = tomorrow.toISOString().split("T")[0]; // YYYY-MM-DD

  const [selectedMonth, setSelectedMonth] = useState(
    monthNames[today.getMonth()],
  );
  const [calendarDate, setCalendarDate] = useState(today);

  // State for leave request modal
  const [dialogOpen, setDialogOpen] = useState(false);
  const [reqSubject, setReqSubject] = useState("");
  const [reqType, setReqType] = useState<
    "leave" | "casual" | "annual" | "maternity" | "paternity"
  >("leave");
  const [reqDate, setReqDate] = useState("");
  const [reqDesc, setReqDesc] = useState("");

  // State for general request modal
  const [requestModalOpen, setRequestModalOpen] = useState(false);
  const [generalReqSubject, setGeneralReqSubject] = useState("");
  const [generalReqType, setGeneralReqType] = useState<
    "wfh" | "equipment" | "travel" | "other"
  >("wfh");
  const [generalReqDate, setGeneralReqDate] = useState("");
  const [generalReqDesc, setGeneralReqDesc] = useState("");

  // API state
  const [todayAttendance, setTodayAttendance] =
    useState<AttendanceRecord | null>(null);
  const [summary, setSummary] = useState<AttendanceSummary | null>(null);
  const [attendanceHistory, setAttendanceHistory] = useState<
    AttendanceRecord[]
  >([]);
  const [punchingIn, setPunchingIn] = useState(false);
  const [punchingOut, setPunchingOut] = useState(false);

  useEffect(() => {
    handleMonthChange(selectedMonth);
  }, []);

  // Fetch attendance data for a given month & year

  const fetchAttendanceData = async (filters?: AttendanceFilters) => {
    try {
      // Today's attendance
      const todayData = await attendanceService.getTodayAttendance();
      setTodayAttendance(todayData);

      // Attendance history using the filters
      const historyData = await attendanceService.getMyAttendance({
        page_size: 100,
        ...filters,
      });
      setAttendanceHistory(historyData.records);

      // Monthly summary if start_date is provided
      if (filters?.start_date && filters?.end_date) {
        const summaryData = await attendanceService.getMySummary(
          new Date(filters.end_date).getMonth() + 1,
          new Date(filters.start_date).getFullYear(),
        );
        setSummary(summaryData);
      }
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error",
        description:
          error?.response?.data?.detail ||
          error?.message ||
          "Failed to load data",
      });
    }
  };

  const handlePunchIn = async () => {
    if (todayAttendance?.check_in_time) {
      toast({
        title: "Already Punched In",
        description: "You have already punched in today.",
      });
      return;
    }

    setPunchingIn(true);
    try {
      const response: PunchInResponse = await attendanceService.punchIn({
        status: "present",
        location: "office",
      });

      toast({
        title: "Success!",
        description: response.message,
      });

      setTodayAttendance(response.attendance);
      const startDate = new Date(today.getFullYear(), today.getMonth(), 1); // first day of month
      const endDate = new Date(today.getFullYear(), today.getMonth() + 1, 0); // last day of month

      fetchAttendanceData({
        start_date: startDate.toISOString().split("T")[0], // "YYYY-MM-DD"
        end_date: endDate.toISOString().split("T")[0],
        page_size: 100,
      });
    } catch (error: any) {
      console.error("Punch in error:", error);
      const errorMessage =
        error?.response?.data?.detail || error?.message || "Failed to punch in";
      toast({
        variant: "destructive",
        title: "Punch In Failed",
        description: errorMessage,
      });
    } finally {
      setPunchingIn(false);
    }
  };

  const handlePunchOut = async () => {
    if (!todayAttendance?.check_in_time) {
      toast({
        variant: "destructive",
        title: "Cannot Punch Out",
        description: "Please punch in first.",
      });
      return;
    }

    if (todayAttendance?.check_out_time) {
      toast({
        title: "Already Punched Out",
        description: "You have already punched out today.",
      });
      return;
    }

    setPunchingOut(true);
    try {
      const response: PunchOutResponse = await attendanceService.punchOut();

      toast({
        title: "Punched Out Successfully!",
        description: `You worked ${attendanceService.formatDuration(
          response.hours_worked,
        )} today.`,
      });

      setTodayAttendance(response.attendance);
      const startDate = new Date(today.getFullYear(), today.getMonth(), 1); // first day of month
      const endDate = new Date(today.getFullYear(), today.getMonth() + 1, 0); // last day of month

      fetchAttendanceData({
        start_date: startDate.toISOString().split("T")[0], // "YYYY-MM-DD"
        end_date: endDate.toISOString().split("T")[0],
        page_size: 100,
      });
    } catch (error: any) {
      console.error("Punch out error:", error);
      const errorMessage =
        error?.response?.data?.detail ||
        error?.message ||
        "Failed to punch out";
      toast({
        variant: "destructive",
        title: "Punch Out Failed",
        description: errorMessage,
      });
    } finally {
      setPunchingOut(false);
    }
  };

  const handleMonthChange = async (month: string) => {
    const monthIndex = monthNames.indexOf(month);
    const year = new Date().getFullYear();

    const newDate = new Date(year, monthIndex, 1);
    setCalendarDate(newDate); // Lazy load the calendar to the selected month

    const start_date = newDate.toISOString().split("T")[0];
    const end_date = new Date(year, monthIndex + 1, 0)
      .toISOString()
      .split("T")[0];

    setSelectedMonth(month);
    fetchAttendanceData({ start_date, end_date, page_size: 100 });
  };

  // Convert attendance records to calendar events
  const calendarEvents = attendanceHistory.map((record) => ({
    id: record.id.toString(),
    start: new Date(`${record.check_in_time}`),
    end: new Date(`${record.check_out_time}`),
    title: attendanceService.getStatusLabel(record.status),
    color: (record.status === "present"
      ? "green"
      : record.status === "wfh"
        ? "blue"
        : record.status === "leave"
          ? "pink"
          : record.status === "absent"
            ? "purple"
            : "default") as "default" | "blue" | "green" | "pink" | "purple",
  }));

  return (
    <div className="min-h-screen bg-white flex flex-col items-center px-4 pt-12">
      <h1 className="text-2xl font-bold mb-6">Attendance</h1>

      {/* Today's Attendance Card */}
      <Card className="w-full max-w-4xl mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="w-5 h-5" /> Today's Attendance
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Check-in */}
            <div className="flex flex-col items-center p-4 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-600 mb-2">Check-in</div>
              <div className="text-2xl font-bold">
                {todayAttendance?.check_in_time
                  ? attendanceService.formatTime(todayAttendance.check_in_time)
                  : "--:--"}
              </div>
              {todayAttendance?.check_in_time && (
                <CheckCircle className="w-5 h-5 text-green-500 mt-2" />
              )}
            </div>

            {/* Check-out */}
            <div className="flex flex-col items-center p-4 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-600 mb-2">Check-out</div>
              <div className="text-2xl font-bold">
                {todayAttendance?.check_out_time
                  ? attendanceService.formatTime(todayAttendance.check_out_time)
                  : "--:--"}
              </div>
              {todayAttendance?.check_out_time && (
                <CheckCircle className="w-5 h-5 text-green-500 mt-2" />
              )}
            </div>

            {/* Hours Worked */}
            <div className="flex flex-col items-center p-4 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-600 mb-2">Hours Worked</div>
              <div className="text-2xl font-bold">
                {todayAttendance?.hours_worked
                  ? attendanceService.formatDuration(
                      todayAttendance.hours_worked,
                    )
                  : "0h 0m"}
              </div>
            </div>
          </div>

          {/* Punch In/Out Buttons */}
          <div className="mt-6 flex flex-col sm:flex-row gap-4 items-center justify-center">
            {!todayAttendance?.check_in_time && (
              <Button
                onClick={handlePunchIn}
                disabled={punchingIn}
                className="w-full sm:w-auto"
                size="lg"
              >
                {punchingIn ? "Punching In..." : "Punch In"}
              </Button>
            )}

            {todayAttendance?.check_in_time &&
              !todayAttendance?.check_out_time && (
                <Button
                  onClick={handlePunchOut}
                  disabled={punchingOut}
                  variant="destructive"
                  className="w-full sm:w-auto"
                  size="lg"
                >
                  {punchingOut ? "Punching Out..." : "Punch Out"}
                </Button>
              )}

            {todayAttendance?.check_out_time && (
              <Badge
                variant="secondary"
                className="text-lg py-2 px-4 flex items-center gap-2"
              >
                <CheckCircle className="w-5 h-5" /> Completed for today
              </Badge>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Monthly Summary */}
      {summary && (
        <div className="w-full max-w-4xl mb-6">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <Card>
              <CardContent className="pt-6 text-center">
                <div className="text-3xl font-bold text-green-600">
                  <AnimatedCounter to={summary.total_present} />
                </div>
                <div className="text-sm text-gray-600 mt-1">Present Days</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6 text-center">
                <div className="text-3xl font-bold text-red-600">
                  <AnimatedCounter to={summary.total_absent} />
                </div>
                <div className="text-sm text-gray-600 mt-1">Absent Days</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6 text-center">
                <div className="text-3xl font-bold text-yellow-600">
                  <AnimatedCounter to={summary.total_leave} />
                </div>
                <div className="text-sm text-gray-600 mt-1">Leave Days</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6 text-center">
                <div className="text-3xl font-bold text-blue-600">
                  <AnimatedCounter to={summary.total_wfh} />
                </div>
                <div className="text-sm text-gray-600 mt-1">WFH Days</div>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="pt-6 text-center">
                <div className="text-3xl font-bold text-purple-600">
                  <AnimatedCounter
                    to={summary.attendance_percentage}
                    decimals={2}
                    suffix="%"
                  />
                </div>
                <div className="text-sm text-gray-600 mt-1">Attendance %</div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* Month Selector and Actions */}
      <div className="flex justify-center items-center gap-4 mb-7 flex-wrap">
        <Button
          onClick={() => {
            setDialogOpen(true);
          }}
          variant="outline"
        >
          Apply For Leave
        </Button>
        <Button
          onClick={() => {
            setRequestModalOpen(true);
          }}
          variant="outline"
        >
          Apply For Request
        </Button>
      </div>

      {/* Calendar */}
      <Calendar
        events={calendarEvents}
        date={calendarDate}
        onDateChange={setCalendarDate}
        onMonthChange={(month, year) => {
          const newMonthName = monthNames[month - 1];
          if (newMonthName !== selectedMonth) {
            handleMonthChange(newMonthName);
          }
        }}
      >
        <div className="h-dvh py-6 flex flex-col w-full">
          <div className="flex px-6 items-center gap-2 mb-6">
            <span className="flex-1" />
            <CalendarCurrentDate />
            <CalendarPrevTrigger>
              <ChevronLeft size={20} />
            </CalendarPrevTrigger>
            <CalendarTodayTrigger>Today</CalendarTodayTrigger>
            <CalendarNextTrigger>
              <ChevronRight size={20} />
            </CalendarNextTrigger>
          </div>
          <div className="flex-1 overflow-auto px-6 relative">
            <CalendarMonthView />
          </div>
        </div>
      </Calendar>

      {/* Leave Request Dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="max-w-md rounded-2xl shadow-lg p-6">
          <DialogHeader>
            <DialogTitle>Send Leave Request</DialogTitle>
          </DialogHeader>
          <div className="flex flex-col gap-4 pt-3">
            <div>
              <label className="font-medium block mb-2">Date</label>
              <input
                type="date"
                value={reqDate}
                onChange={(e) => setReqDate(e.target.value)}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                min={tomorrowISO}
              />
            </div>
            <div>
              <label className="font-medium block mb-2">Leave Type</label>
              <div className="flex gap-2">
                {["casual", "sick", "annual", "maternity", "paternity"].map(
                  (i) => (
                    <Button
                      type="button"
                      className="capitalize"
                      variant={reqType === i ? "default" : "outline"}
                      onClick={() =>
                        setReqType(
                          i as
                            | "leave"
                            | "casual"
                            | "annual"
                            | "maternity"
                            | "paternity",
                        )
                      }
                    >
                      {i}
                    </Button>
                  ),
                )}
              </div>
            </div>
            <div>
              <label className="font-medium block mb-2">Subject</label>
              <input
                value={reqSubject}
                onChange={(e) => setReqSubject(e.target.value)}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                placeholder="Subject for Request..."
              />
            </div>
            <div>
              <label className="font-medium block mb-2">Reason for Leave</label>
              <textarea
                value={reqDesc}
                onChange={(e) => setReqDesc(e.target.value)}
                className="w-full rounded-md border border-input bg-background px-3 py-3 text-sm resize-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                placeholder="Reason for leave..."
                rows={4}
              />
            </div>
            <div className="flex justify-end mt-4 gap-2">
              <DialogClose asChild>
                <Button type="button" variant="outline">
                  Cancel
                </Button>
              </DialogClose>
              <DialogClose asChild>
                <Button
                  type="button"
                  variant="default"
                  onClick={() => {
                    leaveService.applyForLeave({
                      leave_type: reqType as
                        | "leave"
                        | "casual"
                        | "annual"
                        | "maternity"
                        | "paternity",
                      start_date: reqDate, // Format: YYYY-MM-DD
                      end_date: reqDate, // Format: YYYY-MM-DD
                      subject: reqSubject,
                      reason: reqDesc,
                    });
                    toast({
                      title: "Request Submitted",
                      description:
                        "Your leave request has been submitted for approval.",
                    });
                    setDialogOpen(false);
                    setReqSubject("");
                    setReqType("leave");
                    setReqDesc("");
                    setReqDate("");
                  }}
                >
                  Send Request
                </Button>
              </DialogClose>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* General Request Dialog */}
      <Dialog open={requestModalOpen} onOpenChange={setRequestModalOpen}>
        <DialogContent className="max-w-md rounded-2xl shadow-lg p-6">
          <DialogHeader>
            <DialogTitle>Apply for Request</DialogTitle>
          </DialogHeader>
          <div className="flex flex-col gap-4 pt-3">
            <div>
              <label className="font-medium block mb-2">Date</label>
              <input
                type="date"
                value={generalReqDate}
                onChange={(e) => setGeneralReqDate(e.target.value)}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                min={tomorrowISO}
              />
            </div>
            <div>
              <label className="font-medium block mb-2">Request Type</label>
              <div className="flex gap-2">
                {["wfh", "equipment", "travel", "other"].map((i) => (
                  <Button
                    type="button"
                    className="capitalize"
                    variant={generalReqType === i ? "default" : "outline"}
                    onClick={() =>
                      setGeneralReqType(
                        i as "wfh" | "equipment" | "travel" | "other",
                      )
                    }
                  >
                    {i}
                  </Button>
                ))}
              </div>
            </div>
            <div>
              <label className="font-medium block mb-2">Subject</label>
              <input
                value={generalReqSubject}
                onChange={(e) => setGeneralReqSubject(e.target.value)}
                className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                placeholder="Subject for Request..."
              />
            </div>
            <div>
              <label className="font-medium block mb-2">
                Request Description
              </label>
              <textarea
                value={generalReqDesc}
                onChange={(e) => setGeneralReqDesc(e.target.value)}
                className="w-full rounded-md border border-input bg-background px-3 py-3 text-sm resize-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                placeholder="Request description..."
                rows={4}
              />
            </div>
            <div className="flex justify-end mt-4 gap-2">
              <DialogClose asChild>
                <Button type="button" variant="outline">
                  Cancel
                </Button>
              </DialogClose>
              <DialogClose asChild>
                <Button
                  type="button"
                  variant="default"
                  onClick={() => {
                    requestService.submitRequest({
                      request_type: generalReqType,
                      request_date: generalReqDate, // Format: YYYY-MM-DD
                      subject: generalReqSubject,
                      description: generalReqDesc,
                    });
                    toast({
                      title: "Request Submitted",
                      description:
                        "Your request has been submitted for approval.",
                    });
                    setRequestModalOpen(false);
                    setGeneralReqSubject("");
                    setGeneralReqType("wfh");
                    setGeneralReqDesc("");
                    setGeneralReqDate("");
                  }}
                >
                  Send Request
                </Button>
              </DialogClose>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};
export default Attendance;
