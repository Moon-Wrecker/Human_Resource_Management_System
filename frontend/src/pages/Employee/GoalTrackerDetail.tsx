import { useNavigate, useParams } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ArrowLeft } from "lucide-react";

const checkpoints = {
  "module-x": {
    title: "Module X Reading",
    description:
      "Here you can find all the materials and resources for Module X reading. Please go through the documents carefully before proceeding to the next checkpoint.",
    resources: [
      {
        name: "Module X Reading Material (PDF)",
        url: "https://example.com/module-x-reading.pdf",
      },
      {
        name: "Supplementary Video",
        url: "https://example.com/module-x-video",
      },
    ],
  },
  "module-y": {
    title: "Module Y Practice",
    description: "Practice exercises for Module Y.",
    resources: [
      {
        name: "Module Y Practice Sheet",
        url: "https://example.com/module-y-practice.pdf",
      },
    ],
  },
  "module-z": {
    title: "Module Z Quiz",
    description:
      "Take the Module Z assessment quiz to test your understanding.",
    resources: [
      { name: "Quiz Link", url: "https://example.com/module-z-quiz" },
    ],
  },
};
export default function VisitPage() {
  const navigate = useNavigate();
  const { id } = useParams();

  const checkpoint = checkpoints[id as unknown] || {
    title: "Checkpoint Not Found",
    description: "Sorry, we couldn't find the requested checkpoint.",
    resources: [],
  };

  return (
    <div className="max-w-3xl mx-auto mt-10 p-4">
      <Button variant="outline" className="mb-6" onClick={() => navigate(-1)}>
        <ArrowLeft className="w-4 h-4 mr-2" />
        Back
      </Button>

      <Card className="border">
        <CardHeader>
          <CardTitle className="text-2xl font-semibold">
            {checkpoint.title}
          </CardTitle>
        </CardHeader>

        <CardContent className="space-y-4 text-gray-700">
          <p>{checkpoint.description}</p>

          {checkpoint.resources.length > 0 && (
            <div className="space-y-2">
              <h3 className="font-semibold text-lg">Resources:</h3>
              <ul className="list-disc list-inside space-y-1">
                {checkpoint.resources.map((res, index) => (
                  <li key={index}>
                    <a
                      href={res.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      {res.name}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
