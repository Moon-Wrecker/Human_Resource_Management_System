"use client";

import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import profileService, { type ProfileData } from "@/services/profileService";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";
import goalService, { type Goal } from "@/services/goalService";
import feedbackService, { type FeedbackResponse } from "@/services/feedbackService";
import {
  Table,
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const ViewEmployee = () => {
  const { employeeId } = useParams<{ employeeId: string }>();
  const [employee, setEmployee] = useState<ProfileData | null>(null);
  const [goals, setGoals] = useState<Goal[]>([]);
  const [feedback, setFeedback] = useState<FeedbackResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchEmployeeData = async () => {
      if (!employeeId) {
        setError("Employee ID is missing.");
        setLoading(false);
        return;
      }

      const id = parseInt(employeeId, 10);
      if (isNaN(id)) {
        setError("Invalid Employee ID.");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const [employeeData, goalsData, feedbackData] = await Promise.all([
          profileService.getUserProfile(id),
          goalService.getTeamGoals({ employee_id: id, limit: 5 }),
          feedbackService.getEmployeeFeedback(id, { limit: 5 }),
        ]);
        setEmployee(employeeData);
        setGoals(goalsData.goals);
        setFeedback(feedbackData.feedback);
      } catch (err) {
        console.error("Failed to fetch employee data:", err);
        setError("Failed to load employee data. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchEmployeeData();
  }, [employeeId]);

  if (loading) {
    return <div className="container mx-auto p-4 text-center">Loading employee data...</div>;
  }

  if (error) {
    return <div className="container mx-auto p-4 text-center text-red-500">{error}</div>;
  }

  if (!employee) {
    return <div className="container mx-auto p-4 text-center">No employee data found.</div>;
  }

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <div className="mb-4">
        <Button asChild variant="outline">
          <Link to="/manager/team-members">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Team
          </Link>
        </Button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-1">
            <Card>
                <CardHeader className="flex flex-col items-center text-center">
                <Avatar className="w-24 h-24 mb-4">
                    <AvatarImage src={employee.profile_image_url} />
                    <AvatarFallback>{employee.name.charAt(0)}</AvatarFallback>
                </Avatar>
                <CardTitle>{employee.name}</CardTitle>
                <p className="text-muted-foreground">{employee.job_role}</p>
                </CardHeader>
                <CardContent>
                <div className="flex flex-col gap-2">
                    <p><strong>Email:</strong> {employee.email}</p>
                    <p><strong>Department:</strong> {employee.department_name}</p>
                    <p><strong>Join Date:</strong> {employee.hire_date ? new Date(employee.hire_date).toLocaleDateString() : 'N/A'}</p>
                    <p><strong>Manager:</strong> {employee.manager_name || 'N/A'}</p>
                    <p><strong>Phone:</strong> {employee.phone || 'N/A'}</p>
                </div>
                </CardContent>
            </Card>
        </div>
        <div className="md:col-span-2 flex flex-col gap-4">
          <Card>
            <CardHeader>
              <CardTitle>Recent Goals</CardTitle>
            </CardHeader>
            <CardContent>
              {goals.length > 0 ? (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Goal</TableHead>
                      <TableHead>Status</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {goals.map(goal => (
                      <TableRow key={goal.id}>
                        <TableCell>{goal.title}</TableCell>
                        <TableCell><Badge>{goal.status.replace('_', ' ')}</Badge></TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              ) : (
                <p className="text-muted-foreground">No goals found.</p>
              )}
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Recent Feedback</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              {feedback.length > 0 ? (
                feedback.map(f => (
                  <div key={f.id} className="border-b last:border-b-0 py-2">
                    <p className="font-semibold">{f.subject}</p>
                    <p className="text-sm text-muted-foreground">From: {f.given_by_name} on {new Date(f.given_on).toLocaleDateString()}</p>
                  </div>
                ))
              ) : (
                <p className="text-muted-foreground">No feedback found.</p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ViewEmployee;