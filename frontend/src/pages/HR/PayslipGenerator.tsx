"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import payslipService from "@/services/payslipService";
import { CheckCircle, AlertCircle, Loader2 } from "lucide-react";

interface PayslipGeneratorProps {
  onSuccess?: () => void;
}

export default function PayslipGenerator({ onSuccess }: PayslipGeneratorProps) {
  const [month, setMonth] = useState<string>("");
  const [year, setYear] = useState<string>(new Date().getFullYear().toString());
  const [payDate, setPayDate] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const monthOptions = [
    { value: "1", label: "January" },
    { value: "2", label: "February" },
    { value: "3", label: "March" },
    { value: "4", label: "April" },
    { value: "5", label: "May" },
    { value: "6", label: "June" },
    { value: "7", label: "July" },
    { value: "8", label: "August" },
    { value: "9", label: "September" },
    { value: "10", label: "October" },
    { value: "11", label: "November" },
    { value: "12", label: "December" },
  ];

  const currentYear = new Date().getFullYear();
  const yearOptions = Array.from({ length: 5 }, (_, i) => (currentYear - i).toString());

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!month || !year) {
      setError("Please select month and year");
      return;
    }

    try {
      setLoading(true);
      const payload = {
        month: parseInt(month, 10),
        year: parseInt(year, 10),
        pay_date: payDate || undefined,
      };

      const result = await payslipService.generateMonthlyPayslips(payload);
      setSuccess(`Successfully generated ${result.length} payslips for ${monthOptions.find(m => m.value === month)?.label} ${year}`);
      
      // Reset form
      setMonth("");
      setYear(new Date().getFullYear().toString());
      setPayDate("");

      // Call callback if provided
      onSuccess?.();
    } catch (err: any) {
      setError(err?.message || "Failed to generate payslips");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Generate Monthly Payslips</CardTitle>
        <CardDescription>Generate payslips for all employees for a specific month</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleGenerate} className="space-y-6">
          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {success && (
            <Alert className="border-green-200 bg-green-50">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <AlertDescription className="text-green-800">{success}</AlertDescription>
            </Alert>
          )}

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="month">Month *</Label>
              <Select value={month} onValueChange={setMonth}>
                <SelectTrigger id="month">
                  <SelectValue placeholder="Select month" />
                </SelectTrigger>
                <SelectContent>
                  {monthOptions.map((opt) => (
                    <SelectItem key={opt.value} value={opt.value}>
                      {opt.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="year">Year *</Label>
              <Select value={year} onValueChange={setYear}>
                <SelectTrigger id="year">
                  <SelectValue placeholder="Select year" />
                </SelectTrigger>
                <SelectContent>
                  {yearOptions.map((y) => (
                    <SelectItem key={y} value={y}>
                      {y}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="payDate">Pay Date (Optional)</Label>
              <Input
                id="payDate"
                type="date"
                value={payDate}
                onChange={(e) => setPayDate(e.target.value)}
                placeholder="YYYY-MM-DD"
              />
            </div>
          </div>

          <div className="flex justify-end gap-3">
            <Button
              type="button"
              variant="outline"
              onClick={() => {
                setMonth("");
                setYear(new Date().getFullYear().toString());
                setPayDate("");
                setError(null);
                setSuccess(null);
              }}
            >
              Clear
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Generating...
                </>
              ) : (
                "Generate Payslips"
              )}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}