import { useState, useEffect } from "react";
import JobListingsTable from "@/components/JobListingsTable";
import applicationService, {
  type ApplicationResponse,
} from "@/services/applicationService";

const JobListings = () => {
  const [applications, setApplications] = useState<ApplicationResponse[]>([]);

  useEffect(() => {
    applicationService
      .getMyApplications()
      .then((res) => {
        setApplications(res.applications);
      })
      .catch((err) => console.error("Failed to fetch my applications", err));
  }, []);

  return (
    <div>
      <h2 className="text-3xl font-semibold text-center mt-8">Job Listings</h2>
      <JobListingsTable applications={applications} />
    </div>
  );
};

export default JobListings;
