import axios from "axios";

// Talks directly to chatbot/api.py -- no changes made to that service.
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

export default apiClient;
