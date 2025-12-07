"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardHeader,
  CardContent,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import goalService, {
  GoalStatus,
  type GetMyGoalsParams,
  type Goal,
} from "@/services/goalService";
import { useEffect, useState } from "react";

export default function GoalTracker() {
  const [goal, setGoal] = useState<Goal[]>();

  const fetchGoal = (params: GetMyGoalsParams) =>
    goalService
      .getMyGoals(params)
      .then((res) =>
        setGoal(
          res.goals.filter(
            (i) =>
              i.status !== GoalStatus.COMPLETED &&
              i.status !== GoalStatus.CANCELLED &&
              i.status !== GoalStatus.ON_HOLD,
          ),
        ),
      );

  useEffect(() => {
    fetchGoal({
      limit: 100,
    });
  }, []);

  return (
    <div className="w-full max-w-3xl mx-auto mt-10 flex flex-col items-center">
      <h2 className="text-3xl font-semibold text-center my-8">Goal Tracker</h2>

      <Card className="w-full border">
        {goal && goal.length > 0 ? (
          <>
            {" "}
            <CardHeader className="text-center space-y-2">
              <CardTitle className="text-xl font-semibold">
                {goal[0].title}
              </CardTitle>
              <CardDescription className="text-base text-gray-600">
                {goal[0].description}
              </CardDescription>
              <p className="font-semibold text-sm">
                <span className="font-bold">Deadline:</span> {goal[0].target_date}
              </p>
              {goal[0].is_overdue && (
                <Badge variant="destructive">OVERDUE</Badge>
              )}
            </CardHeader>
            <CardContent className="space-y-5 mt-4">
              <h2 className="text-lg font-semibold">Checklist :</h2>

              <div className="space-y-3">
                {goal[0].checkpoints.map((item) => (
                  <div
                    key={item.id}
                    className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b pb-3"
                  >
                    <span className="text-sm sm:text-base truncate">
                      {item.title}:{" "}
                      <span className="text-muted-foreground truncate">
                        {item.description}
                      </span>
                    </span>
                    <div className="flex gap-2 justify-end">
                      {item.is_completed ? (
                        <Button size="sm" className="flex items-center gap-1">
                          Completed
                        </Button>
                      ) : (
                        <Button
                          variant="secondary"
                          size="sm"
                          className="flex items-center gap-1"
                          onClick={() => {
                            goalService.updateCheckpoint(item.id, {
                              is_completed: true,
                            });
                            fetchGoal({ limit: 100 });
                          }}
                        >
                          Mark as Complete
                        </Button>
                      )}
                      <a href={`goal-tracker/${item.goal_id}/${item.id}`}>
                        <Button
                          variant="link"
                          size="sm"
                          className="flex items-center gap-1"
                        >
                          Visit →
                        </Button>
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </>
        ) : (
          <CardContent className="text-center text-muted-foreground">
            All your goals are completed!
          </CardContent>
        )}
      </Card>
    </div>
  );
}
