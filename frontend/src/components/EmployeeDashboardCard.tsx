import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type EmployeeDashboardCardProps = {
  title: string;
  content: string;
};

const EmployeeDashboardCard = ({
  title,
  content,
}: EmployeeDashboardCardProps) => {
  return (
    <Card className="text-center w-full">
      <CardHeader>
        <CardTitle className="font-bold text-2xl">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-xl">{content}</p>
      </CardContent>
    </Card>
  );
};

export default EmployeeDashboardCard;
