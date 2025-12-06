"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/contexts/AuthContext";
import PayslipGenerator from "./PayslipGenerator";
import Payslips from "@/pages/Common/Payslips";

export default function HRPayslipsPage() {
  const { user } = useAuth();
  const [refreshKey, setRefreshKey] = useState(0);

  const isHR = user?.role === "hr" || user?.role === "admin";

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-6xl mx-auto px-6 py-10 space-y-8">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">Payslips</h1>
          <p className="text-muted-foreground mt-2">Manage employee payslips</p>
        </div>

        {isHR && (
          <PayslipGenerator
            onSuccess={() => {
              // Trigger refetch of payslips
              setRefreshKey((prev) => prev + 1);
            }}
          />
        )}

        <div>
          <Payslips key={refreshKey} />
        </div>
      </div>
    </div>
  );
}