import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Download, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

const Policies = () => {
  const suggestions = [
    "How many casual leaves are allowed per year?",
    "What is the policy for sick leave?",
    "How do I enroll in the health insurance plan?",
  ];

  return (
    <div className="w-full max-w-3xl mx-auto px-4 flex flex-col items-center justify-center gap-6 mt-10">
      <h2 className="text-3xl font-semibold text-center mt-8">Policies</h2>

      {/* Download Card */}
      <Card className="w-[60%]">
        <CardHeader>
          <CardTitle className="text-lg font-semibold flex items-center justify-between">
            Download policy document
            <Button variant="outline" className="flex items-center gap-2">
              <Download className="w-4 h-4" />
              Download
            </Button>
          </CardTitle>
        </CardHeader>
      </Card>

      <div className="font-semibold text-gray-500 text-sm uppercase tracking-widest">
        OR
      </div>

      {/* Ask About Policies Card */}
      <Card className="w-[60%]">
        <CardHeader className="flex justify-between items-start">
          <div>
            <CardTitle className="text-lg font-semibold">
              Ask about policies
            </CardTitle>
            <CardDescription>Suggestions :</CardDescription>
          </div>
          <Button variant="secondary" size="sm" className="text-xs font-medium">
            AI - Powered
          </Button>
        </CardHeader>

        <CardContent className="flex flex-col gap-3">
          {suggestions.map((s, i) => (
            <Button
              key={i}
              variant="outline"
              className="justify-start font-normal text-sm"
            >
              {s}
            </Button>
          ))}

          <div className="flex items-center gap-2 mt-2">
            <Input placeholder="Type your question..." className="flex-1" />
            <Button size="icon" variant="default">
              <ArrowRight className="w-4 h-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Policies;
