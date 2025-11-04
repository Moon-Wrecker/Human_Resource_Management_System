"use client";

import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogClose } from "@/components/ui/dialog";

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
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];
const DAYS_IN_WEEK = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];

// Get grid days
function getMonthDays(year: number, month: number) {
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month+1, 0).getDate();
  const days: (number | null)[] = Array(firstDay).fill(null)
    .concat(Array.from({ length: daysInMonth }, (_, i) => i + 1));
  // Fill the last week to complete the grid
  while (days.length % 7 !== 0) days.push(null);
  return days;
}

const Attendance = () => {
  const [selectedMonth, setSelectedMonth] = useState(monthNames[monthIdx]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogDay, setDialogDay] = useState<number | null>(null);
  const [dialogType, setDialogType] = useState<"leave" | "wfh" | "holiday" | null>(null);

  // Request form state (for modal)
  const [reqSubject, setReqSubject] = useState("");
  const [reqType, setReqType] = useState("");
  const [reqDesc, setReqDesc] = useState("");

  const leaveLeft = 8;
  const wfhLeft = 8;
  const days = getMonthDays(year, monthNames.indexOf(selectedMonth));

  function handleCellClick(d: number | null) {
    if (d == null) return;
    const evt = calendarEvents.find(e => e.day === d);
    setDialogDay(d);
    setDialogType(evt?.type ?? "leave");
    setDialogOpen(true);
  }

  return (
    <div className="min-h-screen bg-[#fafafa] flex flex-col items-center px-4 pt-12">
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
          onChange={e => setSelectedMonth(e.target.value)}
          className="border rounded bg-gray-200 h-12 px-6 min-w-[150px] font-semibold"
        >
          {monthNames.map(m => <option key={m} value={m}>{m}</option>)}
        </select>
        <button className="bg-gray-200 px-7 py-2 rounded font-semibold hover:bg-gray-300 transition">Apply For Leave</button>
        <button className="bg-gray-200 px-7 py-2 rounded font-semibold hover:bg-gray-300 transition">Apply for WFH</button>
      </div>
      {/* Calendar Grid */}
      <div className="w-full max-w-4xl">
        <table className="w-full border border-gray-300 rounded overflow-hidden">
          <thead>
            <tr>
              {DAYS_IN_WEEK.map(day => (
                <th key={day} className="px-0.5 text-center font-semibold border border-gray-300 py-2 bg-gray-100">
                  {day}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {[...Array(days.length / 7)].map((_, weekIdx) => (
              <tr key={weekIdx}>
                {days.slice(weekIdx * 7, weekIdx * 7 + 7).map((d, i) => {
                  const evt = calendarEvents.find(e => e.day === d);
                  return (
                    <td
                      key={i}
                      className="border border-gray-300 h-16 align-top px-1 text-center cursor-pointer relative"
                      onClick={() => handleCellClick(d)}
                    >
                      {d && (
                        <div>
                          <div className="font-semibold mb-1">{d}</div>
                          {evt && (
                            <div className="flex flex-col items-center">
                              {evt.type === "leave" && (
                                <span className="text-green-700 flex items-center gap-1 text-xs">
                                  <span className="w-2 h-2 bg-green-500 rounded-full inline-block"></span>
                                  Leave Request Approved
                                </span>
                              )}
                              {evt.type === "holiday" && (
                                <span className="text-yellow-700 flex items-center gap-1 text-xs">
                                  <span className="w-2 h-2 bg-yellow-400 rounded-full inline-block"></span>
                                  Holiday
                                </span>
                              )}
                            </div>
                          )}
                        </div>
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* Dialog on cell click */}
      {dialogOpen && (
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogContent className="max-w-md bg-[#e9e9ea] rounded-2xl shadow-xl p-2">
            <DialogHeader>
              <DialogTitle>Sending Request</DialogTitle>
            </DialogHeader>
            <div className="flex flex-col gap-4 pt-3">
              <div>
                <label className="font-bold underline block mb-1">Subject:</label>
                <input
                  value={reqSubject}
                  onChange={e => setReqSubject(e.target.value)}
                  className="border rounded px-3 py-2 w-full bg-white"
                  placeholder="Subject for Request..."
                />
              </div>
              <div>
                <label className="font-bold underline block mb-1">Request type:</label>
                <input
                  value={reqType}
                  onChange={e => setReqType(e.target.value)}
                  className="border rounded px-3 py-2 w-full bg-white"
                  placeholder="Add request type tag"
                />
              </div>
              <div>
                <label className="font-bold underline block mb-1">Request description:</label>
                <textarea
                  value={reqDesc}
                  onChange={e => setReqDesc(e.target.value)}
                  className="border rounded px-3 py-3 w-full bg-white resize-none"
                  placeholder="Request description..."
                />
              </div>
              <div className="flex justify-end mt-2">
                <DialogClose asChild>
                  <button
                    type="button"
                    className="bg-gray-300 px-7 py-2 rounded font-semibold hover:bg-gray-400 transition"
                    onClick={() => { setDialogOpen(false); setReqSubject(""); setReqType(""); setReqDesc(""); }}
                  >
                    Send
                  </button>
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