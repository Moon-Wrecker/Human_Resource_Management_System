"use client";

import { useEffect, useState } from "react";
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
import payslipService, {
  type PayslipResponse,
} from "@/services/payslipService";
import { IndianRupeeIcon } from "lucide-react";

const years = [...Array(9)].map((_, i) =>
  (new Date().getFullYear() - i).toString(),
);
const Payslips = () => {
  const [year, setYear] = useState(years[0]);
  const [payslips, setPayslips] = useState<PayslipResponse[]>([]);

  useEffect(() => {
    payslipService
      .getMyPayslips({ year: parseInt(year) })
      .then((res) => setPayslips(res.payslips));
  }, [year]);

  return (
    <div className="min-h-screen flex flex-col items-center">
      <h2 className="text-3xl font-semibold text-center my-8">Payslips</h2>
      <div className="w-full max-w-5xl flex justify-center mb-10">
        <Select value={year} onValueChange={(value) => setYear(value)}>
          <SelectTrigger className="w-64">
            <SelectValue placeholder="Month" />
          </SelectTrigger>
          <SelectContent>
            {years.map((m) => (
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
                {slip.issued_at.split("T")[0]}
              </CardTitle>
              <CardDescription className="text-sm text-gray-500 text-center mt-1 flex items-center justify-center ">
                Net Salary: <IndianRupeeIcon className="h-3 w-3" />
                {slip.net_salary}
              </CardDescription>
            </CardHeader>

            <CardFooter className="flex justify-center">
              <Button
                asChild
                variant="outline"
                className="flex items-center gap-2 font-semibold cursor-pointer"
              >
                <a href={`payslips/${slip.id}`} rel="noopener noreferrer">
                  View Details
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

