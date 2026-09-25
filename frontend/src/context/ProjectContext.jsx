import { createContext, useContext, useEffect, useState } from "react";

const ProjectContext = createContext(null);

export function ProjectProvider({ children }) {
  const [project, setProject] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("setu-user");
    return saved ? JSON.parse(saved) : null;
  });

  useEffect(() => {
    if (user) {
      localStorage.setItem("setu-user", JSON.stringify(user));
    } else {
      localStorage.removeItem("setu-user");
    }
  }, [user]);

  const setSubmittedProject = (projectData, predictionsBlock, currentSessionId = null) => {
    setProject(projectData);
    setPredictions(predictionsBlock);
    setSessionId(currentSessionId);
  };

  const clearProject = () => {
    setProject(null);
    setPredictions(null);
    setSessionId(null);
  };

  const loginUser = (userData) => setUser(userData);
  const logoutUser = () => setUser(null);

  return (
    <ProjectContext.Provider value={{
      project,
      predictions,
      sessionId,
      user,
      setSubmittedProject,
      clearProject,
      loginUser,
      logoutUser,
    }}>
      {children}
    </ProjectContext.Provider>
  );
}

export function useProject() {
  const ctx = useContext(ProjectContext);
  if (!ctx) throw new Error("useProject must be used inside <ProjectProvider>");
  return ctx;
}
