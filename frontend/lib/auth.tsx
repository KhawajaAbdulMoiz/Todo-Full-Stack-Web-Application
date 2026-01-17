'use client';

import { createContext, useContext, useState, ReactNode, useEffect } from 'react';

// -------------------- Types --------------------
interface User {
  id: string;
  email: string;
  createdAt: string;
  updatedAt: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

// -------------------- Auth Provider --------------------
export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Restore user and token from localStorage on mount
  useEffect(() => {
    const storedUser = localStorage.getItem('logged_in_user');
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch {
        localStorage.removeItem('logged_in_user');
      }
    }

    // Listen for storage changes to sync across tabs
    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === 'logged_in_user') {
        if (e.newValue) {
          try {
            setUser(JSON.parse(e.newValue));
          } catch {
            setUser(null);
          }
        } else {
          setUser(null);
        }
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, []);

  // -------------------- Login --------------------
  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      // Using FormData to match backend expectations
      const formData = new FormData();
      formData.append('email', email);
      formData.append('password', password);

      const baseUrl =
        process.env.NEXT_PUBLIC_API_BASE_URL ||
        process.env.API_BASE_URL ||
        'http://localhost:8000/api/v1';

      const response = await fetch(`${baseUrl}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        let errorMessage = 'Login failed';

        if (typeof data?.detail === 'string') {
          errorMessage = data.detail;
        } else if (Array.isArray(data?.detail)) {
          errorMessage = data.detail.join(', ');
        } else if (typeof data?.message === 'string') {
          errorMessage = data.message;
        } else {
          errorMessage = JSON.stringify(data);
        }

        throw new Error(errorMessage);
      }

      // Extract token from response (backend returns {"token": "..."})
      const token = data.data?.token || data.token || data.access_token || data.accessToken;
      if (!token) {
        throw new Error('No token received from server');
      }

      // Store the token in localStorage (same as apiClient does)
      localStorage.setItem('auth_token', token);

      // The backend doesn't return user data in login response,
      // so we'll need to fetch user data separately or construct it from the token payload
      // For now, we'll just store the email since that's what we have
      const mockUser: User = {
        id: 'unknown', // Will be updated later when we fetch user details
        email,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      setUser(mockUser);
      localStorage.setItem('logged_in_user', JSON.stringify(mockUser));
    } catch (err: any) {
      console.error('Login error:', err);

      let message = 'Login failed';

      if (typeof err === 'string') {
        message = err;
      } else if (err instanceof Error) {
        message = err.message;
      } else if (err?.detail) {
        message = err.detail;
      } else if (err?.message && typeof err.message === 'string') {
        message = err.message;
      } else {
        message = JSON.stringify(err);
      }

      throw new Error(message);
    }
    finally {
      setIsLoading(false);
    }
  };

  // -------------------- Register --------------------
  const register = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      // Using FormData to match backend expectations
      const formData = new FormData();
      formData.append('email', email);
      formData.append('password', password);

      const baseUrl =
        process.env.NEXT_PUBLIC_API_BASE_URL ||
        process.env.API_BASE_URL ||
        'http://localhost:8000/api/v1';

      const response = await fetch(`${baseUrl}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || data.message || 'Registration failed');
      }

      // Extract token from response (backend returns {"access_token": "...", "user": {...}})
      const token = data.access_token || data.token || data.accessToken;
      if (!token) {
        throw new Error('No token received from server');
      }

      // Store the token in localStorage (same as apiClient does)
      localStorage.setItem('auth_token', token);

      // Extract user data from response
      const userData = data.data?.user || data.user;

      if (!userData) {
        throw new Error('User data not returned from server');
      }

      const normalizedUser: User = {
        id: userData.id,
        email: userData.email,
        createdAt: userData.created_at || userData.createdAt,
        updatedAt: userData.updated_at || userData.updatedAt,
      };

      setUser(normalizedUser);
      localStorage.setItem('logged_in_user', JSON.stringify(normalizedUser));
    } catch (err: any) {
      console.error('Login error:', err);

      let message = 'Login failed';

      if (typeof err === 'string') {
        message = err;
      } else if (err instanceof Error) {
        message = err.message;
      } else if (err?.detail) {
        message = err.detail;
      } else if (err?.message && typeof err.message === 'string') {
        message = err.message;
      } else {
        message = JSON.stringify(err);
      }

      throw new Error(message);
    } finally {
      setIsLoading(false);
    }
  };

  // -------------------- Logout --------------------
  const logout = () => {
    setUser(null);
    localStorage.removeItem('logged_in_user');
    localStorage.removeItem('auth_token'); // Also remove the auth token
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        register,
        logout,
        isAuthenticated: !!user,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// -------------------- Hook --------------------
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
