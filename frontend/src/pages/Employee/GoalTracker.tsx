"use client";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardHeader,
  CardContent,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";

export default function GoalTracker() {
  const checkpoints = [
    {
      id: 1,
      label: "Checkpoint 1 : Module X Reading",
      slug: "module-x",
    },
    {
      id: 2,
      label: "Checkpoint 2 : Module X Practice Exercise",
      slug: "module-y",
    },
    {
      id: 3,
      label: "Checkpoint 3 : Module X Knowledge Check",
      slug: "module-z",
    },
  ];

  return (
    <div className="w-full max-w-3xl mx-auto mt-10 flex flex-col items-center">
      <h2 className="text-3xl font-semibold text-center my-8">Goal Tracker</h2>

      <Card className="w-full border">
        <CardHeader className="text-center space-y-2">
          <CardTitle className="text-xl font-semibold">
            Current Goal: Module X
          </CardTitle>
          <CardDescription className="text-base text-gray-600">
            Complete Module X and pass all knowledge checks
          </CardDescription>
          <p className="font-semibold text-sm">
            <span className="font-bold">Deadline:</span> 21 October 2025
          </p>
        </CardHeader>

        <CardContent className="space-y-5 mt-4">
          <h2 className="text-lg font-semibold">Checklist :</h2>

          <div className="space-y-3">
            {checkpoints.map((item) => (
              <div
                key={item.id}
                className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b pb-3"
              >
                <span className="text-sm sm:text-base">{item.label}</span>
                <div className="flex gap-2 justify-end">
                  <a href={`goal-tracker/${item.slug}`}>
                    <Button
                      variant="link"
                      size="sm"
                      className="flex items-center gap-1"
                    >
                      Visit →
                    </Button>
                  </a>
                  <Button
                    variant="secondary"
                    size="sm"
                    className="flex items-center gap-1"
                  >
                    Mark as Complete
                  </Button>
                </div>
              </div>
            ))}
          </div>

          <div className="pt-4 flex justify-end">
            <Button className="flex items-center gap-2">
              Mark Goal as Complete →
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
