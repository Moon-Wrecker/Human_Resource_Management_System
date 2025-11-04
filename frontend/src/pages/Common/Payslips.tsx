"use client";

import { useState } from "react";
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"; // Adjust import if needed
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";

const payslips = [
  {
    id: 1,
    label: "Slip 1",
    desc: "Salary for October",
    url: "/payslips/slip1.pdf",
  },
  {
    id: 2,
    label: "Slip 2",
    desc: "Salary for September",
    url: "/payslips/slip2.pdf",
  },
  {
    id: 3,
    label: "Slip 3",
    desc: "Salary for August",
    url: "/payslips/slip3.pdf",
  },
  {
    id: 4,
    label: "Slip 4",
    desc: "Salary for July",
    url: "/payslips/slip4.pdf",
  },
  {
    id: 5,
    label: "Slip 5",
    desc: "Salary for June",
    url: "/payslips/slip5.pdf",
  },
  {
    id: 6,
    label: "Slip 6",
    desc: "Salary for May",
    url: "/payslips/slip6.pdf",
  },
];

const months = [
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

const Payslips = () => {
  const [month, setMonth] = useState("");

  // For demo, filtering logic is omitted.
  // You can add month-based filtering here if your payslips have a month property.

  return (
    <div className="min-h-screen flex flex-col items-center">
      <h2 className="text-3xl font-semibold text-center my-8">Payslips</h2>
      <div className="w-full max-w-5xl flex justify-center mb-10">
        <Select value={month} onValueChange={(value) => setMonth(value)}>
          <SelectTrigger className="w-64">
            <SelectValue placeholder="Month" />
          </SelectTrigger>
          <SelectContent>
            {months.map((m) => (
              <SelectItem key={m} value={m}>
                {m}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="grid grid-cols-4 my-8 px-4 gap-4 w-full">
        {payslips.map((slip) => (
          <Card
            key={slip.id}
            className="w-full shadow-md rounded-2xl border border-gray-200"
          >
            <CardHeader>
              <CardTitle className="text-lg font-semibold text-gray-900 text-center">
                {slip.label}
              </CardTitle>
              <CardDescription className="text-sm text-gray-500 text-center mt-1">
                {slip.desc}
              </CardDescription>
            </CardHeader>

            <CardFooter className="flex justify-center">
              <Button
                asChild
                variant="outline"
                className="flex items-center gap-2 font-semibold"
              >
                <a href={slip.url} target="_blank" rel="noopener noreferrer">
                  Download
                </a>
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Payslips;