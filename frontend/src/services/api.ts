import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
});

// Attach JWT token if present
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("leafline_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default API;
