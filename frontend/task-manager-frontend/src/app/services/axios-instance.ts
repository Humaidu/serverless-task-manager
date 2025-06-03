import axios from 'axios';
import { environment } from 'src/environments/environment';

/**
 * Create a reusable Axios instance with default settings.
 * This helps to avoid repeating config (like base URL or headers) across requests.
 */
const axiosInstance = axios.create({
  baseURL: environment.API_BASE_URL, // Base URL for all API requests (e.g., https://api.example.com)
  headers: {
    'Content-Type': 'application/json', // All requests will use JSON content type by default
  },
});

/**
 * Interceptor to attach the JWT auth token to every outgoing request.
 * This is useful for authenticated APIs where the token is required in the Authorization header.
 */
axiosInstance.interceptors.request.use(
  (config) => {
    // Get the auth token from local storage
    const token = localStorage.getItem('authToken');

    // If token exists, add it to the request headers
    if (token) {
      config.headers.Authorization = token;
    }

    // Return the modified request config
    return config;
  },
  (error) => {
    // Handle any error that occurs while setting up the request
    return Promise.reject(error);
  }
);

// Export the configured Axios instance for use in services or components
export default axiosInstance;
