import { Navigate, useLocation } from "react-router-dom";
import { useProject } from "../context/ProjectContext.jsx";

export default function ProtectedRoute({ children }) {
  const { user } = useProject();
  const location = useLocation();

  if (!user?.token) {
    return <Navigate to="/auth" replace state={{ from: location }} />;
  }

  return children;
}
