import EmployeeFeedbackTable from "@/components/FeedbackTable";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useState } from "react";

export default function FeedbackReport() {
  const [timePeriod, setTimePeriod] = useState("Sep - Dec");

  return (
    <div className="w-full px-4 flex items-center justify-center flex-col gap-6">
      <h2 className="text-3xl font-semibold text-center mt-8">
        Feedback Report
      </h2>
      <Select onValueChange={(e) => setTimePeriod(e)} value={timePeriod}>
        <SelectTrigger className="w-[20%]">
          <SelectValue placeholder="Time Period" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="Sep - Dec">Sep - Dec</SelectItem>
          <SelectItem value="Jan - Mar">Jan - Mar</SelectItem>
          <SelectItem value="Apr - Jun">Apr - Jun</SelectItem>
          <SelectItem value="Jul - Sep">Jul - Sep</SelectItem>
        </SelectContent>
      </Select>
      <h3 className="text-xl font-semibold text-center">
        Feedback Report for {timePeriod}
      </h3>
      <EmployeeFeedbackTable />
    </div>
  );
}
