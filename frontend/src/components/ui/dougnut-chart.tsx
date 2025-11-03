"use client";

import { TrendingUp } from "lucide-react";
import { Legend, Pie, PieChart } from "recharts";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  type ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";

export const description = "A donut chart showing learning goals progress";

const chartConfig = {
  value: {
    label: "Value",
  },
  Completed: {
    label: "Completed",
    color: "var(--color-completed)",
  },
  Pending: {
    label: "Pending",
    color: "var(--color-pending)",
  },
} satisfies ChartConfig;

type DataItem = {
  label: string;
  value: number;
  fill: string;
};

type ChartProps = {
  title: string;
  desc?: string;
  data: DataItem[];
};

export function DoughnutChart({ title, desc, data }: ChartProps) {
  return (
    <Card className="flex flex-col text-center">
      <CardHeader className="items-center pb-0">
        <CardTitle className="text-2xl font-bold">{title}</CardTitle>
        {desc && <CardDescription>{desc}</CardDescription>}
      </CardHeader>
      <CardContent className="flex-1 pb-0">
        <ChartContainer
          config={chartConfig}
          className="mx-auto aspect-square max-h-[250px]"
        >
          <PieChart>
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />
            <Pie
              data={data}
              dataKey="value"
              nameKey="label"
              innerRadius={60}
              outerRadius={90}
              fill="#8884d8"
              paddingAngle={5}
              stroke="none"
            />
            <Legend
              verticalAlign="bottom"
              width={280}
              className="flex items-center justify-center gap-4 my-8 w-full"
              payload={data.map((item) => ({
                id: item.label,
                type: "square",
                value: `${item.label} (${item.value}%)`,
                color: item.fill,
              }))}
            />
          </PieChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex-col gap-2 text-sm">
        <div className="flex items-center gap-2 leading-none font-medium">
          Progress updated recently <TrendingUp className="h-4 w-4" />
        </div>
        <div className="text-muted-foreground leading-none">
          Showing learning goals progress
        </div>
      </CardFooter>
    </Card>
  );
}
