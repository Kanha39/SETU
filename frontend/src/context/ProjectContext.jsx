import { createContext, useContext, useState } from "react";

const ProjectContext = createContext(null);

export function ProjectProvider({ children }) {
  // `project` mirrors the enriched project_data object /api/predict returns.
  // `predictions` mirrors its predictions block. Kept here so the Predict
  // page's result can be reused on the Chat page without re-submitting.
  const [project, setProject] = useState(null);
  const [predictions, setPredictions] = useState(null);
  const [sessionId, setSessionId] = useState(null);

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

  return (
    <ProjectContext.Provider value={{ project, predictions, sessionId, setSubmittedProject, clearProject }}>
      {children}
    </ProjectContext.Provider>
  );
}

export function useProject() {
  const ctx = useContext(ProjectContext);
  if (!ctx) throw new Error("useProject must be used inside <ProjectProvider>");
  return ctx;
}
