"use client";

import {
  Calendar,
  CalendarCurrentDate,
  CalendarMonthView,
  CalendarNextTrigger,
  CalendarPrevTrigger,
  CalendarTodayTrigger,
} from "@/components/FullCalendar";
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
import { ChevronLeft, ChevronRight, Clock, CheckCircle, Home, Briefcase } from "lucide-react";
import { useState, useEffect } from "react";
import attendanceService from "@/services/attendanceService";
import type { 
  AttendanceRecord, 
  AttendanceSummary,
  PunchInResponse,
  PunchOutResponse 
} from "@/services/attendanceService";

const Attendance = () => {
  const { toast } = useToast();
  const [selectedMonth, setSelectedMonth] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [reqSubject, setReqSubject] = useState("");
  const [reqType, setReqType] = useState("");
  const [reqDate, setReqDate] = useState("");
  const [reqDesc, setReqDesc] = useState("");
  
  // API State
  const [todayAttendance, setTodayAttendance] = useState<AttendanceRecord | null>(null);
  const [summary, setSummary] = useState<AttendanceSummary | null>(null);
  const [attendanceHistory, setAttendanceHistory] = useState<AttendanceRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [punchingIn, setPunchingIn] = useState(false);
  const [punchingOut, setPunchingOut] = useState(false);
  const [selectedStatus, setSelectedStatus] = useState<'present' | 'wfh'>('present');

  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
  ];

  const today = new Date();

  useEffect(() => {
    setSelectedMonth(monthNames[today.getMonth()]);
    fetchAttendanceData();
  }, []);

  const fetchAttendanceData = async () => {
    setLoading(true);
    try {
      // Fetch today's status
      const todayData = await attendanceService.getTodayAttendance();
      setTodayAttendance(todayData);

      // Fetch monthly summary
      const summaryData = await attendanceService.getMySummary();
      setSummary(summaryData);

      // Fetch attendance history (last 30 days)
      const historyData = await attendanceService.getMyAttendance({ page_size: 30 });
      setAttendanceHistory(historyData.records);
    } catch (error: any) {
      console.error("Error fetching attendance:", error);
      const errorMessage = error?.response?.data?.detail || error?.message || "Failed to load attendance data";
      toast({
        variant: "destructive",
        title: "Error",
        description: errorMessage,
      });
    } finally {
      setLoading(false);
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
        status: selectedStatus,
        location: selectedStatus === 'wfh' ? 'home' : 'office',
      });

      toast({
        title: "Success!",
        description: response.message,
      });

      setTodayAttendance(response.attendance);
      fetchAttendanceData(); // Refresh data
    } catch (error: any) {
      console.error("Punch in error:", error);
      const errorMessage = error?.response?.data?.detail || error?.message || "Failed to punch in";
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
        description: `You worked ${attendanceService.formatDuration(response.hours_worked)} today.`,
      });

      setTodayAttendance(response.attendance);
      fetchAttendanceData(); // Refresh data
    } catch (error: any) {
      console.error("Punch out error:", error);
      const errorMessage = error?.response?.data?.detail || error?.message || "Failed to punch out";
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
    setSelectedMonth(month);
    const monthIndex = monthNames.indexOf(month);
    try {
      const summaryData = await attendanceService.getMySummary(monthIndex + 1, today.getFullYear());
      setSummary(summaryData);
    } catch (error) {
      console.error("Error fetching month summary:", error);
    }
  };

  // Convert attendance records to calendar events
  const calendarEvents = attendanceHistory.map(record => ({
    id: record.id.toString(),
    start: new Date(`${record.date}T09:00:00`),
    end: new Date(`${record.date}T17:00:00`),
    title: attendanceService.getStatusLabel(record.status),
    color: record.status === 'present' ? 'green' : 
           record.status === 'wfh' ? 'blue' :
           record.status === 'leave' ? 'yellow' :
           record.status === 'absent' ? 'red' : 'purple',
  }));

  return (
    <div className="min-h-screen bg-white flex flex-col items-center px-4 pt-12">
      <h1 className="text-2xl font-bold mb-6">Attendance</h1>

      {/* Today's Status Card */}
      <Card className="w-full max-w-4xl mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Clock className="w-5 h-5" />
            Today's Attendance
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Check-in Status */}
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

            {/* Check-out Status */}
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
                  ? attendanceService.formatDuration(todayAttendance.hours_worked)
                  : "0h 0m"}
              </div>
            </div>
          </div>

          {/* Punch In/Out Buttons */}
          <div className="mt-6 flex flex-col sm:flex-row gap-4 items-center justify-center">
            {!todayAttendance?.check_in_time && (
              <>
                <div className="flex gap-2">
                  <Button
                    variant={selectedStatus === 'present' ? 'default' : 'outline'}
                    onClick={() => setSelectedStatus('present')}
                    className="flex items-center gap-2"
                  >
                    <Briefcase className="w-4 h-4" />
                    Office
                  </Button>
                  <Button
                    variant={selectedStatus === 'wfh' ? 'default' : 'outline'}
                    onClick={() => setSelectedStatus('wfh')}
                    className="flex items-center gap-2"
                  >
                    <Home className="w-4 h-4" />
                    WFH
                  </Button>
                </div>
                <Button 
                  onClick={handlePunchIn} 
                  disabled={punchingIn}
                  className="w-full sm:w-auto"
                  size="lg"
                >
                  {punchingIn ? "Punching In..." : "Punch In"}
                </Button>
              </>
            )}

            {todayAttendance?.check_in_time && !todayAttendance?.check_out_time && (
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
              <Badge variant="secondary" className="text-lg py-2 px-4">
                <CheckCircle className="w-5 h-5 mr-2" />
                Completed for today
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
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600">{summary.total_present}</div>
                  <div className="text-sm text-gray-600 mt-1">Present Days</div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-red-600">{summary.total_absent}</div>
                  <div className="text-sm text-gray-600 mt-1">Absent Days</div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-600">{summary.total_leave}</div>
                  <div className="text-sm text-gray-600 mt-1">Leave Days</div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">{summary.total_wfh}</div>
                  <div className="text-sm text-gray-600 mt-1">WFH Days</div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600">{summary.attendance_percentage}%</div>
                  <div className="text-sm text-gray-600 mt-1">Attendance %</div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* Month Selector and Actions */}
      <div className="flex justify-center items-center gap-4 mb-7 flex-wrap">
        <select
          value={selectedMonth}
          onChange={(e) => handleMonthChange(e.target.value)}
          className="border rounded bg-gray-200 h-12 px-6 min-w-[150px] font-semibold"
        >
          {monthNames.map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>
        <Button
          onClick={() => setDialogOpen(true)}
          variant="outline"
        >
          Apply For Leave
        </Button>
        <Button
          onClick={() => {
            setReqType("WFH");
            setDialogOpen(true);
          }}
          variant="outline"
        >
          Apply for WFH
        </Button>
      </div>

      {/* Calendar */}
      <Calendar events={calendarEvents}>
        <div className="h-dvh py-6 flex flex-col w-full">
          <div className="flex px-6 items-center gap-2 mb-6">
            <span className="flex-1" />
            <CalendarCurrentDate />
            <CalendarPrevTrigger>
              <ChevronLeft size={20} />
              <span className="sr-only">Previous</span>
            </CalendarPrevTrigger>
            <CalendarTodayTrigger>Today</CalendarTodayTrigger>
            <CalendarNextTrigger>
              <ChevronRight size={20} />
              <span className="sr-only">Next</span>
            </CalendarNextTrigger>
          </div>
          <div className="flex-1 overflow-auto px-6 relative">
            <CalendarMonthView />
          </div>
        </div>
      </Calendar>

      {/* Leave/WFH Request Dialog */}
      {dialogOpen && (
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogContent className="max-w-md rounded-2xl shadow-lg p-6">
            <DialogHeader>
              <DialogTitle>Send Request</DialogTitle>
            </DialogHeader>

            <div className="flex flex-col gap-4 pt-3">
              <div>
                <label className="font-medium block mb-2">Date</label>
                <input
                  type="date"
                  value={reqDate}
                  onChange={(e) => setReqDate(e.target.value)}
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                />
              </div>

              {/* Toggle for WFH / Leave */}
              <div>
                <label className="font-medium block mb-2">Request Mode</label>
                <div className="flex gap-2">
                  <Button
                    type="button"
                    variant={reqType === "WFH" ? "default" : "outline"}
                    onClick={() => setReqType("WFH")}
                  >
                    WFH
                  </Button>
                  <Button
                    type="button"
                    variant={reqType === "Leave" ? "default" : "outline"}
                    onClick={() => setReqType("Leave")}
                  >
                    Leave
                  </Button>
                </div>
              </div>

              {/* Subject Input */}
              <div>
                <label className="font-medium block mb-2">Subject</label>
                <input
                  value={reqSubject}
                  onChange={(e) => setReqSubject(e.target.value)}
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  placeholder="Subject for Request..."
                />
              </div>

              {/* Request Description */}
              <div>
                <label className="font-medium block mb-2">
                  Request Description
                </label>
                <textarea
                  value={reqDesc}
                  onChange={(e) => setReqDesc(e.target.value)}
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
                      // TODO: Implement leave request API call
                      toast({
                        title: "Request Submitted",
                        description: "Your request has been submitted for approval.",
                      });
                      setDialogOpen(false);
                      setReqSubject("");
                      setReqType("");
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
      )}
    </div>
  );
};

export default Attendance;
