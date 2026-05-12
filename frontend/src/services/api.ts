import { UserCreate, UserPublic, ApiError } from './api';
import { SignupResponse } from '../types/forms';


// To this:
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const API_V1 = `${API_URL}`;

class ApiService {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const url = `${API_V1}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        detail: `HTTP ${response.status}`,
      }));
      throw error;
    }

    return response.json();
  }

  async signup(userData: UserCreate): Promise<SignupResponse> {
    try {
      const response = await this.request<UserPublic>('/users/', {
        method: 'POST',
        body: JSON.stringify(userData),
      });

      // Store user info (but not token, as signup doesn't return one)
      localStorage.setItem('user', JSON.stringify(response));

      return {
        success: true,
        user: response,
      };
    } catch (error: any) {
      const detail = error?.detail || 'Signup failed. Please try again.';
      return {
        success: false,
        message:
          typeof detail === 'string'
            ? detail
            : JSON.stringify(detail),
      };
    }
  }

  async login(
    username: string,
    password: string
  ): Promise<{ access_token: string } | null> {
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch(`${API_V1}/login/access-token`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        return null;
      }

      return response.json();
    } catch {
      return null;
    }
  }

  logout(): void {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
  }

  getStoredUser(): any {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  getStoredToken(): string | null {
    return localStorage.getItem('auth_token');
  }
}

export default new ApiService();