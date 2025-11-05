"use client";

import {
  Calendar,
  CalendarCurrentDate,
  CalendarMonthView,
  CalendarNextTrigger,
  CalendarPrevTrigger,
  CalendarTodayTrigger,
} from "@/components/fullCalendar";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { useState } from "react";

// Example data for calendar events in current month
type CalendarEvent = {
  day: number;
  type: "leave" | "wfh" | "holiday";
  text: string;
};

const calendarEvents: CalendarEvent[] = [
  { day: 5, type: "leave", text: "Leave Request Approved" },
  { day: 9, type: "holiday", text: "Holiday" },
];

// Helper: Get this month's metadata
const today = new Date();
const year = today.getFullYear();
const monthIdx = today.getMonth();
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
const DAYS_IN_WEEK = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];

// Get grid days
function getMonthDays(year: number, month: number) {
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const days: (number | null)[] = Array(firstDay)
    .fill(null)
    .concat(Array.from({ length: daysInMonth }, (_, i) => i + 1));
  // Fill the last week to complete the grid
  while (days.length % 7 !== 0) days.push(null);
  return days;
}

const Attendance = () => {
  const [selectedMonth, setSelectedMonth] = useState(monthNames[monthIdx]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogDay, setDialogDay] = useState<number | null>(null);
  const [dialogType, setDialogType] = useState<
    "leave" | "wfh" | "holiday" | null
  >(null);

  // Request form state (for modal)
  const [reqSubject, setReqSubject] = useState("");
  const [reqType, setReqType] = useState("");
  const [reqDate, setReqDate] = useState("");
  const [reqDesc, setReqDesc] = useState("");

  const leaveLeft = 8;
  const wfhLeft = 8;
  const days = getMonthDays(year, monthNames.indexOf(selectedMonth));

  function handleCellClick(d: number | null) {
    if (d == null) return;
    const evt = calendarEvents.find((e) => e.day === d);
    setDialogDay(d);
    setDialogType(evt?.type ?? "leave");
    setDialogOpen(true);
  }

  return (
    <div className="min-h-screen bg-white flex flex-col items-center px-4 pt-12">
      <h1 className="text-2xl font-bold mb-10">Attendance</h1>
      {/* Summary */}
      <div className="flex gap-12 mb-6">
        <div className="bg-gray-100 rounded px-8 py-3 flex flex-col items-center font-bold text-lg">
          <span>WFH left</span>
          <span className="text-2xl">{wfhLeft}</span>
        </div>
        <div className="bg-gray-100 rounded px-8 py-3 flex flex-col items-center font-bold text-lg">
          <span>Leaves left</span>
          <span className="text-2xl">{leaveLeft}</span>
        </div>
      </div>
      {/* Month and Actions */}
      <div className="flex justify-center items-center gap-4 mb-7">
        <select
          value={selectedMonth}
          onChange={(e) => setSelectedMonth(e.target.value)}
          className="border rounded bg-gray-200 h-12 px-6 min-w-[150px] font-semibold"
        >
          {monthNames.map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>
        <button
          onClick={() => setDialogOpen(true)}
          className="bg-gray-200 px-7 py-2 rounded font-semibold hover:bg-gray-300 transition"
        >
          Apply For Leave
        </button>
        <button
          onClick={() => setDialogOpen(true)}
          className="bg-gray-200 px-7 py-2 rounded font-semibold hover:bg-gray-300 transition"
        >
          Apply for WFH
        </button>
      </div>
      {/* Calendar Grid */}

      <Calendar
        events={[
          {
            id: "1",
            start: new Date("2025-11-26T09:30:00Z"),
            end: new Date("2025-11-26T14:30:00Z"),
            title: "event A",
            color: "pink",
          },
          {
            id: "2",
            start: new Date("2025-11-26T10:00:00Z"),
            end: new Date("2025-11-26T10:30:00Z"),
            title: "event B",
            color: "blue",
          },
        ]}
      >
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

            {/* <ModeToggle /> */}
          </div>

          <div className="flex-1 overflow-auto px-6 relative">
            <CalendarMonthView />
          </div>
        </div>
      </Calendar>
      {/* Dialog on cell click */}
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

              {/* Request Type Input */}
              <div>
                <label className="font-medium block mb-2">Request Type</label>
                <input
                  value={reqType}
                  onChange={(e) => setReqType(e.target.value)}
                  className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  placeholder="Add request type tag"
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
                />
              </div>

              <div className="flex justify-end mt-4">
                <DialogClose asChild>
                  <Button
                    type="button"
                    variant="default"
                    onClick={() => {
                      setDialogOpen(false);
                      setReqSubject("");
                      setReqType("");
                      setReqDesc("");
                    }}
                  >
                    Send
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

