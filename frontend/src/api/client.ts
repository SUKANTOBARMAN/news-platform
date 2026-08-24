import axios from "axios";

/**
 * কেন্দ্রীয় axios instance -- প্রতিটা API কল এই client দিয়ে যাবে, যাতে
 * base URL, auth token attach করা, error handling ইত্যাদি একবারই লেখা লাগে।
 */
export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
    }
    return Promise.reject(error);
  },
);
