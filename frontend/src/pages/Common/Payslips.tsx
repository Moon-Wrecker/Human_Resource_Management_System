"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader } from "@/components/ui/card"; // Adjust import if needed

const payslips = [
  { id: 1, label: "Slip 1", desc: "Salary for October", url: "/payslips/slip1.pdf" },
  { id: 2, label: "Slip 2", desc: "Salary for September", url: "/payslips/slip2.pdf" },
  { id: 3, label: "Slip 3", desc: "Salary for August", url: "/payslips/slip3.pdf" },
  { id: 4, label: "Slip 4", desc: "Salary for July", url: "/payslips/slip4.pdf" },
  { id: 5, label: "Slip 5", desc: "Salary for June", url: "/payslips/slip5.pdf" },
  { id: 6, label: "Slip 6", desc: "Salary for May", url: "/payslips/slip6.pdf" },
];

const months = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

const Payslips = () => {
  const [month, setMonth] = useState("");

  // For demo, filtering logic is omitted.
  // You can add month-based filtering here if your payslips have a month property.

  return (
    <div className="min-h-screen bg-[#fafafa] flex flex-col items-center px-4 pt-12">
      <h1 className="text-2xl font-bold mb-10">Payslips</h1>
      <div className="w-full max-w-5xl flex justify-center mb-10">
        <select
          value={month}
          onChange={e => setMonth(e.target.value)}
          className="border rounded bg-gray-200 h-12 px-5 w-64 font-semibold"
        >
          <option value="">Month</option>
          {months.map(m => (
            <option value={m} key={m}>{m}</option>
          ))}
        </select>
      </div>
      <div className="w-full max-w-5xl grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 justify-items-center">
        {payslips.map(slip => (
          <Card key={slip.id} className="w-full min-h-[150px] flex flex-col">
            <CardHeader>
              <div className="font-bold text-lg text-center">{slip.label}</div>
            </CardHeader>
            <CardContent className="flex flex-col items-center">
              <div className="text-center text-sm mb-4">{slip.desc}</div>
              <a
                href={slip.url}
                className="bg-gray-300 px-6 py-2 rounded font-semibold hover:bg-gray-400 transition text-base"
                target="_blank"
                rel="noopener noreferrer"
              >
                Download
              </a>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Payslips;
