import { Outlet } from "react-router-dom";
import { Toaster } from "@/components/ui/toaster";

function App() {
  return (
    <div>
      {/* Header */}
      <Outlet />
      {/* Footer */}
      <Toaster />
    </div>
  );
}

export default App;
