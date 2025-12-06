import { useEffect, useState } from 'react';
import FullOrganizationalHierarchy from '@/components/FullOrganizationalHierarchy';

import organizationService, { type ReportingStructure } from '@/services/organizationService';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { useAuth } from '@/contexts/AuthContext'; // Import useAuth hook


const OrganizationalChartPage = () => {
  const [orgChartData, setOrgChartData] = useState<ReportingStructure | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth(); // Get current user from AuthContext

  useEffect(() => {
    const fetchOrgChart = async () => {
      try {
        const data = await organizationService.getMyReportingStructure();
        console.log("Fetched reporting structure data in OrganizationalChartPage:", data);
        setOrgChartData(data);
      } catch (err) {
        console.error("Failed to fetch organizational chart:", err);
        setError("Failed to load organizational chart. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchOrgChart();
  }, []);

  if (loading) {
    return (
      <div className="container mx-auto py-8">
        <h1 className="text-3xl font-bold mb-6">Organizational Hierarchy Chart</h1>
        <Card className="w-full p-6 shadow-md">
          <CardHeader>
            <CardTitle>Loading Organizational Chart</CardTitle>
          </CardHeader>
          <CardContent>
            <Skeleton className="h-4 w-[250px] mb-2" />
            <Skeleton className="h-4 w-[200px] mb-2" />
            <Skeleton className="h-4 w-[300px]" />
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto py-8">
        <Card className="w-full p-6 shadow-md">
          <CardHeader>
            <CardTitle>Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-red-500">{error}</p>
            <Button onClick={() => window.location.reload()} className="mt-4">
              Reload Page
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8">
      <div className="flex flex-col items-center">
        {orgChartData ? (
          <FullOrganizationalHierarchy
            reportingStructure={orgChartData}
          />
        ) : (
          <Card className="w-full p-6 shadow-md">
            <CardHeader>
              <CardTitle>No Data</CardTitle>
            </CardHeader>
            <CardContent>
              <p>No organizational chart data available.</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default OrganizationalChartPage;