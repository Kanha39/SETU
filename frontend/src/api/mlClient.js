import axios from "axios";

const mlClient = axios.create({
  baseURL: import.meta.env.VITE_ML_API_BASE_URL || "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

export default mlClient;
