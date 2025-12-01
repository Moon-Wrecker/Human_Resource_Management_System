import { useParams, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft } from "lucide-react";
import { useEffect, useState } from "react";
import skillService, { type SkillModule } from "@/services/skillService";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";

const SkillVisit = () => {
  const { slug } = useParams();
  const navigate = useNavigate();
  const [skill, setSkill] = useState<SkillModule | null>(null);
  const [loading, setLoading] = useState(true);

  // TODO: Add is completed!,

  useEffect(() => {
    skillService
      .getModuleById(parseInt(slug || "0"))
      .then((res) => setSkill(res))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) {
    return (
      <div className="flex flex-col items-center px-4 py-12">
        <div className="w-full max-w-3xl space-y-6">
          <Skeleton className="w-40 h-10" />
          <Card className="border rounded-2xl p-6 space-y-4">
            <Skeleton className="h-8 w-2/3" />
            <Skeleton className="h-20 w-full" />
            <Skeleton className="h-6 w-1/3" />
            <Skeleton className="h-6 w-1/2" />
            <Skeleton className="h-10 w-32 mt-4" />
          </Card>
        </div>
      </div>
    );
  }

  if (!skill) {
    return (
      <div className="flex flex-col items-center justify-center h-screen">
        <p className="text-lg font-medium">Skill not found</p>
        <Button onClick={() => navigate("/skills")} className="mt-4">
          Go Back
        </Button>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center px-4 py-10">
      <Button
        onClick={() => navigate("/employee/skill-development")}
        variant="ghost"
        className="mb-6 flex items-center gap-2 text-sm text-muted-foreground hover:text-primary"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Skills
      </Button>

      <Card className="w-full max-w-3xl border rounded-2xl shadow-sm">
        <CardHeader className="pb-2">
          <CardTitle className="text-3xl font-bold tracking-tight">
            {skill.name}
          </CardTitle>
          {skill.category && (
            <p className="text-sm text-muted-foreground mt-1">
              {skill.category}
            </p>
          )}
        </CardHeader>

        <Separator className="my-4" />

        <CardContent className="space-y-10">
          {/* About Section */}
          <section>
            <h3 className="text-lg font-semibold mb-2">Overview</h3>
            <p className="text-muted-foreground leading-relaxed">
              {skill.description || "No description available."}
            </p>
          </section>

          <Separator />

          {/* Module Details - grid panel */}
          <section>
            <h3 className="text-lg font-semibold mb-4">Module Details</h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div className="space-y-1">
                <p className="text-sm font-medium text-muted-foreground">
                  Duration (hours)
                </p>
                <p className="text-base">{skill.duration_hours || "—"}</p>
              </div>

              <div className="space-y-1">
                <p className="text-sm font-medium text-muted-foreground">
                  Difficulty Level
                </p>
                <p className="text-base capitalize">
                  {skill.difficulty_level || "—"}
                </p>
              </div>

              <div className="space-y-1">
                <p className="text-sm font-medium text-muted-foreground">
                  Active Module
                </p>
                <p className="text-base">{skill.is_active ? "Yes" : "No"}</p>
              </div>
            </div>
          </section>

          <Separator />

          {/* Skill Areas */}
          {skill.skill_areas && (
            <section>
              <h3 className="text-lg font-semibold mb-2">
                Skill Areas Covered
              </h3>
              <div className="flex flex-wrap gap-2">
                {skill.skill_areas.split(",").map((area) => (
                  <Badge
                    key={area}
                    variant="secondary"
                    className="px-3 py-1 text-sm"
                  >
                    {area.trim()}
                  </Badge>
                ))}
              </div>
            </section>
          )}

          <Separator />

          {/* Stats Section */}
          <section>
            <h3 className="text-lg font-semibold mb-4">Enrollment Stats</h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  Enrolled
                </p>
                <p className="text-base">{skill.total_enrollments ?? "—"}</p>
              </div>

              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  Completed
                </p>
                <p className="text-base">{skill.completed_count ?? "—"}</p>
              </div>

              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  Completion Rate
                </p>
                <p className="text-base">
                  {skill.total_enrollments && skill.completed_count
                    ? `${Math.round(
                        (skill.completed_count / skill.total_enrollments) * 100,
                      )}%`
                    : "—"}
                </p>
              </div>
            </div>
          </section>

          <Separator />

          {/* Visit Button */}
          <div className="flex justify-end gap-2">
            <Button variant="outline" asChild>
              <a
                href={skill.module_link}
                target="_blank"
                rel="noopener noreferrer"
              >
                Visit Module
              </a>
            </Button>
            <Button
              onClick={() =>
                skillService.markEnrollmentComplete(parseInt(slug || "0"), {
                  score: 100,
                })
              }
            >
              Mark As Complete
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SkillVisit;
