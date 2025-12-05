"use client";

import { Area, AreaChart, CartesianGrid, XAxis } from "recharts";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  type ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import type { MonthlyModules } from "@/services/performanceReportService";

export const description = "A simple area chart";

const chartConfig = {
  modules_completed: {
    label: "Modules Completed:",
    color: "var(--chart-1)",
  },
} satisfies ChartConfig;

export function ChartAreaDefault({
  chartData,
}: {
  chartData: MonthlyModules[] | undefined;
}) {
  console.log(chartData);
  return (
    <Card className="w-full h-full text-center col-span-2 row-span-2">
      <CardHeader>
        <CardTitle className="text-xl font-bold">
          Modules completed by month
        </CardTitle>
      </CardHeader>
      <CardContent className="h-full w-full flex items-center justify-center">
        {chartData && chartData[0].modules_completed ? (
          <ChartContainer className="flex-1" config={chartConfig}>
            <AreaChart
              accessibilityLayer
              data={chartData}
              margin={{
                left: 12,
                right: 12,
                top: 24,
              }}
            >
              <CartesianGrid vertical={false} />
              <XAxis
                dataKey="month"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                tickFormatter={(value) => value.slice(0, 3)}
              />
              <ChartTooltip
                cursor={true}
                content={<ChartTooltipContent indicator="line" />}
              />
              <Area
                dataKey="modules_completed"
                type="natural"
                fill="var(--color-modules_completed)"
                fillOpacity={0.4}
                stroke="var(--color-modules_completed)"
              />
            </AreaChart>
          </ChartContainer>
        ) : (
          <p>No data found!</p>
        )}
      </CardContent>
    </Card>
  );
}
