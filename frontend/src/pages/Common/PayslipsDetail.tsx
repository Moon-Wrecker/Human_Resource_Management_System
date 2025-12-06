import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import payslipService, {
  type PayslipResponse,
} from "@/services/payslipService";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Printer } from "lucide-react";

const PayslipsDetail = () => {
  const { id: payslipId } = useParams();

  const [payslip, setPayslip] = useState<PayslipResponse>();

  useEffect(() => {
    payslipService
      .getPayslipById(parseInt(payslipId || "0"))
      .then((res) => setPayslip(res));
  }, []);

  if (!payslip) return <p>Data not found!</p>;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="flex justify-center my-8">
      <style>
        {`
          @media print {
            /* Remove browser default headers and footers */
            @page {
              margin: 0;
              size: auto;
            }
            
            /* Hide everything except our content */
            body * {
              visibility: hidden;
            }
            
            /* Make only the payslip card and its children visible */
            .print-card,
            .print-card * {
              visibility: visible;
            }
            
            /* Position the card at the top left */
            .print-card {
              position: absolute;
              left: 0;
              top: 0;
              width: 100% !important;
              margin: 0 !important;
              padding: 2rem !important;
              border: none !important;
              box-shadow: none !important;
              border-radius: 0 !important;
            }
            
            /* Hide buttons and other non-printable elements */
            .no-print {
              display: none !important;
              visibility: hidden !important;
            }
            
            /* Remove margins from body */
            html, body {
              margin: 0 !important;
              padding: 0 !important;
              width: 100%;
              height: 100%;
              print-color-adjust: exact;
              -webkit-print-color-adjust: exact;
            }
          }
        `}
      </style>
      <Card className="w-[80%] shadow-lg rounded-2xl border border-gray-200 print-card">
        {/* Header */}
        <CardHeader className="border-b">
          <CardTitle className="text-2xl font-bold">
            Payslip - {payslip.employee_name}
          </CardTitle>
          <p className="text-sm text-gray-500">
            Employee ID: {payslip.employee_id_number} | Month: {payslip.month}/
            {payslip.year}
          </p>
        </CardHeader>

        {/* Content */}
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-gray-600">Pay Period Start:</p>
              <p className="font-medium">{payslip.pay_period_start}</p>
            </div>
            <div>
              <p className="text-gray-600">Pay Period End:</p>
              <p className="font-medium">{payslip.pay_period_end}</p>
            </div>
            <div>
              <p className="text-gray-600">Pay Date:</p>
              <p className="font-medium">{payslip.pay_date}</p>
            </div>
            <div>
              <p className="text-gray-600">Issued By:</p>
              <p className="font-medium">{payslip.issued_by_name}</p>
            </div>
          </div>

          <div className="border-t border-gray-200 pt-4 space-y-2">
            <h3 className="text-lg font-semibold">Earnings</h3>
            <p>Basic Salary: {payslip.basic_salary}</p>
            <p>Allowances: {payslip.allowances}</p>
            <p>Overtime Pay: {payslip.overtime_pay}</p>
            <p>Bonus: {payslip.bonus}</p>
            <p className="font-bold">Gross Salary: {payslip.gross_salary}</p>
          </div>

          <div className="border-t border-gray-200 pt-4 space-y-2">
            <h3 className="text-lg font-semibold">Deductions</h3>
            <p>Tax Deduction: {payslip.tax_deduction}</p>
            <p>PF Deduction: {payslip.pf_deduction}</p>
            <p>Insurance Deduction: {payslip.insurance_deduction}</p>
            <p>Other Deductions: {payslip.other_deductions}</p>
            <p className="font-bold">
              Total Deductions: {payslip.total_deductions}
            </p>
          </div>

          <div className="border-t border-gray-200 pt-4">
            <h3 className="text-lg font-semibold">Net Salary</h3>
            <p className="text-2xl font-bold text-green-600">
              {payslip.net_salary}
            </p>
          </div>
        </CardContent>

        {/* Footer */}
        <CardFooter className="flex justify-between items-center">
          <div className="flex gap-2 no-print">
            <Button onClick={handlePrint} variant="default">
              <Printer className="h-4 w-4 mr-2" />
              Print Payslip
            </Button>
            {payslip.has_document && (
              <Button asChild variant="outline">
                <a
                  href={payslip.payslip_file_path}
                  target="_blank"
                  rel="noreferrer"
                >
                  Download Payslip
                </a>
              </Button>
            )}
          </div>
          <p className="text-sm text-gray-500">
            Issued at: {new Date(payslip.issued_at).toLocaleString()}
          </p>
        </CardFooter>
      </Card>
    </div>
  );
};

export default PayslipsDetail;
