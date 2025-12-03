import { useNavigate, useParams } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ArrowLeft } from "lucide-react";
import { useEffect, useState } from "react";
import goalService, { type Checkpoint } from "@/services/goalService";

export default function VisitPage() {
  const navigate = useNavigate();
  const { goal, id } = useParams();

  const [checkpoint, setCheckpoint] = useState<Checkpoint>();

  useEffect(() => {
    goalService
      .getGoalById(parseInt(goal || "0"))
      .then((res) =>
        setCheckpoint(
          res.checkpoints.find((cp) => cp.id === parseInt(id || "0")),
        ),
      );
  }, [goal, id]);

  return (
    <div className="max-w-3xl mx-auto mt-10 p-4">
      <Button variant="outline" className="mb-6" onClick={() => navigate(-1)}>
        <ArrowLeft className="w-4 h-4 mr-2" />
        Back
      </Button>

      {!checkpoint ? (
        <Card className="border">
          <CardContent className="text-center text-muted-foreground">
            No checkpoint found!
          </CardContent>
        </Card>
      ) : (
        <Card className="border">
          <CardHeader>
            <CardTitle className="text-2xl font-semibold">
              {checkpoint.title}
            </CardTitle>
          </CardHeader>

          <CardContent className="space-y-4 text-gray-700">
            <p>{checkpoint.description}</p>

            {/* {checkpoint.resources.length > 0 && ( */}
            {/*   <div className="space-y-2"> */}
            {/*     <h3 className="font-semibold text-lg">Resources:</h3> */}
            {/*     <ul className="list-disc list-inside space-y-1"> */}
            {/*       {checkpoint.resources.map((res, index) => ( */}
            {/*         <li key={index}> */}
            {/*           <a */}
            {/*             href={res.url} */}
            {/*             target="_blank" */}
            {/*             rel="noopener noreferrer" */}
            {/*             className="text-blue-600 hover:underline" */}
            {/*           > */}
            {/*             {res.name} */}
            {/*           </a> */}
            {/*         </li> */}
            {/*       ))} */}
            {/*     </ul> */}
            {/*   </div> */}
            {/* )} */}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
