'use client';

// Base API client with JWT token attachment
class ApiClient {
  private baseUrl: string;
  private readonly headers: HeadersInit;

  constructor() {
    this.baseUrl =
      process.env.NEXT_PUBLIC_API_BASE_URL ||
      'http://localhost:8000/api/v1';

    this.headers = {
      'Content-Type': 'application/json',
    };
  }

  // ✅ Get JWT token from localStorage (client-safe)
  private getJwtToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('auth_token');
  }

  // Generic request method that adds JWT token
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    // Get token from localStorage
    const token = this.getJwtToken();

    // Debug logging to help troubleshoot authentication issues
    console.log(`Making request to: ${url}`);
    console.log(`Token available: ${!!token}`);

    const headers: HeadersInit = {
      ...this.headers,
      ...options.headers,
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    };

    // Log the Authorization header being sent (without exposing the full token)
    if (token) {
      console.log('Authorization header will be included');
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      let errorMessage = `HTTP error! status: ${response.status}`;

      try {
        const errorData = await response.json();

        // Handle different possible error response formats
        if (typeof errorData === 'string') {
          errorMessage = errorData;
        } else if (errorData && typeof errorData === 'object') {
          // Check for common error response properties
          errorMessage = errorData.detail ||
                        errorData.message ||
                        errorData.error ||
                        (Array.isArray(errorData) ? errorData.join(', ') :
                         errorData.errors ? Object.values(errorData.errors).flat().join(', ') :
                         JSON.stringify(errorData));
        }
      } catch (parseError) {
        // If parsing fails, use status text or default message
        errorMessage = response.statusText || `HTTP error! status: ${response.status}`;
      }

      console.error(`API request failed: ${errorMessage}`);
      throw new Error(errorMessage);
    }

    // DELETE requests may not return body
    if (response.status === 204) {
      return {} as T;
    }

    return response.json();
  }

  // ---------------- AUTH ----------------

  async register(userData: { email: string; password: string }) {
    // Backend expects form data, not JSON
    const formData = new FormData();
    formData.append('email', userData.email);
    formData.append('password', userData.password);

    const res = await fetch(`${this.baseUrl}/auth/register`, {
      method: 'POST',
      body: formData,
    });

    if (!res.ok) {
      let errorMessage = `HTTP error! status: ${res.status}`;

      try {
        const errorData = await res.json();

        // Handle different possible error response formats
        if (typeof errorData === 'string') {
          errorMessage = errorData;
        } else if (errorData && typeof errorData === 'object') {
          // Check for common error response properties
          errorMessage = errorData.detail ||
                        errorData.message ||
                        errorData.error ||
                        (Array.isArray(errorData) ? errorData.join(', ') :
                         errorData.errors ? Object.values(errorData.errors).flat().join(', ') :
                         JSON.stringify(errorData));
        }
      } catch (parseError) {
        // If parsing fails, use status text or default message
        errorMessage = res.statusText || `HTTP error! status: ${res.status}`;
      }

      throw new Error(errorMessage);
    }

    const data = await res.json();

    // The backend returns the token as 'access_token'
    const token = data.access_token || data.token || data.accessToken;

    if (!token) {
      throw new Error('No token received from server');
    }

    // ✅ Store token after register
    localStorage.setItem('auth_token', token);
    return data;
  }

  async login(credentials: { email: string; password: string }) {
    // Backend expects form data, not JSON
    const formData = new FormData();
    formData.append('email', credentials.email);
    formData.append('password', credentials.password);

    const res = await fetch(`${this.baseUrl}/auth/login`, {
      method: 'POST',
      body: formData,
    });

    if (!res.ok) {
      let errorMessage = `HTTP error! status: ${res.status}`;

      try {
        const errorData = await res.json();

        // Handle different possible error response formats
        if (typeof errorData === 'string') {
          errorMessage = errorData;
        } else if (errorData && typeof errorData === 'object') {
          // Check for common error response properties
          errorMessage = errorData.detail ||
                        errorData.message ||
                        errorData.error ||
                        (Array.isArray(errorData) ? errorData.join(', ') :
                         errorData.errors ? Object.values(errorData.errors).flat().join(', ') :
                         JSON.stringify(errorData));
        }
      } catch (parseError) {
        // If parsing fails, use status text or default message
        errorMessage = res.statusText || `HTTP error! status: ${res.status}`;
      }

      throw new Error(errorMessage);
    }

    const data = await res.json();

    // The backend returns the token as 'access_token'
    const token = data.access_token || data.token || data.accessToken;

    if (!token) {
      throw new Error('No token received from server');
    }

    // ✅ Store token after login
    localStorage.setItem('auth_token', token);
    return data;
  }

  async logout() {
    const token = this.getJwtToken();

    if (token) {
      try {
        await fetch(`${this.baseUrl}/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
      } catch (error) {
        console.error('Logout error:', error);
        // Continue with local cleanup even if server logout fails
      }
    }

    localStorage.removeItem('auth_token');
    // Also remove from cookies
    document.cookie = 'auth_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Lax';
  }

  
  // ---------------- TASKS ----------------

  async getTasks() {
    return this.request<{ tasks: any[]; pagination?: any }>('/tasks');
  }

  async createTask(taskData: {
    title: string;
    description?: string;
    completed?: boolean;
  }) {
    return this.request<{ task: any }>('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async getTask(taskId: string) {
    return this.request<{ task: any }>(`/tasks/${taskId}`);
  }

  async updateTask(
    taskId: string,
    taskData: {
      title?: string;
      description?: string;
      completed?: boolean;
    }
  ) {
    return this.request<{ task: any }>(`/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(taskId: string) {
    return this.request(`/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(taskId: string) {
    return this.request<{ task: any }>(
      `/tasks/${taskId}/toggle-completion`,
      {
        method: 'PATCH',
      }
    );
  }
}

export const apiClient = new ApiClient();
