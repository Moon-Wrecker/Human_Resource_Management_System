import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ArrowRight, Search } from "lucide-react";

const SkillDevelopment = () => {
  const submitSearch = (e: React.FormEvent) => {
    e.preventDefault();
  };

  const skillDevelopmentItems = [
    {
      module: "JavaScript Basics",
      desc: "Learn the fundamentals of JavaScript, including variables, loops, functions, and events.",
      slug: "javascript-basics",
    },
    {
      module: "React Fundamentals",
      desc: "Get started with React, covering components, props, state, and hooks.",
      slug: "https://example.com/react-fundamentals",
    },
    {
      module: "CSS & Tailwind",
      desc: "Master styling with CSS and Tailwind for responsive and modern web designs.",
      slug: "https://example.com/css-tailwind",
    },
    {
      module: "Node.js & Express",
      desc: "Build server-side applications with Node.js and Express framework.",
      slug: "https://example.com/node-express",
    },
    {
      module: "Database Basics",
      desc: "Learn how to work with databases using SQL and NoSQL solutions.",
      slug: "https://example.com/database-basics",
    },
    {
      module: "Version Control with Git",
      desc: "Understand Git workflows, branching, commits, and collaboration using GitHub.",
      slug: "https://example.com/git-basics",
    },
  ];
  return (
    <div className="flex items-center justify-center flex-col">
      <h2 className="text-3xl font-semibold text-center my-8">
        Skill Developement Modules
      </h2>
      <form
        onSubmit={submitSearch}
        className="w-[50%] flex items-center justify-center gap-1"
      >
        <Input placeholder="Search by title and type... " />
        <Button type="submit" variant="outline">
          <Search />
        </Button>
      </form>

      <div className="grid grid-cols-3 my-8 px-4 gap-4">
        {skillDevelopmentItems.map((skillDevelopementItem) => (
          <Card className="w-full max-w-md shadow-md rounded-2xl border border-gray-200">
            <CardHeader>
              <CardTitle className="text-lg font-semibold text-gray-900">
                {skillDevelopementItem.module}
              </CardTitle>
            </CardHeader>

            <CardContent>
              <p className="text-gray-700 text-sm leading-relaxed">
                {skillDevelopementItem.desc}
              </p>
            </CardContent>

            <CardFooter className="flex justify-end">
              <Button
                asChild
                variant="outline"
                className="flex items-center gap-2"
              >
                <a href={`skills/${skillDevelopementItem.slug}`}>
                  View Details
                  <ArrowRight className="w-4 h-4" />
                </a>
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default SkillDevelopment;
