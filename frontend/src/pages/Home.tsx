import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="text-center space-y-6 p-8">
        <h1 className="text-5xl font-bold text-gray-900">
          Welcome to HR Management System
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Streamline your workforce management with our comprehensive HR solution
        </p>
        <div className="pt-4">
          <Button 
            onClick={() => navigate("/login")}
            size="lg"
            className="text-lg px-8 py-6"
          >
            Get Started - Login
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Home;
