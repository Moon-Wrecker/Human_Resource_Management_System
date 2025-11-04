import { useParams, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft } from "lucide-react";

const skillDevelopmentItems = [
  {
    module: "JavaScript Basics",
    slug: "javascript-basics",
    desc: "Learn the fundamentals of JavaScript, including variables, loops, functions, and events.",
    link: "https://example.com/javascript-basics",
  },
  {
    module: "React Fundamentals",
    slug: "react-fundamentals",
    desc: "Get started with React, covering components, props, state, and hooks.",
    link: "https://example.com/react-fundamentals",
  },
  {
    module: "CSS & Tailwind",
    slug: "css-tailwind",
    desc: "Master styling with CSS and Tailwind for responsive and modern web designs.",
    link: "https://example.com/css-tailwind",
  },
  {
    module: "Node.js & Express",
    slug: "node-express",
    desc: "Build server-side applications with Node.js and Express framework.",
    link: "https://example.com/node-express",
  },
  {
    module: "Database Basics",
    slug: "database-basics",
    desc: "Learn how to work with databases using SQL and NoSQL solutions.",
    link: "https://example.com/database-basics",
  },
  {
    module: "Version Control with Git",
    slug: "git-basics",
    desc: "Understand Git workflows, branching, commits, and collaboration using GitHub.",
    link: "https://example.com/git-basics",
  },
];

const SkillVisit = () => {
  const { slug } = useParams();
  const navigate = useNavigate();

  const skill = skillDevelopmentItems.find((item) => item.slug === slug);

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
    <div className="flex flex-col items-center px-4 py-8">
      <Button
        onClick={() => navigate("/employee/skill-development")}
        variant="outline"
        className="mb-6 flex items-center gap-2"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Skills
      </Button>

      <Card className="w-full max-w-2xl shadow-md rounded-2xl border border-gray-200">
        <CardHeader>
          <CardTitle className="text-2xl font-bold">{skill.module}</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-700 text-base leading-relaxed">
            {skill.desc}
          </p>
        </CardContent>
        <div className="flex justify-end p-4">
          <Button asChild variant="outline">
            <a href={skill.link} target="_blank" rel="noopener noreferrer">
              Visit Module
            </a>
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default SkillVisit;
