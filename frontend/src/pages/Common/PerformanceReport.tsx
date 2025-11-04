"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader } from "@/components/ui/card"; // adjust import if needed

const periodLabels = ["Sep - Dec", "May - Aug", "Jan - Apr"];

const modulesByMonth = [
  { month: "Sep", value: 2 },
  { month: "Oct", value: 0.5 },
  { month: "Nov", value: 3.5 },
  { month: "Dec", value: 1 },
];

const PerformanceReport = () => {
  const [period, setPeriod] = useState(periodLabels[0]);
  return (
    <div className="min-h-screen bg-white flex flex-col items-center px-4 pt-12">
      <h1 className="text-3xl font-bold mb-3 text-center">
        Person 1 performance report
      </h1>
      <div className="flex flex-col items-center">
        <select
          value={period}
          onChange={(e) => setPeriod(e.target.value)}
          className="border rounded w-56 px-5 py-2 font-semibold bg-gray-200 mb-4"
        >
          {periodLabels.map((p) => (
            <option value={p} key={p}>
              {p}
            </option>
          ))}
        </select>
        <div className="mb-5 text-lg font-semibold text-center">
          Performance report for {period}
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8 max-w-5xl w-full">
        <Card>
          <CardHeader>
            <span className="font-bold text-lg text-center block">
              Training hours
            </span>
          </CardHeader>
          <CardContent>
            <div className="text-2xl text-center font-bold">134</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <span className="font-bold text-lg text-center block">
              Performance score
            </span>
          </CardHeader>
          <CardContent>
            <div className="text-2xl text-center font-bold">4.3</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <span className="font-bold text-lg text-center block">
              Modules Completed
            </span>
          </CardHeader>
          <CardContent>
            <div className="text-2xl text-center font-bold">7</div>
          </CardContent>
        </Card>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl w-full mb-8">
        <Card>
          <CardHeader>
            <span className="font-bold text-lg text-center block">
              Learner Rank
            </span>
          </CardHeader>
          <CardContent>
            <div className="text-2xl text-center font-bold">3</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <span className="font-bold text-lg text-center block">
              Punctuality Score
            </span>
          </CardHeader>
          <CardContent>
            <div className="text-2xl text-center font-bold">4.9</div>
          </CardContent>
        </Card>
      </div>
      {/* Modules completed by month chart */}
      <Card className="max-w-2xl w-full">
        <CardHeader>
          <span className="font-bold text-lg text-center block">
            Modules completed by month
          </span>
        </CardHeader>
        <CardContent>
          <svg
            viewBox="0 0 400 120"
            width="100%"
            height="80"
            style={{ display: "block", margin: "0 auto" }}
          >
            {/* Axes */}
            <line x1="60" y1="90" x2="370" y2="90" stroke="black" />
            <line x1="60" y1="30" x2="60" y2="90" stroke="black" />
            {/* Line graph */}
            <polyline
              fill="none"
              stroke="black"
              strokeWidth="2"
              points={modulesByMonth
                .map((d, i) => {
                  const x = 60 + i * 90;
                  const y = 90 - d.value * 15;
                  return `${x},${y}`;
                })
                .join(" ")}
            />
            {/* Dots and labels */}
            {modulesByMonth.map((d, i) => {
              const x = 60 + i * 90;
              const y = 90 - d.value * 15;
              return (
                <g key={d.month}>
                  <circle cx={x} cy={y} r={4} fill="black" />
                  <text x={x - 15} y={y - 10} fontSize={14}>
                    {d.value}
                  </text>
                  <text x={x} y={105} fontSize={14} textAnchor="middle">
                    {d.month}
                  </text>
                </g>
              );
            })}
          </svg>
        </CardContent>
      </Card>
      {/* <div className="flex mt-8"> */}
      {/*   <Button variant="secondary" className="px-8 py-2 font-semibold text-lg"> */}
      {/*     &larr; Back to Employees List */}
      {/*   </Button> */}
      {/* </div> */}
    </div>
  );
};

export default PerformanceReport;